"""NC1: non-canonical tokenization of lossy text (pre-registered in RESULTS.md, 2026-10-22, before this script).

Conditions on the lossy text (decoded text span identical in all three):
  (a) canonical;
  (b) non-canonical, per-sentence text-span token count = the lowercase lossless rung's count for the same sentence;
  (c) non-canonical at the canonical count: every word (b) re-splits is re-split at its canonical count where a
      non-canonical split at that count exists.
Contrasts: NC-F = (c) - (b) (predicted positive, L2 thresholds); NC-O = (a) - (c) (reported, no prediction).

Forced splits: random valid segmentation from the vocabulary. A unit is one whitespace word of the text span: the run
of canonical tokens that starts in it (so it carries its space marker, "Ġ" or "▁"); units never cross pretokenizer
boundaries. Units are re-segmented in token-string space (the concatenation of the unit's canonical token strings),
with a dynamic program that counts segmentations into exactly k vocabulary pieces and samples one uniformly, rejecting
the canonical split. Added/special tokens and byte-fallback tokens are excluded from the pieces. Seeds:
numpy default_rng([0, crc32(model), condition, crc32(item id)]).

Only the text span is re-split; the prompt template and the content-free calibration inputs stay canonical. Text-span
tokens are the canonical prompt tokens whose character range overlaps the field text.

Usage: python scripts/nc1.py chars   (CPU: every character of every lossy text is a single vocab token, 4 tokenizers)
       python scripts/nc1.py pilot   (GPU, Gemma 4 E2B: 20 sentiment items + 20 M4c sentences; no accuracy or
                                      retrieval value is computed; pilot scores are not kept)
Outputs: results/nc1/{chars.json, pilot.json}
"""
import json
import sys
import time
import zlib
from functools import lru_cache

import numpy as np

from shattered.runlog import REPO, results_dir, write_json
from shattered.translit import to_lossy

sys.path.insert(0, str(REPO / "scripts"))
import e0b_familiarity as e0b  # noqa: E402
import l_ladder as lad  # noqa: E402
from m4b_mapping import ACT  # noqa: E402

CONDITIONS = ["a", "b", "c"]
TOKENIZER_MODELS = ["qwen3-1.7b", "qwen3.5-2b", "sarvam-1", "gemma4-e2b"]  # qwen2.5 shares qwen3's tokenizer
PILOT_MODEL, PILOT_N, BASE_SEED = "gemma4-e2b", 20, 0


# ---------------------------------------------------------------- vocabulary and segmentation

class Vocab:
    def __init__(self, tok):
        special = set(tok.all_special_tokens) | set(tok.get_added_vocab())
        self.ids = {s: i for s, i in tok.get_vocab().items()
                    if s not in special and not (s.startswith("<0x") and s.endswith(">"))}
        self.maxlen = max(map(len, self.ids))
        self.tok = tok

    def counts(self, u: str) -> list[dict]:
        """C[i][k] = number of segmentations of u[i:] into exactly k pieces."""
        n = len(u)
        C = [dict() for _ in range(n + 1)]
        C[n][0] = 1
        for i in range(n - 1, -1, -1):
            for j in range(i + 1, min(n, i + self.maxlen) + 1):
                if u[i:j] in self.ids:
                    for k, c in C[j].items():
                        C[i][k + 1] = C[i].get(k + 1, 0) + c
        return C

    def sample(self, u: str, C: list[dict], k: int, rng) -> list[str]:
        out, i = [], 0
        while i < len(u):
            js = [j for j in range(i + 1, min(len(u), i + self.maxlen) + 1) if u[i:j] in self.ids and C[j].get(k - 1)]
            w = np.array([C[j][k - 1] for j in js], dtype=float)
            j = js[rng.choice(len(js), p=w / w.sum())]
            out.append(u[i:j])
            i, k = j, k - 1
        return out


def units(tok, ids: list[int], offs: list, span: tuple[int, int], text: str) -> list[list[int]]:
    """Group the text-span token positions into whitespace words of text[span]."""
    s0, s1 = span
    pos = [p for p, (a, b) in enumerate(offs) if a < s1 and b > s0 and b > a]
    n_words = len(text[s0:s1].split())
    groups, cur, cur_word = [], [], None
    for p in pos:
        a = max(offs[p][0], s0)
        while a < s1 and text[a].isspace():  # a token's own leading space belongs to the word that follows it
            a += 1
        word = n_words if a >= s1 else len(text[s0:a + 1].split())
        if cur and word != cur_word:
            groups.append(cur)
            cur = []
        cur.append(p)
        cur_word = word
    if cur:
        groups.append(cur)
    return groups


