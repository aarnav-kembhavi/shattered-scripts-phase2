"""K3b: Gemini vs native-speaker natural romanization on Dakshina Kannada (pre-registered in RESULTS.md, 2026-10-23,
before this script was written).

Usage: python scripts/k3b_dakshina.py sample [hi]   (CPU: 500 strings, seed 6; resample subset 200, seed 7)
       python scripts/k3b_dakshina.py draft [hi]    (API; exit 3 on a quota stop, re-run to continue)
       python scripts/k3b_dakshina.py analyse [hi]  (CPU)
`hi` runs K3b-hi (registered 2026-10-23 12:05 IST): Dakshina Hindi, prompt `natural_romanization_hi_v1`, same design.
Outputs: results/k3b/ (results/k3b_hi/ for hi): {sample.json, drafts.jsonl, chrf.json, stats.csv, verdict.json}
"""
import csv
import json
import re
import sys

import numpy as np
import pandas as pd

from shattered.llm.ratelimit import DailyQuotaExceeded
from shattered.runlog import REPO, commit, results_dir, tmp_path, write_json
from shattered.translit.natural import MODEL, PROMPT_VERSION, defective, make_client, prompt, romanize

sys.path.insert(0, str(REPO / "scripts"))
import english_share as es  # noqa: E402

LANG = sys.argv[2] if len(sys.argv) > 2 else "kn"
assert LANG in ("kn", "hi"), LANG
SRC = REPO / f"data/raw/dakshina_official/dakshina_dataset_v1.0/{LANG}/romanized/{LANG}.romanized.rejoined.tsv"
OUT = results_dir("k3b" if LANG == "kn" else "k3b_hi")
PV = PROMPT_VERSION if LANG == "kn" else "natural_romanization_hi_v1"
REGISTERED = "RESULTS.md 2026-10-23 (K3b)" if LANG == "kn" else "RESULTS.md 2026-10-23 12:05 (K3b-hi)"
SAMPLE, DRAFTS = OUT / "sample.json", OUT / "drafts.jsonl"
N, N_RES, SEED, SEED_RES, N_BOOT = 500, 200, 6, 7, 10000
VOWELS = re.compile(r"aa|ee|ii|oo|uu")
HDIG = re.compile(r"chh|kh|gh|jh|th|dh|ph|bh")


def do_sample() -> None:
    D = pd.read_csv(SRC, sep="\t", header=None, names=["native", "romanized"], quoting=csv.QUOTE_NONE, dtype=str,
                    keep_default_na=False)
    dup = D.native.duplicated(keep=False)
    short = D.native.str.split().str.len() < 3
    pool = D[~dup & ~short].reset_index()
    pick = np.sort(np.random.default_rng(SEED).choice(len(pool), N, replace=False))
    rows = [{"row": int(pool["index"][i]), "native": pool.native[i], "human": pool.romanized[i]} for i in pick]
    res = sorted(np.random.default_rng(SEED_RES).choice(N, N_RES, replace=False).tolist())
    write_json(SAMPLE, {"rows": rows, "resample_positions": res},
               {"n_total": len(D), "n_dropped_duplicate_native": int(dup.sum()), "n_dropped_short": int((short & ~dup).sum()),
                "pool": len(pool), "seed": SEED, "seed_resample": SEED_RES})
    print({"total": len(D), "dup": int(dup.sum()), "short": int((short & ~dup).sum()), "pool": len(pool)})


def do_draft() -> int:
    S = json.load(open(SAMPLE, encoding="utf-8"))
    rows, res = S["rows"], set(S["resample_positions"])
    client = make_client()
    done = {(r["pos"], r["kind"]): r for r in map(json.loads, DRAFTS.open(encoding="utf-8"))} if DRAFTS.exists() else {}
    stopped = None
    for pos, r in enumerate(rows):
        try:
            key = (pos, "primary")
            if not (key in done and (not done[key]["defective"] or done[key]["attempt"] >= 3)):
                start = done[key]["attempt"] + 1 if key in done else 1
                for attempt in range(start, 4):
                    out = romanize(client, r["native"], version=PV, attempt=attempt)["natural"]
                    d = defective({"native": r["native"], "natural": out})
                    done[key] = {"pos": pos, "kind": "primary", "text": out, "attempt": attempt, "defective": d}
                    if not d:
                        break
            if pos in res:
                for k in ("G1", "G2"):
                    if (pos, k) in done:
                        continue
                    out = client.generate(prompt(r["native"], PV), max_tokens=1024, temperature=1.0,
                                          resample=k).text.strip()
                    done[(pos, k)] = {"pos": pos, "kind": k, "text": out, "attempt": 1,
                                      "defective": defective({"native": r["native"], "natural": out})}
        except DailyQuotaExceeded as e:
            stopped = str(e)[:200]
            break
    with tmp_path(DRAFTS).open("w", encoding="utf-8") as f:
        for k in sorted(done):
            f.write(json.dumps(done[k], ensure_ascii=False) + "\n")
    commit(tmp_path(DRAFTS), DRAFTS)
    need = len(rows) + 2 * len(res)
    complete = stopped is None and len(done) == need
    print({"n_done": len(done), "n_target": need, "stopped": stopped, "complete": complete,
           "primary_defective": sum(v["defective"] for (p, k), v in done.items() if k == "primary")}, flush=True)
    return 0 if complete else 3


