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
       python scripts/nc1.py forward (GPU: (a)/(b)/(c) sentence vectors, 500 M4c sentences, 4 models)
       python scripts/nc1.py score   (GPU: sentiment, XNLI, SIB-200 in (a)/(b)/(c), 5 models)
       python scripts/nc1.py analyse (CPU: segmentation checks, retrieval, accuracy, NC-F / NC-O, verdicts)
Outputs: results/nc1/{chars.json, pilot.json, segmentation.csv, retrieval.csv, accuracy.csv, contrasts.csv,
         verdict.json}; vectors cache/activations/nc1/<model>/{a,b,c}500.npz; scores results/nc1/scores/
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


def build_with_spans(task: str, fields: dict) -> tuple[str, dict]:
    """The prompt (identical to loglik.build_prompt) and the character span of each field in it."""
    import string
    from shattered.eval.loglik import TEMPLATES, build_prompt
    tpl = (TEMPLATES / f"e0_{task}_v1.txt").read_text(encoding="utf-8")
    out, spans = "", {}
    for lit, name, _, _ in string.Formatter().parse(tpl):
        out += lit
        if name is not None:
            assert name not in spans, "field used twice"
            spans[name] = (len(out), len(out) + len(fields[name]))
            out += fields[name]
    assert out == build_prompt(task, fields)
    return out, spans


def prompt_conditions(V, model, item_id, task, fields: dict, lower_fields: dict) -> dict:
    """Forced prompt ids per condition for one item; every text field is re-split. Each field is re-segmented on the
    canonical prompt ids (fields never share a token: checked) and the new spans are spliced in from the end."""
    tok = V.tok
    prompt, spans = build_with_spans(task, fields)
    prompt_low, spans_l = build_with_spans(task, lower_fields)
    enc = tok(prompt, return_offsets_mapping=True, add_special_tokens=False)
    enc_l = tok(prompt_low, return_offsets_mapping=True, add_special_tokens=False)
    ids, offs = enc["input_ids"], enc["offset_mapping"]
    per_field = []
    for key in fields:
        span, span_l = spans[key], spans_l[key]
        n_low = sum(1 for a, b in enc_l["offset_mapping"] if a < span_l[1] and b > span_l[0] and b > a)
        groups = units(tok, ids, offs, span, prompt)
        g0, g1 = groups[0][0], groups[-1][-1]
        cond = make_conditions(V, model, f"{item_id}|{key}", ids, offs, span, prompt, n_low)
        repl = {c: cond[c][0][g0:len(cond[c][0]) - (len(ids) - g1 - 1)] for c in CONDITIONS}
        per_field.append((g0, g1, repl, cond, n_low))
    per_field.sort(key=lambda x: x[0])
    for (_, e0, *_), (s1, *_) in zip(per_field, per_field[1:]):
        assert e0 < s1, "two fields share a token"
    out = {}
    for c in CONDITIONS:
        new = list(ids)
        for g0, g1, repl, _, _ in reversed(per_field):
            new[g0:g1 + 1] = repl[c]
        info = [u for *_, cond, _ in per_field for u in cond[c][1]]
        flags = [f for *_, cond, _ in per_field for f in cond[c][2]]
        out[c] = (new, info, flags + [f"n_lower_span={sum(x[4] for x in per_field)}"])
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


# ---------------------------------------------------------------- full run (after the gate, approved 2026-10-22)

NC_ACT = REPO / "cache" / "activations" / "nc1"
SCORES = REPO / "results" / "nc1" / "scores"
CONTRASTS_NC = [("NC-F", "c", "b"), ("NC-O", "a", "c")]


def m4c_conditions(V, m, R, native):
    """[(index, text, n_lower, {cond: (ids, info, flags)})] for all 500 M4c rows."""
    out = []
    for r, t in zip(R, native):
        i, text = r["index"], to_lossy(t)
        enc = V.tok(text, return_offsets_mapping=True, add_special_tokens=False)
        n_low = len(V.tok(lad.to_lower(t), add_special_tokens=False)["input_ids"])
        out.append((i, text, n_low, make_conditions(V, m, f"m4c|{i}", enc["input_ids"], enc["offset_mapping"],
                                                     (0, len(text)), text, n_low)))
    return out


def do_forward() -> None:
    import torch
    from shattered.interp.load import load
    from shattered.runlog import commit, tmp_path
    R, _, native = lad.m4c_sample()
    for m in lad.M4_MODELS:
        todo = [c for c in CONDITIONS if not (NC_ACT / m / f"{c}500.npz").exists()]
        if not todo:
            continue
        t0 = time.time()
        model, tok = load(m, "cuda")
        V = Vocab(tok)
        Q = m4c_conditions(V, m, R, native)
        for c in todo:
            vecs = np.stack([sentence_vector(model, tok, q[3][c][0]) for q in Q])
            path = NC_ACT / m / f"{c}500.npz"
            path.parent.mkdir(parents=True, exist_ok=True)
            np.savez(tmp_path(path), flores_states=vecs, index=np.array([q[0] for q in Q]),
                     n_tokens=np.array([len(q[3][c][0]) for q in Q]))
            commit(tmp_path(path), path)
            print(f"{m}: nc {c}500 forward done ({time.time() - t0:.0f}s since load)", flush=True)
        del model
        torch.cuda.empty_cache()


