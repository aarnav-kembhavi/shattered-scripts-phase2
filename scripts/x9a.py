"""X9a: tiny GPT, familiarity manipulated, fragmentation fixed (Amendment 2, X9a; laptop). Registered rules are implemented exactly; nothing is tuned.

  python scripts/x9a.py prep               CPU: cipher + round trip, the one fixed tokenizer (1,024), exposure streams (levels 0, 1, 5, 20, 50 percent), evaluation pairs,
                                           disjointness check, tokenizer statistics; writes data/processed/x9a/ and results/phase2/x9a/prep.json. Nothing trains if a check fails.
  python scripts/x9a.py pilot              one run at level 20, seed 0, 10 percent of the budget (round trip, tokenizer statistics, timing, the whole evaluation path)
  python scripts/x9a.py train LEVEL SEED   one full run (resumable); then `eval` is run automatically
  python scripts/x9a.py eval LEVEL SEED    retrieval (cipher story -> English story, Phase 1 M4b protocol, unmapped, test half) and the MDL word-assembly probe on cipher and English words
  python scripts/x9a.py analyse            X9a-R and X9a-A decision rules over the 15 runs

Cipher: ASCII a-z -> the first 26 Cyrillic lowercase letters (U+0430..U+0449) by `default_rng(9).permutation(26)`, A-Z -> the same letters in capitals; everything else unchanged.
Corpus: the Phase 1 E5 stream (TinyStories V2, data_seed 0, 400 MB, the same shuffled order). Exposure p replaces the first p percent of `default_rng(9).permutation(n_stories)` by their cipher
renderings (nested; a story is seen in one rendering only). Tokenizer: byte-level BPE, 1,024 tokens, trained once on 50 MB English stories plus 50 MB cipher renderings of other stories, all taken from the
shuffled stories BEYOND the 400 MB training prefix (disjoint from every training story and from the evaluation stories). Model, optimizer, schedule, steps and tokens per step: Phase 1 vocabulary-1,024
(6,173 steps x 64 sequences x 320 tokens); each level's stream is cut at exactly that many tokens (stories consumed per level are reported).
"""
import argparse
import hashlib
import json
import random
import re
import sys
import time
from collections import Counter
from pathlib import Path

import numpy as np
import torch
import yaml
from scipy import stats

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kaggle_retrieval_gate as KR  # noqa: E402
import m1_tiny_mdl as M  # noqa: E402

from shattered.interp.probes import bootstrap_mdl_detok, mdl_curve  # noqa: E402
from shattered.pretrain import data as D  # noqa: E402
from shattered.pretrain.model import GPT, GPTConfig  # noqa: E402
from shattered.pretrain.train import train_run  # noqa: E402
from shattered.runlog import REPO, results_dir, write_json  # noqa: E402

PROC = REPO / "data" / "processed" / "x9a"
OUT = results_dir("phase2/x9a")
LEVELS = [0, 1, 5, 20, 50]
LOW = {"0p01": 0.01, "0p03": 0.03, "0p1": 0.1, "0p3": 0.3}  # X9a-low (RESULTS.md, tag phase2-x9a-low): exposure percent by level key
EVAL_N, EVAL_CHARS, TOK_VOCAB = 500, 700, 1024
CFG = yaml.safe_load(open(REPO / "configs" / "e05_pretrain.yaml", encoding="utf-8"))
N_WORDS, MAX_OCC, MAX_PER_STORY = 300, 40, 2
CYR = "а-щА-Щ"
WORD_RE = {"cipher": re.compile(rf"(?<= )[{CYR}]{{3,}}(?![{CYR}])"), "english": re.compile(r"(?<= )[A-Za-z]{3,}(?![A-Za-z])")}


# ------------------------------------------------------------------------------------------------------------------ cipher
def cipher_tables():
    perm = np.random.default_rng(9).permutation(26)
    m = {chr(97 + i): chr(0x430 + int(perm[i])) for i in range(26)}
    m.update({chr(65 + i): chr(0x410 + int(perm[i])) for i in range(26)})
    return str.maketrans(m), str.maketrans({v: k for k, v in m.items()}), m


