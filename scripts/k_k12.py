"""K1 and K2 on human verified Gemini romanization (registered 2026-10-16; data label and implementation choices fixed
in RESULTS.md 2026-10-26 03:15 IST before this script ran). No rule or threshold differs from the registration.

Forms (A's verification, data/annotation/verified_A_v1.jsonl): k_nat_ver, k_kan_ver (verified; natural uses the draft
for indicsentiment-test-249), k_nat_draft, k_kan_draft (Gemini drafts, secondary comparison).
Tasks: sentiment on the 200 sentiment items (E0 template), SIB-200 topic on the 300 FLORES items (E0c template).

Usage: python scripts/k_k12.py pilot            (GPU, Qwen3.5-2B, 10 sentiment + 10 SIB items; no accuracy or test)
       python scripts/k_k12.py score <model>    (GPU: the four forms, both tasks; GPU guard first)
       python scripts/k_k12.py forward <model>  (GPU: K2b Kanglish-verified vectors, 300 FLORES items)
       python scripts/k_k12.py analyse          (CPU: K1, K2a, K2b)
Outputs: results/k12/{pilot.json, scores/, vectors/, k1.csv, k2a.csv, k2b.csv, verdict.json}
"""
import json
import shutil
import sys
import time

import numpy as np
import pandas as pd

from shattered.runlog import REPO, commit, results_dir, tmp_path, write_json

sys.path.insert(0, str(REPO / "scripts"))
import k_annotation as K  # noqa: E402
import l_ladder as lad  # noqa: E402

OUT = results_dir("k12")
SCORES, VEC = OUT / "scores", OUT / "vectors"
VER = REPO / "data/annotation/verified_A_v1.jsonl"
FORMS = ["k_nat_ver", "k_kan_ver", "k_nat_draft", "k_kan_draft"]
ACC_MODELS = lad.ACC_MODELS  # qwen2.5-1.5b, qwen3.5-2b, sarvam-1, gemma4-e2b, qwen3-1.7b
M4_MODELS = lad.M4_MODELS
USE_DRAFT = {"indicsentiment-test-249"}  # natural: A's fix drops content (Aarnav, 2026-10-26)
REGISTERED = "RESULTS.md 2026-10-16 (K1-K3); data label and implementation 2026-10-26 03:15 IST"
PILOT_MODEL, SEED = "qwen3.5-2b", 0


def k_items() -> dict:
    """{"sentiment": [...200], "sib": [...300]} in the e0b item format; SIB ids are FLORES indices (as E0c)."""
    V = {r["item_id"]: r for r in map(json.loads, VER.open(encoding="utf-8"))}
    sib_label = {it["id"]: int(it["label"]) for it in lad.e0c_items()["sib"]}  # SIB topic labels (E0c items)
    out = {"sentiment": [], "sib": []}
    for it in K.items():
        v = V[it["id"]]
        nat = v["natural_draft"] if it["id"] in USE_DRAFT else v["natural_verified"]
        forms = {"k_nat_ver": {"text": nat}, "k_kan_ver": {"text": v["kanglish_verified"]},
                 "k_nat_draft": {"text": v["natural_draft"]}, "k_kan_draft": {"text": v["kanglish_draft"]},
                 "native": {"text": it["native"]}}
        if it["source"] == "sentiment":
            out["sentiment"].append({"id": it["id"], "label": int(it["label"]), "forms": forms, "english": it["english"]})
        else:
            fid = int(it["id"].split("-")[1])
            out["sib"].append({"id": fid, "label": sib_label[fid], "forms": forms,
                               "item_id": it["id"], "english": it["english"]})
    assert (len(out["sentiment"]), len(out["sib"])) == (200, 300)
    return out


