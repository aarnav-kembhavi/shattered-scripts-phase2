"""EP-R: E-P1 / E-P2 recovery on all eligible SIB items (exploratory; registered in RESULTS.md 2026-10-26 02:40 IST
before this script was written or run). No prediction, no verdict; the registered E-P1/E-P2 outcomes are unchanged.

Patching is exactly ep_patching.py's (same functions): E-P1 scheme "final" ((a) -> (c)), E-P2 scheme "word"
(native -> lossy), points P = 0..N. Items already run in E-P1/E-P2 (registered primary and control) are reused from
results/ep{1,2}/raw/ (the pilot shows they reproduce); only the other SIB items are run here.

Usage: python scripts/ep_robust.py pilot             (GPU, Qwen3.5-2B, 20 items per experiment; no R computed)
       python scripts/ep_robust.py run <1|2> <model> (GPU: one model, one process per model load; resumable)
       python scripts/ep_robust.py analyse           (CPU)
       python scripts/ep_robust.py main              (CPU: main estimates for the paper -> main_estimates.csv)
Outputs: results/ep_robust/{pilot.json, raw/ep<1|2>_<model>.json, table.csv, gaps.csv, summary.json}
"""
import json
import sys
import time

import numpy as np
import pandas as pd

from shattered.runlog import REPO, commit, results_dir, tmp_path, write_json

sys.path.insert(0, str(REPO / "scripts"))
import ep_patching as E  # noqa: E402
import nc1  # noqa: E402

OUT = results_dir("ep_robust")
RAW = OUT / "raw"
SCHEME = {1: "final", 2: "word"}
REGISTERED = "RESULTS.md 2026-10-26 02:40 IST (EP-R, exploratory)"
GAP_MIN, N_BOOT, SEED, TOL = 0.5, 10000, 0, 0.05


def stored(exp: int, m: str) -> dict:
    """SIB rows already run in E-P1/E-P2: {id: row}."""
    R = json.load(open(E.OUT[exp] / "raw" / f"{m}.json"))
    return {r["id"]: r for r in R["rows"] if r["task"] == "sib"}


def pair(exp, V, tok, m, it):
    """(src ids, dst ids, src positions, dst positions, fids, eligible, extra positions for the integrity check)."""
    from shattered.eval.loglik import VERBALIZERS
    if exp == 1:
        pr = E.ep1_pair(V, tok, m, "sib", it)
        ok = pr["aligned"] and pr["words_match"]
        fids = E.first_ids(tok, pr["prompt"], VERBALIZERS["sib"])
        last = [g[-1] for g in pr["groups"]]
        text = sorted(q for g in pr["groups"] for q in g)
        return pr["a"], pr["c"], last, last, fids, ok, (0, text, text)
    pr = E.ep2_pair(tok, "sib", it)
    ok = pr["same_word_count"] and pr["words_decode"]
    fids = E.first_ids(tok, pr["prompt_native"], VERBALIZERS["sib"])
    assert fids == E.first_ids(tok, pr["prompt_lossy"], VERBALIZERS["sib"])
    src, dst = pr["native"], pr["lossy"]
    return src, dst, pr["last_native"], pr["last_lossy"], fids, ok, (None, [len(src) - 1], [len(dst) - 1])


def item_curve(model, pt, exp, src, dst, ps, pd_, fids, gold, integrity=False):
    lg, rec = E.run_source(model, pt, src)
    m_src, m_dst = E.margin(lg, fids, gold), E.margin(E.last_logits(model, dst), fids, gold)
    curve = [E.margin(E.run_patched(model, pt, dst, P, pd_, rec[P][ps]), fids, gold) for P in range(pt.n + 1)]
    return m_src, m_dst, curve, rec


