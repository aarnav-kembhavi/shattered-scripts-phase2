"""V-VER: natural_verified vs the original natural drafts (exploratory; registered in RESULTS.md 2026-10-26 03:15 IST
before this script was written or run). No prediction, no verdict.

Texts: data/processed/natural_flores_m4_500_verified_v1.jsonl (M4c: retrieval, SIB-257) and
data/processed/natural_e0_verified_v1.jsonl (sentiment), built by scripts/k_verified.py. Everything else is the
natural pipeline unchanged (ladder retrieval procedure; E0b/E0c prompts, stored content-free calibration and the
raw-fallback rule from the full stored English rows).

Usage: python scripts/v_ver.py forward <model>   (GPU; retrieval models; GPU guard first)
       python scripts/v_ver.py score <model>     (GPU; sentiment + SIB-257; GPU guard first)
       python scripts/v_ver.py analyse           (CPU)
Outputs: results/v_ver/{differences.csv, summary.json, scores_e0b/, scores_e0c/},
         cache/activations/m14full/<model>/natural_verified500.npz
"""
import json
import shutil
import sys
import time

import numpy as np
import pandas as pd

from shattered.runlog import REPO, commit, results_dir, tmp_path, write_json

sys.path.insert(0, str(REPO / "scripts"))
import l_ladder as lad  # noqa: E402
from m4b_mapping import ACT, layer_fit  # noqa: E402
from m4c_natural_flores import SEED as SPLIT_SEED  # noqa: E402

OUT = results_dir("v_ver")
M4V = REPO / "data/processed/natural_flores_m4_500_verified_v1.jsonl"
E0V = REPO / "data/processed/natural_e0_verified_v1.jsonl"
RET_MODELS = lad.COUNT_RETRIEVAL  # qwen3.5-2b, sarvam-1, gemma4-e2b
ACC_MODELS = lad.COUNT_ACC  # qwen3-1.7b, qwen3.5-2b, sarvam-1, gemma4-e2b
FORM_SIB, FORM_SENT = "natural_verified257", "natural_verified"
REGISTERED = "RESULTS.md 2026-10-26 03:15 IST (V-VER, exploratory)"


def m4v() -> list:
    R = [json.loads(x) for x in M4V.open(encoding="utf-8")]
    assert [r["index"] for r in R] == [r["index"] for r in lad.m4c_sample()[0]]
    return R


def sib_items() -> dict:
    s = lad.sib257_items()
    v = {r["index"]: r["natural"] for r in m4v()}
    for it in s["sib"]:
        it["forms"][FORM_SIB] = {"text": v[it["id"]]}
    return s


def sent_items() -> dict:
    v = {r["native"]: r["natural"] for r in map(json.loads, E0V.open(encoding="utf-8"))}
    a = lad.e0b_items()
    its = a["sentiment"]
    for it in its:
        it["forms"][FORM_SENT] = {k: v[t] for k, t in it["forms"]["native"].items()}
    return {"sentiment": its}


def guard() -> None:
    from shattered.gpuguard import wait_gpu_free
    wait_gpu_free()


def do_forward(m: str) -> None:
    path = ACT / m / "natural_verified500.npz"
    if path.exists():
        print(f"{m}: natural_verified500 exists", flush=True)
        return
    guard()
    import torch
    from shattered.interp.load import load
    R = m4v()
    t0 = time.time()
    model, tok = load(m, "cuda")
    out = lad.forward_form(model, tok, [r["natural"] for r in R], [r["index"] for r in R])
    np.savez(tmp_path(path), flores_states=out["sent_states"], index=np.array([r["index"] for r in R]),
             n_tokens=out["n_tokens"])
    commit(tmp_path(path), path)
    print(f"{m}: natural_verified500 forward done ({time.time() - t0:.0f}s incl. load)", flush=True)
    del model
    torch.cuda.empty_cache()


def do_score(m: str) -> None:
    import e0b_familiarity as e0b
    todo = []
    for d, src, form in ((OUT / "scores_e0b", lad.E0B_DIR, FORM_SENT), (OUT / "scores_e0c", lad.E0C_DIR, FORM_SIB)):
        d.mkdir(parents=True, exist_ok=True)
        if not (d / f"cf_{m}.json").exists():  # the stored content-free log-probs: calibration exactly as stored
            shutil.copyfile(src / f"cf_{m}.json", d / f"cf_{m}.json")
        if not (d / f"{m}__{form}.parquet").exists():
            todo.append((d, form))
    if not todo:
        print(f"{m}: scores exist", flush=True)
        return
    guard()
    for d, form in todo:  # score_model loads the model once per call; one load at a time
        e0b.score_model(m, sent_items() if form == FORM_SENT else sib_items(), [form], d)


