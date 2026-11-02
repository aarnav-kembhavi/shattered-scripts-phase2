"""Expected CI widths for X8 at n = 100 and n = 200, using the K3b data (Gemini vs Dakshina human, Kannada strings) as a proxy.
Proxy limits: K3b compares Gemini with ONE human; X8 compares two humans (P, Q) and averages them for the Gemini ratio."""
import json, sys, re
import numpy as np
from pathlib import Path
R = str(Path(__file__).resolve().parents[1])
sys.path.insert(0, R + "/scripts")
sys.path.insert(0, R + "/src")
import k3b_dakshina as k3
import english_share as es

S = json.load(open(k3.SAMPLE, encoding="utf-8"))
rows = S["rows"]
done = {(r["pos"], r["kind"]): r for r in map(json.loads, k3.DRAFTS.open(encoding="utf-8"))}
ok = [p for p in range(len(rows)) if not done[(p, "primary")]["defective"]]
wl = es.wordlists()["zipf>=3"]
gem = [done[(p, "primary")]["text"].lower() for p in ok]
hum = [rows[p]["human"].lower() for p in ok]
print("strings", len(ok))

def counts_arr(texts):
    c = [k3.counts(t, wl) for t in texts]
    return {k: np.array([x[k] for x in c], float) for k in c[0]}
G, H = counts_arr(gem), counts_arr(hum)

def ratio(idx, num, den):
    g = G[num][idx].sum() / G[den][idx].sum()
    h = H[num][idx].sum() / H[den][idx].sum()
    return g / h if h > 0 else np.nan

def lev(a, b):
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[-1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]

norm = lambda s: re.sub(r"[^a-z ]", "", s)
cer = np.array([lev(norm(a), norm(b)) / max(len(norm(a)), len(norm(b)), 1) for a, b in zip(gem, hum)])
DBL = re.compile(r"aa|ee|ii|oo|uu")
def word_labels(g, h):
    gw, hw = g.split(), h.split()
    if len(gw) != len(hw):
        return None
    return [(bool(DBL.search(a)), bool(DBL.search(b))) for a, b in zip(gw, hw)]
labs = [word_labels(a, b) for a, b in zip(gem, hum)]
eq = [i for i, l in enumerate(labs) if l is not None]
print("equal word count strings:", len(eq), "of", len(ok))

def kappa(idx):
    a = np.array([x for i in idx if labs[i] for x, _ in labs[i]], float)
    b = np.array([y for i in idx if labs[i] for _, y in labs[i]], float)
    po = (a == b).mean()
    pe = a.mean() * b.mean() + (1 - a.mean()) * (1 - b.mean())
    return (po - pe) / (1 - pe) if pe < 1 else np.nan

rng = np.random.default_rng(0)
def width(stat, pool, n, level, reps=120, boots=1500):
    ws = []
    for _ in range(reps):
        sub = rng.choice(pool, n, replace=False)
        vals = []
        for _ in range(boots):
            vals.append(stat(rng.choice(sub, n, replace=True)))
        lo, hi = np.nanpercentile(vals, [(100 - level) / 2, 100 - (100 - level) / 2])
        ws.append(hi - lo)
    return float(np.mean(ws))

allidx = np.arange(len(ok))
print("point values on all strings: ratio vd %.3f, hd %.3f, en %.3f; mean CER %.3f; kappa %.3f" % (
    ratio(allidx, "vowel_doubling", "letters"), ratio(allidx, "h_digraph", "letters"), ratio(allidx, "english", "words"),
    cer.mean(), kappa(np.array(eq))))
out = {}
for n in (100, 200):
    out[n] = {
        "ratio_vowel_doubling_90": width(lambda i: ratio(i, "vowel_doubling", "letters"), allidx, n, 90),
        "ratio_h_digraph_90": width(lambda i: ratio(i, "h_digraph", "letters"), allidx, n, 90),
        "ratio_english_share_90": width(lambda i: ratio(i, "english", "words"), allidx, n, 90),
        "mean_cer_95": width(lambda i: cer[i].mean(), allidx, n, 95),
        "kappa_95": width(kappa, np.array(eq), n, 95),
    }
    print(n, {k: round(v, 3) for k, v in out[n].items()})
dest = Path(R) / "results" / "phase2" / "x8"
dest.mkdir(parents=True, exist_ok=True)
json.dump(out, open(dest / "expected_ci_widths.json", "w"), indent=1)
