"""Verified texts from Annotator A's merged verification (RESULTS.md 2026-10-26): fine = draft, wrong = fix.

Writes
  data/annotation/verified_A_v1.jsonl                 all 500 items: natural_verified, kanglish_verified, verdicts,
                                                      drafts (A's data as given; indicsentiment-test-249 keeps A's fix)
  data/processed/natural_e0_verified_v1.jsonl         natural_e0_v1.jsonl with the natural text replaced by the verified
                                                      one for the annotated sentiment items (same format: native, natural)
  data/processed/natural_flores_m4_500_verified_v1.jsonl  natural_flores_m4_500_v1.jsonl, the same for the annotated
                                                      FLORES items in the M4c sample (same format: index, native, natural)
In the experiment files a verified text replaces the experiment's text only where A's draft is identical to it (so
"fine" means that exact text was checked); every other row is copied unchanged. indicsentiment-test-249's natural fix
drops content (the lead author, 2026-10-26): the draft is used for it in the experiment files (logged as a substitution).
Each experiment row gets "verified" (the item was verified against this exact text) and "verified_changed".

Usage: python scripts/k_verified.py      Output summary: results/k_verified/build.json
"""
import csv
import json
import sys

from shattered.runlog import REPO, results_dir, write_json

sys.path.insert(0, str(REPO / "scripts"))
import k_annotation as K  # noqa: E402

A_CSV = REPO / "annotation/results/annotator_A.csv"
ALL = REPO / "data/annotation/verified_A_v1.jsonl"
E0, E0V = REPO / "data/processed/natural_e0_v1.jsonl", REPO / "data/processed/natural_e0_verified_v1.jsonl"
M4, M4V = (REPO / "data/processed/natural_flores_m4_500_v1.jsonl",
           REPO / "data/processed/natural_flores_m4_500_verified_v1.jsonl")
USE_DRAFT = {("indicsentiment-test-249", "natural"): "A's fix is a paraphrase that drops content (the lead author, 2026-10-26)"}


def main() -> None:
    items = {it["id"]: it for it in K.items()}
    A = {r["item_id"]: r for r in csv.DictReader(open(A_CSV, encoding="utf-8-sig"))}
    assert len(A) == 500 and all(A[i][f"{k}_verdict"] in ("fine", "wrong") for i in A for k in ("natural", "kanglish"))
    with open(ALL, "w", encoding="utf-8") as f:
        for i, it in items.items():
            r = A[i]
            f.write(json.dumps({"item_id": i, "source": it["source"], "native": it["native"], "english": it["english"],
                                **{f"{k}_{x}": r[f"{k}_{y}"] for k in ("natural", "kanglish")
                                   for x, y in (("draft", "draft"), ("verdict", "verdict"), ("verified", "text"))},
                                "note": r["note"], "annotator": "A (pool of about 50)",
                                "flag": USE_DRAFT.get((i, "natural"), "")}, ensure_ascii=False) + "\n")
    exp_text = {i: (A[i]["natural_draft"] if (i, "natural") in USE_DRAFT else A[i]["natural_text"]) for i in A}
    rep = {"substitutions": [{"item_id": i, "form": k, "reason": v} for (i, k), v in USE_DRAFT.items()]}

    def rewrite(src, dst, key_of, label):
        rows = [json.loads(x) for x in open(src, encoding="utf-8")]
        st = {"rows": len(rows), "annotated_items_in_file": 0, "draft_equals_experiment_text": 0,
              "draft_differs_from_experiment_text": [], "verified": 0, "verified_changed": 0, "changed_items": []}
        with open(dst, "w", encoding="utf-8") as f:
            for r in rows:
                i = key_of(r)
                r = {**r, "verified": False, "verified_changed": False}
                if i is not None:
                    st["annotated_items_in_file"] += 1
                    if A[i]["natural_draft"] == r["natural"]:
                        st["draft_equals_experiment_text"] += 1
                        new = exp_text[i]
                        r.update({"item_id": i, "verified": True, "verified_changed": new != r["natural"],
                                  "natural": new})
                        st["verified"] += 1
                        if r["verified_changed"]:
                            st["verified_changed"] += 1
                            st["changed_items"].append(i)
                    else:
                        st["draft_differs_from_experiment_text"].append(i)
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        rep[label] = st

    by_native = {it["native"]: i for i, it in items.items() if it["source"] == "sentiment"}
    rewrite(E0, E0V, lambda r: by_native.get(r["native"]), "natural_e0")
    flores = {int(i.split("-")[1]): i for i, it in items.items() if i.startswith("flores-")}

    def m4_key(r):
        i = flores.get(r["index"])
        if i is not None:
            assert items[i]["native"] == r["native"], (i, "native text differs from the M4c row")
        return i
    rewrite(M4, M4V, m4_key, "natural_flores_m4_500")
    write_json(results_dir("k_verified") / "build.json", rep, {"source": str(A_CSV.relative_to(REPO))})
    print(json.dumps({k: ({kk: (len(vv) if isinstance(vv, list) and kk == "changed_items" else vv)
                           for kk, vv in v.items()} if isinstance(v, dict) else v) for k, v in rep.items()},
                     indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
