"""X3: frequency-matched non-canonical tokenization of lossy Kannada (registered in RESULTS.md, 2026-11-01, section X3).

Conditions (all decode to the same lossy string): a = canonical and NC-O = the Phase 1 equal-count random split (both read
from the Phase 1 NC1 files, never rescored except for a 2-item recompute control); m = the Phase 2 frequency-matched equal-count
split built with the tokenizer-internal proxy s_int(p) = ln(1 + merge rank of p) (the registered primary); r = the same rule
with the corpus proxy s_ref (exploratory, no verdict). Tolerance 0.25 x SD of the proxy over the canonical tokenization of a
decontaminated 100,000-word lossy Wikipedia sample; exhaustive enumeration up to 50,000 segmentations, else 50,000 uniform
samples; the segmentation closest in mean proxy to the canonical split is chosen (ties at random, seeded); no segmentation
inside the tolerance leaves the word canonical. An item is eligible if changed words >= 0.5 x multi-piece words.

Usage: python scripts/x3.py build    (CPU: reference sample, proxies, splits for 5 models x 4 datasets, eligibility, balance)
       python scripts/x3.py pilot    (GPU, Gemma 4 E2B: timing on 20 eligible items and 20 sentences; no accuracy computed)
       python scripts/x3.py score    (GPU: eligible items in m and r, M4c vectors, recompute control; resumable)
       python scripts/x3.py analyse  (CPU: D1-D3 per measure, floors, verdicts)
Outputs: results/phase2/x3/{reference_sample.json, proxies.json, splits/<model>.json, eligibility.csv, balance.csv, pilot.json,
         scores/, control.csv, retrieval.csv, accuracy.csv, contrasts.csv, verdict.json}; cache/activations/x3/<model>/{m,r}500.npz
"""
import json
import math
import sys
import time
import unicodedata
import zlib
from collections import Counter

import numpy as np

from shattered.runlog import REPO, results_dir, write_json
from shattered.translit import to_lossy

sys.path.insert(0, str(REPO / "scripts"))
import l_ladder as lad  # noqa: E402
import nc1  # noqa: E402

OUT = results_dir("phase2/x3")
X3_ACT = REPO / "cache" / "activations" / "x3"
SCORES = OUT / "scores"
MODELS = lad.ACC_MODELS  # qwen2.5-1.5b, qwen3.5-2b, sarvam-1, gemma4-e2b, qwen3-1.7b
CONDS = ["m", "r"]  # m = primary (s_int), r = exploratory (s_ref)
TOL_SD, ENUM_CAP, SAMPLE_N, REF_WORDS, ELIG = 0.25, 50_000, 50_000, 100_000, 0.5
FLOOR_ACC, FLOOR_RET = 300, 150
GROUPS = nc1.GROUPS


# ---------------------------------------------------------------- reference sample and proxies

def eval_texts() -> list[str]:
    """Kannada evaluation texts (native script) that no reference article may contain."""
    from m14_full import flores_forms
    out = list(flores_forms()["native"])
    a, c = lad.e0b_items(), lad.e0c_items()
    for its in list(a.values()) + [c["sib"]]:
        for it in its:
            out += list(it["forms"]["native"].values())
    kn = REPO / "data" / "raw" / "indicsentiment" / "data" / "test" / "kn.json"  # every IndicSentiment kn review, used or not
    for line in kn.open(encoding="utf-8"):
        r = json.loads(line)
        out += [r[k] for k in r if "REVIEW" in k and k != "ENGLISH REVIEW"]
    return sorted({unicodedata.normalize("NFC", t.strip()) for t in out if t and t.strip()})


def contaminated(article: str, short: set, windows: dict) -> bool:
    art = unicodedata.normalize("NFC", article)
    if art.strip() in short:
        return True
    for i in range(len(art) - 19):
        for s in windows.get(art[i:i + 20], ()):
            if s in art:
                return True
    return False