def force(V: Vocab, ids: list[int], groups: list[list[int]], targets: dict | None, rng, resplit: set | None):
    """Re-segment the units in `groups`.
    (b): targets is None -> computed by the caller; here `targets` maps unit index -> k and `resplit` is None.
    Returns new ids, per-unit info [(k_canonical, k_new, changed, flag)]."""
    toks = V.tok.convert_ids_to_tokens(ids)
    new, info, last = [], [], 0
    for g_i, g in enumerate(groups):
        new += ids[last:g[0]]
        canon = [toks[p] for p in g]
        u = "".join(canon)
        k = targets.get(g_i, len(g)) if targets else len(g)
        want = resplit is None or g_i in resplit
        flag = None
        if any(t not in V.ids for t in canon):
            pieces, flag = canon, "atomic_token"
        elif want and (len(g) > 1 or k != len(g)):
            C = V.counts(u)
            if not C[0].get(k):
                flag, k = "infeasible_k", len(g)
            n_ways = C[0].get(k, 0)
            if k == len(g) and n_ways <= 1:
                pieces, flag = canon, flag or "canonical_unique"
            else:
                while True:
                    pieces = V.sample(u, C, k, rng)
                    if pieces != canon:
                        break
        else:
            pieces = canon
        new += [V.ids[s] for s in pieces] if flag != "atomic_token" else [ids[p] for p in g]
        info.append({"k_canonical": len(g), "k_new": len(pieces), "changed": pieces != canon, "flag": flag,
                     "pieces": pieces})
        last = g[-1] + 1
    new += ids[last:]
    return new, info


def plan_b(V: Vocab, ids, groups, extra: int, rng) -> tuple[dict, list]:
    """Per-unit target counts for (b): `extra` pieces spread at random over words (cap: max feasible k); if extra < 0,
    pieces are removed down to each word's minimum feasible k. Returns ({unit: k}, flags)."""
    toks = V.tok.convert_ids_to_tokens(ids)
    caps = []
    for g in groups:
        if any(toks[p] not in V.ids for p in g):
            caps.append((len(g), len(g)))
            continue
        C = V.counts("".join(toks[p] for p in g))
        ks = [k for k, c in C[0].items() if c]
        caps.append((min(ks), max(ks)))
    k = [len(g) for g in groups]
    flags = []
    step = 1 if extra >= 0 else -1
    for _ in range(abs(extra)):
        ok = [i for i in range(len(groups)) if (k[i] < caps[i][1] if step > 0 else k[i] > caps[i][0])]
        if not ok:
            flags.append("target_unreachable")
            break
        k[rng.choice(ok)] += step
    if extra < 0:
        flags.append("negative_extra")
    return {i: v for i, v in enumerate(k)}, flags


def rng_for(model: str, cond: str, item: str):
    return np.random.default_rng([BASE_SEED, zlib.crc32(model.encode()), CONDITIONS.index(cond),
                                  zlib.crc32(str(item).encode())])


def make_conditions(V: Vocab, model: str, item: str, ids, offs, span, text, n_target: int) -> dict:
    """{cond: (ids, unit info, flags)} for one text span. n_target = the lowercase rung's span token count."""
    groups = units(V.tok, ids, offs, span, text)
    n_canon = sum(len(g) for g in groups)
    tb, flags_b = plan_b(V, ids, groups, n_target - n_canon, rng_for(model, "b", item))
    ib, info_b = force(V, ids, groups, tb, rng_for(model, "b", item), None)
    resplit_b = {i for i, x in enumerate(info_b) if x["changed"]}
    ic, info_c = force(V, ids, groups, None, rng_for(model, "c", item), resplit_b)
    info_a = [{"k_canonical": len(g), "k_new": len(g), "changed": False, "flag": None,
               "pieces": V.tok.convert_ids_to_tokens([ids[p] for p in g])} for g in groups]
    return {"a": (list(ids), info_a, []), "b": (ib, info_b, flags_b), "c": (ic, info_c, [])}


# ---------------------------------------------------------------- model passes on forced ids

def span_of(prompt: str, value: str, start: int = 0) -> tuple[int, int]:
    s = prompt.find(value, start)
    assert s >= 0
    return s, s + len(value)


