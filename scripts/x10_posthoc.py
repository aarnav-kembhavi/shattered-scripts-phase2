"""X10 POST HOC extraction check for Qwen3.5-2B (added 2026-11-05 at the lead author's request; NOT part of the registration, the registered X10 verdict is unchanged).

The registered protocol cuts the generated text at the first newline and scores an empty first line as empty; Qwen3.5-2B returns an empty first line for 62% to 88% of inputs. This script regenerates Qwen3.5-2B with
the registered instruction, greedy decoding and 128 new tokens (identical settings), keeps the full raw output, and extracts the FIRST NON-EMPTY LINE (post hoc). It reports the empty-first-line share, the
chrF2 scores under both extractions, and native minus form paired bootstrap differences (10,000, seed 0) under the post hoc extraction, for information only.
Usage: python scripts/x10_posthoc.py score | analyse        Output: results/phase2/x10/posthoc/ (labelled post hoc)"""
import json
import sys
import time
from pathlib import Path

import numpy as np
import torch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import x10 as X  # noqa: E402

from shattered.interp.load import load  # noqa: E402
from shattered.runlog import results_dir, write_json  # noqa: E402

MODEL = "qwen3.5-2b"
OUT = results_dir("phase2/x10/posthoc")


def generate_raw(model, tok, prompts: list[str], batch: int = 16) -> list[str]:
    bos = [tok.bos_token_id] if tok.bos_token_id is not None else []
    pad = tok.pad_token_id if tok.pad_token_id is not None else (tok.eos_token_id or 0)
    outs = []
    for i in range(0, len(prompts), batch):
        ids = [bos + tok(p, add_special_tokens=False)["input_ids"] for p in prompts[i:i + batch]]
        L = max(map(len, ids))
        x = torch.tensor([[pad] * (L - len(s)) + s for s in ids], device=model.device)
        m = torch.tensor([[0] * (L - len(s)) + [1] * len(s) for s in ids], device=model.device)
        with torch.no_grad():
            g = model.generate(input_ids=x, attention_mask=m, max_new_tokens=X.MAX_NEW, do_sample=False, pad_token_id=pad)
        outs += [tok.decode(row, skip_special_tokens=True) for row in g[:, L:]]
    return outs


def first_nonempty(t: str) -> str:
    for ln in t.split("\n"):
        if ln.strip():
            return ln.strip()
    return ""


def score() -> None:
    data = X.inputs()
    model, tok = load(MODEL, "cuda")
    for f in X.FORMS:
        path = OUT / f"{MODEL}__{f}.json"
        if path.exists():
            continue
        ids = sorted(data["natural"]) if f == "natural" else list(range(1012))
        texts = [data["natural"][i] for i in ids] if f == "natural" else [data["forms"][f][i] for i in ids]
        t0 = time.time()
        raw = generate_raw(model, tok, [X.INSTR.format(s=t) for t in texts])
        write_json(path, {"ids": ids, "raw": raw, "registered_first_line": [r.split("\n")[0].strip() for r in raw], "posthoc_first_nonempty_line": [first_nonempty(r) for r in raw]},
                   {"label": "POST HOC extraction, not part of the registration", "model": MODEL, "form": f, "instruction": X.INSTR, "max_new_tokens": X.MAX_NEW, "greedy": True})
        print(f, len(ids), f"{time.time() - t0:.0f}s", flush=True)


def analyse() -> None:
    from sacrebleu.metrics import CHRF
    data = X.inputs()
    refs = data["reference"]
    S, res = {}, {}
    for f in X.FORMS:
        d = json.load(open(OUT / f"{MODEL}__{f}.json", encoding="utf-8"))
        r = [refs[i] for i in d["ids"]]
        row = {"n": len(d["ids"])}
        for key in ("registered_first_line", "posthoc_first_nonempty_line"):
            outs = d[key]
            row[key] = {"empty_share": float(np.mean([not o for o in outs])), "corpus_chrf": CHRF(char_order=6, word_order=0, beta=2).corpus_score(outs, [r]).score}
            if key == "posthoc_first_nonempty_line":
                S[f] = dict(zip(d["ids"], X.chrf_scores(outs, r)))
        res[f] = row
    contrasts = {}
    for f in ("itrans", "lower", "lossy", "natural"):
        ids = sorted(set(S["native"]) & set(S[f]))
        contrasts[f"native - {f}"] = {"n": len(ids), **X.boot_p(np.array([S["native"][i] - S[f][i] for i in ids]))}
    write_json(OUT / "analysis.json", {"label": "POST HOC extraction (first non-empty line); the registered X10 verdict is unchanged", "model": MODEL, "by_form": res, "posthoc_contrasts_unadjusted": contrasts},
               {"registration": "none; added 2026-11-05"})
    print(json.dumps({"by_form": {f: (round(v["registered_first_line"]["empty_share"], 3), round(v["registered_first_line"]["corpus_chrf"], 1), round(v["posthoc_first_nonempty_line"]["empty_share"], 3),
                                      round(v["posthoc_first_nonempty_line"]["corpus_chrf"], 1)) for f, v in res.items()}, "contrasts": {k: (round(v["diff"], 2), [round(x, 2) for x in v["ci95"]]) for k, v in contrasts.items()}}, indent=1))


if __name__ == "__main__":
    {"score": score, "analyse": analyse}[sys.argv[1]]()
