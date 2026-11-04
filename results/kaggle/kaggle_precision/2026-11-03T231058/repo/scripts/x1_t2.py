"""X1: second prompt template (T2) on Kannada accuracy. Registered in RESULTS.md ("PHASE 2 PRE-REGISTRATION (2026-11-01)", X1).

Scores every Phase 1 accuracy cell again with the T2 templates (src/shattered/llm/templates/e0_*_v2.txt): 5 models x forms
english, native, itrans, lower (E9 universal|lower), lossy, natural (sentiment 198, XNLI 193, SIB natural257) and the NC1 forced
tokenizations a (canonical), b = NC-F condition, c = NC-O condition, with the Phase 1 seeded segmentations. Everything else is
the Phase 1 code path: items from l_ladder.e0b_items / e0c_items / sib257_items, e0b content-free calibration and scoring loop,
nc1.prompt_conditions / choice_logprobs_ids. Only the template version differs (e0b.build_prompt and nc1.build_with_spans are
patched here, nothing in the Phase 1 scripts is edited).

Usage: python scripts/x1_t2.py pilot    (GPU, Gemma 4 E2B; 20 items per task; timing only, no accuracy is computed or printed)
       python scripts/x1_t2.py score    (GPU: all models; resumable per model x form)
       python scripts/x1_t2.py analyse  (CPU: T-a, T-b, T-c; see analyse())
Outputs: results/phase2/x1/t2/{scores_e0b,scores_e0c,scores_nc}/ ; analysis files under results/phase2/x1/t2/.
"""
import json
import os
import string
import sys
import time
from functools import partial

import numpy as np
import pandas as pd

from shattered.runlog import REPO, commit, results_dir, tmp_path, write_json

sys.path.insert(0, str(REPO / "scripts"))
import e0b_familiarity as e0b  # noqa: E402
import l_ladder as lad  # noqa: E402
import nc1  # noqa: E402
from shattered.eval import loglik  # noqa: E402

VERSION = os.environ.get("X1_TEMPLATE", "v2")  # "v3" = T3 (Kannada instruction, native-speaker verified, exploratory): same code path, outputs under results/phase2/x1/t3
assert VERSION in ("v2", "v3")
ROOT = REPO / "results" / "phase2" / "x1" / ("t2" if VERSION == "v2" else "t3")
T3_LABEL = "instruction verified by a native speaker, exploratory"
D_B, D_C, D_NC = ROOT / "scores_e0b", ROOT / "scores_e0c", ROOT / "scores_nc"
MODELS = lad.ACC_MODELS  # qwen2.5-1.5b, qwen3.5-2b, sarvam-1, gemma4-e2b, qwen3-1.7b
FORMS_B = ["english", "native", "itrans", "lower", "lossy", "natural"]
FORMS_C = ["english", "native", "itrans", "lower", "lossy"]
CONDS = nc1.CONDITIONS

# ---- the only change to the Phase 1 code path: the template version
e0b.build_prompt = partial(loglik.build_prompt, version=VERSION)


def build_with_spans_t2(task: str, fields: dict):
    tpl = (loglik.TEMPLATES / f"e0_{task}_{VERSION}.txt").read_text(encoding="utf-8")
    out, spans = "", {}
    for lit, name, _, _ in string.Formatter().parse(tpl):
        out += lit
        if name is not None:
            assert name not in spans, "field used twice"
            spans[name] = (len(out), len(out) + len(fields[name]))
            out += fields[name]
    assert out == loglik.build_prompt(task, fields, VERSION)
    return out, spans


nc1.build_with_spans = build_with_spans_t2


def items_all(limit: int | None = None):
    a, c, s = lad.e0b_items(), lad.e0c_items(), lad.sib257_items()
    if limit:
        a = {t: its[:limit] for t, its in a.items()}
        c = {t: its[:limit] for t, its in c.items()}
        s = {t: its[:limit] for t, its in s.items()}
    return a, c, s


