"""Kaggle scoring job for X12 and X13 (Amendment 2): Kannada SIB-200 log-likelihood scoring (T1 template, the Phase 1 prompts and verbalizers) in the forms
english, native, itrans, lossy, lower (and natural on the 257 items with a clean natural romanization), content-free calibration inputs, and unmapped FLORES+
retrieval curves (native, ITRANS against English; per-layer test-half correctness, train-half layer choice, M4b split) with the model sharded over both T4s in
float16 (no quantization; a model must have passed A1-P first, enforced by the caller). Items are built exactly as Phase 1 (`e0c_sib.load_items`): FLORES+ sentence
index_id of each SIB-200 item, NFC, ITRANS word by word, `to_lossy`, `universal|lower`; the FLORES+ text and the natural drafts come from the PRIVATE Kaggle dataset
`shattered-flores-private` (never public). One shard (model, form) at a time is written to out/<model>/ so a timeout loses at most one shard; finished shards are
skipped. Output rows have the Phase 1 columns (model, task, form, id, label, logprobs, prompt_tokens) so the Phase 1 analysis code applies unchanged.
Usage: python scripts/x_score.py --out DIR --models ambari-7b-base [--forms ...] [--no-retrieval] [--limit N]
"""
import argparse
import glob
import json
import sys
import time
import unicodedata
from pathlib import Path

import numpy as np
import pandas as pd
import torch

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
from kaggle_retrieval_gate import retrieval, unmapped_curves  # noqa: E402
from shattered.eval.loglik import VERBALIZERS, build_prompt, choice_logprobs  # noqa: E402
from shattered.interp.collect import Sentence, collect  # noqa: E402
from shattered.interp.load import load  # noqa: E402
from shattered.translit import to_itrans, to_lossy  # noqa: E402

SIB_REPO, SIB_REV = "Davlan/sib200", "38977a667f6fc264d5c26ec57a01e16db040b358"
CATS = ["science/technology", "travel", "politics", "sports", "health", "entertainment", "geography"]
CONTENT_FREE = ["N/A", "", "[MASK]"]
ALL_FORMS = ["english", "native", "itrans", "lossy", "lower", "natural"]


_LOWER = None


def to_lower(text: str) -> str:
    """The E9 `universal|lower` scheme, as scripts/l_ladder.py (needs results/e09_romanize/best_schemes.json in the package)."""
    global _LOWER
    if _LOWER is None:
        from e09_eval import scheme_from
        best = json.load(open(REPO / "results" / "e09_romanize" / "best_schemes.json", encoding="utf-8"))["best"]
        _LOWER = scheme_from(best["universal|lower"]["assignment"])
    return _LOWER.encode(text)


def private() -> dict:
    p = glob.glob("/kaggle/input/**/flores_private.json", recursive=True)
    p = p[0] if p else str(REPO / "build" / "kaggle" / "flores_private" / "flores_private.json")
    return json.load(open(p, encoding="utf-8"))


def sib_items(limit: int | None) -> list[dict]:
    import os
    from huggingface_hub import hf_hub_download
    S = pd.concat([pd.read_csv(hf_hub_download(SIB_REPO, f"data/kan_Knda/{s}.tsv", repo_type="dataset", revision=SIB_REV, token=os.environ.get("HF_TOKEN")),
                               sep="\t") for s in ("train", "dev", "test")], ignore_index=True).sort_values("index_id", ignore_index=True)
    P = private()
    kn, en, nat = P["kn"], P["en"], P.get("natural", {})
    items = []
    for i, c in zip(S.index_id, S.category):
        n = unicodedata.normalize("NFC", kn[int(i)])
        f = {"english": en[int(i)], "native": n, "itrans": " ".join(to_itrans(w) for w in n.split()), "lossy": to_lossy(n), "lower": to_lower(n)}
        if str(int(i)) in nat:
            f["natural"] = nat[str(int(i))]
        items.append({"id": int(i), "label": CATS.index(c), "forms": f})
    if limit:
        items = [items[j] for j in np.random.default_rng(0).choice(len(items), limit, replace=False)]
    return items


