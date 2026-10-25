"""natural+dbl: vowel-doubling sensitivity (exploratory, post hoc; registered in RESULTS.md 2026-10-25 23:58 IST before
this script was written or run). No prediction, no verdict; registered verdicts are unchanged whatever it shows.

The M4c natural romanizations with long vowels doubled where the aligned native word has a long vowel, with one keep
rate p (per-string generators) tuned so the pooled doubling rate equals the Dakshina human rate of K3b.

Usage: python scripts/v_dbl.py build            (CPU; stops with exit 2 if the alignment failure rate is above 20%)
       python scripts/v_dbl.py tpw              (CPU; tokenizers only)
       python scripts/v_dbl.py forward <model>  (GPU; one model; GPU guard first)
       python scripts/v_dbl.py score <model>    (GPU; SIB-257; GPU guard first)
       python scripts/v_dbl.py analyse          (CPU)
Outputs: results/v_dbl/{natural_dbl500.jsonl, build.json, word_failures.csv, tokens_per_word.csv, retrieval.csv,
         sib.csv, summary.json}, results/v_dbl/scores/, cache/activations/m14full/<model>/natural_dbl500.npz
"""
import json
import re
import shutil
import sys
import time
import unicodedata

import numpy as np
import pandas as pd

from shattered.runlog import REPO, commit, results_dir, tmp_path, write_json
from shattered.translit import to_lossy

sys.path.insert(0, str(REPO / "scripts"))
import english_share as es  # noqa: E402
import l_ladder as lad  # noqa: E402
from m4b_mapping import ACT, boot, layer_fit  # noqa: E402
from m4c_natural_flores import SEED as SPLIT_SEED  # noqa: E402

OUT = results_dir("v_dbl")
TEXTS = OUT / "natural_dbl500.jsonl"
SCORES = OUT / "scores"
MODELS = ["qwen3.5-2b", "sarvam-1", "gemma4-e2b"]
SEED, SIM_MIN, GATE = 26, 0.5, 0.20
FORM = "natural_dbl257"

INDEP = {"ಅ": ("a", 0), "ಆ": ("a", 1), "ಇ": ("i", 0), "ಈ": ("i", 1), "ಉ": ("u", 0), "ಊ": ("u", 1), "ಋ": ("u", 0),
         "ೠ": ("u", 1), "ಎ": ("e", 0), "ಏ": ("e", 1), "ಐ": ("ai", 0), "ಒ": ("o", 0), "ಓ": ("o", 1), "ಔ": ("au", 0)}
SIGN = {"ಾ": ("a", 1), "ಿ": ("i", 0), "ೀ": ("i", 1), "ು": ("u", 0), "ೂ": ("u", 1), "ೃ": ("u", 0), "ೄ": ("u", 1),
        "ೆ": ("e", 0), "ೇ": ("e", 1), "ೈ": ("ai", 0), "ೊ": ("o", 0), "ೋ": ("o", 1), "ೌ": ("au", 0)}
VIRAMA, NUKTA = "್", "಼"
VOWELS = re.compile("aa|ee|ii|oo|uu")  # the K3b statistic (k3b_dakshina.VOWELS; that module reads argv on import)
GROUP = re.compile(r"[aeiou]+", re.I)


def kannada(w: str) -> bool:
    return any("ಀ" <= c <= "೿" for c in w)


def is_consonant(c: str) -> bool:
    return "ಕ" <= c <= "ಹ" or c in "ೞಱ"


def nuclei(word: str) -> list:
    """[(quality, long)] for each vowel nucleus of a Kannada word: independent vowels, each consonant's vowel sign or
    its inherent a; none after a virama."""
    out, pending = [], False
    for c in unicodedata.normalize("NFC", word):
        if c == NUKTA:
            continue
        if pending:
            pending = False
            if c in SIGN:
                out.append(SIGN[c])
                continue
            if c == VIRAMA:
                continue
            out.append(("a", 0))
        if c in "ೕ" and out:  # length mark (normally composed away by NFC)
            out[-1] = (out[-1][0], 1)
        elif c in "ೖ" and out:
            out[-1] = ("ai", 0)
        elif c in INDEP:
            out.append(INDEP[c])
        elif is_consonant(c):
            pending = True
    if pending:
        out.append(("a", 0))
    return out


def norm(s: str) -> str:
    s = re.sub(r"[^a-z]", "", s.lower())
    return re.sub(r"([aeiou])\1+", r"\1", s)


def lev(a: str, b: str) -> int:
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i] + [0] * len(b)
        for j, cb in enumerate(b, 1):
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb))
        prev = cur
    return prev[-1]