def reference_sample() -> dict:
    path = OUT / "reference_sample.json"
    if path.exists():
        return json.load(open(path, encoding="utf-8"))
    from shattered.data import corpora
    ev = eval_texts()
    short = {s for s in ev if len(s) < 20}
    windows: dict = {}
    for s in ev:
        if len(s) >= 20:
            windows.setdefault(s[:20], []).append(s)
    arts = corpora.wikipedia("kn")
    order = np.random.default_rng(0).permutation(len(arts))
    words, used, removed, unmapped = [], 0, 0, 0
    for i in order:
        if len(words) >= REF_WORDS:
            break
        if contaminated(arts[i], short, windows):
            removed += 1
            continue
        used += 1
        for w in unicodedata.normalize("NFC", arts[i]).split():
            try:
                words.append(to_lossy(w))
            except KeyError:
                unmapped += 1
    words = words[:REF_WORDS]
    res = {"words": words, "n_articles_used": used, "n_articles_removed_while_drawing": removed,
           "n_articles_total": len(arts), "n_eval_texts": len(ev), "unmapped_words_dropped": unmapped}
    write_json(path, res, {"seed": 0, "words": REF_WORDS, "rule": "exact or containment (>= 20 characters) match with an evaluation text removes the article"})
    return res


def merge_scores(tok) -> dict:
    j = json.loads(tok.backend_tokenizer.to_str())["model"]
    rank: dict = {}
    for r, m in enumerate(j["merges"]):
        a, b = (m if isinstance(m, list) else m.split(" "))
        rank.setdefault(a + b, r)
    return rank


class Proxy:
    def __init__(self, name: str, sc: dict, sd: float):
        self.name, self.sc, self.sd = name, sc, sd

    def piece(self, p: str) -> float:
        return self.sc.get(p, 0.0)


def make_proxies(tok, V, ref_words: list[str]) -> dict:
    rank = merge_scores(tok)
    s_int = {p: math.log1p(rank.get(p, 0)) for p in V.ids}  # base pieces and pieces no merge creates: rank 0 (registered)
    lines = [" ".join(ref_words[i:i + 20]) for i in range(0, len(ref_words), 20)]
    toks = [t for x in tok(lines, add_special_tokens=False)["input_ids"] for t in tok.convert_ids_to_tokens(x)]
    cnt = Counter(toks)
    s_ref = {p: math.log1p(cnt.get(p, 0)) for p in V.ids}
    return {"m": Proxy("s_int", s_int, float(np.std([s_int.get(t, 0.0) for t in toks]))),
            "r": Proxy("s_ref", s_ref, float(np.std([s_ref.get(t, 0.0) for t in toks]))),
            "_n_sample_tokens": len(toks), "_n_merge_ranked_pieces": sum(p in rank for p in V.ids)}


# ---------------------------------------------------------------- the frequency-matched split

_ENUM: dict = {}


def enumerate_all(V, u: str, C: list, k: int) -> list:
    out = []

    def rec(i, kk, acc):
        if i == len(u):
            out.append(tuple(acc))
            return
        for j in range(i + 1, min(len(u), i + V.maxlen) + 1):
            if u[i:j] in V.ids and C[j].get(kk - 1):
                acc.append(u[i:j])
                rec(j, kk - 1, acc)
                acc.pop()

    rec(0, k, [])
    return out