ENC, DEC, CIPHER_MAP = cipher_tables()


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def phase1_steps() -> tuple[int, int]:
    fin = json.load(open(REPO / "results" / "e05_pretrain" / "run_v1024_s0" / "final.json"))
    return fin["steps"], fin["ctx_tokens"]


# ------------------------------------------------------------------------------------------------------------------ prep
def take(stories: list[str], start: int, n_bytes: int, render=None) -> tuple[list[str], int]:
    out, total, j = [], 0, start
    while total < n_bytes and j < len(stories):
        t = render(stories[j]) if render else stories[j]
        out.append(t)
        total += len(t.encode("utf-8")) + 1
        j += 1
    return out, j


def tokenize_until(tok, texts_iter, n_tokens: int, batch: int = 20000):
    """First n_tokens tokens (plus one) of the EOS-joined stream; returns (array, stories consumed, bytes consumed, cipher stories consumed)."""
    eos = tok.token_to_id(D.EOS)
    parts, total, used, nbytes, ncipher = [], 0, 0, 0, 0

    def flush(buf) -> bool:
        nonlocal total, used, nbytes, ncipher
        for (text, is_c), enc in zip(buf, tok.encode_batch([b[0] for b in buf])):
            parts.append(np.asarray(enc.ids, dtype=np.uint16))
            parts.append(np.asarray([eos], dtype=np.uint16))
            total += len(enc.ids) + 1
            used += 1
            nbytes += len(text.encode("utf-8")) + 1
            ncipher += int(is_c)
            if total >= n_tokens + 1:
                return True
        return False

    buf, done = [], False
    for item in texts_iter:
        buf.append(item)
        if len(buf) >= batch:
            done = flush(buf)
            buf = []
            if done:
                break
    if not done and buf:
        done = flush(buf)
    if not done:
        raise RuntimeError("the stream is shorter than the token budget")
    arr = np.concatenate(parts)[: n_tokens + 1]
    return arr, used, nbytes, ncipher


