"""M4c: natural romanization in M4. A random 500 FLORES+ sentences (seed 0, from the 2,009 dev+devtest) are romanized
with the same model, prompt and temperature as E0 (gemini-3.5-flash-lite, natural_romanization_v1, temperature 0;
cached, so sentences already done for E2 cost nothing). Defective outputs (shattered.translit.natural.defective) are
retried twice (attempts 2-3, as for E0) and excluded if still defective. Then, on the same sentences for every form
(native, ITRANS, natural): best-layer retrieval vs English (unmapped) and the M4b ridge mapping test (50/50 split of
these sentences, seed 0, same procedure as scripts/m4b_mapping.py).

Usage: python scripts/m4c_natural_flores.py romanize      (API; stops on the daily quota, re-run to continue)
       python scripts/m4c_natural_flores.py forward       (GPU; natural-form sentence vectors for the 4 models)
       python scripts/m4c_natural_flores.py analyse
Outputs: data/processed/natural_flores_m4_500_v1.jsonl, cache/activations/m14full/<model>/natural500.npz,
         results/m4c_natural/{summary.csv, verdict.json}
"""
import json
import sys

import numpy as np
import pandas as pd

from shattered.llm.ratelimit import DailyQuotaExceeded
from shattered.runlog import REPO, commit, results_dir, tmp_path, write_json
from shattered.translit.natural import MODEL, PROMPT_VERSION, defective, make_client, romanize

sys.path.insert(0, str(REPO / "scripts"))
from m4b_mapping import ACT, MODELS, boot, layer_fit, retrieval  # noqa: E402

N_SENT, SEED = 500, 0
OUT = REPO / "data" / "processed" / "natural_flores_m4_500_v1.jsonl"


def sample_idx() -> np.ndarray:
    return np.sort(np.random.default_rng(SEED).choice(2009, N_SENT, replace=False))


def do_romanize() -> None:
    from m14_full import flores_forms
    F = flores_forms()
    client = make_client()
    done = {r["index"]: r for r in map(json.loads, OUT.open(encoding="utf-8"))} if OUT.exists() else {}
    stopped = None
    for i in sample_idx():
        i = int(i)
        if i in done and not done[i]["defective"]:
            continue
        start = done[i]["attempt"] + 1 if i in done else 1
        for attempt in range(start, 4):
            try:
                r = romanize(client, F["native"][i], attempt=attempt)
            except DailyQuotaExceeded as e:
                stopped = str(e)[:200]
                break
            row = {"index": i, "native": F["native"][i], **r}
            row["defective"] = defective(row)
            done[i] = row
            if not row["defective"]:
                break
        if stopped:
            break
    with tmp_path(OUT).open("w", encoding="utf-8") as f:
        for i in sorted(done):
            f.write(json.dumps(done[i], ensure_ascii=False) + "\n")
    commit(tmp_path(OUT), OUT)
    n_def = sum(r["defective"] for r in done.values())
    print({"n_done": len(done), "n_target": N_SENT, "n_defective_after_retries": n_def, "stopped": stopped,
           "complete": len(done) == N_SENT and stopped is None})


def rows() -> list:
    return [json.loads(l) for l in OUT.open(encoding="utf-8")]


def do_forward() -> None:
    import torch
    from shattered.interp.collect import Sentence, collect
    from shattered.interp.load import load
    R = rows()
    assert len(R) == N_SENT, "romanization incomplete"
    for m in MODELS:
        path = ACT / m / "natural500.npz"
        if path.exists():
            continue
        model, tok = load(m, "cuda")
        f = collect(model, tok, [Sentence(str(r["index"]), r["natural"], []) for r in R])
        np.savez(tmp_path(path), flores_states=f["sent_states"], index=np.array([r["index"] for r in R]),
                 n_tokens=f["n_tokens"])
        commit(tmp_path(path), path)
        del model
        torch.cuda.empty_cache()
        print(f"{m}: natural500 forward done", flush=True)


def do_analyse() -> None:
    R = rows()
    keep = np.array([not r["defective"] for r in R])
    idx = np.array([r["index"] for r in R])[keep]
    n = len(idx)
    order = np.random.default_rng(SEED).permutation(n)
    tr, te = np.sort(order[: n // 2]), np.sort(order[n // 2:])
    folds = np.array_split(np.random.default_rng(SEED + 2).permutation(tr), 5)
    out, res, items = results_dir("m4c_natural"), [], {}
    for m in MODELS:
        E = np.load(ACT / m / "english.npz")["flores_states"][idx]
        nat = np.load(ACT / m / "natural500.npz")
        assert np.array_equal(nat["index"][keep], idx)
        forms = {"native": np.load(ACT / m / "native.npz")["flores_states"][idx],
                 "itrans": np.load(ACT / m / "itrans.npz")["flores_states"][idx],
                 "natural": nat["flores_states"][keep]}
        for f, X in forms.items():
            fits = [layer_fit(X[:, l], E[:, l], tr, te, folds) for l in range(X.shape[1])]
            lm = int(np.argmax([r["cv"] for r in fits]))
            lu = int(np.argmax([r["unmapped_train"] for r in fits]))
            Xc, Ec = X.astype(np.float64), E.astype(np.float64)
            full = np.stack([retrieval(Xc[:, l] - Xc[:, l].mean(0), Ec[:, l] - Ec[:, l].mean(0))
                             for l in range(X.shape[1])])  # unmapped, all n sentences (as in M4)
            items[(m, f)] = {"mapped": fits[lm]["mapped"], "unmapped": fits[lu]["unmapped"]}
            res.append({"model": m, "form": f, "n_sentences": n, "unmapped_all_best": full.mean(1).max(),
                        "unmapped_all_best_layer": int(full.mean(1).argmax()),
                        "mapped_test": fits[lm]["mapped"].mean(), "mapped_test_ci": boot(fits[lm]["mapped"]),
                        "mapped_layer": lm, "unmapped_test": fits[lu]["unmapped"].mean(),
                        "unmapped_test_ci": boot(fits[lu]["unmapped"]), "shuffled_control": fits[lm]["shuffled"].mean()})
            print(res[-1], flush=True)
    S = pd.DataFrame(res)
    S.to_csv(out / "summary.csv", index=False)
    comp = {}
    for m in MODELS:
        for a, b in (("native", "natural"), ("natural", "itrans")):
            for k in ("mapped", "unmapped"):
                x, y = items[(m, a)][k], items[(m, b)][k]
                comp[f"{m}|{a}-{b}|{k}"] = {"diff": float(x.mean() - y.mean()), "ci": boot(x, y)}
    write_json(out / "verdict.json", {"paired_differences": comp, "n_sentences": n,
                                      "n_defective_excluded": int((~keep).sum())},
               {"model": MODEL, "prompt": PROMPT_VERSION, "sample_seed": SEED, "registered": "RESULTS.md 2026-10-16"})
    pd.set_option("display.width", 250)
    print(S.round(3).to_string(index=False))
    print(json.dumps(comp, indent=1))


if __name__ == "__main__":
    {"romanize": do_romanize, "forward": do_forward, "analyse": do_analyse}[sys.argv[1]]()