def prompt_conditions(V, model, item_id, task, fields: dict, lower_fields: dict) -> dict:
    """Forced prompt ids per condition for one item (all text fields re-split)."""
    from shattered.eval.loglik import build_prompt
    tok = V.tok
    prompt = build_prompt(task, fields)
    prompt_low = build_prompt(task, lower_fields)
    enc = tok(prompt, return_offsets_mapping=True, add_special_tokens=False)
    enc_l = tok(prompt_low, return_offsets_mapping=True, add_special_tokens=False)
    ids, offs = enc["input_ids"], enc["offset_mapping"]
    out = {c: (list(ids), [], []) for c in CONDITIONS}
    cur, cur_l = 0, 0
    for key, value in fields.items():  # templates use each field once, in dict order
        span = span_of(prompt, value, cur)
        span_l = span_of(prompt_low, lower_fields[key], cur_l)
        cur, cur_l = span[1], span_l[1]
        n_low = sum(1 for a, b in enc_l["offset_mapping"] if a < span_l[1] and b > span_l[0] and b > a)
        # re-split each field on the current ids of each condition (offsets refer to the canonical prompt, so fields
        # are processed on the canonical ids and spliced; with one field per prompt this is exact)
        cond = make_conditions(V, model, f"{item_id}|{key}", ids, offs, span, prompt, n_low)
        assert len(fields) == 1, "multi-field splicing not implemented (pilot is sentiment only)"
        out = {c: (cond[c][0], cond[c][1], cond[c][2] + [f"n_lower_span={n_low}"]) for c in CONDITIONS}
    return {"prompt": prompt, "canonical_ids": ids, **out}


def choice_logprobs_ids(model, tok, prompt: str, p_core: list[int], choices: list[str]) -> list[float]:
    """As shattered.eval.loglik.choice_logprobs, but the prompt ids are given; continuation ids are computed from the
    canonical prompt string exactly as there."""
    import torch
    from shattered.eval.loglik import _prefix
    bos = _prefix(tok)
    p_can = bos + tok(prompt, add_special_tokens=False)["input_ids"]
    p_ids = bos + p_core
    out = []
    with torch.no_grad():
        for c in choices:
            full = bos + tok(prompt + c, add_special_tokens=False)["input_ids"]
            cont = full[len(p_can):] if full[: len(p_can)] == p_can else tok(c, add_special_tokens=False)["input_ids"]
            seq = torch.tensor([p_ids + cont], device=model.device)
            n = len(cont)
            logits = model(input_ids=seq, logits_to_keep=n + 1).logits[0, :-1].float()
            logp = torch.log_softmax(logits, -1)
            out.append(float(logp[torch.arange(n), torch.tensor(cont, device=model.device)].sum()))
    return out


def sentence_vector(model, tok, ids: list[int]) -> np.ndarray:
    """As shattered.interp.collect: mean residual over the sentence tokens (after BOS), every layer, float16."""
    import torch
    bos = [tok.bos_token_id] if tok.bos_token_id is not None else []
    with torch.no_grad():
        hs = model(input_ids=torch.tensor([bos + ids], device=model.device), output_hidden_states=True).hidden_states
    H = torch.stack([h[0] for h in hs])
    return H[:, len(bos):].float().mean(1).half().cpu().numpy()


# ---------------------------------------------------------------- summaries

def summarize(per_item: list[dict], words: list[int]) -> dict:
    """per_item: [{cond: (ids_span_count, info)}]; words: whitespace words per item."""
    out = {}
    for c in CONDITIONS:
        n_tok = sum(len([p for u in it[c][1] for p in u["pieces"]]) for it in per_item)
        ranks = [V_ID[p] for it in per_item for u in it[c][1] for p in u["pieces"] if p in V_ID]  # atomic: skipped
        out[c] = {"span_tokens": n_tok, "tokens_per_word": n_tok / sum(words), "median_token_id": float(np.median(ranks)),
                  "mean_piece_chars": float(np.mean([len(p) for it in per_item for u in it[c][1] for p in u["pieces"]]))}
    n_units = sum(len(it["a"][1]) for it in per_item)
    multi = sum(u["k_canonical"] > 1 for it in per_item for u in it["a"][1])
    b_ch = [(ub["changed"], uc["changed"], ub["k_canonical"]) for it in per_item for ub, uc in zip(it["b"][1], it["c"][1])]
    out["words"] = {"n": n_units, "multi_token": multi, "resplit_b_only": sum(b and not c for b, c, _ in b_ch),
                    "resplit_c_only": sum(c and not b for b, c, _ in b_ch), "resplit_both": sum(b and c for b, c, _ in b_ch),
                    "c_resplit_share_of_multi_token": sum(c for b, c, k in b_ch if k > 1) / max(multi, 1),
                    "flags_b": sorted({f for it in per_item for f in it["b"][2] if not f.startswith("n_lower")}),
                    "unit_flags_b": {f: sum(u["flag"] == f for it in per_item for u in it["b"][1])
                                     for f in ("infeasible_k", "canonical_unique", "atomic_token")},
                    "unit_flags_c": {f: sum(u["flag"] == f for it in per_item for u in it["c"][1])
                                     for f in ("infeasible_k", "canonical_unique", "atomic_token")}}
    return out