def sim(native_word: str, natural_word: str) -> float:
    a, b = norm(to_lossy(native_word)), norm(natural_word)
    if not a or not b:
        return 0.0
    return 1 - lev(a, b) / max(len(a), len(b))


def align(nat_words: list, rom_words: list) -> dict:
    """Monotonic 1:1 alignment maximizing total similarity (gaps free; a pair needs sim >= SIM_MIN).
    Returns {native position: roman position}."""
    n, m = len(nat_words), len(rom_words)
    S = np.array([[sim(a, b) for b in rom_words] for a in nat_words]) if n and m else np.zeros((n, m))
    D = np.zeros((n + 1, m + 1))
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            best = max(D[i - 1, j], D[i, j - 1])
            if S[i - 1, j - 1] >= SIM_MIN:
                best = max(best, D[i - 1, j - 1] + S[i - 1, j - 1])
            D[i, j] = best
    pairs, i, j = {}, n, m
    while i > 0 and j > 0:
        if S[i - 1, j - 1] >= SIM_MIN and np.isclose(D[i, j], D[i - 1, j - 1] + S[i - 1, j - 1]):
            pairs[i - 1] = j - 1
            i, j = i - 1, j - 1
        elif np.isclose(D[i, j], D[i - 1, j]):
            i -= 1
        else:
            j -= 1
    return pairs


def candidates(native: str, natural: str, wl: set) -> tuple[list, list]:
    """Candidate doublings [(token position, char offset, letter)] and one record per native Kannada word."""
    toks = natural.split(" ")  # split on single spaces so the text is rebuilt exactly
    rom_pos = [k for k, t in enumerate(toks) if t]
    nat_words = [w for w in native.split() if kannada(w)]
    pairs = align(nat_words, [toks[k] for k in rom_pos])
    cands, recs = [], []
    for i, w in enumerate(nat_words):
        nu = nuclei(w)
        has_long = any(L for _, L in nu)
        rec = {"native": w, "has_long": has_long, "aligned": i in pairs, "natural": None, "english": False,
               "count_match": None, "n_candidates": 0}
        if i in pairs:
            k = rom_pos[pairs[i]]
            t = toks[k]
            rec["natural"] = t
            letters = re.sub(r"[^a-z]", "", t.lower())
            if len(letters) >= 4 and letters in wl:
                rec["english"] = True
            else:
                groups = list(GROUP.finditer(t))
                rec["count_match"] = len(groups) == len(nu)
                if rec["count_match"]:
                    for (q, L), g in zip(nu, groups):
                        if L and g.group(0).lower() == q:
                            cands.append((k, g.start(), g.group(0)))
                            rec["n_candidates"] += 1
        rec["failed"] = (not rec["aligned"]) or rec["count_match"] is False
        recs.append(rec)
    return cands, recs


def apply(natural: str, cands: list, keep: np.ndarray) -> str:
    toks = natural.split(" ")
    for (k, off, ch), kept in sorted(zip(cands, keep), key=lambda x: (x[0][0], -x[0][1])):
        if kept:
            toks[k] = toks[k][:off + 1] + ch + toks[k][off + 1:]
    return " ".join(toks)


def pooled_rate(texts: list) -> float:
    t = [x.lower() for x in texts]  # as k3b_dakshina.counts()
    return sum(len(VOWELS.findall(x)) for x in t) / sum(sum("a" <= c <= "z" for c in x) for x in t)


