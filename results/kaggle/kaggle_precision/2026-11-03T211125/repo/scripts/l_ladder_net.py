"""Net ITRANS -> lossy sentiment change, = L1 + L2 (post hoc descriptive, 2026-10-22, no verdict). CPU only; stored
ladder scores, same calibration and paired bootstrap as `l_ladder.py analyse`. McNemar p is reported unadjusted (no
test is registered here).

Usage: python scripts/l_ladder_net.py     Output: results/l_ladder_posthoc/net_itrans_to_lossy.csv
"""
import json
import sys

import numpy as np
import pandas as pd

from shattered.runlog import REPO, results_dir, write_json

sys.path.insert(0, str(REPO / "scripts"))
import e0b_familiarity as e0b  # noqa: E402
import l_ladder as lad  # noqa: E402


def main() -> None:
    cf = {m: json.load(open(lad.E0B_DIR / f"cf_{m}.json")) for m in lad.ACC_MODELS}
    B = pd.concat([pd.read_parquet(lad.E0B_DIR / f"{m}__{f}.parquet") for m in lad.ACC_MODELS
                   for f in ("english", "itrans", "lower", "lossy")], ignore_index=True)
    B, _ = e0b.apply_calibration(B, cf)
    K = pd.read_csv(REPO / "results/l_ladder/contrasts.csv")
    K = K[K.measure == "sentiment"].set_index(["model", "contrast"])["diff"]
    rows = []
    for m in lad.ACC_MODELS:
        g = B[(B.model == m) & (B.task == "sentiment")]
        piv = g.pivot_table(index="id", columns="form", values="pred_cal")
        corr = piv.eq(g.drop_duplicates("id").set_index("id").label.loc[piv.index], axis=0)
        r = lad.paired(corr["lossy"].to_numpy(), corr["itrans"].to_numpy())
        l1, l2 = K[(m, "L1")], K[(m, "L2")]
        assert np.isclose(r["diff"], l1 + l2), (m, r["diff"], l1 + l2)
        rows.append({"model": m, "counted": m in lad.COUNT_ACC,
                     "n": r["n"], "acc_itrans": r["acc_b"], "acc_lossy": r["acc_a"], "L1": l1, "L2": l2,
                     "net_lossy_minus_itrans": r["diff"], "ci_low": r["ci"][0], "ci_high": r["ci"][1],
                     "mcnemar_p_unadjusted": r["p"]})
    out = results_dir("l_ladder_posthoc")
    pd.DataFrame(rows).to_csv(out / "net_itrans_to_lossy.csv", index=False)
    write_json(out / "net_itrans_to_lossy_provenance.json", {"rows": len(rows)},
               {"status": "post hoc descriptive, 2026-10-22, no verdict", "task": "sentiment (200)"})
    print(pd.DataFrame(rows).to_string())


if __name__ == "__main__":
    main()
