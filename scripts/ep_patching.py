"""E-P1 / E-P2 activation patching (pre-registered in RESULTS.md, 2026-10-23 16:00 IST, before this script was written).

E-P1: NC1 (a) canonical -> (c) non-canonical at the canonical count (same lossy text, positions align exactly);
      schemes "final" (each text word's last piece) and "all" (every piece of every text word).
E-P2: native -> lossy, aligned by word; schemes "word" (word k's last piece <- native word k's last piece) and "read"
      (final prompt position only).
Patch points: P = 0..N for a model with N decoder layers. Point P < N is the residual stream entering decoder layer P
(P = 0: the embedding output); point P = N is the final residual stream after the last layer, before the final norm
(the registration's "L = N+1" in E-P2). Gold margin M: next-token logits at the final prompt position, gold
verbalizer's first token minus the largest other verbalizer's first token.

Usage: python scripts/ep_patching.py items          (CPU: item lists vs the registered counts; first-token
                                                     distinctness for 4 tokenizers; SIB word-count alignment)
       python scripts/ep_patching.py pilot1         (GPU, Qwen3.5-2B, 10 SIB primary items; checks + timing only)
       python scripts/ep_patching.py pilot2         (GPU, Qwen3.5-2B, 10 SIB primary items; checks + timing only)
Pilots compute no recovery value. Outputs: results/ep1/{items.json, pilot.json}, results/ep2/{items.json, pilot.json}
"""
import json
import sys
import time

import numpy as np
import pandas as pd

from shattered.runlog import REPO, results_dir, write_json

sys.path.insert(0, str(REPO / "scripts"))
import e0b_familiarity as e0b  # noqa: E402
import l_ladder as lad  # noqa: E402
import nc1  # noqa: E402

MODELS = lad.COUNT_ACC  # qwen3-1.7b, qwen3.5-2b, sarvam-1, gemma4-e2b
OUT = {1: results_dir("ep1"), 2: results_dir("ep2")}
CAP, SEED, PILOT_MODEL, PILOT_N, TOL = 200, 0, "qwen3.5-2b", 10, 0.05
REGISTERED = {  # (primary, control) from the registration
    1: {("qwen3-1.7b", "sib"): (73, 70), ("qwen3.5-2b", "sib"): (117, 52), ("sarvam-1", "sib"): (222, 51),
        ("gemma4-e2b", "sib"): (133, 59), ("qwen3-1.7b", "sentiment"): (23, 29), ("qwen3.5-2b", "sentiment"): (31, 10),
        ("sarvam-1", "sentiment"): (39, 8), ("gemma4-e2b", "sentiment"): (18, 7)},
    2: {("qwen3-1.7b", "sib"): (398, 31), ("qwen3.5-2b", "sib"): (345, 43), ("sarvam-1", "sib"): (126, 65),
        ("gemma4-e2b", "sib"): (293, 39), ("qwen3-1.7b", "sentiment"): (69, 16), ("qwen3.5-2b", "sentiment"): (27, 16),
        ("sarvam-1", "sentiment"): (16, 4), ("gemma4-e2b", "sentiment"): (41, 2)},
}


# ---------------------------------------------------------------- items

def correctness(exp: int) -> pd.DataFrame:
    """Per-item calibrated correctness in the two forms of the experiment (stored scores; English rows decide the raw
    fallback, as in NC1 and the ladder)."""
    src, dst = ("nc_a", "nc_c") if exp == 1 else ("native", "lossy")
    out = []
    for d, grp, task in ((lad.E0B_DIR, "e0b", "sentiment"), (lad.E0C_DIR, "e0c", "sib")):
        cf = {m: json.load(open(d / f"cf_{m}.json")) for m in lad.ACC_MODELS}
        files = [d / f"{m}__english.parquet" for m in lad.ACC_MODELS]
        files += ([nc1.SCORES / f"{m}__{f}__{grp}.parquet" for m in lad.ACC_MODELS for f in (src, dst)] if exp == 1
                  else [d / f"{m}__{f}.parquet" for m in lad.ACC_MODELS for f in (src, dst)])
        B = pd.concat([pd.read_parquet(f) for f in files], ignore_index=True)
        B, _ = e0b.apply_calibration(B[B.task == task], cf)
        B = B[B.model.isin(MODELS) & B.form.isin([src, dst])]
        B["correct"] = B.pred_cal == B.label
        out.append(B.pivot_table(index=["model", "task", "id"], columns="form", values="correct").reset_index()
                   .rename(columns={src: "src", dst: "dst"}))
    return pd.concat(out, ignore_index=True)