def do_build() -> int:
    R, keep, _ = lad.m4c_sample()
    wl = es.wordlists()["zipf>=3"]
    target = json.load(open(REPO / "results/k3b/verdict.json"))["statistics"]["vowel_doubling"]["human_rate"]
    C, U, words = {}, {}, []
    for r, k in zip(R, keep):
        if not k:
            continue
        c, recs = candidates(r["native"], r["natural"], wl)
        C[r["index"]] = c
        U[r["index"]] = np.random.default_rng([SEED, r["index"]]).random(len(c))
        words += [{"index": r["index"], **x} for x in recs]
    W = pd.DataFrame(words)
    den = W[W.has_long & ~W.english]
    fail_long, fail_all = float(den.failed.mean()), float(W[~W.english].failed.mean())
    gate = {"failure_rate_long_vowel_words": fail_long, "n_long_vowel_words": len(den),
            "n_failed_long_vowel_words": int(den.failed.sum()), "failure_rate_all_words": fail_all,
            "n_words": int((~W.english).sum()), "n_english_list_words_unchanged": int(W.english.sum()),
            "n_unaligned_long": int((~den.aligned).sum()), "n_count_mismatch_long": int((den.count_match == False).sum()),  # noqa: E712
            "gate": GATE, "passed": fail_long <= GATE}
    W.to_csv(OUT / "word_failures.csv", index=False)
    nat = {r["index"]: r["natural"] for r, k in zip(R, keep) if k}
    texts = lambda p: [apply(nat[i], C[i], U[i] < p) for i in nat]  # noqa: E731
    base, full = pooled_rate(list(nat.values())), pooled_rate(texts(1.0))
    if not gate["passed"]:
        write_json(OUT / "build.json", {"gate": gate, "stopped": "alignment failure rate above 20%"},
                   {"registered": "RESULTS.md 2026-10-25 23:58 IST (exploratory)"})
        print(json.dumps(gate, indent=1))
        return 2
    if full <= target:
        p = 1.0
    else:
        lo, hi = 0.0, 1.0
        for _ in range(60):
            mid = (lo + hi) / 2
            lo, hi = (mid, hi) if pooled_rate(texts(mid)) < target else (lo, mid)
        p = (lo + hi) / 2
    D = {i: t for i, t in zip(nat, texts(p))}
    with tmp_path(TEXTS).open("w", encoding="utf-8") as f:
        for r in R:
            i = r["index"]
            f.write(json.dumps({"index": i, "natural": r["natural"], "natural_dbl": D.get(i, r["natural"]),
                                "retained": i in D, "n_candidates": len(C.get(i, [])),
                                "n_doubled": int((U[i] < p).sum()) if i in D else 0}, ensure_ascii=False) + "\n")
    commit(tmp_path(TEXTS), TEXTS)
    n_c = sum(len(c) for c in C.values())
    res = {"gate": gate, "keep_p": p, "target_rate": target, "natural_rate": base, "rate_p1": full,
           "natural_dbl_rate": pooled_rate(list(D.values())), "n_strings": len(D), "n_candidates": n_c,
           "n_doubled": int(sum((U[i] < p).sum() for i in D)), "shortfall": full < target,
           "n_strings_changed": int(sum(D[i] != nat[i] for i in D))}
    write_json(OUT / "build.json", res, {"registered": "RESULTS.md 2026-10-25 23:58 IST (exploratory)", "seed": SEED,
                                         "sim_min": SIM_MIN})
    print(json.dumps(res, indent=1))
    return 0


def texts500() -> list:
    return [json.loads(l) for l in TEXTS.open(encoding="utf-8")]


def sib257_dbl() -> dict:
    s = lad.sib257_items()
    d = {r["index"]: r["natural_dbl"] for r in texts500() if r["retained"]}
    for it in s["sib"]:
        it["forms"][FORM] = {"text": d[it["id"]]}
    return s


def do_tpw() -> None:
    from transformers import AutoTokenizer
    from shattered.interp.load import MODELS as REPOS
    T = [r for r in texts500() if r["retained"]]
    s = sib257_dbl()["sib"]
    sets = {"m4c496": {"natural": [r["natural"] for r in T], "natural_dbl": [r["natural_dbl"] for r in T]},
            "sib257": {"natural": [it["forms"]["natural257"]["text"] for it in s],
                       "natural_dbl": [it["forms"][FORM]["text"] for it in s]}}
    out = []
    for m in lad.ACC_MODELS:
        tok = AutoTokenizer.from_pretrained(REPOS[m])
        for d, forms in sets.items():
            v = {}
            for f, X in forms.items():
                n = sum(len(x) for x in tok(X, add_special_tokens=False)["input_ids"])
                v[f] = n / sum(len(x.split()) for x in X)
                out.append({"model": m, "dataset": d, "form": f, "n_texts": len(X), "tokens_per_word": v[f]})
            out[-1]["ratio_dbl_to_natural"] = v["natural_dbl"] / v["natural"]
    T = pd.DataFrame(out)
    T.to_csv(OUT / "tokens_per_word.csv", index=False)
    print(T.round(4).to_string(index=False))


def guard() -> None:
    from shattered.gpuguard import wait_gpu_free
    wait_gpu_free()


def do_forward(m: str) -> None:
    path = ACT / m / "natural_dbl500.npz"
    if path.exists():
        print(f"{m}: natural_dbl500 exists", flush=True)
        return
    guard()
    import torch
    from shattered.interp.load import load
    R = texts500()
    t0 = time.time()
    model, tok = load(m, "cuda")
    out = lad.forward_form(model, tok, [r["natural_dbl"] for r in R], [r["index"] for r in R])
    np.savez(tmp_path(path), flores_states=out["sent_states"], index=np.array([r["index"] for r in R]),
             n_tokens=out["n_tokens"])
    commit(tmp_path(path), path)
    print(f"{m}: natural_dbl500 forward done ({time.time() - t0:.0f}s incl. load)", flush=True)
    del model
    torch.cuda.empty_cache()