def integrity_checks(model, pt, exp, src, dst, fids, gold, m_src, m_dst, rec, extra):
    """(no-patch delta, integrity delta, new Patcher): hooks without a patch reproduce M_dst; E-P2 readout at P = N
    reproduces M_src; E-P1 all text pieces at P = 0 reproduce M_src."""
    pt.remove()
    plain = E.margin(E.last_logits(model, dst), fids, gold)
    pt = E.Patcher(model)
    P, s_pos, d_pos = extra
    P = pt.n if P is None else P
    m = E.margin(E.run_patched(model, pt, dst, P, d_pos, rec[P][s_pos]), fids, gold)
    return abs(plain - m_dst), abs(m - m_src), pt


def do_pilot() -> int:
    import torch
    from shattered.gpuguard import wait_gpu_free
    from shattered.interp.load import load
    m = E.PILOT_MODEL
    by_id = E.items_by_id()["sib"]
    used = wait_gpu_free()
    model, tok = load(m, "cuda")
    pt = E.Patcher(model)
    V = nc1.Vocab(tok)
    out = {"model": m, "gpu_mb_before_load": used, "n_points": pt.n + 1}
    for exp in (1, 2):
        S, L = stored(exp, m), E.item_lists(exp)[(m, "sib")]
        old = L["primary"][:5] + L["control"][:5]
        new_pool = sorted(i for i in by_id if i not in S)
        new = [new_pool[k] for k in np.random.default_rng(SEED).choice(len(new_pool), 10, replace=False)]
        elig = [i for i in by_id if pair(exp, V if exp == 1 else None, tok, m, by_id[i])[5]]
        rows, times, worst_np, worst_int = [], [], 0.0, 0.0
        for k, i in enumerate(old + new):
            it, gold = by_id[i], int(by_id[i]["label"])
            src, dst, ps, pd_, fids, ok, extra = pair(exp, V if exp == 1 else None, tok, m, it)
            torch.cuda.synchronize()
            t0 = time.time()
            m_src, m_dst, curve, rec = item_curve(model, pt, exp, src, dst, ps, pd_, fids, gold)
            torch.cuda.synchronize()
            times.append(time.time() - t0)
            if k < 3:
                d_np, d_int, pt = integrity_checks(model, pt, exp, src, dst, fids, gold, m_src, m_dst, rec, extra)
                worst_np, worst_int = max(worst_np, d_np), max(worst_int, d_int)
            r = {"id": i, "stored": i in S, "eligible": ok}
            if i in S:
                s = S[i]
                r["max_abs_delta_vs_stored"] = float(max(abs(m_src - s["m_src"]), abs(m_dst - s["m_dst"]),
                                                         *np.abs(np.array(curve) - np.array(s[SCHEME[exp]]))))
            rows.append(r)
        rep = [r["max_abs_delta_vs_stored"] for r in rows if r["stored"]]
        n_new = {mm: 1004 - len(stored(exp, mm)) for mm in E.MODELS}
        out[f"E-P{exp}"] = {
            "eligible_of_1004": len(elig), "stored_items_reproduced": f"{sum(d < TOL for d in rep)}/{len(rep)}",
            "max_abs_delta_vs_stored": max(rep), "no_patch_max_abs_delta": worst_np,
            "integrity_max_abs_delta": worst_int, "new_items_eligible": f"{sum(r['eligible'] for r in rows if not r['stored'])}/10",
            "seconds_per_item_qwen3.5": float(np.mean(times)), "new_items_to_run": n_new, "rows": rows}
    pt.remove()
    # extrapolation: seconds per item scale with the number of points; Qwen3.5 speed for every model (caveat)
    pts = {mm: json.load(open(E.OUT[1] / "raw" / f"{mm}.json"))["meta"]["n_points"] for mm in E.MODELS}
    est = sum(out[f"E-P{e}"]["seconds_per_item_qwen3.5"] / (pt.n + 1) * pts[mm] * out[f"E-P{e}"]["new_items_to_run"][mm]
              for e in (1, 2) for mm in E.MODELS) / 3600
    out["points_per_model"], out["estimate_hours_at_qwen3.5_speed"] = pts, est
    ok = all(out[f"E-P{e}"]["max_abs_delta_vs_stored"] < TOL and out[f"E-P{e}"]["no_patch_max_abs_delta"] < TOL
             and out[f"E-P{e}"]["integrity_max_abs_delta"] < TOL for e in (1, 2))
    out["all_passed"] = ok
    write_json(OUT / "pilot.json", out, {"registered": REGISTERED, "status": "pilot; no R computed"})
    print(json.dumps({k: ({kk: vv for kk, vv in v.items() if kk != "rows"} if isinstance(v, dict) else v)
                      for k, v in out.items()}, indent=1), flush=True)
    return 0 if ok else 1