def prep() -> None:
    t0 = time.time()
    steps, ctx = phase1_steps()
    n_tokens = steps * CFG["train"]["batch_seqs"] * ctx
    PROC.mkdir(parents=True, exist_ok=True)
    stories = D.read_stories("train")
    random.Random(CFG["data"]["data_seed"]).shuffle(stories)  # the Phase 1 order (data.training_stories)
    train, _ = take(stories, 0, CFG["data"]["train_bytes"])
    n_train = len(train)
    tail_en, j = take(stories, n_train, 50_000_000)
    tail_c, j2 = take(stories, j, 50_000_000, render=lambda s: s.translate(ENC))
    # round trip on every story used
    bad = sum(1 for s in train + tail_en if s.translate(ENC).translate(DEC) != s)
    bad += sum(1 for c in tail_c if c.translate(DEC).translate(ENC) != c)
    valid = D.read_stories("valid")
    ev = valid[:EVAL_N]
    ev_en = [s[:EVAL_CHARS] for s in ev]
    ev_c = [s.translate(ENC) for s in ev_en]
    bad += sum(1 for a, c in zip(ev_en, ev_c) if c.translate(DEC) != a)
    used_texts = set(train) | set(tail_en) | {c.translate(DEC) for c in tail_c}
    overlap = sum(1 for s in valid[:EVAL_N] if s in used_texts) + sum(1 for s in ev_en if s in used_texts)
    assert bad == 0, f"cipher round trip failed on {bad} stories"
    assert overlap == 0, f"{overlap} evaluation stories occur in the training or tokenizer stories"
    tok_path = PROC / "tokenizer_1024.json"
    tok = D.load_tokenizer(tok_path) if tok_path.exists() else D.train_tokenizer(tail_en + tail_c, TOK_VOCAB, tok_path)
    words = lambda texts: sum(len(t.split()) for t in texts)  # noqa: E731
    tpw_en = sum(len(e.ids) for e in tok.encode_batch(ev_en)) / words(ev_en)
    tpw_c = sum(len(e.ids) for e in tok.encode_batch(ev_c)) / words(ev_c)
    # evaluation pairs and the English validation stream used for monitoring
    json.dump({"english": ev_en, "cipher": ev_c}, open(PROC / "eval_pairs.json", "w", encoding="utf-8"), ensure_ascii=False)
    val_stories = valid[EVAL_N:EVAL_N + 3000]
    val = D.tokenize_stream(tok, val_stories)
    np.save(PROC / "valid_en.npy", val)
    val_bytes = sum(len(s.encode("utf-8")) + 1 for s in val_stories)
    order = np.random.default_rng(9).permutation(n_train)
    meta = {"_x9a": {"steps": steps, "ctx_tokens": ctx, "tokens_per_run": n_tokens, "n_train_stories": n_train, "round_trip_bad": bad, "eval_overlap": overlap,
                     "tokenizer_sha256": sha(tok_path), "tokenizer_vocab_with_eos": tok.get_vocab_size(), "tokens_per_word_english_eval": tpw_en,
                     "tokens_per_word_cipher_eval": tpw_c, "tpw_relative_difference": abs(tpw_c - tpw_en) / tpw_en,
                     "tokenizer_stories": {"english": len(tail_en), "cipher": len(tail_c), "english_bytes": sum(len(s.encode()) + 1 for s in tail_en),
                                           "cipher_bytes": sum(len(s.encode()) + 1 for s in tail_c)},
                     "cipher_map": {k: v for k, v in CIPHER_MAP.items() if k.islower()}}}
    for p in LEVELS:
        path = PROC / f"train_p{p}.npy"
        n_c = int(round(n_train * p / 100))
        cset = set(order[:n_c].tolist())
        gen = ((train[i].translate(ENC), True) if i in cset else (train[i], False) for i in range(n_train))
        arr, used, nbytes, ncipher = tokenize_until(tok, gen, n_tokens)
        np.save(path, arr)
        meta[f"x9a_p{p}"] = {"vocab": TOK_VOCAB, "vocab_with_eos": tok.get_vocab_size(), "train_tokens": len(arr), "valid_tokens": len(val), "train_bytes": nbytes,
                             "valid_bytes": val_bytes, "bytes_per_token_train": nbytes / len(arr), "bytes_per_token_valid": val_bytes / len(val),
                             "tokenizer": str(tok_path.relative_to(REPO)), "train_stream": str(path.relative_to(REPO)), "valid_stream": str((PROC / "valid_en.npy").relative_to(REPO)),
                             "exposure_percent": p, "cipher_stories_in_set": n_c, "stories_consumed": used, "cipher_stories_consumed": ncipher,
                             "cipher_share_consumed": ncipher / used, "train_stream_sha256": sha(path)}
        print(f"level {p}: {used} stories, cipher {ncipher}, {len(arr)} tokens, {time.time() - t0:.0f}s", flush=True)
    (PROC / "meta.json").write_text(json.dumps(meta, indent=1, ensure_ascii=False), encoding="utf-8")
    summ = {k: v for k, v in meta["_x9a"].items() if k != "cipher_map"}
    summ["levels"] = {k: {a: b for a, b in v.items() if a in ("stories_consumed", "cipher_stories_consumed", "cipher_share_consumed", "train_tokens")} for k, v in meta.items() if k != "_x9a"}
    write_json(OUT / "prep.json", summ, {"registration": "RESULTS.md X9a", "seconds": time.time() - t0})
    print(json.dumps({k: summ[k] for k in ("round_trip_bad", "eval_overlap", "tokenizer_sha256", "tokens_per_word_english_eval", "tokens_per_word_cipher_eval", "tpw_relative_difference")}, indent=1))


