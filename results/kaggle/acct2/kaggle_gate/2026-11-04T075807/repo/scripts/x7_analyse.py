"""X7 analysis, exactly as registered (RESULTS.md, X7).

(i) Accounting (analysis only): per vocabulary, embedding parameters, non-embedding parameters, total parameters and embedding share for the Phase 1 grid (results/e05_pretrain/T6.csv)
    and for the factorized control (results/phase2/x7/grid_status.jsonl params).
(ii) Control decision rule on the 18 factorized-embedding runs (6 vocabularies x seeds 0, 1, 2; validation BPB = val_bpb_full):
    SURVIVES if Spearman(tokens per word, seed-mean validation BPB) >= 0.8 over the vocabularies AND the vocab-256 mean BPB exceeds the vocab-4096 mean by more than 3 times the larger of the two
    seed SDs; DOES NOT SURVIVE if the Spearman is <= 0 or the 256 - 4096 difference is <= 0; otherwise INCONCLUSIVE. Tokens per word per vocabulary: Phase 1 (T6.csv; the tokenizers are unchanged).
    The seed SD is the sample SD (ddof = 1, as pandas std in scripts/e05_analysis.py, the Phase 1 convention); the ddof = 0 value is reported next to it.
Output: results/phase2/x7/analysis.json. The Phase 1 MDL assembly probes on the control models (descriptive) are a separate step.
"""
import json

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

from shattered.runlog import REPO, results_dir, write_json


def main() -> None:
    rows = [json.loads(line) for line in (REPO / "results" / "phase2" / "x7" / "grid_status.jsonl").open(encoding="utf-8")]
    rows = [r for r in rows if r["status"] == "done"]
    df = pd.DataFrame([{"vocab": r["vocab"], "seed": r["seed"], "bpb": r["val_bpb_full"], "emb": r["params"]["embedding"], "nonemb": r["params"]["non_embedding"],
                        "total": r["params"]["total"], "wall_s": r["wall_seconds"]} for r in rows])
    t6 = pd.read_csv(REPO / "results" / "e05_pretrain" / "T6.csv").set_index("vocab")
    assert len(df) == 18 and set(df.seed) == {0, 1, 2}, (len(df), set(df.seed))
    g = df.groupby("vocab")
    agg = pd.DataFrame({"bpb_mean": g.bpb.mean(), "bpb_sd_ddof1": g.bpb.std(ddof=1), "bpb_sd_ddof0": g.bpb.std(ddof=0), "n_seeds": g.bpb.count(), "embedding_params": g.emb.first(),
                        "non_embedding_params": g.nonemb.first(), "total_params": g.total.first()})
    agg["embedding_share"] = agg.embedding_params / agg.total_params
    agg["tokens_per_word"] = t6.loc[agg.index, "tokens_per_word"]
    agg["phase1_bpb_mean"] = t6.loc[agg.index, "val_bpb_mean"]
    agg["phase1_embedding_params"] = t6.loc[agg.index, "params_embedding"]
    rho, p = spearmanr(agg.tokens_per_word, agg.bpb_mean)
    d = float(agg.loc[256, "bpb_mean"] - agg.loc[4096, "bpb_mean"])
    out = {}
    for ddof in ("ddof1", "ddof0"):
        sd = max(agg.loc[256, f"bpb_sd_{ddof}"], agg.loc[4096, f"bpb_sd_{ddof}"])
        out[ddof] = {"larger_sd": float(sd), "diff_256_minus_4096": d, "diff_over_sd": float(d / sd), "exceeds_3sd": bool(d > 3 * sd)}
    def verdict(ex: bool) -> str:
        if rho >= 0.8 and ex:
            return "survives"
        if rho <= 0 or d <= 0:
            return "does not survive"
        return "inconclusive"
    v1, v0 = verdict(out["ddof1"]["exceeds_3sd"]), verdict(out["ddof0"]["exceeds_3sd"])
    res = {"n_runs": int(len(df)), "spearman_tokens_per_word_vs_bpb": float(rho), "spearman_p": float(p), "per_vocab": agg.round(6).reset_index().to_dict("records"),
           "decision": out, "verdict": v1, "verdict_if_ddof0": v0, "prediction": "the bits-per-byte ordering by fragmentation survives equalized embedding capacity",
           "phase1_embedding_params_range": [float(t6.params_embedding.min()), float(t6.params_embedding.max())],
           "control_embedding_params_range": [float(agg.embedding_params.min()), float(agg.embedding_params.max())], "total_wall_hours": float(df.wall_s.sum() / 3600),
           "mdl_probes_on_control_models": "not run yet (descriptive, separate step)"}
    write_json(results_dir("phase2/x7") / "analysis.json", res, {"registration": "RESULTS.md X7 (Phase 2 pre-registration)", "bpb": "val_bpb_full"})
    print(agg[["tokens_per_word", "bpb_mean", "bpb_sd_ddof1", "phase1_bpb_mean", "embedding_params", "embedding_share"]].round(4).to_string())
    print("Spearman", round(rho, 4), "p", round(p, 4), "| 256-4096 diff", round(d, 4), out, "| VERDICT", v1, "(ddof0:", v0 + ")")


if __name__ == "__main__":
    main()