def score_items():
    a, c = lad.e0b_items(), lad.e0c_items()
    return [("sentiment", a["sentiment"]), ("xnli", a["xnli"]), ("sib", c["sib"])]


def do_score() -> None:
    import pandas as pd
    import torch
    from shattered.eval.loglik import VERBALIZERS
    from shattered.interp.load import load
    from shattered.runlog import commit, tmp_path
    SCORES.mkdir(parents=True, exist_ok=True)
    tasks = score_items()
    print({t: len(its) for t, its in tasks}, flush=True)
    for m in lad.ACC_MODELS:
        todo = [c for c in CONDITIONS if not (SCORES / f"{m}__nc_{c}.parquet").exists()]
        if not todo:
            continue
        t0 = time.time()
        model, tok = load(m, "cuda")
        V = Vocab(tok)
        rows = {c: [] for c in todo}
        for t, its in tasks:
            for it in its:
                P = prompt_conditions(V, m, it["id"], t, it["forms"]["lossy"], it["forms"]["lower"])
                for c in todo:
                    lp = choice_logprobs_ids(model, tok, P["prompt"], P[c][0], VERBALIZERS[t])
                    rows[c].append({"model": m, "task": t, "form": f"nc_{c}", "id": it["id"], "label": it["label"],
                                    "logprobs": lp, "pred_raw": int(np.argmax(lp)), "prompt_tokens": len(P[c][0])})
            print(f"{m}: {t} done ({time.time() - t0:.0f}s since load)", flush=True)
        for c in todo:
            path = SCORES / f"{m}__nc_{c}.parquet"
            pd.DataFrame(rows[c]).to_parquet(tmp_path(path))
            commit(tmp_path(path), path)
        del model
        torch.cuda.empty_cache()


def segmentation_table():
    """CPU: tokens per word, re-split counts and rank proxy per tokenizer x dataset x condition (deterministic seeds,
    so identical to the splits used in the forward and score steps)."""
    import pandas as pd
    from transformers import AutoTokenizer
    from shattered.interp.load import MODELS as REPOS
    global V_ID
    R, keep, native = lad.m4c_sample()
    tasks = score_items()
    lad_tpw = pd.read_csv(REPO / "results/l_ladder/tokens_per_word.csv").set_index(["model", "dataset", "form"])
    rows = []
    for m in lad.ACC_MODELS:
        V = Vocab(AutoTokenizer.from_pretrained(REPOS[m]))
        V_ID = V.ids
        sets = {}
        Q = m4c_conditions(V, m, R, native)
        sets["m4c496"] = ([{c: q[3][c] for c in CONDITIONS} for q, k in zip(Q, keep) if k],
                          [len(q[1].split()) for q, k in zip(Q, keep) if k])
        for t, its in tasks:
            P = [prompt_conditions(V, m, it["id"], t, it["forms"]["lossy"], it["forms"]["lower"]) for it in its]
            sets[t] = (P, [sum(len(v.split()) for v in it["forms"]["lossy"].values()) for it in its])
        for d, (items, words) in sets.items():
            sm = summarize(items, words)
            canon_equal = sum(sum(len(u["pieces"]) for u in it["c"][1]) == sum(len(u["pieces"]) for u in it["a"][1])
                              for it in items)
            low = lad_tpw.loc[(m, d, "lower"), "tokens_per_word"]
            for c in CONDITIONS:
                row = {"model": m, "dataset": d, "condition": c, "n_items": len(items), **sm[c],
                       "lower_rung_tokens_per_word": low, "ratio_to_lower_rung": sm[c]["tokens_per_word"] / low}
                if c == "b":
                    row["b_within_2pct_of_lower"] = abs(sm[c]["tokens_per_word"] / low - 1) <= 0.02
                if c == "c":
                    row["c_items_equal_canonical"] = canon_equal
                row.update({f"words_{k}": v for k, v in sm["words"].items() if not isinstance(v, (list, dict))})
                row.update({k: json.dumps(sm["words"][k]) for k in ("unit_flags_b", "unit_flags_c", "flags_b")})
                rows.append(row)
            print(m, d, "segmentation done", flush=True)
    return pd.DataFrame(rows)