def do_run(exp: int, m: str) -> int:
    from shattered.gpuguard import wait_gpu_free
    from shattered.interp.load import load
    RAW.mkdir(parents=True, exist_ok=True)
    final, part = RAW / f"ep{exp}_{m}.json", RAW / f"ep{exp}_{m}.partial.json"
    if final.exists():
        return 0
    by_id, S = E.items_by_id()["sib"], stored(exp, m)
    todo = sorted(i for i in by_id if i not in S)
    done = {r["id"]: r for r in json.load(open(part))["rows"]} if part.exists() else {}
    excluded = json.load(open(part))["excluded"] if part.exists() else []
    used = wait_gpu_free()
    t0 = time.time()
    model, tok = load(m, "cuda")
    pt = E.Patcher(model)
    V = nc1.Vocab(tok) if exp == 1 else None
    meta = {"model": m, "experiment": f"E-P{exp}", "scheme": SCHEME[exp], "n_layers": pt.n, "n_points": pt.n + 1,
            "gpu_mb_before_load": used, "libraries": E.lib_versions(), "load_seconds": time.time() - t0,
            "n_reused_from_registered_run": len(S)}
    print(json.dumps(meta), flush=True)
    worst = {"no_patch": 0.0, "integrity": 0.0}
    n_checked = 0

    def flush():
        tmp = tmp_path(part)
        tmp.write_text(json.dumps({"meta": meta, "rows": list(done.values()), "excluded": excluded}), encoding="utf-8")
        commit(tmp, part)

    t1 = time.time()
    for i in todo:
        if i in done or i in excluded:
            continue
        it, gold = by_id[i], int(by_id[i]["label"])
        src, dst, ps, pd_, fids, ok, extra = pair(exp, V, tok, m, it)
        if not ok:
            excluded.append(i)
            continue
        assert len(set(fids)) == len(fids), "verbalizer first tokens not distinct"
        m_src, m_dst, curve, rec = item_curve(model, pt, exp, src, dst, ps, pd_, fids, gold)
        if n_checked < 3:
            d_np, d_int, pt = integrity_checks(model, pt, exp, src, dst, fids, gold, m_src, m_dst, rec, extra)
            worst["no_patch"], worst["integrity"] = max(worst["no_patch"], d_np), max(worst["integrity"], d_int)
            n_checked += 1
            if d_np >= TOL or (d_int >= TOL and not (exp == 1 and m == "gemma4-e2b")):
                flush()
                print(f"CHECK FAILED: {worst}", flush=True)
                return 1
        done[i] = {"id": i, "m_src": m_src, "m_dst": m_dst, SCHEME[exp]: curve}
        if len(done) % 25 == 0:
            flush()
            print(f"{m} E-P{exp}: {len(done)}/{len(todo)} items, {time.time() - t1:.0f}s", flush=True)
    pt.remove()
    meta.update({"run_seconds": time.time() - t1, "n_items_run": len(done), "excluded_ineligible": excluded,
                 "max_abs_no_patch_delta": worst["no_patch"], "max_abs_integrity_delta": worst["integrity"]})
    write_json(final, {"meta": meta, "rows": list(done.values())}, {"registered": REGISTERED})
    part.unlink(missing_ok=True)
    print(json.dumps({k: v for k, v in meta.items() if k != "excluded_ineligible"}), flush=True)
    return 0