V_ID: dict = {}


# ---------------------------------------------------------------- steps

def do_chars() -> None:
    """In token-string space (what the segmenter works on): every character of every canonical token string of every
    lossy text must itself be a vocabulary token; tokens outside the piece vocabulary (byte fallback) are counted."""
    from transformers import AutoTokenizer
    from shattered.interp.load import MODELS as REPOS
    a, c = lad.e0b_items(), lad.e0c_items()
    _, _, native = lad.m4c_sample()
    texts = [v for its in a.values() for it in its for v in it["forms"]["lossy"].values()]
    texts += [it["forms"]["lossy"]["text"] for it in c["sib"]] + [to_lossy(t) for t in native]
    res = {}
    for m in TOKENIZER_MODELS:
        V = Vocab(AutoTokenizer.from_pretrained(REPOS[m]))
        toks = [t for x in V.tok(texts, add_special_tokens=False)["input_ids"] for t in V.tok.convert_ids_to_tokens(x)]
        atomic = [t for t in toks if t not in V.ids]
        chars = {ch for t in toks if t in V.ids for ch in t}
        res[m] = {"n_tokens": len(toks), "n_atomic_tokens": len(atomic), "atomic_examples": sorted(set(atomic))[:20],
                  "n_chars": len(chars), "chars_not_single_tokens": sorted(ch for ch in chars if ch not in V.ids)}
        print(m, res[m], flush=True)
    write_json(results_dir("nc1") / "chars.json", res, {"texts": len(texts)})