def check_labels(items) -> dict:
    """Labels and native texts must equal the stored E0b / E0c items where those exist."""
    a, c = lad.e0b_items(), lad.e0c_items()
    eb, ec = {it["id"]: it for it in a["sentiment"]}, {it["id"]: it for it in c["sib"]}
    res = {}
    for t, store in (("sentiment", eb), ("sib", ec)):
        both = [it for it in items[t] if it["id"] in store]
        res[t] = {"in_store": len(both), "of": len(items[t]),
                  "label_mismatch": sum(int(store[it["id"]]["label"]) != it["label"] for it in both),
                  "native_mismatch": sum(store[it["id"]]["forms"]["native"]["text"] != it["forms"]["native"]["text"]
                                         for it in both)}
    return res


def guard() -> int:
    from shattered.gpuguard import wait_gpu_free
    return wait_gpu_free()


def score(m: str, items: dict, out_dir) -> None:
    import e0b_familiarity as e0b
    out_dir.mkdir(parents=True, exist_ok=True)
    e0b.score_model(m, items, FORMS, out_dir)


def vectors(model, tok, texts, ids) -> np.ndarray:
    return lad.forward_form(model, tok, texts, ids)["sent_states"]


def do_pilot() -> int:
    import torch
    from shattered.interp.load import load
    from shattered.translit.codemix import code_mixing_v2
    items = k_items()
    rng = np.random.default_rng(SEED)
    pick = {t: [items[t][k] for k in sorted(rng.choice(len(items[t]), 10, replace=False))] for t in items}
    used = guard()
    pdir = OUT / "pilot_scores"
    shutil.rmtree(pdir, ignore_errors=True)
    t0 = time.time()
    score(PILOT_MODEL, pick, pdir)  # loads, scores 20 items x 4 forms, unloads (no accuracy computed)
    t_score = time.time() - t0
    meta = json.load(open(pdir / f"{PILOT_MODEL}__k_kan_ver.json"))
    cf_new = json.load(open(pdir / f"cf_{PILOT_MODEL}.json"))
    cf_old = {"sentiment": json.load(open(lad.E0B_DIR / f"cf_{PILOT_MODEL}.json")),
              "sib": json.load(open(lad.E0C_DIR / f"cf_{PILOT_MODEL}.json"))}
    cf_delta = max(abs(a - b) for x in cf_new for t in cf_new[x] for a, b in zip(cf_new[x][t], cf_old[t][x][t]))
    rows = pd.concat([pd.read_parquet(pdir / f"{PILOT_MODEL}__{f}.parquet") for f in FORMS])
    t1 = time.time()
    model, tok = load(PILOT_MODEL, "cuda")
    S = vectors(model, tok, [it["forms"]["k_kan_ver"]["text"] for it in pick["sib"]], [it["id"] for it in pick["sib"]])
    t_fwd = time.time() - t1
    del model
    torch.cuda.empty_cache()
    share = [code_mixing_v2(it["forms"]["k_kan_ver"]["text"], it["english"])["english_share"]
             for t in pick for it in pick[t]]
    m4b = pd.read_csv(REPO / "results/m4b_mapping/summary.csv")
    layers = {m: int(m4b[(m4b.model == m) & (m4b.form == "native")].best_layer_unmapped.item()) for m in M4_MODELS}
    te = np.load(REPO / "results/m4b_mapping/items.npz")["test_idx"]
    n_prompts = len(rows)
    out = {"model": PILOT_MODEL, "gpu_mb_before_load": used, "items": {t: [it.get("item_id", it["id"]) for it in v]
                                                                       for t, v in pick.items()},
           "label_and_native_check_all_items": check_labels(items),
           "prompts_scored": n_prompts, "prompts_expected": 20 * len(FORMS),
           "content_free_max_abs_delta_vs_stored": cf_delta,
           "k2b_vectors_shape": list(S.shape), "k2b_layers_from_m4b": layers,
           "k2b_all_300_in_m4b_test_half": bool(set(it["id"] for it in items["sib"]) <= set(te.tolist())),
           "m4b_test_half_size": int(len(te)), "english_share_range_pilot": [min(share), max(share)],
           "fertility_k_kan_ver": meta["fertility"],
           "seconds": {"score_20_items_4_forms_incl_load": t_score, "forward_10_items_incl_load": t_fwd}}
    per_prompt = t_score / n_prompts
    out["estimate_hours_full"] = {
        "score_500_items_4_forms_5_models_at_pilot_speed": per_prompt * 500 * len(FORMS) * 5 / 3600,
        "forward_300_items_4_models_at_pilot_speed": t_fwd / 10 * 300 * 4 / 3600}
    ok = (n_prompts == 20 * len(FORMS) and cf_delta < 1e-3 and out["k2b_all_300_in_m4b_test_half"]
          and all(v["label_mismatch"] == 0 and v["native_mismatch"] == 0 for v in out["label_and_native_check_all_items"]
                  .values()))
    out["all_passed"] = ok
    write_json(OUT / "pilot.json", out, {"registered": REGISTERED, "status": "pilot; no accuracy or test computed"})
    shutil.rmtree(pdir, ignore_errors=True)
    print(json.dumps(out, indent=1), flush=True)
    return 0 if ok else 1


