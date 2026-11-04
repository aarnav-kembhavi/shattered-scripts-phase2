"""X10 (registered, Amendment 2): generation, FLORES+ devtest Kannada -> English (laptop; pilot first).

Inputs: the 1,012 FLORES+ devtest Kannada sentences in native, ITRANS, lowercase (E9 `universal|lower`), lossy, and natural (the devtest ids that have a clean natural romanization of the Kannada
M4 sample; n reported). One registered instruction, identical for all forms: `Translate this Kannada sentence into English.\\nKannada: {sentence}\\nEnglish:`. Base models, BOS whenever the model has
one (as Phase 1), greedy decoding, max_new_tokens 128, output cut at the first newline; an empty output is scored as empty (share reported per model and form). Models: the four counted accuracy
models (Qwen3-1.7B, Qwen3.5-2B, Sarvam-1, Gemma 4 E2B). Metric: chrF (sacreBLEU chrF2: char order 6, word order 0, beta 2), sentence-level for the paired bootstrap, corpus chrF reported.
Contrasts (Holm over 4 contrasts x 4 models = 16): native - ITRANS, native - lowercase, native - lossy (1,012 sentences), native - natural (the natural subset); paired bootstrap over sentences
(10,000, seed 0), two-sided bootstrap p = 2 x min(P(d* <= 0), P(d* >= 0)) (floor 1/10,001). **X10-P:** native beats ITRANS in at least 3 of 4 models (Holm-significant, positive): SUPPORTED if at least 3 of 4;
PARTLY SUPPORTED if exactly 2; REFUTED if at most 1. The other three contrasts are reported with the same effect rule, no prediction.
Pilot: 20 sentences per model and form, timing and output sanity only (no chrF is used for any decision); the time estimate is reported before the full run.
Usage: python scripts/x10.py pilot | score <model> | analyse     Output: results/phase2/x10/
"""
import json
import sys
import time
from pathlib import Path

import numpy as np
import torch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import l_ladder as lad  # noqa: E402
from m14_full import flores_forms  # noqa: E402

from shattered.interp.load import load  # noqa: E402
from shattered.runlog import REPO, results_dir, write_json  # noqa: E402
from shattered.translit import to_lossy  # noqa: E402

MODELS = ["qwen3-1.7b", "qwen3.5-2b", "sarvam-1", "gemma4-e2b"]
FORMS = ["native", "itrans", "lower", "lossy", "natural"]
INSTR = "Translate this Kannada sentence into English.\nKannada: {s}\nEnglish:"
OUT = results_dir("phase2/x10")
N_DEV = 997  # FLORES+ dev sentences precede devtest in flores_forms(); devtest ids = 997 .. 2008
MAX_NEW = 128
N_BOOT = 10_000


def inputs() -> dict:
    F = flores_forms()
    kn, en = F["native"][N_DEV:], F["english"][N_DEV:]
    assert len(kn) == 1012 and len(en) == 1012
    nat = {}
    for ln in (REPO / "data" / "processed" / "natural_flores_m4_500_v1.jsonl").open(encoding="utf-8"):
        r = json.loads(ln)
        if not r["defective"] and r["index"] >= N_DEV:
            nat[r["index"] - N_DEV] = r["natural"]
    forms = {"native": kn, "itrans": F["itrans"][N_DEV:], "lower": [lad.to_lower(s) for s in kn], "lossy": [to_lossy(s) for s in kn]}
    return {"reference": en, "forms": forms, "natural": nat}


def generate(model, tok, prompts: list[str], batch: int) -> list[str]:
    bos = [tok.bos_token_id] if tok.bos_token_id is not None else []
    pad = tok.pad_token_id if tok.pad_token_id is not None else (tok.eos_token_id or 0)
    outs = []
    for i in range(0, len(prompts), batch):
        ids = [bos + tok(p, add_special_tokens=False)["input_ids"] for p in prompts[i:i + batch]]
        L = max(map(len, ids))
        x = torch.tensor([[pad] * (L - len(s)) + s for s in ids], device=model.device)  # left padding
        m = torch.tensor([[0] * (L - len(s)) + [1] * len(s) for s in ids], device=model.device)
        with torch.no_grad():
            g = model.generate(input_ids=x, attention_mask=m, max_new_tokens=MAX_NEW, do_sample=False, pad_token_id=pad)
        for row in g[:, L:]:
            outs.append(tok.decode(row, skip_special_tokens=True).split("\n")[0].strip())
    return outs


