"""X12/X13 tokenizer screen (CPU, tokenizer files only, no model weights): vocabulary size and tokens per word for Kannada native and
ITRANS (the 2,009 FLORES+ sentences, as the Phase 1 gate E0) per tokenizer, plus the HF metadata (gating, licence) of each repo.
Output: results/phase2/x12/tokenizers.json. Usage: python scripts/x12_tokenizers.py"""
import json
import os
import sys

from shattered.runlog import REPO, results_dir, write_json
sys.path.insert(0, str(REPO / "scripts"))
from m14_full import flores_forms  # noqa: E402

REPOS = ["meta-llama/Llama-2-7b-hf", "Cognitive-Lab/Ambari-7B-base-v0.1", "Cognitive-Lab/Ambari-7B-Instruct-v0.1",
         "Cognitive-Lab/Ambari-7B-Instruct-v0.2", "Qwen/Qwen3-8B", "meta-llama/Llama-3.1-8B"]


def main() -> None:
    from huggingface_hub import HfApi
    from transformers import AutoTokenizer
    F = flores_forms()
    out, tok_ids = {}, {}
    for r in REPOS:
        row = {}
        try:
            info = HfApi().model_info(r, token=os.environ.get("HF_TOKEN"))
            row.update({"gated": info.gated, "license": (info.card_data or {}).get("license") if info.card_data else None,
                        "sha": info.sha, "safetensors_params": getattr(getattr(info, "safetensors", None), "total", None)})
        except Exception as e:  # noqa: BLE001
            row["metadata_error"] = repr(e)[:200]
        try:
            tok = AutoTokenizer.from_pretrained(r, token=os.environ.get("HF_TOKEN"))
            row["vocab_size"] = len(tok)
            for form in ("native", "itrans"):
                n = sum(len(x) for x in tok(F[form], add_special_tokens=False)["input_ids"])
                row[f"tokens_per_word_{form}"] = n / sum(len(s.split()) for s in F[form])
            probe = tok("ಕನ್ನಡ ಭಾಷೆ", add_special_tokens=False)["input_ids"]
            row["probe_ids"] = probe
            tok_ids[r] = (len(tok), tuple(tok(F["native"][:200], add_special_tokens=False)["input_ids"][0]))
            row["tokenizer_class"] = type(tok).__name__
        except Exception as e:  # noqa: BLE001
            row["tokenizer_error"] = repr(e)[:300]
        out[r] = row
        print(r, {k: (round(v, 3) if isinstance(v, float) else v) for k, v in row.items() if k != "probe_ids"}, flush=True)
    base = tok_ids.get("meta-llama/Llama-2-7b-hf")
    out["_identical_to_llama2_on_first_200_sentences"] = {r: (tok_ids[r] == base if r in tok_ids and base else None) for r in REPOS[1:4]}
    write_json(results_dir("phase2/x12") / "tokenizers.json", out, {"note": "tokenizer files only; descriptive; no model weights loaded"})


if __name__ == "__main__":
    main()
