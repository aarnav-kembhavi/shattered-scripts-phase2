"""X4 retrieval, R2 (registered, Phase 2 pre-registration, X4): unmapped FLORES+ retrieval against English on the 2,009 dev+devtest sentences (the M4b split, SEED 0: test half n = 1,005, layer chosen on the train
half) for Bengali and Telugu, forms native, ITRANS, lossy. Models with retrieval: Qwen3.5-2B, Sarvam-1, Gemma 4 E2B (counted candidates) and Qwen2.5-1.5B (reported, never counted); Qwen3-1.7B has no retrieval
(Phase 1). Counting rule per language (registered): native unmapped retrieval on the test half at least 0.50. R2: native > ITRANS on the 2,009 sentences (test half), paired bootstrap over test sentences
(10,000, seed 0, 95%), the enlarged-set effect rule (all-but-one: positive with the CI above 0 in at least n - 1 of the n counted models; uninformative with fewer than three).
Usage: python scripts/x4_ret.py score | analyse      Output: results/phase2/x4/<lang>/retrieval/, r2.json. Not included here: the lowercase form, natural (R3), the surface baseline."""
import json
import sys
import time
from pathlib import Path

import numpy as np
import torch

sys.path.insert(0, str(Path(__file__).resolve().parent))
from kaggle_retrieval_gate import SEED, unmapped_curves  # noqa: E402
from m14_full import flores_any, flores_forms  # noqa: E402

from shattered.interp.collect import Sentence, collect  # noqa: E402
from shattered.interp.load import load  # noqa: E402
from shattered.runlog import REPO, results_dir, write_json  # noqa: E402
from shattered.translit import to_lossy  # noqa: E402
from shattered.translit.scheme import SCRIPTS, itrans_for  # noqa: E402

LANGS = {"bn": "ben_Beng", "te": "tel_Telu"}
MODELS = ["qwen3.5-2b", "sarvam-1", "gemma4-e2b", "qwen2.5-1.5b"]
FORMS = ["native", "itrans", "lossy"]
N_BOOT = 10_000


def sentences(code: str) -> dict:
    F = flores_any(code, "dev", "flores_plus", nfc=True) + flores_any(code, "devtest", "flores_plus", nfc=True)
    assert len(F) == 2009
    it = itrans_for(SCRIPTS[code])
    return {"native": F, "itrans": [it.encode(s) for s in F], "lossy": [to_lossy(s, code) for s in F]}


def states(model, tok, texts: list[str]) -> np.ndarray:
    return collect(model, tok, [Sentence(str(i), s, []) for i, s in enumerate(texts)])["sent_states"].astype(np.float32)


def score() -> None:
    en = flores_forms()["english"]
    assert len(en) == 2009
    order = np.random.default_rng(SEED).permutation(2009)
    tr, te = np.sort(order[:1004]), np.sort(order[1004:])
    S = {l: sentences(c) for l, c in LANGS.items()}
    for m in MODELS:
        todo = [(l, f) for l in LANGS for f in FORMS if not (results_dir(f"phase2/x4/{l}/retrieval") / f"{m}__{f}.npz").exists()]
        if not todo:
            continue
        t0 = time.time()
        model, tok = load(m, "cuda")
        E = states(model, tok, en)
        for l, f in todo:
            X = states(model, tok, S[l][f])
            tra, tes = unmapped_curves(X, E, tr, te)
            lu = int(tra.argmax())
            np.savez(results_dir(f"phase2/x4/{l}/retrieval") / f"{m}__{f}.npz", layer=lu, acc=float(tes[lu].mean()), correct=tes[lu].astype(np.uint8), curve=tes.mean(1), train_curve=tra)
            print(m, l, f, "layer", lu, "acc", round(float(tes[lu].mean()), 4), f"{time.time() - t0:.0f}s", flush=True)
        del model
        torch.cuda.empty_cache()


def boot(d: np.ndarray) -> dict:
    idx = np.random.default_rng(0).integers(0, len(d), (N_BOOT, len(d)))
    b = d[idx].mean(1)
    return {"diff": float(d.mean()), "ci95": [float(np.percentile(b, 2.5)), float(np.percentile(b, 97.5))], "n": int(len(d))}


def analyse() -> None:
    for l in LANGS:
        d = results_dir(f"phase2/x4/{l}/retrieval")
        out = {"language": l, "models": {}}
        for m in MODELS:
            z = {f: np.load(d / f"{m}__{f}.npz") for f in FORMS}
            out["models"][m] = {"acc": {f: float(z[f]["acc"]) for f in FORMS}, "layer": {f: int(z[f]["layer"]) for f in FORMS}, "counted": bool(m != "qwen2.5-1.5b" and float(z["native"]["acc"]) >= 0.50),
                                "native_minus_itrans": boot(z["native"]["correct"].astype(float) - z["itrans"]["correct"].astype(float)),
                                "native_minus_lossy": boot(z["native"]["correct"].astype(float) - z["lossy"]["correct"].astype(float))}
        counted = [m for m, v in out["models"].items() if v["counted"]]
        n = len(counted)
        pos = sum(1 for m in counted if out["models"][m]["native_minus_itrans"]["ci95"][0] > 0)
        neg = sum(1 for m in counted if out["models"][m]["native_minus_itrans"]["ci95"][1] < 0)
        out["counted_models"] = counted
        out["R2"] = {"n_counted": n, "native_minus_itrans_ci_above_0": pos, "ci_below_0": neg,
                     "verdict": "uninformative (fewer than three counted models)" if n < 3 else "supported" if pos >= n - 1 and neg == 0 else "refuted" if neg > 0 or pos == 0 else "partly supported"}
        write_json(REPO / "results" / "phase2" / "x4" / l / "r2.json", out, {"registration": "RESULTS.md X4 (R2)"})
        print(l, out["R2"], {m: {f: round(a, 3) for f, a in v["acc"].items()} for m, v in out["models"].items()})


if __name__ == "__main__":
    {"score": score, "analyse": analyse}[sys.argv[1]]()