def score_forms(model, tok, name: str, items: dict, forms: list[str], score_dir) -> dict:
    """The body of e0b.score_model, for a model that is already loaded. Returns seconds per (form)."""
    from shattered.eval.loglik import VERBALIZERS, choice_logprobs
    score_dir.mkdir(parents=True, exist_ok=True)
    todo = [f for f in forms if not (score_dir / f"{name}__{f}.parquet").exists()]
    cf = e0b.content_free(name, items, score_dir, model, tok)["N/A"]  # as e0b.score_model: per-task N/A log-probs (the primary
    # avg3 calibration is applied from cf_<model>.json at analysis time)
    secs = {}
    for f in todo:
        t1, rows, fert = time.time(), [], []
        for t, its in items.items():
            for it in its:
                if f == "natural" and it.get("natural_defective"):
                    continue
                lp, n_tok = choice_logprobs(model, tok, e0b.build_prompt(t, it["forms"][f]), VERBALIZERS[t])
                cal = np.asarray(lp) - np.asarray(cf[t])
                rows.append({"model": name, "task": t, "form": f, "id": it["id"], "label": it["label"],
                             "logprobs": lp, "logprobs_cal": cal.tolist(), "pred_raw": int(np.argmax(lp)),
                             "pred_cal": int(np.argmax(cal)), "prompt_tokens": n_tok})
            texts = [v for it in its if not (f == "natural" and it.get("natural_defective")) for v in it["forms"][f].values()]
            ntok = sum(len(x) for x in tok(texts, add_special_tokens=False)["input_ids"])
            fert.append({"model": name, "task": t, "form": f, "n_texts": len(texts),
                         "tokens_per_word": ntok / sum(len(x.split()) for x in texts)})
        meta_path, pq_path = score_dir / f"{name}__{f}.json", score_dir / f"{name}__{f}.parquet"
        tmp_path(meta_path).write_text(json.dumps({"content_free_logprobs": cf, "fertility": fert, "seconds": time.time() - t1,
                                                   "template": VERSION}, indent=1), encoding="utf-8")
        commit(tmp_path(meta_path), meta_path)
        pd.DataFrame(rows).to_parquet(tmp_path(pq_path))
        commit(tmp_path(pq_path), pq_path)
        secs[f] = (time.time() - t1, len(rows))
        print(f"{name}/{f}: {len(rows)} items in {time.time() - t1:.0f}s", flush=True)
    return secs


def score_nc(model, tok, name: str, groups: list, score_dir, check_ids: bool = False) -> dict:
    """NC1 conditions a/b/c with T2 prompts. groups = [(task, items)]. One parquet per model x condition x group (as nc1)."""
    from shattered.eval.loglik import VERBALIZERS
    score_dir.mkdir(parents=True, exist_ok=True)
    todo = [c for c in CONDS if not all((score_dir / f"{name}__nc_{c}__{g}.parquet").exists() for g in nc1.GROUPS)]
    if not todo:
        return {}
    V = nc1.Vocab(tok)
    rows = {c: [] for c in todo}
    t0, secs = time.time(), {}
    for t, its in groups:
        t1 = time.time()
        for it in its:
            P = nc1.prompt_conditions(V, name, it["id"], t, it["forms"]["lossy"], it["forms"]["lower"])
            if check_ids:  # the forced pieces must equal Phase 1's (same seeds, same field text, same prefix before the field)
                nc1.build_with_spans = lambda task, fields: _v1_spans(task, fields)
                P1 = nc1.prompt_conditions(V, name, it["id"], t, it["forms"]["lossy"], it["forms"]["lower"])
                nc1.build_with_spans = build_with_spans_t2
                for c in CONDS:
                    assert [u["pieces"] for u in P[c][1]] == [u["pieces"] for u in P1[c][1]], ("T2 pieces differ from T1", it["id"], c)
            for c in todo:
                lp = nc1.choice_logprobs_ids(model, tok, P["prompt"], P[c][0], VERBALIZERS[t])
                rows[c].append({"model": name, "task": t, "form": f"nc_{c}", "id": it["id"], "label": it["label"],
                                "logprobs": lp, "pred_raw": int(np.argmax(lp)), "prompt_tokens": len(P[c][0])})
        secs[t] = (time.time() - t1, len(its) * len(todo))
        print(f"{name}: NC {t} done ({time.time() - t0:.0f}s)", flush=True)
    for c in todo:
        df = pd.DataFrame(rows[c])
        for g, tasks_g in nc1.GROUPS.items():
            path = score_dir / f"{name}__nc_{c}__{g}.parquet"
            df[df.task.isin(tasks_g)].to_parquet(tmp_path(path))
            commit(tmp_path(path), path)
    return secs


def _v1_spans(task: str, fields: dict):
    tpl = (loglik.TEMPLATES / f"e0_{task}_v1.txt").read_text(encoding="utf-8")
    out, spans = "", {}
    for lit, name, _, _ in string.Formatter().parse(tpl):
        out += lit
        if name is not None:
            spans[name] = (len(out), len(out) + len(fields[name]))
            out += fields[name]
    return out, spans