def run_model(name: str, n: int | None, batch: int = 16) -> dict:
    data = inputs()
    model, tok = load(name, "cuda")
    res = {"model": name, "n": n or 1012, "forms": {}}
    for f in FORMS:
        path = OUT / (f"{name}__{f}.json" if n is None else f"pilot_{name}__{f}.json")
        if path.exists():
            res["forms"][f] = json.load(open(path, encoding="utf-8"))["summary"]
            continue
        ids = sorted(data["natural"]) if f == "natural" else list(range(1012))
        if n:
            ids = ids[:n]
        texts = [data["natural"][i] for i in ids] if f == "natural" else [data["forms"][f][i] for i in ids]
        t0 = time.time()
        try:
            outs = generate(model, tok, [INSTR.format(s=t) for t in texts], batch)
        except Exception as e:  # noqa: BLE001 - generate failed for this model: one by one
            print(name, f, "batched generate failed, one by one:", repr(e)[:160], flush=True)
            outs = generate(model, tok, [INSTR.format(s=t) for t in texts], 1)
        secs = time.time() - t0
        summ = {"n": len(ids), "seconds": secs, "seconds_per_sentence": secs / len(ids), "empty_share": float(np.mean([not o for o in outs])), "mean_words": float(np.mean([len(o.split()) for o in outs]))}
        write_json(path, {"summary": summ, "ids": ids, "outputs": outs}, {"model": name, "form": f, "instruction": INSTR, "max_new_tokens": MAX_NEW, "greedy": True})
        res["forms"][f] = summ
        print(name, f, {k: round(v, 3) if isinstance(v, float) else v for k, v in summ.items()}, flush=True)
    del model
    torch.cuda.empty_cache()
    return res


def pilot() -> None:
    allr = {m: run_model(m, 20) for m in MODELS}
    per_sent = {m: np.mean([allr[m]["forms"][f]["seconds_per_sentence"] for f in FORMS]) for m in MODELS}
    est = {m: float(per_sent[m] * (4 * 1012 + 496 // 2) / 3600) for m in MODELS}  # four full forms plus the natural subset (about 250 devtest ids; counted as 248)
    write_json(OUT / "pilot.json", {"models": allr, "seconds_per_sentence_mean": {m: float(v) for m, v in per_sent.items()}, "estimated_full_hours_per_model": est,
                                    "estimated_full_hours_total": float(sum(est.values())), "note": "timing and output sanity only; no chrF is used for any decision"}, {"registration": "RESULTS.md X10 pilot"})
    print("estimated full hours per model", {m: round(v, 2) for m, v in est.items()}, "total", round(sum(est.values()), 2))


def chrf_scores(outs: list[str], refs: list[str]) -> np.ndarray:
    from sacrebleu.metrics import CHRF
    m = CHRF(char_order=6, word_order=0, beta=2)
    return np.array([m.sentence_score(o, [r]).score for o, r in zip(outs, refs)])


def boot_p(d: np.ndarray) -> dict:
    idx = np.random.default_rng(0).integers(0, len(d), (N_BOOT, len(d)))
    b = d[idx].mean(1)
    p = 2 * min((np.sum(b <= 0) + 1) / (N_BOOT + 1), (np.sum(b >= 0) + 1) / (N_BOOT + 1))
    return {"diff": float(d.mean()), "ci95": [float(np.percentile(b, 2.5)), float(np.percentile(b, 97.5))], "p": float(min(p, 1.0))}


def analyse() -> None:
    from statsmodels.stats.multitest import multipletests
    data = inputs()
    refs = data["reference"]
    S, corpus, rows = {}, {}, []
    from sacrebleu.metrics import CHRF
    for m in MODELS:
        for f in FORMS:
            d = json.load(open(OUT / f"{m}__{f}.json", encoding="utf-8"))
            r = [refs[i] for i in d["ids"]]
            S[(m, f)] = dict(zip(d["ids"], chrf_scores(d["outputs"], r)))
            corpus[f"{m}__{f}"] = {"corpus_chrf": CHRF(char_order=6, word_order=0, beta=2).corpus_score(d["outputs"], [r]).score, "empty_share": d["summary"]["empty_share"], "n": d["summary"]["n"]}
    for m in MODELS:
        for f in ("itrans", "lower", "lossy", "natural"):
            ids = sorted(set(S[(m, "native")]) & set(S[(m, f)]))
            dd = np.array([S[(m, "native")][i] - S[(m, f)][i] for i in ids])
            rows.append({"model": m, "contrast": f"native - {f}", "n": len(ids), **boot_p(dd)})
    ph = multipletests([r["p"] for r in rows], method="holm")[1]
    for r, p in zip(rows, ph):
        r["p_holm"], r["significant_positive"] = float(p), bool(p < 0.05 and r["diff"] > 0)
    pos = [r["model"] for r in rows if r["contrast"] == "native - itrans" and r["significant_positive"]]
    verdict = "supported" if len(pos) >= 3 else "partly supported" if len(pos) == 2 else "refuted"
    write_json(OUT / "analysis.json", {"contrasts": rows, "corpus": corpus, "X10_P": {"models_native_beats_itrans_holm_significant": pos, "n_models": len(pos), "verdict": verdict,
                                                                              "rule": "supported: >= 3 of 4; partly supported: exactly 2; refuted: <= 1"}},
               {"registration": "RESULTS.md X10", "family": "Holm over 4 contrasts x 4 models = 16"})
    print(json.dumps({"X10_P": verdict, "native_beats_itrans": pos, "contrasts": [(r["model"], r["contrast"], round(r["diff"], 2), round(r["p_holm"], 4)) for r in rows]}, indent=1))


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "pilot":
        pilot()
    elif cmd == "score":
        run_model(sys.argv[2], None)
    else:
        analyse()