def split_word(V, proxy: Proxy, canon: list[str], rng) -> tuple[list[str], str | None, int]:
    """Pieces of the frequency-matched split for one multi-piece unit; returns (pieces, flag, number of candidates)."""
    u, k = "".join(canon), len(canon)
    C = V.counts(u)
    n_ways = C[0].get(k, 0)
    if n_ways <= 1:
        return canon, "canonical_unique", n_ways
    key = (id(V), proxy.name, u, k)
    if n_ways <= ENUM_CAP:
        if key not in _ENUM:
            cands = enumerate_all(V, u, C, k)
            _ENUM[key] = (cands, np.array([sum(proxy.piece(p) for p in c) for c in cands]))
        cands, sums = _ENUM[key]
    else:
        cands = [tuple(V.sample(u, C, k, rng)) for _ in range(SAMPLE_N)]
        sums = np.array([sum(proxy.piece(p) for p in c) for c in cands])
    target = sum(proxy.piece(p) for p in canon)
    d = np.abs(sums - target)
    ok = np.array([c != tuple(canon) for c in cands]) & (d <= TOL_SD * proxy.sd * k + 1e-12)
    if not ok.any():
        return canon, "no_candidate_within_tolerance", n_ways
    best = d[ok].min()
    tied = np.flatnonzero(ok & (d <= best + 1e-12))
    return list(cands[int(tied[rng.integers(len(tied))]) if len(tied) > 1 else int(tied[0])]), None, n_ways


def rng_word(model: str, item: str, w: int, cond: str):
    base = [nc1.BASE_SEED, zlib.crc32(model.encode()), zlib.crc32(str(item).encode()), w]
    return np.random.default_rng(base + ([1] if cond == "r" else []))


def split_units(V, model: str, item: str, ids: list[int], groups: list, proxy: Proxy, cond: str):
    """As nc1.force for the re-split of every multi-piece unit; returns new ids and per-unit info."""
    toks = V.tok.convert_ids_to_tokens(ids)
    new, info, last = [], [], 0
    for w, g in enumerate(groups):
        new += ids[last:g[0]]
        canon = [toks[p] for p in g]
        flag, pieces = None, canon
        if any(t not in V.ids for t in canon):
            flag = "atomic_token"
        elif len(g) > 1:
            pieces, flag, _ = split_word(V, proxy, canon, rng_word(model, item, w, cond))
        else:
            flag = "single_piece"
        new += [V.ids[s] for s in pieces] if flag != "atomic_token" else [ids[p] for p in g]
        info.append({"k_canonical": len(g), "k_new": len(pieces), "changed": pieces != canon, "flag": flag, "pieces": pieces})
        last = g[-1] + 1
    new += ids[last:]
    return new, info


def prompt_variants(V, model: str, item_id, task: str, fields: dict, proxies: dict) -> dict:
    """Forced prompt ids for m and r; every text field is re-split, as nc1.prompt_conditions."""
    tok = V.tok
    prompt, spans = nc1.build_with_spans(task, fields)
    enc = tok(prompt, return_offsets_mapping=True, add_special_tokens=False)
    ids, offs = enc["input_ids"], enc["offset_mapping"]
    per_field = []
    for key in fields:
        groups = nc1.units(tok, ids, offs, spans[key], prompt)
        g0, g1 = groups[0][0], groups[-1][-1]
        res = {c: split_units(V, model, f"{item_id}|{key}", ids, groups, proxies[c], c) for c in CONDS}
        per_field.append((g0, g1, {c: res[c][0][g0:len(res[c][0]) - (len(ids) - g1 - 1)] for c in CONDS}, res))
    per_field.sort(key=lambda x: x[0])
    out = {"prompt": prompt, "canonical_ids": ids}
    for c in CONDS:
        new = list(ids)
        for g0, g1, repl, _ in reversed(per_field):
            new[g0:g1 + 1] = repl[c]
        out[c] = (new, [u for *_, res in per_field for u in res[c][1]])
    return out


def sentence_variants(V, model: str, idx, text: str, proxies: dict) -> dict:
    enc = V.tok(text, return_offsets_mapping=True, add_special_tokens=False)
    ids, offs = enc["input_ids"], enc["offset_mapping"]
    groups = nc1.units(V.tok, ids, offs, (0, len(text)), text)
    out = {"text": text, "canonical_ids": ids}
    for c in CONDS:
        out[c] = split_units(V, model, f"m4c|{idx}", ids, groups, proxies[c], c)
    return out


def elig(info: list) -> tuple[int, int]:
    multi = sum(u["k_canonical"] > 1 for u in info)
    return multi, sum(u["changed"] for u in info)


# ---------------------------------------------------------------- steps