def do_pilot() -> None:
    """Timing only: Gemma 4 E2B (the slowest model), 20 items per task, forms english + lossy + NC (a, b, c). Throwaway dir,
    no accuracy or prediction is computed, printed or kept."""
    import shutil

    import torch

    from shattered.interp.load import load
    from shattered.eval.loglik import VERBALIZERS, choice_logprobs
    a, c, s = items_all(20)
    t0 = time.time()
    model, tok = load("gemma4-e2b", "cuda")
    print(f"load {time.time() - t0:.0f}s", flush=True)
    res = {"load_s": time.time() - t0}
    for t, its in list(a.items()) + list(c.items()):
        t1 = time.time()
        for it in its:
            choice_logprobs(model, tok, e0b.build_prompt(t, it["forms"]["lossy"]), VERBALIZERS[t])
        res[f"{t}_per_prompt_s"] = (time.time() - t1) / len(its)
    V = nc1.Vocab(tok)
    for t, its in list(a.items()) + list(c.items()):
        t1 = time.time()
        for it in its[:10]:
            P = nc1.prompt_conditions(V, "gemma4-e2b", it["id"], t, it["forms"]["lossy"], it["forms"]["lower"])
            nc1.choice_logprobs_ids(model, tok, P["prompt"], P["b"][0], VERBALIZERS[t])
        res[f"{t}_nc_per_prompt_s"] = (time.time() - t1) / 10
    # T2 field pieces equal T1 pieces (identical forced token ids for the text fields)
    for t, its in list(a.items()) + list(c.items()):
        for it in its[:10]:
            P2 = nc1.prompt_conditions(V, "gemma4-e2b", it["id"], t, it["forms"]["lossy"], it["forms"]["lower"])
            saved = nc1.build_with_spans
            nc1.build_with_spans = _v1_spans
            P1 = nc1.prompt_conditions(V, "gemma4-e2b", it["id"], t, it["forms"]["lossy"], it["forms"]["lower"])
            nc1.build_with_spans = saved
            for cnd in CONDS:
                assert [u["pieces"] for u in P2[cnd][1]] == [u["pieces"] for u in P1[cnd][1]], (t, it["id"], cnd)
    res["nc_pieces_identical_t1_t2_checked_items"] = 30
    out = REPO / "results" / "phase2" / "x1" / "pilot_timing.json"
    write_json(out, res, {"model": "gemma4-e2b", "items_per_task": 20, "template": VERSION, "note": "timing only; no accuracy computed"})
    print(json.dumps(res, indent=1), flush=True)
    del model
    torch.cuda.empty_cache()
    shutil.rmtree(ROOT / "pilot_tmp", ignore_errors=True)


def do_score(models: list[str] | None = None) -> None:
    if VERSION == "v3":
        t = json.loads((REPO / "results" / "phase2" / "x1" / "t3_templates.json").read_text(encoding="utf-8"))
        assert t.get("verified_by_native_speaker") is True, "T3 instruction is not verified"
        ROOT.mkdir(parents=True, exist_ok=True)
        (ROOT / "LABEL.txt").write_text(T3_LABEL + chr(10), encoding="utf-8")  # every T3 result carries this label
    import torch

    from shattered.interp.load import load
    a, c, s = items_all()
    print(f"items: sentiment {len(a['sentiment'])}, xnli {len(a['xnli'])}, sib {len(c['sib'])}, sib257 {len(s['sib'])}", flush=True)
    groups = [("sentiment", a["sentiment"]), ("xnli", a["xnli"]), ("sib", c["sib"])]
    for m in (models or MODELS):
        done_b = all((D_B / f"{m}__{f}.parquet").exists() for f in FORMS_B)
        done_c = all((D_C / f"{m}__{f}.parquet").exists() for f in FORMS_C + ["natural257"])
        done_n = all((D_NC / f"{m}__nc_{cc}__{g}.parquet").exists() for cc in CONDS for g in nc1.GROUPS)
        if done_b and done_c and done_n:
            continue
        t0 = time.time()
        model, tok = load(m, "cuda")
        print(f"{m}: loaded in {time.time() - t0:.0f}s", flush=True)
        score_forms(model, tok, m, a, FORMS_B, D_B)
        score_forms(model, tok, m, c, FORMS_C, D_C)
        score_forms(model, tok, m, s, ["natural257"], D_C)
        score_nc(model, tok, m, groups, D_NC, check_ids=(m == "sarvam-1"))
        print(f"{m}: finished in {time.time() - t0:.0f}s", flush=True)
        del model
        torch.cuda.empty_cache()


if __name__ == "__main__":
    if sys.argv[1] == "pilot":
        do_pilot()
    elif sys.argv[1] == "score":
        do_score(sys.argv[2:] or None)