def item_lists(exp: int) -> dict:
    """{(model, task): {"primary": ids, "control": ids}}; primary SIB capped at 200 (random, seed 0), in that order."""
    C = correctness(exp)
    out = {}
    for (m, t), g in C.groupby(["model", "task"]):
        prim = sorted(g[(g.src == 1) & (g.dst == 0)].id.tolist())
        ctrl = sorted(g[(g.src == 0) & (g.dst == 1)].id.tolist())
        assert (len(prim), len(ctrl)) == REGISTERED[exp][(m, t)], (exp, m, t, len(prim), len(ctrl))
        order = [prim[i] for i in np.random.default_rng(SEED).permutation(len(prim))]
        out[(m, t)] = {"primary": order[:CAP] if t == "sib" else order, "control": ctrl,
                       "n_primary_available": len(prim)}
    return out


def items_by_id() -> dict:
    a, c = lad.e0b_items(), lad.e0c_items()
    return {"sentiment": {it["id"]: it for it in a["sentiment"]}, "sib": {it["id"]: it for it in c["sib"]}}


# ---------------------------------------------------------------- prompts, positions

def first_ids(tok, prompt: str, choices: list[str]) -> list[int]:
    """First continuation token of each verbalizer, computed exactly as nc1.choice_logprobs_ids."""
    from shattered.eval.loglik import _prefix
    bos = _prefix(tok)
    p_can = bos + tok(prompt, add_special_tokens=False)["input_ids"]
    out = []
    for c in choices:
        full = bos + tok(prompt + c, add_special_tokens=False)["input_ids"]
        cont = full[len(p_can):] if full[: len(p_can)] == p_can else tok(c, add_special_tokens=False)["input_ids"]
        out.append(cont[0])
    return out


def word_units(tok, task: str, fields: dict) -> tuple[str, list[int], list[list[int]]]:
    """(prompt, canonical ids, one list of positions per text word, all fields in prompt order)."""
    prompt, spans = nc1.build_with_spans(task, fields)
    enc = tok(prompt, return_offsets_mapping=True, add_special_tokens=False)
    groups = []
    for key in sorted(fields, key=lambda k: spans[k][0]):
        groups += nc1.units(tok, enc["input_ids"], enc["offset_mapping"], spans[key], prompt)
    return prompt, enc["input_ids"], groups


def ep1_pair(V, tok, m: str, task: str, it: dict) -> dict:
    """(a) and (c) ids (with BOS), word groups (positions in the BOS-prefixed sequence) and checks."""
    from shattered.eval.loglik import _prefix
    bos = _prefix(tok)
    P = nc1.prompt_conditions(V, m, it["id"], task, it["forms"]["lossy"], it["forms"]["lower"])
    prompt, can, groups = word_units(tok, task, it["forms"]["lossy"])
    a, c = P["a"][0], P["c"][0]
    info_c = P["c"][1]
    ok_len = len(a) == len(c) == len(can) and a == can and len(info_c) == len(groups) and all(
        u["k_new"] == len(g) for u, g in zip(info_c, groups))
    words_ok = ok_len and all(tok.decode([a[p] for p in g]) == tok.decode([c[p] for p in g]) for g in groups)
    off = len(bos)
    return {"a": bos + a, "c": bos + c, "groups": [[p + off for p in g] for g in groups], "prompt": prompt,
            "aligned": ok_len, "words_match": words_ok}


def ep2_pair(tok, task: str, it: dict) -> dict:
    from shattered.eval.loglik import _prefix
    bos = _prefix(tok)
    pn, idn, gn = word_units(tok, task, it["forms"]["native"])
    pl, idl, gl = word_units(tok, task, it["forms"]["lossy"])
    nat_words = [w for k in sorted(it["forms"]["native"]) for w in it["forms"]["native"][k].split()]
    los_words = [w for k in sorted(it["forms"]["lossy"]) for w in it["forms"]["lossy"][k].split()]
    same_count = len(gn) == len(gl) == len(nat_words) == len(los_words)
    dec_ok = same_count and all(tok.decode([idn[p] for p in g]).strip() == w for g, w in zip(gn, nat_words)) and all(
        tok.decode([idl[p] for p in g]).strip() == w for g, w in zip(gl, los_words))
    off = len(bos)
    return {"native": bos + idn, "lossy": bos + idl, "prompt_native": pn, "prompt_lossy": pl,
            "last_native": [g[-1] + off for g in gn], "last_lossy": [g[-1] + off for g in gl],
            "same_word_count": same_count, "words_decode": dec_ok}


