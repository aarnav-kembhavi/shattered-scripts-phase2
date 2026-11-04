"""Exact parameter counts of the five study models, summed from the shapes in the safetensors headers of the local HF snapshots
(the files the experiments loaded). Writes results/phase2/model_sizes.json. CPU only, reads headers only (no weights).

Groups: audio / vision towers (key contains 'audio' or 'vision'/'visual'); Gemma 4 per-layer embedding table
(key 'embed_tokens_per_layer'); everything else is text. 'effective_text' = total - towers - per-layer embedding table.
"""
import glob
import json
import os
import struct
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))
from shattered.runlog import provenance  # noqa: E402

HUB = os.path.expanduser("~/.cache/huggingface/hub")
MODELS = {"Qwen2.5-1.5B": "Qwen/Qwen2.5-1.5B-Instruct", "Qwen3-1.7B": "Qwen/Qwen3-1.7B", "Qwen3.5-2B": "Qwen/Qwen3.5-2B",
          "Sarvam-1": "sarvamai/sarvam-1", "Gemma 4 E2B": "google/gemma-4-E2B-it"}


def count(repo):
    files = sorted(glob.glob(f"{HUB}/models--{repo.replace('/', '--')}/snapshots/*/*.safetensors"))
    tot = ple = vision = audio = 0
    for f in files:
        with open(f, "rb") as b:
            n = struct.unpack("<Q", b.read(8))[0]
            h = json.loads(b.read(n))
        for k, v in h.items():
            if k == "__metadata__":
                continue
            p = 1
            for d in v["shape"]:
                p *= d
            tot += p
            if "audio" in k:
                audio += p
            elif "vision" in k or "visual" in k:
                vision += p
            elif k.endswith("embed_tokens_per_layer.weight"):
                ple += p
    return dict(repo=repo, files=len(files), total=tot, vision_tower=vision, audio_tower=audio, per_layer_embedding_table=ple,
                effective_text=tot - vision - audio - ple)


if __name__ == "__main__":
    out = {"provenance": provenance({"source": "safetensors headers of the local HF snapshots"}), "models": {}}
    for name, repo in MODELS.items():
        r = count(repo)
        r.update({k + "_b": round(v / 1e9, 3) for k, v in r.items() if k in ("total", "vision_tower", "audio_tower",
                                                                                "per_layer_embedding_table", "effective_text")})
        out["models"][name] = r
        print(name, r["total_b"], "effective text", r["effective_text_b"], "ple", r["per_layer_embedding_table_b"],
              "towers", r["vision_tower_b"], r["audio_tower_b"])
    dest = REPO / "results" / "phase2"
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "model_sizes.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