def do_score(m: str) -> None:
    import e0b_familiarity as e0b
    SCORES.mkdir(parents=True, exist_ok=True)
    cf = SCORES / f"cf_{m}.json"
    if not cf.exists():  # the stored E0c content-free log-probs, so calibration is exactly natural257's
        shutil.copyfile(lad.E0C_DIR / f"cf_{m}.json", cf)
    if (SCORES / f"{m}__{FORM}.parquet").exists():
        print(f"{m}: {FORM} scores exist", flush=True)
        return
    guard()
    e0b.score_model(m, sib257_dbl(), [FORM], SCORES)


def do_analyse() -> None:
    import e0b_familiarity as e0b
    R, keep, _ = lad.m4c_sample()
    idx = np.array([r["index"] for r in R])[keep]
    n = len(idx)
    order = np.random.default_rng(SPLIT_SEED).permutation(n)
    tr, te = np.sort(order[: n // 2]), np.sort(order[n // 2:])
    folds = np.array_split(np.random.default_rng(SPLIT_SEED + 2).permutation(tr), 5)
    ladder = pd.read_csv(REPO / "results/l_ladder/retrieval.csv")
    rows = []
    for m in MODELS:
        E = np.load(ACT / m / "english.npz")["flores_states"][idx]
        hits = {}
        for f, name in (("natural", "natural500.npz"), ("natural_dbl", "natural_dbl500.npz")):
            z = np.load(ACT / m / name)
            assert np.array_equal(z["index"][keep], idx)
            X = z["flores_states"][keep]
            fits = [layer_fit(X[:, l], E[:, l], tr, te, folds) for l in range(X.shape[1])]
            lu = int(np.argmax([r["unmapped_train"] for r in fits]))
            hits[f] = (fits[lu]["unmapped"], lu)
        ref = ladder[(ladder.model == m) & (ladder.form == "natural")].unmapped_test.item()
        assert np.isclose(hits["natural"][0].mean(), ref), (m, hits["natural"][0].mean(), ref)
        rows.append({"measure": "retrieval", "model": m, **paired(hits["natural_dbl"][0], hits["natural"][0]),
                     "layer_natural": hits["natural"][1], "layer_natural_dbl": hits["natural_dbl"][1]})
    cf = {m: json.load(open(lad.E0C_DIR / f"cf_{m}.json")) for m in MODELS}
    C = pd.concat([pd.read_parquet(lad.E0C_DIR / f"{m}__{f}.parquet") for m in MODELS for f in ("english", "natural257")]
                  + [pd.read_parquet(SCORES / f"{m}__{FORM}.parquet") for m in MODELS], ignore_index=True)
    C, fb = e0b.apply_calibration(C, cf)
    ref = pd.read_csv(REPO / "results/l_ladder/accuracy.csv")
    for m in MODELS:
        g = C[(C.model == m) & (C.task == "sib")]
        piv = g.pivot_table(index="id", columns="form", values="pred_cal")
        lab = g.drop_duplicates("id").set_index("id").label.loc[piv.index]
        k = piv["natural257"].notna() & piv[FORM].notna()
        corr = piv.eq(lab, axis=0)[k]
        r0 = ref[(ref.model == m) & (ref.task == "sib") & (ref.form == "natural257")].acc_cal.item()
        assert np.isclose(corr["natural257"].mean(), r0), (m, corr["natural257"].mean(), r0)
        rows.append({"measure": "sib257", "model": m, **paired(corr[FORM].to_numpy(), corr["natural257"].to_numpy())})
    K = pd.DataFrame(rows)
    K.to_csv(OUT / "differences.csv", index=False)
    write_json(OUT / "summary.json", {"differences": K.to_dict("records")},
               {"registered": "RESULTS.md 2026-10-25 23:58 IST (exploratory)", "status": "post hoc descriptive, no verdict",
                "difference": "natural_dbl - natural", "p": "exact McNemar, unadjusted"})
    pd.set_option("display.width", 250)
    print(K.round(4).to_string(index=False))


def paired(a: np.ndarray, b: np.ndarray) -> dict:
    d = lad.paired(a, b)
    return {"n": d["n"], "acc_natural_dbl": d["acc_a"], "acc_natural": d["acc_b"], "diff": d["diff"],
            "ci_low": d["ci"][0], "ci_high": d["ci"][1], "dbl_only": d["a_only"], "natural_only": d["b_only"],
            "p_mcnemar": d["p"]}


if __name__ == "__main__":
    step = sys.argv[1]
    if step == "build":
        sys.exit(do_build())
    if step in ("forward", "score"):
        assert sys.argv[2] in MODELS, sys.argv[2]
        {"forward": do_forward, "score": do_score}[step](sys.argv[2])
    else:
        {"tpw": do_tpw, "analyse": do_analyse}[step]()