def load_meta() -> dict:
    meta = json.loads((PROC / "meta.json").read_text(encoding="utf-8"))
    if (PROC / "meta_low.json").exists():
        meta.update(json.loads((PROC / "meta_low.json").read_text(encoding="utf-8")))
    return meta


def prep_low() -> None:
    """X9a-low streams: same stories, order, tokenizer and token budget as X9a; only the cipher share differs (CPU)."""
    t0 = time.time()
    base = load_meta()
    n_tokens = base["_x9a"]["tokens_per_run"]
    stories = D.read_stories("train")
    random.Random(CFG["data"]["data_seed"]).shuffle(stories)
    train, _ = take(stories, 0, CFG["data"]["train_bytes"])
    n_train = len(train)
    assert n_train == base["_x9a"]["n_train_stories"], (n_train, base["_x9a"]["n_train_stories"])
    tok_path = PROC / "tokenizer_1024.json"
    assert sha(tok_path) == base["_x9a"]["tokenizer_sha256"]
    tok = D.load_tokenizer(tok_path)
    order = np.random.default_rng(9).permutation(n_train)
    meta = {}
    for key, pct in LOW.items():
        path = PROC / f"train_p{key}.npy"
        n_c = int(round(n_train * pct / 100))
        cset = set(order[:n_c].tolist())
        gen = ((train[i].translate(ENC), True) if i in cset else (train[i], False) for i in range(n_train))
        arr, used, nbytes, ncipher = tokenize_until(tok, gen, n_tokens)
        np.save(path, arr)
        ref = base["x9a_p1"]
        meta[f"x9a_p{key}"] = {**{k: ref[k] for k in ("vocab", "vocab_with_eos", "valid_tokens", "valid_bytes", "bytes_per_token_valid", "tokenizer", "valid_stream")},
                               "train_tokens": len(arr), "train_bytes": nbytes, "bytes_per_token_train": nbytes / len(arr), "train_stream": str(path.relative_to(REPO)),
                               "exposure_percent": pct, "cipher_stories_in_set": n_c, "stories_consumed": used, "cipher_stories_consumed": ncipher,
                               "cipher_share_consumed": ncipher / used, "train_stream_sha256": sha(path)}
        print(f"level {key}%: {used} stories, cipher {ncipher}, {len(arr)} tokens, {time.time() - t0:.0f}s", flush=True)
    (PROC / "meta_low.json").write_text(json.dumps(meta, indent=1, ensure_ascii=False), encoding="utf-8")
    write_json(OUT / "prep_low.json", {k: {a: b for a, b in v.items() if a in ("exposure_percent", "stories_consumed", "cipher_stories_consumed", "cipher_share_consumed", "train_tokens")} for k, v in meta.items()},
               {"registration": "RESULTS.md X9a-low", "seconds": time.time() - t0})


# ------------------------------------------------------------------------------------------------------------------ train
def run_cfg(level: int, seed: int, fraction: float, tag: str, meta: dict) -> dict:
    return {**CFG["train"], "vocab": f"x9a_p{level}", "seed": seed, "fraction": fraction, "model": CFG["model"], "train_bytes": meta[f"x9a_p{level}"]["train_bytes"],
            "run_name": f"{tag}_p{level}_s{seed}", "ctx_tokens": meta["_x9a"]["ctx_tokens"], "mp_during_training": False, "snapshot_fracs": []}


def train(level: int, seed: int, fraction: float = 1.0, tag: str = "x9a") -> dict:
    meta = load_meta()
    return train_run(run_cfg(level, seed, fraction, tag, meta), meta)


