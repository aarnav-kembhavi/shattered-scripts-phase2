"""X7 (ii): E5 grid retrained with a factorized embedding (registered in RESULTS.md 2026-11-01, section X7).
Embedding table V x e plus projection e x 384 matches the vocab-256 baseline's 98,304 parameters within 0.4%. All other settings are
Phase 1 (configs/e05_pretrain.yaml). Runs are named x7_v{V}_s{S} (raw run files under results/e05_pretrain/ and checkpoints/e05/, no
collision with the Phase 1 `run_*`); summaries go to results/phase2/x7/.

Usage: python scripts/x7_control.py pilot   (V=256 and V=4096, seed 0, 5% of the budget: timing and the embedding-size check)
       python scripts/x7_control.py grid    (18 runs, seed-major, each resumable from its checkpoint)
"""
import json
import sys
import time

sys.path.insert(0, "scripts")
import e05_pretrain as e05  # noqa: E402
from shattered.runlog import results_dir, write_json  # noqa: E402

EMB = {256: 154, 384: 128, 512: 110, 768: 85, 1024: 70, 4096: 22}
BASE_EMB = 98_304


def cfg_for(cfg: dict, v: int) -> dict:
    c = dict(cfg)
    c["model"] = {**cfg["model"], "emb_dim": EMB[v]}
    return c


def main() -> None:
    cfg = e05.load_cfg("configs/e05_pretrain.yaml")
    assert cfg["vocabs"] == list(EMB), cfg["vocabs"]
    meta = e05.get_meta(cfg)
    out = results_dir("phase2/x7")
    if sys.argv[1] == "pilot":
        res = {}
        for v in (256, 4096):
            c = cfg_for(cfg, v)
            t0 = time.time()
            r = e05.train_run(e05.run_cfg(c, v, 0, 0.05, "x7pilot"), meta)
            wall = time.time() - t0
            steps_full = e05.full_steps(c, meta, v)
            res[str(v)] = {"pilot_steps": r["steps"], "wall_s": wall, "s_per_step": wall / r["steps"], "full_steps": steps_full,
                           "hours_per_run": steps_full * wall / r["steps"] / 3600, "params": r.get("params")}
            print(v, json.dumps(res[str(v)]), flush=True)
        tot = 3 * sum(res[str(v)]["hours_per_run"] for v in (256, 4096)) / 2 * 6
        res["estimated_grid_hours_18_runs"] = tot
        write_json(out / "pilot.json", res, {"status": "pilot at 5% of budget; no BPB value used for any decision"})
        print("estimated 18-run hours", tot)
    else:
        for seed in cfg["seeds"]:
            for v in cfg["vocabs"]:
                c = cfg_for(cfg, v)
                t0 = time.time()
                r = e05.train_run(e05.run_cfg(c, v, seed, 1.0, "x7"), meta)
                row = {"vocab": v, "seed": seed, "emb_dim": EMB[v], "status": r["status"], "val_bpb_full": r.get("val_bpb_full"),
                       "params": r.get("params"), "wall_seconds": time.time() - t0}
                print(json.dumps(row), flush=True)
                with open(out / "grid_status.jsonl", "a") as f:
                    f.write(json.dumps(row) + "\n")


if __name__ == "__main__":
    main()
