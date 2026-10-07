"""E0 step 1: candidate open models for the Kannada understanding gate, with sizes, licenses, gating and hardware fit.

Usage: python scripts/e00_candidates.py [--download-under-gb 5]
Outputs: results/e00_gate/candidates.csv, candidates.md. With --download-under-gb, downloads weights + tokenizer of
ungated candidates whose total weight files are under that size (never any single file over 5 GB).
"""
import argparse
import json
import os

import pandas as pd
from dotenv import load_dotenv
from huggingface_hub import HfApi, hf_hub_download, snapshot_download

from shattered.models import CANDIDATES
from shattered.runlog import REPO, results_dir, write_json

load_dotenv(REPO / ".env")



def weight_bytes(info) -> tuple[int, int]:
    files = [s for s in info.siblings if s.rfilename.endswith(".safetensors")]
    return sum(s.size or 0 for s in files), max((s.size or 0 for s in files), default=0)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--download-under-gb", type=float, default=None)
    args = ap.parse_args()
    api = HfApi(token=os.environ.get("HF_TOKEN"))
    rows = []
    for repo, family, note in CANDIDATES:
        try:
            info = api.model_info(repo, files_metadata=True)
        except Exception as e:  # noqa: BLE001
            rows.append({"repo": repo, "family": family, "error": f"{type(e).__name__}"})
            continue
        params = info.safetensors.total if info.safetensors else None
        total, largest = weight_bytes(info)
        lic = (info.card_data or {}).get("license") if info.card_data else None
        cfg = info.config or {}
        model_type = cfg.get("model_type")
        vocab = None
        if not info.gated:
            try:
                c = json.load(open(hf_hub_download(repo, "config.json", token=os.environ.get("HF_TOKEN"))))
                vocab = c.get("vocab_size") or (c.get("text_config") or {}).get("vocab_size")
            except Exception:  # noqa: BLE001
                pass
        gb_bf16 = params * 2 / 1e9 if params else None
        rows.append({
            "repo": repo, "family": family, "note": note, "params_b": round(params / 1e9, 2) if params else None,
            "weights_gb_on_hub": round(total / 1e9, 2), "largest_file_gb": round(largest / 1e9, 2),
            "license": lic, "gated": info.gated or False, "model_type": model_type, "vocab_size": vocab,
            "created": str(info.created_at)[:10],
            # fit heuristics: weights + ~1.5 GB for activations/cache at short (<=512 token) inputs
            "fits_8gb_bf16_local": bool(gb_bf16 and gb_bf16 + 1.5 <= 8.0),
            "fits_t4_16gb_fp16": bool(gb_bf16 and gb_bf16 + 1.5 <= 15.0),
            "fits_8gb_4bit": bool(params and params * 0.56 / 1e9 + 1.5 <= 8.0),
        })
    df = pd.DataFrame(rows)
    out = results_dir("e00_gate")
    df.to_csv(out / "candidates.csv", index=False)
    (out / "candidates.md").write_text(df.to_markdown(index=False), encoding="utf-8")
    print(df.to_string(index=False))

    downloaded = []
    if args.download_under_gb:
        for r in rows:
            if r.get("gated") or r.get("error") or r["weights_gb_on_hub"] >= args.download_under_gb \
                    or r["largest_file_gb"] >= 5.0:
                continue
            path = snapshot_download(r["repo"], token=os.environ.get("HF_TOKEN"),
                                     allow_patterns=["*.json", "*.safetensors", "*.model", "*.txt", "*.jinja",
                                                     "*.tiktoken"])
            downloaded.append({"repo": r["repo"], "path": path, "weights_gb": r["weights_gb_on_hub"]})
            print("downloaded", r["repo"], r["weights_gb_on_hub"], "GB")
    write_json(out / "candidates.json", {"candidates": rows, "downloaded": downloaded},
               {"download_under_gb": args.download_under_gb})


if __name__ == "__main__":
    main()
