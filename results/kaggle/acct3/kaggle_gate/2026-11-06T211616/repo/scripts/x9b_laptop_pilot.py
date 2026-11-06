"""X9b on the laptop: feasibility pilot for the extra Sarvam-1 seeds (VRAM and tokens per second of the registered QLoRA recipe on the RTX 3070 laptop GPU, 50 micro-steps, ITRANS and native streams).
Uses the registered recipe unchanged (kaggle_x9b.py: 4-bit NF4 with double quantisation, fp16 compute with loss scaling, LoRA r16/alpha 32, 512-token sequences, 16,384 tokens per optimizer step).
Usage: python scripts/x9b_laptop_pilot.py        Output: results/phase2/x9b/laptop_pilot.json"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kaggle_x9b as K  # noqa: E402

from shattered.runlog import REPO, write_json  # noqa: E402


def main() -> None:
    pool = K.Pool()
    res = {}
    for cond in ("itrans", "native"):
        r, _ = K.pilot_one(pool, "sarvam-1", cond, "cuda", True, 50)
        res[cond] = r
        print(cond, {k: (round(v, 3) if isinstance(v, float) else v) for k, v in r.items() if k in ("micro_batch", "tokens_per_s", "peak_vram_gib", "finite_loss", "loss_first", "loss_last")}, flush=True)
    d = json.loads((REPO / "results" / "phase2" / "x9b" / "pilot_done.json").read_text(encoding="utf-8"))
    B = d["models"]["sarvam-1"]["B"]
    slow = min(v["tokens_per_s"] for v in res.values())
    res["estimate"] = {"B_tokens_per_run": B, "slowest_tokens_per_s": slow, "train_hours_per_run": B / slow / 3600, "t4_slowest_tokens_per_s_registered": d["models"]["sarvam-1"]["slowest_tokens_per_s"]}
    write_json(REPO / "results" / "phase2" / "x9b" / "laptop_pilot.json", res, {"purpose": "feasibility of extra Sarvam-1 seeds on the laptop; no accuracy is used"})
    print(res["estimate"])


if __name__ == "__main__":
    main()