# ------------------------------------------------------------------------------------------------------------------ eval
def build_words(texts: list[str], kind: str, tok, min_tokens: int) -> dict:
    rx = WORD_RE[kind]
    freq = Counter(m.group() for s in texts for m in rx.finditer(s))
    words = [w for w, _ in freq.most_common() if len(tok.encode(" " + w).ids) >= min_tokens][:N_WORDS]
    wid = {w: i for i, w in enumerate(words)}
    occ, count, used = [], Counter(), []
    for s in texts:
        per, hit = Counter(), False
        for m in rx.finditer(s):
            w = m.group()
            if w in wid and count[w] < MAX_OCC and per[w] < MAX_PER_STORY:
                occ.append({"story": len(used), "start": m.start(), "end": m.end(), "word": w, "label": wid[w]})
                count[w] += 1
                per[w] += 1
                hit = True
        if hit:
            used.append(s)
    return {"words": words, "stories": used, "occurrences": occ, "min_tokens": min_tokens, "n_words": len(words), "n_occ": len(occ)}


def fit_pairs(pairs: dict, tok, ctx: int) -> tuple[dict, dict]:
    """The registered texts are the first 700 characters; a pair is cut further, at a word boundary, only if the cipher or English text exceeds the model context (the same characters
    in both, so the pair stays parallel). Returns the pairs and the counts of cut pairs (identical for every run: the tokenizer is fixed)."""
    out_en, out_c, cut, lens = [], [], 0, []
    for e, c in zip(pairs["english"], pairs["cipher"]):
        n = len(e)
        while n > 0 and max(len(tok.encode(e[:n]).ids), len(tok.encode(c[:n]).ids)) > ctx:
            n = e.rfind(" ", 0, n)
        cut += int(n < len(e))
        out_en.append(e[:n])
        out_c.append(c[:n])
        lens.append(n)
    return {"english": out_en, "cipher": out_c}, {"pairs_cut_to_fit_context": cut, "mean_chars": float(np.mean(lens)), "min_chars": int(min(lens))}


@torch.no_grad()
def story_states(model, tok, texts: list[str], ctx: int, device: str) -> np.ndarray:
    """Mean residual over tokens per layer, [n, L+1, d]."""
    out = None
    for i, t in enumerate(texts):
        ids = tok.encode(t).ids
        assert len(ids) <= ctx, (len(ids), ctx)
        _, _, hidden = model(torch.tensor([ids], device=device), return_hidden=True)
        H = torch.stack([h[0].float().mean(0) for h in hidden]).cpu().numpy()
        if out is None:
            out = np.zeros((len(texts), H.shape[0], H.shape[1]), np.float32)
        out[i] = H
    return out