def datasets():
    a, c = lad.e0b_items(), lad.e0c_items()
    return {"sentiment": a["sentiment"], "xnli": a["xnli"], "sib": c["sib"]}


def do_build() -> None:
    import pandas as pd
    from transformers import AutoTokenizer
    from shattered.interp.load import MODELS as REPOS
    (OUT / "splits").mkdir(exist_ok=True)
    ref = reference_sample()
    print("reference sample:", {k: v for k, v in ref.items() if k != "words"}, flush=True)
    sets = datasets()
    R, keep, native = lad.m4c_sample()
    elig_rows, bal_rows, prox_out = [], [], {}
    for m in MODELS:
        t0 = time.time()
        V = nc1.Vocab(AutoTokenizer.from_pretrained(REPOS[m]))
        P = make_proxies(V.tok, V, ref["words"])
        prox_out[m] = {"s_int_sd": P["m"].sd, "s_ref_sd": P["r"].sd, "n_sample_tokens": P["_n_sample_tokens"],
                       "n_pieces_with_merge_rank": P["_n_merge_ranked_pieces"], "n_vocab_pieces": len(V.ids)}
        split, rows = {}, []  # rows: per item, pieces of a, NC-O, m, r
        for d, its in sets.items():
            split[d] = {}
            for it in its:
                low = it["forms"]["lower"]
                N = nc1.prompt_conditions(V, m, it["id"], d, it["forms"]["lossy"], low)  # a, b, c (= NC-O)
                X = prompt_variants(V, m, it["id"], d, it["forms"]["lossy"], P)
                split[d][str(it["id"])] = {c: X[c][0] for c in CONDS}
                rows.append((d, str(it["id"]), {"a": N["a"][1], "o": N["c"][1], "m": X["m"][1], "r": X["r"][1]}))
        split["m4c"] = {}
        for r, k, t in zip(R, keep, native):
            if not k:
                continue
            text = to_lossy(t)
            enc = V.tok(text, return_offsets_mapping=True, add_special_tokens=False)
            n_low = len(V.tok(lad.to_lower(t), add_special_tokens=False)["input_ids"])
            N = nc1.make_conditions(V, m, f"m4c|{r['index']}", enc["input_ids"], enc["offset_mapping"], (0, len(text)), text, n_low)
            X = sentence_variants(V, m, r["index"], text, P)
            split["m4c"][str(r["index"])] = {c: X[c][0] for c in CONDS}
            rows.append(("m4c", str(r["index"]), {"a": N["a"][1], "o": N["c"][1], "m": X["m"][1], "r": X["r"][1]}))
        for d, i, pc in rows:
            for c in CONDS:
                mu, ch = elig(pc[c])
                flags = Counter(u["flag"] for u in pc[c])
                elig_rows.append({"model": m, "dataset": d, "id": i, "cond": c, "multi_piece_words": mu, "changed_words": ch,
                                  "eligible": bool(mu > 0 and ch >= ELIG * mu), "atomic_units": flags["atomic_token"],
                                  "no_candidate": flags["no_candidate_within_tolerance"], "unique": flags["canonical_unique"],
                                  "n_words": len(pc[c])})
        E = pd.DataFrame([r for r in elig_rows if r["model"] == m])
        for c in CONDS:
            ok = {(r["dataset"], r["id"]) for r in elig_rows if r["model"] == m and r["cond"] == c and r["eligible"]}
            for d in list(sets) + ["m4c"]:
                pcs = [pc for dd, i, pc in rows if dd == d and (dd, i) in ok]
                for proxy_name, pr in (("s_int", P["m"]), ("s_ref", P["r"])):
                    mean = {k: float(np.mean([pr.piece(p) for pc in pcs for u in pc[k] for p in u["pieces"]])) if pcs else float("nan")
                            for k in ("a", "o", c)}
                    bal_rows.append({"model": m, "dataset": d, "cond": c, "proxy": proxy_name, "n_items": len(pcs), "mean_a": mean["a"],
                                     "mean_nco": mean["o"], "mean_c": mean[c], "sd_ref": pr.sd,
                                     "abs_c_minus_a_over_sd": abs(mean[c] - mean["a"]) / pr.sd,
                                     "matched_within_0.25sd": bool(abs(mean[c] - mean["a"]) <= TOL_SD * pr.sd)})
        json.dump(split, open(OUT / "splits" / f"{m}.json", "w"))
        print(f"{m}: built in {time.time() - t0:.0f}s; eligible m: " + ", ".join(
            f"{d} {int(E[(E.dataset == d) & (E.cond == 'm')].eligible.sum())}/{int(((E.dataset == d) & (E.cond == 'm')).sum())}"
            for d in list(sets) + ["m4c"]), flush=True)
    pd.DataFrame(elig_rows).to_csv(OUT / "eligibility.csv", index=False)
    pd.DataFrame(bal_rows).to_csv(OUT / "balance.csv", index=False)
    write_json(OUT / "proxies.json", prox_out, {"tolerance_sd": TOL_SD, "enum_cap": ENUM_CAP, "sample_n": SAMPLE_N, "eligibility": ELIG,
                                                "registered": "RESULTS.md 2026-11-01 (X3)", "reference": {k: v for k, v in ref.items() if k != "words"}})