def do_pilot() -> None:
    import pandas as pd
    import torch
    from shattered.eval.loglik import VERBALIZERS, choice_logprobs
    from shattered.interp.load import load
    global V_ID
    m = PILOT_MODEL
    a = lad.e0b_items()
    sent = a["sentiment"][:PILOT_N]
    R, keep, native = lad.m4c_sample()
    m4c = [(r["index"], t) for r, k, t in zip(R, keep, native) if k][:PILOT_N]
    t0 = time.time()
    model, tok = load(m, "cuda")
    load_s = time.time() - t0
    V = Vocab(tok)
    V_ID = V.ids
    report = {"model": m, "load_s": load_s}

    # --- sentiment: forced prompt ids per condition
    t_build = time.time()
    P = [prompt_conditions(V, m, it["id"], "sentiment", it["forms"]["lossy"], it["forms"]["lower"]) for it in sent]
    report["sentiment_build_s"] = time.time() - t_build
    # check 1: decoded prompt identical in every condition
    dec_ok = {c: sum(tok.decode(p[c][0]) == tok.decode(p["canonical_ids"]) for p in P) for c in CONDITIONS}
    # check 2: (b) span count hits the lowercase-rung target; (c) equals canonical
    def span_n(p, c):
        return sum(len(u["pieces"]) for u in p[c][1])
    tgt = [int(next(f for f in p["b"][2] if f.startswith("n_lower_span=")).split("=")[1]) for p in P]
    report["sentiment_check2"] = {"b_hits_target": sum(span_n(p, "b") == t for p, t in zip(P, tgt)),
                                  "c_equals_canonical": sum(span_n(p, "c") == span_n(p, "a") for p in P),
                                  "b_minus_target": [span_n(p, "b") - t for p, t in zip(P, tgt)], "n": len(P)}
    words = [len(it["forms"]["lossy"]["text"].split()) for it in sent]
    report["sentiment_check1_decode_identical"] = dec_ok
    report["sentiment_summary"] = summarize(P, words)
    report["sentiment_tokens_per_word_lower_target"] = sum(tgt) / sum(words)

    # check 4 + timing: canonical ids through the forced path vs stored lossy log-probs; (b), (c) timed only
    stored = pd.read_parquet(lad.E0B_DIR / f"{m}__lossy.parquet").set_index(["task", "id"])
    diffs, same_pred, timing = [], 0, {}
    lp_cache = {}
    for c in CONDITIONS:
        t1 = time.time()
        for it, p in zip(sent, P):
            lp_cache[(c, it["id"])] = choice_logprobs_ids(model, tok, p["prompt"], p[c][0], VERBALIZERS["sentiment"])
        timing[c] = (time.time() - t1) / len(sent)
    t1 = time.time()
    for it, p in zip(sent, P):
        choice_logprobs(model, tok, p["prompt"], VERBALIZERS["sentiment"])
    timing["standard_path"] = (time.time() - t1) / len(sent)
    for it in sent:
        s = np.asarray(stored.loc[("sentiment", it["id"])].logprobs)
        x = np.asarray(lp_cache[("a", it["id"])])
        diffs.append(float(np.abs(s - x).max()))
        same_pred += int(np.argmax(s) == np.argmax(x))
    report["sentiment_check4"] = {"same_raw_prediction": same_pred, "n": len(sent), "max_abs_dlogprob": max(diffs)}
    report["sentiment_seconds_per_item"] = timing
    del lp_cache  # pilot scores are not kept and no accuracy is computed

    # --- M4c sentences: forced ids per condition, sentence vectors
    low = {i: lad.to_lower(t) for i, t in m4c}
    Q, vec_diff, ftime = [], [], {}
    for i, t in m4c:
        text = to_lossy(t)
        enc = tok(text, return_offsets_mapping=True, add_special_tokens=False)
        n_low = len(tok(low[i], add_special_tokens=False)["input_ids"])
        cond = make_conditions(V, m, f"m4c|{i}", enc["input_ids"], enc["offset_mapping"], (0, len(text)), text, n_low)
        Q.append({"text": text, "canonical_ids": enc["input_ids"], "n_low": n_low, **cond})
    report["m4c_check1_decode_identical"] = {c: sum(tok.decode(q[c][0]) == q["text"] for q in Q) for c in CONDITIONS}
    report["m4c_check1_canonical_decode_identical"] = sum(tok.decode(q["canonical_ids"]) == q["text"] for q in Q)
    report["m4c_check2"] = {"b_hits_target": sum(len(q["b"][0]) == q["n_low"] for q in Q),
                            "c_equals_canonical": sum(len(q["c"][0]) == len(q["a"][0]) for q in Q),
                            "b_minus_target": [len(q["b"][0]) - q["n_low"] for q in Q], "n": len(Q)}
    report["m4c_summary"] = summarize(Q, [len(q["text"].split()) for q in Q])
    report["m4c_tokens_per_word_lower_target"] = sum(q["n_low"] for q in Q) / sum(len(q["text"].split()) for q in Q)
    st = np.load(ACT / m / "lossy500.npz")
    pos = {int(ix): j for j, ix in enumerate(st["index"])}
    for c in CONDITIONS:
        t1 = time.time()
        for (i, _), q in zip(m4c, Q):
            v = sentence_vector(model, tok, q[c][0])
            if c == "a":
                ref = st["flores_states"][pos[i]].astype(np.float32)
                vec_diff.append(float(np.abs(v.astype(np.float32) - ref).max() / (np.abs(ref).max() + 1e-9)))
        ftime[c] = (time.time() - t1) / len(m4c)
    report["m4c_check4_canonical_vs_stored_vectors"] = {"max_rel_abs_diff": max(vec_diff), "n": len(vec_diff)}
    report["m4c_seconds_per_sentence"] = ftime
    del model
    torch.cuda.empty_cache()

    # --- extrapolation from the ladder's stored scoring times (lower form) x forced/standard time ratio
    ratio = np.mean([timing[c] for c in CONDITIONS]) / timing["standard_path"]
    est = {}
    for mm in lad.ACC_MODELS:
        s = sum(json.load(open(d / f"{mm}__lower.json"))["seconds"] for d in (lad.E0B_DIR, lad.E0C_DIR))
        est[mm] = s * ratio * len(CONDITIONS)
    fwd = np.mean([ftime[c] for c in CONDITIONS]) * 500 * len(CONDITIONS) * len(lad.M4_MODELS)
    report["estimate"] = {"forced_over_standard_time_ratio": ratio,
                          "scoring_s_per_model_3_conditions": est, "scoring_total_h": sum(est.values()) / 3600,
                          "forward_total_min_using_gemma_rate": fwd / 60,
                          "basis": "ladder lower-form scoring seconds (E0b sentiment+xnli, E0c sib) x forced/standard "
                                   "ratio measured here x 3 conditions; forward at Gemma's measured rate"}
    write_json(results_dir("nc1") / "pilot.json", report,
               {"status": "pilot, no accuracy or retrieval computed", "n": PILOT_N, "model": m})
    print(json.dumps(report, indent=1, default=str), flush=True)


if __name__ == "__main__":
    {"chars": do_chars, "pilot": do_pilot}[sys.argv[1]]()