# ---------------------------------------------------------------- hooks

class Patcher:
    """Pre-hooks on every decoder layer and on the final norm: point P < N = input of layer P, P = N = norm input."""

    def __init__(self, model):
        inner = model.model
        self.points = list(inner.layers) + [inner.norm]
        self.n = len(self.points) - 1
        self.record, self.patch = None, None
        self.handles = [mod.register_forward_pre_hook(self._make(P), with_kwargs=True)
                        for P, mod in enumerate(self.points)]

    def _make(self, P: int):
        def hook(mod, args, kwargs):
            pos_arg = len(args) > 0
            h = args[0] if pos_arg else kwargs["hidden_states"]
            if self.record is not None:
                self.record[P] = h[0].detach().clone()
            if self.patch is not None and self.patch[0] == P:
                _, pos, val = self.patch
                h = h.clone()
                h[0, pos] = val.to(h.dtype)
                if pos_arg:
                    return (h,) + tuple(args[1:]), kwargs
                kwargs["hidden_states"] = h
                return args, kwargs
            return None
        return hook

    def remove(self) -> None:
        for h in self.handles:
            h.remove()


def last_logits(model, ids: list[int]):
    import torch
    with torch.no_grad():
        return model(input_ids=torch.tensor([ids], device=model.device), use_cache=False,
                     logits_to_keep=1).logits[0, -1].float()


def margin(logits, fids: list[int], gold: int) -> float:
    v = logits[fids]
    return float(v[gold] - torch_max_other(v, gold))


def torch_max_other(v, gold: int):
    import torch
    mask = torch.ones_like(v, dtype=torch.bool)
    mask[gold] = False
    return v[mask].max()


def run_source(model, pt: Patcher, ids: list[int]) -> tuple:
    pt.record = {}
    lg = last_logits(model, ids)
    rec, pt.record = pt.record, None
    return lg, rec


def run_patched(model, pt: Patcher, ids: list[int], P: int, pos: list[int], val) -> object:
    import torch
    pt.patch = (P, torch.tensor(pos, device=model.device), val)
    try:
        return last_logits(model, ids)
    finally:
        pt.patch = None


# ---------------------------------------------------------------- steps

def do_items() -> int:
    from shattered.eval.loglik import VERBALIZERS
    from shattered.interp.load import MODELS as HF
    from transformers import AutoTokenizer
    by_id = items_by_id()
    rep = {}
    for exp in (1, 2):
        L = item_lists(exp)
        write_json(OUT[exp] / "items.json", {f"{m}|{t}": v for (m, t), v in L.items()},
                   {"registered": "RESULTS.md 2026-10-23 16:00 IST", "cap_primary_sib": CAP, "seed": SEED})
        rep[f"E-P{exp}"] = {f"{m}|{t}": [len(v["primary"]), len(v["control"])] for (m, t), v in L.items()}
    distinct = {}
    for m in MODELS:
        tok = AutoTokenizer.from_pretrained(HF[m])
        bad = 0
        for t in ("sentiment", "sib"):
            for it in by_id[t].values():
                for form in ("native", "lossy"):
                    f = first_ids(tok, nc1.build_with_spans(t, it["forms"][form])[0], VERBALIZERS[t])
                    bad += len(set(f)) != len(f)
        distinct[m] = {"items_x_forms_with_shared_first_token": bad}
    sib_words = sum(len(it["forms"]["native"]["text"].split()) != len(it["forms"]["lossy"]["text"].split())
                    for it in by_id["sib"].values())
    rep["first_token_distinct"] = distinct
    rep["sib_word_count_mismatch"] = {"n": sib_words, "of": len(by_id["sib"])}
    write_json(OUT[2] / "alignment_check.json", rep, {})
    print(json.dumps(rep, indent=1), flush=True)
    return 0