def load_split(m: str) -> dict:
    return json.load(open(OUT / "splits" / f"{m}.json"))


def eligible_ids(m: str, cond: str) -> dict:
    import pandas as pd
    E = pd.read_csv(OUT / "eligibility.csv", dtype={"id": str})
    E = E[(E.model == m) & (E.cond == cond) & E.eligible]
    return {d: set(g.id) for d, g in E.groupby("dataset")}


def do_pilot() -> None:
    import torch
    from shattered.eval.loglik import VERBALIZERS
    from shattered.interp.load import load
    m = "gemma4-e2b"
    sp = load_split(m)
    el = eligible_ids(m, "m")
    sets = datasets()
    model, tok = load(m, "cuda")
    V = nc1.Vocab(tok)
    report = {"model": m}
    sib = [it for it in sets["sib"] if str(it["id"]) in el["sib"]][:20]
    t0 = time.time()
    ok_dec = 0
    for it in sib:
        P = nc1.build_with_spans("sib", it["forms"]["lossy"])[0]
        ids = sp["sib"][str(it["id"])]["m"]
        ok_dec += tok.decode(ids) == tok.decode(tok(P, add_special_tokens=False)["input_ids"])
        nc1.choice_logprobs_ids(model, tok, P, ids, VERBALIZERS["sib"])
    report["sib_seconds_per_item"] = (time.time() - t0) / len(sib)
    report["sib_decode_identical"] = f"{ok_dec}/{len(sib)}"
    m4 = [i for i in list(sp["m4c"]) if i in el.get("m4c", set())][:20]
    t0 = time.time()
    for i in m4:
        nc1.sentence_vector(model, tok, sp["m4c"][i]["m"])
    report["m4c_seconds_per_sentence"] = (time.time() - t0) / len(m4)
    import pandas as pd
    E = pd.read_csv(OUT / "eligibility.csv", dtype={"id": str})
    n = E[(E.cond == "m")].groupby(["model", "dataset"]).eligible.sum().unstack()
    report["eligible_items_m"] = n.to_dict()
    tot = {mm: int(n.loc[mm, ["sentiment", "xnli", "sib"]].sum()) for mm in MODELS}
    report["estimate_hours_total_m_and_r"] = sum(tot.values()) * 2 * report["sib_seconds_per_item"] / 3600
    write_json(OUT / "pilot.json", report, {"status": "pilot: timing and decode check only; no accuracy or retrieval computed"})
    print(json.dumps(report, indent=1, default=str), flush=True)
    del model
    torch.cuda.empty_cache()