def paired(a: np.ndarray, b: np.ndarray) -> dict:
    d = lad.paired(a, b)
    return {"n": d["n"], "verified": d["acc_a"], "original": d["acc_b"], "diff": d["diff"], "ci_low": d["ci"][0],
            "ci_high": d["ci"][1], "verified_only": d["a_only"], "original_only": d["b_only"], "p_mcnemar": d["p"]}


def do_analyse() -> None:
    import e0b_familiarity as e0b
    rows = []
    # retrieval
    R, keep, _ = lad.m4c_sample()
    idx = np.array([r["index"] for r in R])[keep]
    n = len(idx)
    order = np.random.default_rng(SPLIT_SEED).permutation(n)
    tr, te = np.sort(order[: n // 2]), np.sort(order[n // 2:])
    folds = np.array_split(np.random.default_rng(SPLIT_SEED + 2).permutation(tr), 5)
    V = {r["index"]: r for r in m4v()}
    changed_test = int(sum(V[i]["verified_changed"] for i in idx[te]))
    ladder = pd.read_csv(REPO / "results/l_ladder/retrieval.csv")
    for m in RET_MODELS:
        E = np.load(ACT / m / "english.npz")["flores_states"][idx]
        hits = {}
        for f, name in (("original", "natural500.npz"), ("verified", "natural_verified500.npz")):
            z = np.load(ACT / m / name)
            assert np.array_equal(z["index"][keep], idx)
            X = z["flores_states"][keep]
            fits = [layer_fit(X[:, l], E[:, l], tr, te, folds) for l in range(X.shape[1])]
            lu = int(np.argmax([r["unmapped_train"] for r in fits]))
            hits[f] = (fits[lu]["unmapped"], lu)
        ref = ladder[(ladder.model == m) & (ladder.form == "natural")].unmapped_test.item()
        assert np.isclose(hits["original"][0].mean(), ref), (m, hits["original"][0].mean(), ref)
        rows.append({"measure": "retrieval", "model": m, "items_text_changed": changed_test,
                     **paired(hits["verified"][0], hits["original"][0]),
                     "layer_original": hits["original"][1], "layer_verified": hits["verified"][1]})
    # accuracy
    ref = pd.read_csv(REPO / "results/l_ladder/accuracy.csv")
    for task, d, src, form, orig, n_changed in (
            ("sib", OUT / "scores_e0c", lad.E0C_DIR, FORM_SIB, "natural257",
             int(sum(V[it["id"]]["verified_changed"] for it in lad.sib257_items()["sib"]))),
            ("sentiment", OUT / "scores_e0b", lad.E0B_DIR, FORM_SENT, "natural", None)):
        cf = {m: json.load(open(src / f"cf_{m}.json")) for m in ACC_MODELS}
        full_en = pd.concat([pd.read_parquet(src / f"{m}__english.parquet") for m in ACC_MODELS], ignore_index=True)
        C = pd.concat([full_en] + [pd.read_parquet(src / f"{m}__{orig}.parquet") for m in ACC_MODELS]
                      + [pd.read_parquet(d / f"{m}__{form}.parquet") for m in ACC_MODELS], ignore_index=True)
        C, _ = e0b.apply_calibration(C, cf)  # raw-fallback decided on the full stored English rows, as stored
        if task == "sentiment":
            ev = {r["native"]: r for r in map(json.loads, E0V.open(encoding="utf-8"))}
            items = {it["id"]: it for it in sent_items()["sentiment"]}
            n_changed = sum(ev[items[i]["forms"]["native"]["text"]]["verified_changed"] for i in items
                            if not items[i].get("natural_defective"))
        for m in ACC_MODELS:
            g = C[(C.model == m) & (C.task == task) & C.form.isin([orig, form])]
            piv = g.pivot_table(index="id", columns="form", values="pred_cal")
            lab = g.drop_duplicates("id").set_index("id").label.loc[piv.index]
            k = piv[orig].notna() & piv[form].notna()
            corr = piv.eq(lab, axis=0)[k]
            r0 = ref[(ref.model == m) & (ref.task == task) & (ref.form == orig)].acc_cal.item()
            assert np.isclose(corr[orig].mean(), r0), (m, task, corr[orig].mean(), r0)
            pred_changed = int((piv.loc[k, orig] != piv.loc[k, form]).sum())
            rows.append({"measure": "sib257" if task == "sib" else "sentiment", "model": m,
                         "items_text_changed": n_changed, "predictions_changed": pred_changed,
                         **paired(corr[form].to_numpy(), corr[orig].to_numpy())})
    K = pd.DataFrame(rows)
    K.to_csv(OUT / "differences.csv", index=False)
    write_json(OUT / "summary.json", {"differences": K.to_dict("records")},
               {"registered": REGISTERED, "status": "exploratory, no verdict", "difference": "verified - original"})
    pd.set_option("display.width", 250)
    print(K.round(4).to_string(index=False))


if __name__ == "__main__":
    step = sys.argv[1]
    if step in ("forward", "score"):
        {"forward": do_forward, "score": do_score}[step](sys.argv[2])
    else:
        do_analyse()