# ---------------------------------------------------------------- analysis

def boot_w(n: int) -> np.ndarray:
    return np.random.default_rng(SEED).multinomial(n, np.full(n, 1 / n), size=N_BOOT).astype(np.float64)


def ratio_sums(num: np.ndarray, den: np.ndarray, W: np.ndarray) -> dict:
    """num, den: per-item sums. R = sum(num) / sum(den), bootstrap CI over items."""
    r = num.sum() / den.sum()
    bs = (W @ num) / (W @ den)
    return {"R": float(r), "lo": float(np.nanpercentile(bs, 2.5)), "hi": float(np.nanpercentile(bs, 97.5))}


def median_item(num: np.ndarray, den: np.ndarray) -> dict:
    keep = den >= GAP_MIN
    x = num[keep] / den[keep]
    if not len(x):
        return {"median": None, "lo": None, "hi": None, "n": 0}
    idx = np.random.default_rng(SEED).integers(0, len(x), (N_BOOT, len(x)))
    bs = np.median(x[idx], axis=1)
    return {"median": float(np.median(x)), "lo": float(np.percentile(bs, 2.5)), "hi": float(np.percentile(bs, 97.5)),
            "n": int(keep.sum())}


def do_analyse() -> int:
    rows, gaps = [], []
    for exp in (1, 2):
        s = SCHEME[exp]
        P = json.load(open(E.OUT[exp] / "predictions.json"))["per_model"]
        for m in E.MODELS:
            S = stored(exp, m)
            new = json.load(open(RAW / f"ep{exp}_{m}.json"))
            n = new["meta"]["n_layers"]
            D = pd.DataFrame([{"id": i, "m_src": r["m_src"], "m_dst": r["m_dst"], "curve": r[s]} for i, r in S.items()]
                             + [{"id": r["id"], "m_src": r["m_src"], "m_dst": r["m_dst"], "curve": r[s]}
                                for r in new["rows"]]).set_index("id")
            L = E.item_lists(exp)[(m, "sib")]
            sel, ctrl = set(L["primary"]), set(L["control"])
            group = {"selected": [i for i in D.index if i in sel], "all": list(D.index),
                     "excluded": [i for i in D.index if i not in sel],
                     "excluded: control": [i for i in D.index if i in ctrl],
                     "excluded: other": [i for i in D.index if i not in sel and i not in ctrl]}
            bands = {f"L* = {P[m]['L_star']}": [P[m]["L_star"]], "early": list(range(0, n // 3)),
                     "middle": list(range(n // 3, 2 * n // 3)), "late": list(range(2 * n // 3, n + 1))}
            for gname, ids in group.items():
                g = D.loc[ids]
                gap = (g.m_src - g.m_dst).to_numpy(float)
                X = np.stack(g.curve.to_numpy()).astype(float) - g.m_dst.to_numpy(float)[:, None]
                gaps.append({"experiment": f"E-P{exp}", "model": m, "set": gname, "n": len(g),
                             "gap_negative": int((gap < 0).sum()), "gap_near_0": int(((gap >= 0) & (gap < GAP_MIN)).sum()),
                             "gap_at_least_0.5": int((gap >= GAP_MIN).sum()), "mean_gap": float(gap.mean())})
                W = boot_w(len(g))
                for bname, pts in bands.items():
                    num, den = X[:, pts].sum(1), gap * len(pts)
                    k = gap >= GAP_MIN
                    sens = ratio_sums(num[k], den[k], boot_w(int(k.sum()))) if k.sum() else {"R": None}
                    rows.append({"experiment": f"E-P{exp}", "model": m, "n_layers": n, "band": bname,
                                 "points": f"{pts[0]}-{pts[-1]}", "set": gname, "n": len(g),
                                 **{f"ratio_of_sums_{k2}": v for k2, v in ratio_sums(num, den, W).items()},
                                 **{f"median_item_{k2}": v for k2, v in median_item(num / len(pts), gap).items()},
                                 "ratio_of_sums_gap_ge_0.5": sens["R"]})
            print(f"E-P{exp} {m}: {len(D)} items ({len(S)} reused, {len(new['rows'])} run, "
                  f"{len(new['meta']['excluded_ineligible'])} ineligible)", flush=True)
    T, G = pd.DataFrame(rows), pd.DataFrame(gaps)
    T.to_csv(OUT / "table.csv", index=False)
    G.to_csv(OUT / "gaps.csv", index=False)
    write_json(OUT / "summary.json", {"gaps": gaps}, {"registered": REGISTERED, "status": "exploratory, no verdict",
                                                      "gap_min_for_median": GAP_MIN, "n_boot": N_BOOT})
    pd.set_option("display.width", 250)
    print(T[T.set.isin(["selected", "all", "excluded"])][["experiment", "model", "band", "set", "n",
          "ratio_of_sums_R", "ratio_of_sums_lo", "ratio_of_sums_hi", "median_item_median", "median_item_n"]]
          .round(3).to_string(index=False))
    print(G.to_string(index=False))
    return 0


def do_main() -> int:
    """Main estimates for the paper (the lead author, 2026-10-26): E-P2 = all items; E-P1 = items with gap >= GAP_MIN only (the
    all-items E-P1 ratio of sums is never reported), with the share of items meeting that condition; R at the registered
    L* per model, ratio of sums with a 95% bootstrap CI over items, per-item median (gap >= GAP_MIN)."""
    rows = []
    for exp in (1, 2):
        s = SCHEME[exp]
        P = json.load(open(E.OUT[exp] / "predictions.json"))["per_model"]
        for m in E.MODELS:
            S = stored(exp, m)
            new = json.load(open(RAW / f"ep{exp}_{m}.json"))
            D = pd.DataFrame([{"id": i, "m_src": r["m_src"], "m_dst": r["m_dst"], "curve": r[s]} for i, r in S.items()]
                             + [{"id": r["id"], "m_src": r["m_src"], "m_dst": r["m_dst"], "curve": r[s]}
                                for r in new["rows"]]).set_index("id")
            sel = set(E.item_lists(exp)[(m, "sib")]["primary"])
            L = P[m]["L_star"]
            gap = (D.m_src - D.m_dst).to_numpy(float)
            X = np.stack(D.curve.to_numpy()).astype(float)[:, L] - D.m_dst.to_numpy(float)
            big = gap >= GAP_MIN
            in_sel = D.index.isin(sel)
            for name, k in (("all items", np.ones(len(D), bool)), ("gap >= 0.5", big), ("selected (as run)", in_sel)):
                r = ratio_sums(X[k], gap[k], boot_w(int(k.sum())))
                med = median_item(X[k], gap[k])
                rows.append({"experiment": f"E-P{exp}", "model": m, "L_star": L, "set": name, "n": int(k.sum()),
                             "share_of_1004": float(k.sum() / len(D)), "R": r["R"], "lo": r["lo"], "hi": r["hi"],
                             "median_item_R": med["median"], "median_n": med["n"],
                             "n_gap_ge_0.5": int(big.sum()), "share_gap_ge_0.5": float(big.mean()),
                             "n_gap_lt_0.5": int((~big).sum()), "n_gap_negative": int((gap < 0).sum())})
    T = pd.DataFrame(rows)
    T.to_csv(OUT / "main_estimates.csv", index=False)
    pd.set_option("display.width", 250)
    print(T.round(3).to_string(index=False))
    return 0


if __name__ == "__main__":
    step = sys.argv[1]
    sys.exit({"pilot": do_pilot, "run": lambda: do_run(int(sys.argv[2]), sys.argv[3]),
              "analyse": do_analyse, "main": do_main}[step]() or 0)