def evaluate(level: int, seed: int, tag: str = "x9a") -> dict:
    meta = load_meta()
    device = "cuda" if torch.cuda.is_available() else "cpu"
    run = f"{tag}_p{level}_s{seed}"
    fin = json.load(open(REPO / "results" / "e05_pretrain" / run / "final.json"))
    from safetensors.torch import load_file
    model = GPT(GPTConfig(**fin["model_config"]))
    model.load_state_dict(load_file(str(REPO / "checkpoints" / "e05" / run / "final.safetensors")))
    model = model.to(device).eval()
    ctx = fin["ctx_tokens"]
    tok = D.load_tokenizer(REPO / meta[f"x9a_p{level}"]["tokenizer"])
    pairs = json.load(open(PROC / "eval_pairs.json", encoding="utf-8"))
    pairs, fit = fit_pairs(pairs, tok, ctx)
    t0 = time.time()
    Xc = story_states(model, tok, pairs["cipher"], ctx, device)
    Xe = story_states(model, tok, pairs["english"], ctx, device)
    order = np.random.default_rng(0).permutation(len(pairs["english"]))
    tr, te = np.sort(order[: len(order) // 2]), np.sort(order[len(order) // 2:])
    tra, tes = KR.unmapped_curves(Xc, Xe, tr, te)
    lu = int(tra.argmax())
    res = {"run": run, "level": level, "seed": seed, "pairs": fit, "retrieval": {"layer": lu, "acc_unmapped": float(tes[lu].mean()), "n_test": int(len(te)), "chance": 1 / len(te),
                                                                 "test_acc_per_layer": tes.mean(1).tolist(), "train_acc_per_layer": tra.tolist(),
                                                                 "mapped": "secondary, not computed in this version"}}
    for kind in ("cipher", "english"):
        texts = pairs[kind]
        data = build_words(texts, kind, tok, 3)
        if data["n_words"] < N_WORDS:  # the only fallback of the registration
            data = build_words(texts, kind, tok, 2)
        labels = np.array([o["label"] for o in data["occurrences"]])
        states, ntok, _ = M.collect(model, tok, ctx, data, device)
        mdl = mdl_curve(states, labels, seed=0)
        K = int(labels.max()) + 1
        b = bootstrap_mdl_detok(mdl["costs"], K)
        res[f"assembly_{kind}"] = {"detok_layer": b["detok_layer"], "ci_low": b["ci_low"], "ci_high": b["ci_high"], "n_words": data["n_words"], "n_occ": data["n_occ"],
                                   "min_tokens": data["min_tokens"], "tokens_per_word_probed": float(ntok.mean()), "compression": [float(x) for x in b["compression"]]}
    res["seconds"] = time.time() - t0
    res["train"] = {k: fin[k] for k in ("steps", "val_bpb_full", "train_seconds_this_session", "wall_seconds_this_session") if k in fin}
    write_json(OUT / f"{run}.json", res, {"registration": "RESULTS.md X9a", "checkpoint": f"checkpoints/e05/{run}/final.safetensors"})
    del model
    torch.cuda.empty_cache()
    return res


def pilot() -> None:
    meta = load_meta()
    t0 = time.time()
    r = train(20, 0, 0.1, "x9apilot")
    t1 = time.time()
    ev = evaluate(20, 0, "x9apilot")
    info = {k: v for k, v in meta["_x9a"].items() if k != "cipher_map"}
    write_json(OUT / "pilot.json", {"train": {k: r.get(k) for k in ("status", "steps", "val_bpb_full", "train_seconds_this_session", "wall_seconds_this_session", "seconds_per_step")},
                                    "eval_seconds": time.time() - t1, "retrieval_acc": ev["retrieval"]["acc_unmapped"], "retrieval_layer": ev["retrieval"]["layer"],
                                    "assembly_cipher_layer": ev["assembly_cipher"]["detok_layer"], "assembly_english_layer": ev["assembly_english"]["detok_layer"],
                                    "tokenizer_checks": info, "full_run_hours_estimate": r["seconds_per_step"] * r["steps"] * 10 / 3600 if "seconds_per_step" in r else None,
                                    "note": "timing and path check only; no accuracy is used for any decision"}, {"registration": "RESULTS.md X9a pilot"})
    print(json.dumps({k: v for k, v in r.items() if k in ("steps", "seconds_per_step", "val_bpb_full")}), "eval", round(time.time() - t1), "s; total", round(time.time() - t0), "s")


# ------------------------------------------------------------------------------------------------------------------ decision rules
def analyse() -> None:
    rows = {}
    for p in LEVELS:
        for s in (0, 1, 2):
            f = OUT / f"x9a_p{p}_s{s}.json"
            if f.exists():
                rows[(p, s)] = json.load(open(f))
    missing = [(p, s) for p in LEVELS for s in (0, 1, 2) if (p, s) not in rows]
    ret = {p: [rows[(p, s)]["retrieval"]["acc_unmapped"] for s in (0, 1, 2) if (p, s) in rows] for p in LEVELS}
    det = {p: [rows[(p, s)]["assembly_cipher"]["detok_layer"] for s in (0, 1, 2) if (p, s) in rows] for p in LEVELS}
    detE = {p: [rows[(p, s)]["assembly_english"]["detok_layer"] for s in (0, 1, 2) if (p, s) in rows] for p in LEVELS}
    mean = lambda x: float(np.mean(x)) if len(x) else None  # noqa: E731
    sd = lambda x: float(max(np.std(x, ddof=1), 1 / 250)) if len(x) > 1 else 1 / 250  # noqa: E731
    res = {"n_runs": len(rows), "missing": missing, "retrieval_by_level": {p: {"seeds": ret[p], "mean": mean(ret[p])} for p in LEVELS},
           "assembly_cipher_by_level": {p: {"seeds": det[p], "mean": mean([d for d in det[p] if d is not None])} for p in LEVELS},
           "assembly_english_by_level": {p: {"seeds": detE[p]} for p in LEVELS}}
    if not missing:
        m = {p: mean(ret[p]) for p in (1, 5, 20, 50)}
        nondec = all(m[a] <= m[b] for a, b in ((1, 5), (5, 20), (20, 50)))
        gap, sdl = m[50] - m[1], max(sd(ret[1]), sd(ret[50]))
        rho = stats.spearmanr([1, 5, 20, 50], [m[p] for p in (1, 5, 20, 50)]).statistic
        R = "supported" if nondec and gap > 3 * sdl else "refuted" if (m[50] <= m[1] or rho <= 0.6) else "inconclusive"
        res["X9a_R"] = {"means": m, "non_decreasing": nondec, "mean50_minus_mean1": gap, "3x_larger_seed_sd": 3 * sdl, "spearman_level_vs_mean": float(rho), "verdict": R}
        undefined = {p: sum(d is None for d in det[p]) for p in (1, 5, 20, 50)}
        lm = None
        if any(u > 1 for u in undefined.values()):
            A, span = "inconclusive", None
        else:
            lm = [mean([d for d in det[p] if d is not None]) for p in (1, 5, 20, 50)]
            span = max(lm) - min(lm)
            A = "supported" if span <= 1 else "refuted" if span >= 2 else "inconclusive"
        res["X9a_A"] = {"seed_mean_detok_layer": lm if span is not None else None, "max_minus_min": span, "undefined_by_level": undefined, "verdict": A}
        res["joint_reading"] = ("familiarity moves meaning alignment while word assembly stays put at fixed fragmentation" if R == "supported" and A == "supported" else
                                "exposure also moves assembly; the dissociation is not clean" if R == "supported" and A == "refuted" else
                                "no familiarity effect in this setting (small model, letter cipher, no claim beyond that)" if R == "refuted" else "not decided")
        res["level0_descriptive"] = {"retrieval_seeds": ret[0], "chance": 1 / 250, "assembly_cipher_seeds": det[0]}
    write_json(OUT / "analysis.json", res, {"registration": "RESULTS.md X9a (decision rules X9a-R, X9a-A)"})
    print(json.dumps({k: v for k, v in res.items() if k in ("n_runs", "missing", "X9a_R", "X9a_A", "joint_reading")}, indent=1, default=str))


def level0_stripped() -> None:
    """Descriptive only (X9a level-0 observation): level-0 retrieval on pairs with digits and punctuation removed from both texts."""
    meta = load_meta()
    pairs0 = json.load(open(PROC / "eval_pairs.json", encoding="utf-8"))
    strip = lambda t: " ".join(re.sub(r"[0-9]|[^\w\s]|_", "", t).split())  # noqa: E731
    pairs0 = {k: [strip(t) for t in v] for k, v in pairs0.items()}
    out = {}
    for seed in (0, 1, 2):
        run = f"x9a_p0_s{seed}"
        fin = json.load(open(REPO / "results" / "e05_pretrain" / run / "final.json"))
        from safetensors.torch import load_file
        model = GPT(GPTConfig(**fin["model_config"]))
        model.load_state_dict(load_file(str(REPO / "checkpoints" / "e05" / run / "final.safetensors")))
        model = model.cuda().eval()
        tok = D.load_tokenizer(REPO / meta["x9a_p0"]["tokenizer"])
        pairs, fit = fit_pairs(pairs0, tok, fin["ctx_tokens"])
        Xc = story_states(model, tok, pairs["cipher"], fin["ctx_tokens"], "cuda")
        Xe = story_states(model, tok, pairs["english"], fin["ctx_tokens"], "cuda")
        order = np.random.default_rng(0).permutation(len(pairs["english"]))
        tr, te = np.sort(order[: len(order) // 2]), np.sort(order[len(order) // 2:])
        tra, tes = KR.unmapped_curves(Xc, Xe, tr, te)
        lu = int(tra.argmax())
        out[str(seed)] = {"layer": lu, "acc_unmapped": float(tes[lu].mean()), "n_test": int(len(te)), "chance": 1 / len(te), "unstripped_acc": json.load(open(OUT / f"{run}.json"))["retrieval"]["acc_unmapped"]}
        del model
        torch.cuda.empty_cache()
    write_json(OUT / "level0_stripped.json", {"by_seed": out, "mean": float(np.mean([v["acc_unmapped"] for v in out.values()]))}, {"registration": "RESULTS.md X9a level-0 observation (descriptive only)"})
    print(json.dumps(out, indent=1))


def analyse_low() -> None:
    """X9a-low decision rule (registered before any run): six levels 0, 0.01, 0.03, 0.1, 0.3, 1 percent."""
    keys = [("0", 0.0), ("0p01", 0.01), ("0p03", 0.03), ("0p1", 0.1), ("0p3", 0.3), ("1", 1.0)]
    rows = {(k, s): json.load(open(OUT / f"x9a_p{k}_s{s}.json")) for k, _ in keys for s in (0, 1, 2) if (OUT / f"x9a_p{k}_s{s}.json").exists()}
    missing = [(k, s) for k, _ in keys for s in (0, 1, 2) if (k, s) not in rows]
    ret = {k: [rows[(k, s)]["retrieval"]["acc_unmapped"] for s in (0, 1, 2) if (k, s) in rows] for k, _ in keys}
    det = {k: [rows[(k, s)]["assembly_cipher"]["detok_layer"] for s in (0, 1, 2) if (k, s) in rows] for k, _ in keys}
    mean = lambda x: float(np.mean(x)) if len(x) else None  # noqa: E731
    res = {"n_runs": len(rows), "missing": missing, "retrieval_by_level": {str(v): {"seeds": ret[k], "mean": mean(ret[k])} for k, v in keys},
           "assembly_cipher_by_level": {str(v): {"seeds": det[k], "mean": mean([d for d in det[k] if d is not None])} for k, v in keys}}
    if not missing:
        m = [mean(ret[k]) for k, _ in keys]
        rho = float(stats.spearmanr([v for _, v in keys], m).statistic)
        gap = mean(ret["1"]) - mean(ret["0p01"])
        res["rule"] = {"spearman_six_levels": rho, "mean_1pct_minus_mean_0p01pct": gap, "verdict": "dose-response present" if rho >= 0.8 and gap >= 0.05 else "no dose-response",
                       "text": "present if Spearman >= 0.8 and mean(1%) - mean(0.01%) >= 0.05, else no dose-response"}
    write_json(OUT / "analysis_low.json", res, {"registration": "RESULTS.md X9a-low (tag phase2-x9a-low)"})
    print(json.dumps(res, indent=1, default=str))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["prep", "prep_low", "pilot", "train", "eval", "analyse", "analyse_low", "level0_stripped"])
    ap.add_argument("args", nargs="*")
    a = ap.parse_args()
    if a.cmd == "prep":
        prep()
    elif a.cmd == "prep_low":
        prep_low()
    elif a.cmd == "level0_stripped":
        level0_stripped()
    elif a.cmd == "analyse_low":
        analyse_low()
    elif a.cmd == "pilot":
        pilot()
    elif a.cmd == "train":
        level, seed = a.args[0], int(a.args[1])
        r = train(level, seed)
        if r.get("status") == "done" and not (OUT / f"x9a_p{level}_s{seed}.json").exists():
            evaluate(level, seed)
    elif a.cmd == "eval":
        evaluate(a.args[0], int(a.args[1]))
    else:
        analyse()


if __name__ == "__main__":
    main()