def do_score(m: str) -> None:
    if all((SCORES / f"{m}__{f}.parquet").exists() for f in FORMS):
        print(f"{m}: scores exist", flush=True)
        return
    guard()
    score(m, k_items(), SCORES)


def do_forward(m: str) -> None:
    import torch
    from shattered.interp.load import load
    path = VEC / f"{m}__k_kan_ver300.npz"
    if path.exists():
        return
    VEC.mkdir(parents=True, exist_ok=True)
    sib = k_items()["sib"]
    guard()
    model, tok = load(m, "cuda")
    S = vectors(model, tok, [it["forms"]["k_kan_ver"]["text"] for it in sib], [it["id"] for it in sib])
    np.savez(tmp_path(path), sent_states=S, index=np.array([it["id"] for it in sib]))
    commit(tmp_path(path), path)
    del model
    torch.cuda.empty_cache()
    print(f"{m}: K2b vectors {S.shape}", flush=True)


def do_analyse() -> int:
    import statsmodels.api as sm
    from statsmodels.stats.contingency_tables import mcnemar
    from statsmodels.stats.multitest import multipletests
    from transformers import AutoTokenizer
    import e0b_familiarity as e0b
    from shattered.interp.load import MODELS as HF
    from shattered.translit.codemix import code_mixing, code_mixing_v2
    items = k_items()
    text = {(t, it["id"]): it["forms"]["k_kan_ver"]["text"] for t in items for it in items[t]}
    eng = {(t, it["id"]): it["english"] for t in items for it in items[t]}
    # English share: v2 (primary; Aarnav 2026-10-26, option A) and v1 (the registered tagger; sensitivity)
    SHARE = {"v2": {k: code_mixing_v2(v, eng[k])["english_share"] for k, v in text.items()},
             "v1": {k: code_mixing(v)["english_share"] for k, v in text.items()}}
    # calibration: stored content-free files; raw fallback from the full stored English rows (E0b / E0c)
    C, cells = [], []
    for task, src in (("sentiment", lad.E0B_DIR), ("sib", lad.E0C_DIR)):
        cf = {m: json.load(open(src / f"cf_{m}.json")) for m in ACC_MODELS}
        en = pd.concat([pd.read_parquet(src / f"{m}__english.parquet") for m in ACC_MODELS], ignore_index=True)
        ks = pd.concat([pd.read_parquet(SCORES / f"{m}__{f}.parquet") for m in ACC_MODELS for f in FORMS],
                       ignore_index=True)
        D, _ = e0b.apply_calibration(pd.concat([en, ks[ks.task == task]], ignore_index=True), cf)
        D = D[D.task == task]
        ids = {it["id"] for it in items[task]}
        for m in ACC_MODELS:
            e = D[(D.model == m) & (D.form == "english") & D.id.isin(ids)]
            acc_en = float((e.pred_cal == e.label).mean())
            cells.append({"model": m, "task": task, "n_english": len(e), "english_acc": acc_en,
                          "chance": e0b.CHANCE[task], "informative": acc_en >= e0b.CHANCE[task] + 0.05})
        C.append(D[D.form.isin(FORMS)])
    C = pd.concat(C, ignore_index=True)
    C["correct"] = C.pred_cal == C.label
    cells = pd.DataFrame(cells)
    k1, k2a = [], []
    for r in cells.itertuples():
        g = C[(C.model == r.model) & (C.task == r.task)].pivot_table(index="id", columns="form", values="correct")
        p = C[(C.model == r.model) & (C.task == r.task) & (C.form == "k_kan_ver")].set_index("id")
        for a, b, kind in (("k_kan_ver", "k_nat_ver", "primary"), ("k_kan_draft", "k_nat_draft", "secondary_drafts")):
            ca, cb = g[a].astype(bool).to_numpy(), g[b].astype(bool).to_numpy()
            tab = [[int((ca & cb).sum()), int((ca & ~cb).sum())], [int((~ca & cb).sum()), int((~ca & ~cb).sum())]]
            d = lad.paired(ca, cb)
            k1.append({"model": r.model, "task": r.task, "comparison": kind, "informative": r.informative,
                       "n": len(ca), "acc_kanglish": ca.mean(), "acc_natural": cb.mean(), "diff": ca.mean() - cb.mean(),
                       "ci_low": d["ci"][0], "ci_high": d["ci"][1], "p": mcnemar(tab, exact=True).pvalue})
        tok = AutoTokenizer.from_pretrained(HF[r.model])
        ids = list(p.index)
        y = p.correct.astype(float).to_numpy()
        lt = np.log([len(tok(text[(r.task, i)], add_special_tokens=False)["input_ids"]) for i in ids])
        const = float(np.bincount(p.pred_cal.astype(int)).max() / len(p))
        z = lambda x: (x - x.mean()) / x.std()  # noqa: E731
        for tagger in ("v2", "v1"):
            sh = np.array([SHARE[tagger][(r.task, i)] for i in ids])
            X = sm.add_constant(np.column_stack([z(sh), z(lt)]))
            try:
                f = sm.Logit(y, X).fit(disp=0)
                coef, pv = float(f.params[1]), float(f.pvalues[1])
            except Exception as ex:  # noqa: BLE001 - perfect separation etc.: reported, not counted
                coef, pv = float("nan"), float("nan")
                print(f"K2a {r.model} {r.task} {tagger}: fit failed ({ex})", flush=True)
            k2a.append({"tagger": tagger, "model": r.model, "task": r.task, "n": len(y), "coef_english_share": coef,
                        "p_one_sided": (pv / 2 if coef > 0 else 1 - pv / 2) if pv == pv else float("nan"),
                        "constant_label_rate": const, "counted": bool(r.informative and const <= 0.90)})
    K1, K2a = pd.DataFrame(k1), pd.DataFrame(k2a)
    prim = (K1.comparison == "primary") & K1.informative
    K1["p_holm"] = np.nan
    K1.loc[prim, "p_holm"] = multipletests(K1.loc[prim, "p"], method="holm")[1]
    g = K1[prim]
    n_inf = len(g)
    sig = int(((g.p_holm < 0.05) & (g["diff"] > 0)).sum())
    k1v = ("supported" if n_inf and (g["diff"] > 0).all() and sig >= n_inf / 2 else
           "refuted" if n_inf and ((g["diff"] <= 0).sum() >= n_inf / 2 or ((g.p_holm < 0.05) & (g["diff"] < 0)).any())
           else "inconclusive")
    def rule(df, coef_col):
        n = len(df)
        if not n:
            return "inconclusive"
        if (df[coef_col] > 0).all() and (df.p_holm < 0.05).sum() >= n / 2:
            return "supported"
        if (df[coef_col] <= 0).sum() >= n / 2:
            return "refuted"
        return "inconclusive"
    K2a["p_holm"] = np.nan
    k2av, k2a_counted = {}, {}
    for tagger in ("v2", "v1"):
        cnt = (K2a.tagger == tagger) & K2a.counted & K2a.p_one_sided.notna()
        K2a.loc[cnt, "p_holm"] = multipletests(K2a.loc[cnt, "p_one_sided"], method="holm")[1]
        k2av[tagger], k2a_counted[tagger] = rule(K2a[cnt], "coef_english_share"), int(cnt.sum())
    # K2b
    m4b = pd.read_csv(REPO / "results/m4b_mapping/summary.csv")
    te = np.load(REPO / "results/m4b_mapping/items.npz")["test_idx"]
    sib = items["sib"]
    k2b = []
    for m in M4_MODELS:
        L = int(m4b[(m4b.model == m) & (m4b.form == "native")].best_layer_unmapped.item())
        z_ = np.load(VEC / f"{m}__k_kan_ver300.npz")
        X = z_["sent_states"][:, L].astype(np.float64)
        E = np.load(lad.ACT / m / "english.npz")["flores_states"][te, L].astype(np.float64)
        X /= np.linalg.norm(X, axis=1, keepdims=True)
        E /= np.linalg.norm(E, axis=1, keepdims=True)
        pos = {int(i): k for k, i in enumerate(te)}
        sims = X @ E.T
        rank = np.array([1 + int((sims[k] > sims[k, pos[int(i)]]).sum()) for k, i in enumerate(z_["index"])])
        tok = AutoTokenizer.from_pretrained(HF[m])
        lt = np.log([len(tok(it["forms"]["k_kan_ver"]["text"], add_special_tokens=False)["input_ids"]) for it in sib])
        zz = lambda x: (x - x.mean()) / x.std()  # noqa: E731
        for tagger in ("v2", "v1"):
            sh = np.array([SHARE[tagger][("sib", it["id"])] for it in sib])
            f = sm.OLS(-np.log(rank), sm.add_constant(np.column_stack([zz(sh), zz(lt)]))).fit()
            coef, pv = float(f.params[1]), float(f.pvalues[1])
            k2b.append({"tagger": tagger, "model": m, "layer": L, "n": len(rank), "median_rank": float(np.median(rank)),
                        "coef_english_share": coef, "p_one_sided": pv / 2 if coef > 0 else 1 - pv / 2})
    K2b = pd.DataFrame(k2b)
    K2b["p_holm"] = np.nan
    k2bv = {}
    for tagger in ("v2", "v1"):
        k = K2b.tagger == tagger
        K2b.loc[k, "p_holm"] = multipletests(K2b.loc[k, "p_one_sided"], method="holm")[1]
        k2bv[tagger] = rule(K2b[k], "coef_english_share")
    for name, df in (("k1", K1), ("k2a", K2a), ("k2b", K2b), ("cells", cells)):
        df.to_csv(OUT / f"{name}.csv", index=False)
    v = {"K1": k1v, "K1_n_informative": n_inf, "K1_n_significant_positive": sig,
         "K2a": k2av, "K2a_n_counted": k2a_counted, "K2b": k2bv,
         "K2a_differs_v1_v2": k2av["v1"] != k2av["v2"], "K2b_differs_v1_v2": k2bv["v1"] != k2bv["v2"],
         "primary_tagger": "v2 (codemix_v2 with KN_FORCE 'ee'); v1 = registered tagger, sensitivity"}
    write_json(OUT / "verdict.json", v, {"registered": REGISTERED, "data": "human verified Gemini romanization"})
    pd.set_option("display.width", 250)
    print(cells.to_string(index=False)); print(K1.round(4).to_string(index=False))
    print(K2a.round(4).to_string(index=False)); print(K2b.round(4).to_string(index=False)); print(json.dumps(v))
    return 0


if __name__ == "__main__":
    step = sys.argv[1]
    if step in ("score", "forward"):
        {"score": do_score, "forward": do_forward}[step](sys.argv[2])
    else:
        sys.exit({"pilot": do_pilot, "analyse": do_analyse}[step]() or 0)