def do_analyse() -> None:
    import pandas as pd
    from statsmodels.stats.multitest import multipletests
    from m4b_mapping import boot, layer_fit
    from m4c_natural_flores import SEED
    out = results_dir("nc1")
    seg = segmentation_table()
    seg.to_csv(out / "segmentation.csv", index=False)
    # retrieval: exactly as the ladder (M4c split, train-half best unmapped layer)
    R, keep, _ = lad.m4c_sample()
    idx = np.array([r["index"] for r in R])[keep]
    n = len(idx)
    order = np.random.default_rng(SEED).permutation(n)
    tr, te = np.sort(order[: n // 2]), np.sort(order[n // 2:])
    folds = np.array_split(np.random.default_rng(SEED + 2).permutation(tr), 5)
    res, con = [], []
    for m in lad.M4_MODELS:
        E = np.load(ACT / m / "english.npz")["flores_states"][idx]
        hits = {}
        for c in CONDITIONS:
            z = np.load(NC_ACT / m / f"{c}500.npz")
            assert np.array_equal(z["index"][keep], idx)
            X = z["flores_states"][keep]
            fits = [layer_fit(X[:, l], E[:, l], tr, te, folds) for l in range(X.shape[1])]
            lu = int(np.argmax([r["unmapped_train"] for r in fits]))
            hits[c] = fits[lu]["unmapped"]
            res.append({"model": m, "condition": c, "n_test": len(te), "unmapped_test": hits[c].mean(),
                        "unmapped_test_ci": boot(hits[c]), "unmapped_layer": lu})
        for L, a, b in CONTRASTS_NC:
            con.append({"measure": "retrieval", "model": m, "contrast": L, "a": a, "b": b,
                        **lad.paired(hits[a], hits[b])})
    pd.DataFrame(res).to_csv(out / "retrieval.csv", index=False)
    # accuracy: stored canonical-English rows decide the calibration fallback, as in the ladder
    acc_rows = []
    for d, tasks in ((lad.E0B_DIR, ("sentiment", "xnli")), (lad.E0C_DIR, ("sib",))):
        cf = {m: json.load(open(d / f"cf_{m}.json")) for m in lad.ACC_MODELS}
        B = pd.concat([pd.read_parquet(d / f"{m}__english.parquet") for m in lad.ACC_MODELS]
                      + [pd.read_parquet(SCORES / f"{m}__nc_{c}.parquet") for m in lad.ACC_MODELS
                         for c in CONDITIONS], ignore_index=True)
        B = B[B.task.isin(tasks)]
        B, _ = e0b.apply_calibration(B, cf)
        acc_rows.append(e0b.accuracy_table(B))
        for t in tasks:
            measure = t if t != "xnli" else "xnli_reported_only"
            for m in lad.ACC_MODELS:
                g = B[(B.model == m) & (B.task == t)]
                piv = g.pivot_table(index="id", columns="form", values="pred_cal")
                corr = piv.eq(g.drop_duplicates("id").set_index("id").label.loc[piv.index], axis=0)
                for L, a, b in CONTRASTS_NC:
                    con.append({"measure": measure, "model": m, "contrast": L, "a": a, "b": b,
                                **lad.paired(corr[f"nc_{a}"].to_numpy(), corr[f"nc_{b}"].to_numpy())})
    pd.concat(acc_rows, ignore_index=True).to_csv(out / "accuracy.csv", index=False)
    K = pd.DataFrame(con)
    counted = {"retrieval": lad.COUNT_RETRIEVAL, "sentiment": lad.COUNT_ACC, "sib": lad.COUNT_ACC}
    need = {"retrieval": 2, "sentiment": 3, "sib": 3}
    K["counted"] = [m in counted.get(s, []) for s, m in zip(K.measure, K.model)]
    K["p_holm"] = np.nan
    for s in counted:
        k = (K.measure == s) & K.counted
        K.loc[k, "p_holm"] = multipletests(K.loc[k, "p"], method="holm")[1]
    K["significant"] = K.p_holm < 0.05
    K["ci_excludes_0"] = [c[0] > 0 or c[1] < 0 for c in K.ci]
    K["ci_holm_disagree"] = K.counted & (K.significant != K.ci_excludes_0)
    K.to_csv(out / "contrasts.csv", index=False)
    dataset = {"retrieval": "m4c496", "sentiment": "sentiment", "sib": "sib"}
    verdicts = {}
    for s in counted:
        for L, _, _ in CONTRASTS_NC:
            g = K[(K.measure == s) & (K.contrast == L) & K.counted]
            pos, neg = int((g.significant & (g["diff"] > 0)).sum()), int((g.significant & (g["diff"] < 0)).sum())
            v = "effect, positive" if pos >= need[s] else "effect, negative" if neg >= need[s] else "no effect detected"
            sg = seg[(seg.dataset == dataset[s]) & seg.model.isin(counted[s]) & (seg.condition == "b")]
            verdicts[f"{L}|{s}"] = {
                "verdict": v, "status": "registered prediction: positive" if L == "NC-F" else "reported, no prediction",
                "n_significant_positive": pos, "n_significant_negative": neg, "needed": need[s], "n_counted": len(g),
                "tpw_check_b_failed_models": sg[~sg.b_within_2pct_of_lower.astype(bool)].model.tolist(),
                "ci_holm_disagreements": g[g.ci_holm_disagree].model.tolist()}
    write_json(out / "verdict.json", verdicts, {"registered": "RESULTS.md 2026-10-22 (NC1)",
                                                 "counted_retrieval": lad.COUNT_RETRIEVAL,
                                                 "counted_accuracy": lad.COUNT_ACC, "m4c_split_seed": SEED})
    print("analysis written", flush=True)  # results are read only after the chain finishes


if __name__ == "__main__":
    {"chars": do_chars, "pilot": do_pilot, "forward": do_forward, "score": do_score,
     "analyse": do_analyse}[sys.argv[1]]()
