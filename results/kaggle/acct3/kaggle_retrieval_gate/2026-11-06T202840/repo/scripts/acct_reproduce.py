"""Reproducibility check for a new Kaggle account: compare its A1-R retrieval gate (kaggle_retrieval_gate) with account 1's (the untrained base must give the same numbers), and the laptop values.
Usage: python scripts/acct_reproduce.py 3        Output: results/kaggle/acct<N>/a1r_reproduced.json and ACCEPTED (only if the gate passed and the curves match)"""
import glob
import json
import sys
from pathlib import Path

import numpy as np

from shattered.runlog import REPO

n = sys.argv[1]
base = REPO / "results" / "kaggle"
a1 = json.load(open(sorted(glob.glob(str(base / "kaggle_retrieval_gate" / "*" / "out" / "gate_retrieval.json")))[-1]))
new_dir = base / f"acct{n}" / "kaggle_retrieval_gate"
a_n = json.load(open(sorted(glob.glob(str(new_dir / "*" / "out" / "gate_retrieval.json")))[-1]))
res = {"check": f"account {n} A1-R reproduction (kaggle_retrieval_gate)", "by_model_form": {}, "tolerance_acc_at_1": a_n["rule"]["tolerance_acc_at_1"], "gate_passed": bool(a_n["gate_passed"])}
mx = 0.0
for m in a1["models"]:
    for f in ("native", "itrans"):
        x, y = a1["models"][m]["forms"][f], a_n["models"][m]["forms"][f]
        mx = max(mx, float(np.max(np.abs(np.array(x["test_acc_per_layer"], float) - np.array(y["test_acc_per_layer"], float)))), abs(x["acc_kaggle"] - y["acc_kaggle"]))
        res["by_model_form"][f"{m} {f}"] = {"account1": x["acc_kaggle"], f"account{n}": y["acc_kaggle"], "layer_account1": x["layer_kaggle"], f"layer_account{n}": y["layer_kaggle"]}
res["max_curve_diff_vs_account1"] = mx
res["reproduces_account1_exactly"] = bool(mx == 0.0)
(base / f"acct{n}").mkdir(parents=True, exist_ok=True)
(base / f"acct{n}" / "a1r_reproduced.json").write_text(json.dumps(res, indent=1))
ok = res["gate_passed"] and mx <= 1e-6
if ok:
    (base / f"acct{n}" / "ACCEPTED").write_text("smoke gate and A1-R reproduction passed\n")
print(json.dumps(res, indent=1), "ACCEPTED" if ok else "NOT accepted")