def score_sib(model, tok, name: str, items: list[dict], forms: list[str], mdir: Path) -> None:
    cfp = mdir / "cf.json"
    if not cfp.exists():
        cf = {x: {"sib": choice_logprobs(model, tok, build_prompt("sib", {"text": x}), VERBALIZERS["sib"])[0]} for x in CONTENT_FREE}
        cfp.write_text(json.dumps(cf, indent=1))
    for f in forms:
        path = mdir / f"sib_{f}.parquet"
        if path.exists():
            continue
        t0, rows = time.time(), []
        nonfinite = 0
        for it in items:
            if f not in it["forms"]:
                continue
            lp, n_tok = choice_logprobs(model, tok, build_prompt("sib", {"text": it["forms"][f]}), VERBALIZERS["sib"])
            nonfinite += int((~np.isfinite(np.asarray(lp))).sum())
            rows.append({"model": name, "task": "sib", "form": f if f != "natural" else "natural257", "id": it["id"], "label": it["label"],
                         "logprobs": lp, "prompt_tokens": n_tok})
        pd.DataFrame(rows).to_parquet(path)
        (mdir / f"sib_{f}.meta.json").write_text(json.dumps({"n": len(rows), "non_finite": nonfinite, "seconds": time.time() - t0}))
        print(name, f, len(rows), f"{time.time() - t0:.0f}s non-finite {nonfinite}", flush=True)


def score_retrieval(model, tok, name: str, mdir: Path) -> None:
    path = mdir / "retrieval.json"
    if path.exists():
        return
    P = private()
    F = {"english": P["en"], "native": P["kn"], "itrans": [" ".join(to_itrans(w) for w in s.split()) for s in P["kn"]]}
    n = len(F["english"])
    order = np.random.default_rng(0).permutation(n)
    tr, te = np.sort(order[: n // 2]), np.sort(order[n // 2:])
    t0, st, nonfinite = time.time(), {}, {}
    for f in ("english", "native", "itrans"):
        S = collect(model, tok, [Sentence(str(i), s, []) for i, s in enumerate(F[f])])["sent_states"]
        nonfinite[f] = int((~np.isfinite(S.astype(np.float32))).sum())
        st[f] = S.astype(np.float32)
    res = {"n": n, "n_test": len(te), "non_finite": nonfinite, "seconds": time.time() - t0, "forms": {}}
    for f in ("native", "itrans"):
        tra, tes = unmapped_curves(st[f], st["english"], tr, te)
        lu = int(tra.argmax())
        res["forms"][f] = {"layer": lu, "acc_unmapped": float(tes[lu].mean()), "test_acc_per_layer": tes.mean(1).tolist(), "train_acc_per_layer": tra.tolist()}
        np.save(mdir / f"retrieval_test_correct_{f}.npy", tes[lu])  # per-sentence correctness at the chosen layer, for paired bootstraps
    path.write_text(json.dumps(res, indent=1))
    print(name, "retrieval", {f: round(v["acc_unmapped"], 4) for f, v in res["forms"].items()}, flush=True)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--models", nargs="+", required=True)
    ap.add_argument("--forms", nargs="+", default=ALL_FORMS)
    ap.add_argument("--no-retrieval", action="store_true")
    ap.add_argument("--quant", choices=["4bit", "8bit"], default=None, help="bitsandbytes quantization for a model that does not fit in fp16 (X13: SIB-200 only, never retrieval)")
    ap.add_argument("--limit", type=int)
    a = ap.parse_args()
    out = Path(a.out)
    items = sib_items(a.limit)
    print("items", len(items), "natural", sum("natural" in i["forms"] for i in items), flush=True)
    for m in a.models:
        mdir = out / m
        mdir.mkdir(parents=True, exist_ok=True)
        t0 = time.time()
        model, tok = load(m, "auto", dtype=torch.float16, quant=a.quant)
        print(m, "loaded", f"{time.time() - t0:.0f}s", flush=True)
        score_sib(model, tok, m, items, a.forms, mdir)
        if not a.no_retrieval:
            score_retrieval(model, tok, m, mdir)
        (mdir / "done.json").write_text(json.dumps({"seconds": time.time() - t0, "dtype": "float16", "forms": a.forms, "retrieval": not a.no_retrieval}))
        del model
        torch.cuda.empty_cache()


if __name__ == "__main__":
    main()
