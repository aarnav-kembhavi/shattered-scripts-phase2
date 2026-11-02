"""X8 analysis, exactly as registered (RESULTS.md, X8 / K4 / K5 / K6, Phase 2 pre-registration). Runs as soon as results/phase2/x8/x8_annotator_P.json and _Q.json exist
(the output of scripts/import_x8.py). No outcome-dependent choice: every definition below is the registered one, and the bootstrap is the project's (10,000 resamples of
sentences, seed 0).

K4 (primary = inter-annotator agreement; no pass/fail threshold):
  (i)  Cohen's kappa between X8-P and X8-Q on the binary per-word label "the word contains a doubled vowel (aa, ee, ii, oo, uu)", over the words of the sentences in which P and Q have
       equal word counts (words aligned by position; the other sentences are counted and reported); 95% bootstrap CI over those sentences.
  (ii) character error rate between P and Q: per sentence, the Levenshtein distance between the lowercased texts reduced to [a-z ], divided by the length of the longer string,
       averaged over sentences (all 100); 95% bootstrap CI over sentences.
  Descriptive (no rule, no verdict): the K3b statistics (vowel doubling per letter, h-digraph per letter, English-word share per word; definitions and the word list of scripts/k3b_dakshina.py
  and scripts/english_share.py) for Gemini vs the mean of P and Q (pooled rates per annotator, then averaged), as ratios Gemini / human with 90% (and 95%) CIs, shown against [0.80, 1.25]
  for orientation only.
K5 (descriptive): chrF (sacreBLEU chrF2: char order 6, word order 0, beta 2; lowercased) between P and Q and between each annotator and Gemini, with 95% CIs; the vowel-doubling rate of P vs Q.
K6 (exploratory: retrieval and SIB-200 accuracy on the P, Q and Gemini texts) needs the GPU and is not part of this script.

Usage: python scripts/analyze_x8.py [--in DIR] [--out DIR]   (defaults: results/phase2/x8)
"""
import argparse
import json
import re
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import english_share as es  # noqa: E402

from shattered.runlog import REPO, results_dir, write_json  # noqa: E402

N_BOOT, SEED = 10_000, 0
VOWELS = re.compile(r"aa|ee|ii|oo|uu")
HDIG = re.compile(r"chh|kh|gh|jh|th|dh|ph|bh")


def lev(a: str, b: str) -> int:
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def cer(a: str, b: str) -> float | None:
    x, y = (re.sub(r"[^a-z ]", "", t.lower()) for t in (a, b))
    n = max(len(x), len(y))
    return lev(x, y) / n if n else None


def kappa(a: np.ndarray, b: np.ndarray) -> float:
    a, b = a.astype(float), b.astype(float)
    po = (a == b).mean()
    pa, pb = a.mean(), b.mean()
    pe = pa * pb + (1 - pa) * (1 - pb)
    return float((po - pe) / (1 - pe)) if pe < 1 else float("nan")


def counts(text: str, wl: set) -> dict:  # as scripts/k3b_dakshina.py
    t = text.lower()
    w = es.words(t)
    return {"letters": sum("a" <= c <= "z" for c in t), "vowel_doubling": len(VOWELS.findall(t)), "h_digraph": len(HDIG.findall(t)),
            "words": len(w), "english": sum(len(x) >= 4 and x in wl for x in w)}


