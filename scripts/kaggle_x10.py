"""X10 on Kaggle for a 4-bit model (registered: 4-bit models run SIB-200 and X10): FLORES+ devtest Kannada -> English generation, the registered instruction, greedy, max_new_tokens 128, output cut at the first
newline (empty scored as empty), forms native, ITRANS, lowercase, lossy, natural (257 items), exactly as scripts/x10.py. Inputs come from the private dataset shattered-x10-inputs (x10_inputs.json, exported
from scripts/x10.py `inputs()`), so no FLORES text is in the repository. Resumable: after every batch the outputs so far are written, so a cap that hits mid-form loses at most one batch.
Usage (kernel): kaggle_x10.py --out DIR --models sarvam-m [--n 20] [--batch 8] [--quant 4bit] [--forms native itrans ...]"""
import argparse
import glob
import json
import sys
import time
from pathlib import Path

import numpy as np
import torch

sys.path.insert(0, str(Path(__file__).resolve().parent))
from shattered.interp.load import load  # noqa: E402

INSTR = "Translate this Kannada sentence into English.\nKannada: {s}\nEnglish:"
MAX_NEW = 128
ALL = ["native", "itrans", "lower", "lossy", "natural"]


def inputs() -> dict:
    p = glob.glob("/kaggle/input/**/x10_inputs.json", recursive=True)
    p = p[0] if p else str(Path(__file__).resolve().parents[1] / "build" / "kaggle_acct3" / "x10_inputs" / "x10_inputs.json")
    d = json.load(open(p, encoding="utf-8"))
    d["natural"] = {int(k): v for k, v in d["natural"].items()}
    return d


def gen_batch(model, tok, prompts: list[str]) -> list[str]:
    bos = [tok.bos_token_id] if tok.bos_token_id is not None else []
    pad = tok.pad_token_id if tok.pad_token_id is not None else (tok.eos_token_id or 0)
    ids = [bos + tok(p, add_special_tokens=False)["input_ids"] for p in prompts]
    L = max(map(len, ids))
    x = torch.tensor([[pad] * (L - len(s)) + s for s in ids], device=model.device)
    m = torch.tensor([[0] * (L - len(s)) + [1] * len(s) for s in ids], device=model.device)
    with torch.no_grad():
        g = model.generate(input_ids=x, attention_mask=m, max_new_tokens=MAX_NEW, do_sample=False, pad_token_id=pad)
    return [tok.decode(row, skip_special_tokens=True) for row in g[:, L:]]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--models", nargs="+", required=True)
    ap.add_argument("--n", type=int, default=None, help="pilot: sentences per form")
    ap.add_argument("--batch", type=int, default=8)
    ap.add_argument("--quant", default="4bit")
    ap.add_argument("--forms", nargs="+", default=ALL)
    a = ap.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    data = inputs()
    for name in a.models:
        t_load = time.time()
        model, tok = load(name, "auto", dtype=torch.float16, quant=a.quant)
        print(name, "loaded", f"{time.time() - t_load:.0f}s", flush=True)
        mdir = out / name
        mdir.mkdir(exist_ok=True)
        for f in a.forms:
            path = mdir / (f"pilot_{f}.json" if a.n else f"{f}.json")
            part = mdir / (f"pilot_{f}.part.json" if a.n else f"{f}.part.json")
            ids = sorted(data["natural"]) if f == "natural" else list(range(len(data["reference"])))
            if a.n:
                ids = ids[:a.n]
            texts = [data["natural"][i] for i in ids] if f == "natural" else [data["forms"][f][i] for i in ids]
            raw = json.load(open(part, encoding="utf-8")) if part.exists() else []
            if path.exists():
                continue
            t0 = time.time()
            n0 = len(raw)
            while len(raw) < len(ids):
                i = len(raw)
                raw += gen_batch(model, tok, [INSTR.format(s=t) for t in texts[i:i + a.batch]])
                part.write_text(json.dumps(raw, ensure_ascii=False))
                if (len(raw) // a.batch) % 4 == 0:
                    print(name, f, len(raw), "of", len(ids), f"{(time.time() - t0) / max(1, len(raw) - n0):.2f}s per sentence", flush=True)
            first = [r.split("\n")[0].strip() for r in raw]
            secs = time.time() - t0
            path.write_text(json.dumps({"summary": {"n": len(ids), "seconds_this_session": secs, "seconds_per_sentence": secs / max(1, len(ids) - n0), "empty_share": float(np.mean([not o for o in first])),
                                                    "starts_with_think_share": float(np.mean([r.lstrip().startswith("<think>") for r in raw]))}, "ids": ids, "raw": raw,
                                        "registered_first_line": first}, ensure_ascii=False))
            print(name, f, "done", f"{secs:.0f}s", flush=True)
        del model
        torch.cuda.empty_cache()
    (out / "done.json").write_text(json.dumps({"models": a.models, "n": a.n}))


if __name__ == "__main__":
    main()