def counts(text: str, wl: set) -> dict:
    t = text.lower()
    letters = sum("a" <= c <= "z" for c in t)
    w = es.words(t)
    return {"letters": letters, "vowel_doubling": len(VOWELS.findall(t)), "h_digraph": len(HDIG.findall(t)),
            "words": len(w), "english": sum(len(x) >= 4 and x in wl for x in w)}


def ratio_ci(G: pd.DataFrame, H: pd.DataFrame, num: str, den: str) -> dict:
    g, h = G[[num, den]].to_numpy(float), H[[num, den]].to_numpy(float)
    rate = lambda a: a[..., 0].sum(-1) / a[..., 1].sum(-1)  # noqa: E731
    r = rate(g) / rate(h) if rate(h) > 0 else np.nan
    idx = np.random.default_rng(0).integers(0, len(g), (N_BOOT, len(g)))
    hb = rate(h[idx])
    bs = np.where(hb > 0, rate(g[idx]) / np.where(hb > 0, hb, 1), np.nan)
    ci90, ci95 = np.nanpercentile(bs, [5, 95]), np.nanpercentile(bs, [2.5, 97.5])
    if not np.isfinite(r):
        v = "inconclusive"
    elif 0.80 <= ci90[0] and ci90[1] <= 1.25:
        v = "matches"
    elif (ci95[0] > 1 or ci95[1] < 1):
        v = "differs (" + ("Gemini higher" if r > 1 else "Gemini lower") + ")"
    else:
        v = "inconclusive"
    return {"gemini_rate": float(rate(g)), "human_rate": float(rate(h)), "ratio": float(r),
            "ci90": [float(x) for x in ci90], "ci95": [float(x) for x in ci95], "verdict": v}


def do_analyse() -> None:
    from sacrebleu.metrics import CHRF
    S = json.load(open(SAMPLE, encoding="utf-8"))
    rows = S["rows"]
    done = {(r["pos"], r["kind"]): r for r in map(json.loads, DRAFTS.open(encoding="utf-8"))}
    ok = [p for p in range(len(rows)) if not done[(p, "primary")]["defective"]]
    wl = es.wordlists()["zipf>=3"]
    G = pd.DataFrame([counts(done[(p, "primary")]["text"], wl) for p in ok])
    H = pd.DataFrame([counts(rows[p]["human"], wl) for p in ok])
    stats = {"vowel_doubling": ratio_ci(G, H, "vowel_doubling", "letters"),
             "h_digraph": ratio_ci(G, H, "h_digraph", "letters"),
             "english_word_share": ratio_ci(G, H, "english", "words")}
    m = CHRF(char_order=6, word_order=0, beta=2)
    sc = lambda a, b: m.sentence_score(a.lower(), [b.lower()]).score  # noqa: E731
    ch = np.array([sc(done[(p, "primary")]["text"], rows[p]["human"]) for p in ok])
    rp = [p for p in S["resample_positions"] if not done[(p, "G1")]["defective"] and not done[(p, "G2")]["defective"]]
    cg = np.array([sc(done[(p, "G1")]["text"], done[(p, "G2")]["text"]) for p in rp])
    bci = lambda x: [float(v) for v in np.percentile(x[np.random.default_rng(0).integers(0, len(x), (N_BOOT, len(x)))]  # noqa: E731
                                                     .mean(1), [2.5, 97.5])]
    chrf = {"gemini_vs_human": {"n": len(ch), "mean": float(ch.mean()), "ci": bci(ch)},
            "gemini_vs_gemini_resample": {"n": len(cg), "mean": float(cg.mean()), "ci": bci(cg)},
            "status": "descriptive only"}
    vs = [v["verdict"] for v in stats.values()]
    verdict = ("holds" if all(v == "matches" for v in vs) else
               "refuted" if any(v.startswith("differs") for v in vs) else "inconclusive")
    pd.DataFrame([{"statistic": k, **v} for k, v in stats.items()]).to_csv(OUT / "stats.csv", index=False)
    write_json(OUT / "chrf.json", chrf, {"registered": REGISTERED})
    write_json(OUT / "verdict.json", {"K3b": verdict, "statistics": stats, "n": len(ok),
                                      "n_primary_defective_excluded": len(rows) - len(ok)},
               {"registered": REGISTERED, "model": MODEL, "prompt": PV})
    print("K3b analysis written", flush=True)


if __name__ == "__main__":
    step = sys.argv[1]
    if step == "draft":
        sys.exit(do_draft())
    {"sample": do_sample, "analyse": do_analyse}[step]()