def do_score(only=None) -> None:
    import pandas as pd
    import torch
    from shattered.eval.loglik import VERBALIZERS
    from shattered.interp.load import load
    from shattered.runlog import commit, tmp_path
    SCORES.mkdir(parents=True, exist_ok=True)
    sets = datasets()
    R, keep, _ = lad.m4c_sample()
    ctl_rows = []
    for m in (only or MODELS):
        todo = [c for c in CONDS if not (all((SCORES / f"{m}__x3_{c}__{g}.parquet").exists() for g in GROUPS)
                                         and (m not in lad.M4_MODELS or (X3_ACT / m / f"{c}500.npz").exists()))]
        ctl_path = OUT / "control" / f"{m}.json"
        if not todo and ctl_path.exists():
            continue
        t0 = time.time()
        model, tok = load(m, "cuda")
        V = nc1.Vocab(tok)
        sp = load_split(m)
        for c in todo:
            el = eligible_ids(m, c)
            rows = []
            for d, its in sets.items():
                for it in its:
                    if str(it["id"]) not in el.get(d, set()):
                        continue
                    P = nc1.build_with_spans(d, it["forms"]["lossy"])[0]
                    ids = sp[d][str(it["id"])][c]
                    lp = nc1.choice_logprobs_ids(model, tok, P, ids, VERBALIZERS[d])
                    rows.append({"model": m, "task": d, "form": f"x3_{c}", "id": it["id"], "label": it["label"], "logprobs": lp,
                                 "pred_raw": int(np.argmax(lp)), "prompt_tokens": len(ids)})
                print(f"{m}/{c}: {d} done ({time.time() - t0:.0f}s since load)", flush=True)
            df = pd.DataFrame(rows)
            for g, tasks_g in GROUPS.items():
                path = SCORES / f"{m}__x3_{c}__{g}.parquet"
                df[df.task.isin(tasks_g)].to_parquet(tmp_path(path))
                commit(tmp_path(path), path)
            if m in lad.M4_MODELS:
                ids_el = [str(r["index"]) for r, k in zip(R, keep) if k and str(r["index"]) in el.get("m4c", set())]
                vecs = np.stack([nc1.sentence_vector(model, tok, sp["m4c"][i][c]) for i in ids_el])
                path = X3_ACT / m / f"{c}500.npz"
                path.parent.mkdir(parents=True, exist_ok=True)
                np.savez(tmp_path(path), flores_states=vecs, index=np.array([int(i) for i in ids_el]))
                commit(tmp_path(path), path)
                print(f"{m}/{c}: {len(ids_el)} M4c vectors done ({time.time() - t0:.0f}s since load)", flush=True)
        # recompute control: two eligible SIB items, canonical and NC-O ids through this path against the stored Phase 1 scores
        el = eligible_ids(m, "m")
        its = [it for it in sets["sib"] if str(it["id"]) in el["sib"]][:2]
        ctl = []
        for it in its:
            N = nc1.prompt_conditions(V, m, it["id"], "sib", it["forms"]["lossy"], it["forms"]["lower"])
            for cond in ("a", "c"):
                lp = nc1.choice_logprobs_ids(model, tok, N["prompt"], N[cond][0], VERBALIZERS["sib"])
                st = pd.read_parquet(nc1.SCORES / f"{m}__nc_{cond}__e0c.parquet")
                st = np.asarray(st[st.id == it["id"]].iloc[0].logprobs)
                ctl.append({"model": m, "id": it["id"], "cond": cond, "max_abs_dlogprob": float(np.abs(st - np.asarray(lp)).max())})
        (OUT / "control").mkdir(exist_ok=True)
        json.dump(ctl, open(ctl_path, "w"))
        print(f"{m}: control max |d| = {max(x['max_abs_dlogprob'] for x in ctl):.2e}; finished in {time.time() - t0:.0f}s", flush=True)
        del model
        torch.cuda.empty_cache()


if __name__ == "__main__":
    if sys.argv[1] == "score":
        do_score(sys.argv[2:] or None)
    else:
        {"build": do_build, "pilot": do_pilot}.get(sys.argv[1], lambda: None)()
