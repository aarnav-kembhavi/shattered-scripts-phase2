"""50-item hand-check sheet for E0 natural romanization, from the texts finished so far.

Stratified across sentiment reviews, XNLI premises and XNLI hypotheses (as close to 50/3 each as possible), always
including the 9 outputs flagged for leftover Kannada script. Seed 0.

Usage: python scripts/e0b_check_sheet.py
Output: data/annotation/natural_romanization_e0_check_v1.csv
"""
import csv
import json
import random

from shattered.data import tasks
from shattered.runlog import REPO
from shattered.translit import to_itrans
from shattered.translit.natural import defective

N, SEED = 50, 0
OUT = REPO / "data" / "annotation" / "natural_romanization_e0_check_v1.csv"


def main() -> None:
    rows = [json.loads(line) for line in open(REPO / "data" / "processed" / "natural_e0_v1.jsonl", encoding="utf-8")]
    source = {}
    for t in ("xnli", "sentiment"):
        for it in tasks.stratified_sample(tasks.load_task(t), 200, seed=0):
            for field, text in it["forms"]["native"].items():
                source.setdefault(text, ("sentiment" if t == "sentiment" else f"xnli_{field}", it["id"]))
    strata = ["sentiment", "xnli_premise", "xnli_hypothesis"]
    by = {s: [r for r in rows if source[r["native"]][0] == s] for s in strata}
    flagged = [r for r in rows if r["flag"]]
    quota = {s: N // 3 + (i < N % 3) for i, s in enumerate(strata)}  # 17, 17, 16
    rng = random.Random(SEED)
    chosen = list(flagged)
    for s in strata:
        need = quota[s] - sum(source[r["native"]][0] == s for r in flagged)
        pool = [r for r in by[s] if not r["flag"]]
        chosen += rng.sample(pool, max(need, 0))
    rng.shuffle(chosen)
    with OUT.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["n", "stratum", "item_id", "flagged_leftover_kannada", "queued_for_regeneration", "native",
                    "natural", "itrans_reference", "faithful_yn", "natural_looking_1to5", "annotator", "notes"])
        for k, r in enumerate(chosen, 1):
            s, iid = source[r["native"]]
            w.writerow([k, s, iid, int(r["flag"]), int(defective(r)), r["native"], r["natural"],
                        to_itrans(r["native"]), "", "", "", ""])
    counts = {s: sum(source[r["native"]][0] == s for r in chosen) for s in strata}
    print(f"{len(chosen)} rows -> {OUT}; per stratum {counts}; flagged {len(flagged)}; "
          f"pool sizes { {s: len(v) for s, v in by.items()} }")


if __name__ == "__main__":
    main()