def pct(x, q):
    return [float(v) for v in np.nanpercentile(x, q)]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", default=None)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    d = Path(a.inp) if a.inp else results_dir("phase2/x8")
    out = Path(a.out) if a.out else d
    out.mkdir(parents=True, exist_ok=True)
    A = {r: {x["index"]: x["romanization"] for x in json.load(open(d / f"x8_annotator_{r}.json", encoding="utf-8"))["answers"]} for r in "PQ"}
    gem = {}
    for ln in (REPO / "data" / "processed" / "natural_flores_m4_500_v1.jsonl").open(encoding="utf-8"):
        r = json.loads(ln)
        gem[r["index"]] = None if r["defective"] else r["natural"]
    sel = json.load(open(REPO / "results" / "phase2" / "x8" / "selection.json", encoding="utf-8"))["indices"]
    idx = [i for i in sel if i in A["P"] and i in A["Q"]]
    n = len(idx)
    P, Q = [A["P"][i] for i in idx], [A["Q"][i] for i in idx]
    G = [gem[i] for i in idx]
    rng = np.random.default_rng(SEED)
    boot = rng.integers(0, n, (N_BOOT, n))  # one set of resampled sentences for every statistic

    # ---- K4 (i): kappa on the doubled-vowel word label, equal-word-count sentences
    eq = [k for k in range(n) if len(P[k].split()) == len(Q[k].split())]
    lab = lambda t: np.array([bool(VOWELS.search(w.lower())) for w in t.split()])  # noqa: E731
    wp, wq = [lab(P[k]) for k in eq], [lab(Q[k]) for k in eq]
    kap = kappa(np.concatenate(wp), np.concatenate(wq)) if eq else float("nan")
    ke = []
    rng2 = np.random.default_rng(SEED)
    for b in rng2.integers(0, len(eq), (N_BOOT, len(eq))) if eq else []:
        ke.append(kappa(np.concatenate([wp[i] for i in b]), np.concatenate([wq[i] for i in b])))
    ke = np.array(ke)
    k4i = {"kappa": kap, "ci95": pct(ke, [2.5, 97.5]) if len(ke) else None, "n_sentences_equal_word_count": len(eq), "n_sentences_other": n - len(eq),
           "n_words": int(sum(len(x) for x in wp)), "bootstrap_nan_share": float(np.isnan(ke).mean()) if len(ke) else None,
           "label": "word contains aa, ee, ii, oo or uu (lowercased)", "status": "primary outcome: the agreement itself, no threshold"}

    # ---- K4 (ii): character error rate over all sentences
    c = np.array([cer(P[k], Q[k]) if cer(P[k], Q[k]) is not None else np.nan for k in range(n)])
    cm = np.nanmean(c[boot], axis=1)
    k4ii = {"cer_mean": float(np.nanmean(c)), "ci95": pct(cm, [2.5, 97.5]), "n_sentences": int(np.isfinite(c).sum()), "status": "primary outcome: the agreement itself, no threshold"}

    # ---- descriptive K3b statistics: Gemini vs mean(P, Q)
    wl = es.wordlists()["zipf>=3"]
    CG, CP, CQ = (np.array([[counts(t, wl)[k] for k in ("letters", "vowel_doubling", "h_digraph", "words", "english")] for t in X], float) for X in (G, P, Q))
    cols = {"letters": 0, "vowel_doubling": 1, "h_digraph": 2, "words": 3, "english": 4}
    rate = lambda M, num, den: M[..., cols[num]].sum(-1) / M[..., cols[den]].sum(-1)  # noqa: E731
    desc = {}
    for name, num, den in (("vowel_doubling", "vowel_doubling", "letters"), ("h_digraph", "h_digraph", "letters"), ("english_word_share", "english", "words")):
        g0 = rate(CG, num, den)
        h0 = (rate(CP, num, den) + rate(CQ, num, den)) / 2
        gb = rate(CG[boot], num, den)
        hb = (rate(CP[boot], num, den) + rate(CQ[boot], num, den)) / 2
        r = np.where(hb > 0, gb / np.where(hb > 0, hb, 1), np.nan)
        ci90, ci95 = pct(r, [5, 95]), pct(r, [2.5, 97.5])
        desc[name] = {"gemini_rate": float(g0), "human_rate_mean_of_P_Q": float(h0), "rate_P": float(rate(CP, num, den)), "rate_Q": float(rate(CQ, num, den)),
                      "ratio_gemini_over_human": float(g0 / h0) if h0 > 0 else None, "ci90": ci90, "ci95": ci95,
                      "orientation_only_ci90_within_0.80_1.25": bool(0.80 <= ci90[0] and ci90[1] <= 1.25), "status": "descriptive, no verdict"}

    # ---- K5: chrF and the P vs Q vowel-doubling rate
    from sacrebleu.metrics import CHRF
    m = CHRF(char_order=6, word_order=0, beta=2)
    sc = lambda x, y: m.sentence_score(x.lower(), [y.lower()]).score  # noqa: E731
    k5 = {}
    for nm, X, Y in (("P_vs_Q", P, Q), ("P_vs_Gemini", P, G), ("Q_vs_Gemini", Q, G)):
        v = np.array([sc(x, y) for x, y in zip(X, Y)])
        k5[f"chrF_{nm}"] = {"mean": float(v.mean()), "ci95": pct(v[boot].mean(1), [2.5, 97.5]), "n": n}
    rp, rq = rate(CP, "vowel_doubling", "letters"), rate(CQ, "vowel_doubling", "letters")
    rb = rate(CP[boot], "vowel_doubling", "letters") / rate(CQ[boot], "vowel_doubling", "letters")
    k5["vowel_doubling_rate_P"], k5["vowel_doubling_rate_Q"] = float(rp), float(rq)
    k5["vowel_doubling_ratio_P_over_Q"] = {"ratio": float(rp / rq) if rq > 0 else None, "ci95": pct(rb, [2.5, 97.5]), "status": "descriptive"}

    res = {"n_sentences": n, "n_boot": N_BOOT, "seed": SEED, "K4_i_kappa": k4i, "K4_ii_cer": k4ii, "descriptive_K3b_statistics": desc, "K5": k5,
           "K6": "exploratory (retrieval and SIB-200 on the P, Q and Gemini texts): needs the GPU, not run here"}
    write_json(out / "analysis.json", res, {"registration": "RESULTS.md X8 / K4 / K5 / K6 (Phase 2 pre-registration)", "source": "x8_annotator_P.json, x8_annotator_Q.json"})
    print(json.dumps({"kappa": k4i, "cer": k4ii, "ratios": {k: (round(v["ratio_gemini_over_human"], 3), [round(x, 3) for x in v["ci90"]]) for k, v in desc.items()}}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