def do_pilot(exp: int) -> int:
    import torch
    from shattered.eval.loglik import VERBALIZERS
    from shattered.gpuguard import wait_gpu_free
    from shattered.interp.load import load
    L = item_lists(exp)[(PILOT_MODEL, "sib")]
    ids = L["primary"][:PILOT_N]
    by_id = items_by_id()["sib"]
    used = wait_gpu_free()
    t0 = time.time()
    model, tok = load(PILOT_MODEL, "cuda")
    load_s = time.time() - t0
    pt = Patcher(model)
    V = nc1.Vocab(tok) if exp == 1 else None
    checks, times = [], {}
    for i in ids:
        it = by_id[i]
        gold = int(it["label"])
        if exp == 1:
            pr = ep1_pair(V, tok, PILOT_MODEL, "sib", it)
            fids = first_ids(tok, pr["prompt"], VERBALIZERS["sib"])
            src, dst = pr["a"], pr["c"]
        else:
            pr = ep2_pair(tok, "sib", it)
            fids = first_ids(tok, pr["prompt_native"], VERBALIZERS["sib"])
            assert fids == first_ids(tok, pr["prompt_lossy"], VERBALIZERS["sib"])
            src, dst = pr["native"], pr["lossy"]
        lg_src, rec = run_source(model, pt, src)
        m_src = margin(lg_src, fids, gold)
        pt.remove()
        m_dst_plain = margin(last_logits(model, dst), fids, gold)  # no hooks at all
        pt = Patcher(model)
        m_dst = margin(last_logits(model, dst), fids, gold)        # hooks, no patch
        row = {"id": int(i), "first_tokens_distinct": len(set(fids)) == len(fids),
               "check2_no_patch_reproduces_dst": abs(m_dst - m_dst_plain) < TOL, "check2_delta": m_dst - m_dst_plain}
        if exp == 1:
            text_pos = sorted(p for g in pr["groups"] for p in g)
            m1 = margin(run_patched(model, pt, dst, 0, text_pos, rec[0][text_pos]), fids, gold)
            row.update({"check1_all_text_at_0_reproduces_a": abs(m1 - m_src) < TOL, "check1_delta": m1 - m_src,
                        "check3_aligned": pr["aligned"], "check3_words_match": pr["words_match"]})
            schemes = {"final": [g[-1] for g in pr["groups"]], "all": text_pos}
            pos_src = schemes
        else:
            last_src, last_dst = len(src) - 1, len(dst) - 1
            m1 = margin(run_patched(model, pt, dst, pt.n, [last_dst], rec[pt.n][[last_src]]), fids, gold)
            row.update({"check1_readout_at_final_point_reproduces_native": abs(m1 - m_src) < TOL,
                        "check1_delta": m1 - m_src, "check3_same_word_count": pr["same_word_count"],
                        "check3_words_decode": pr["words_decode"]})
            schemes = {"word": pr["last_lossy"], "read": [last_dst]}
            pos_src = {"word": pr["last_native"], "read": [last_src]}
        for s, pos in schemes.items():  # timing: one patched forward per point (values discarded: no R in a pilot)
            torch.cuda.synchronize()
            t1 = time.time()
            for P in range(pt.n + 1):
                run_patched(model, pt, dst, P, pos, rec[P][pos_src[s]])
            torch.cuda.synchronize()
            times.setdefault(s, []).append((time.time() - t1) / (pt.n + 1))
        row["n_tokens_src"], row["n_tokens_dst"] = len(src), len(dst)
        checks.append(row)
    pt.remove()
    keys = [k for k in checks[0] if k.startswith("check") and not k.endswith("delta")] + ["first_tokens_distinct"]
    passed = {k: int(sum(bool(r[k]) for r in checks)) for k in keys}
    full = item_lists(exp)
    n_items = sum(len(v["primary"]) + len(v["control"]) for v in full.values())
    per_fwd = {s: float(np.mean(v)) for s, v in times.items()}
    est_h = sum(per_fwd.values()) * (pt.n + 1) * n_items / 3600
    out = {"model": PILOT_MODEL, "n_items": len(checks), "n_points": pt.n + 1, "gpu_mb_before_load": used,
           "load_seconds": load_s, "checks_passed_of_10": passed, "all_passed": all(v == len(checks) for v in passed.values()),
           "seconds_per_patched_forward": per_fwd, "items_full_run_all_models": n_items,
           "estimate_hours_full_run_at_pilot_speed": est_h, "rows": checks}
    write_json(OUT[exp] / "pilot.json", out, {"registered": "RESULTS.md 2026-10-23 16:00 IST", "status": "pilot; no R computed"})
    print(json.dumps({k: v for k, v in out.items() if k != "rows"}, indent=1), flush=True)
    return 0 if out["all_passed"] else 1


if __name__ == "__main__":
    step = sys.argv[1]
    sys.exit({"items": do_items, "pilot1": lambda: do_pilot(1), "pilot2": lambda: do_pilot(2)}[step]() or 0)
