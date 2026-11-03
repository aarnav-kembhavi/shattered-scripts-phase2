"""Natural romanization of FLORES Kannada with Gemini free tier (cached; resumable across days).

Usage: python scripts/e02_natural.py [--corpus flores_plus] [--limit N]
Outputs: data/processed/natural_romanization_<corpus>_v1.jsonl, results/e02_translit/natural_<corpus>.json,
         data/annotation/natural_romanization_check_v1.csv (50 random items for hand checking)
"""
import argparse
import csv
import json
import random

from shattered.data import corpora
from shattered.llm.ratelimit import DailyQuotaExceeded
from shattered.runlog import REPO, results_dir, write_json
from shattered.translit import to_itrans
from shattered.translit.natural import MODEL, PROMPT_VERSION, make_client, romanize


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", default="flores_plus")
    ap.add_argument("--limit", type=int, default=None)
    args = ap.parse_args()
    items = [(f"{split}-{i}", t) for split in ("dev", "devtest")
             for i, t in enumerate(corpora.flores_any("kan_Knda", split, args.corpus, nfc=True))]
    items = items[: args.limit] if args.limit else items
    client = make_client()
    rows, stopped = [], None
    for k, (iid, text) in enumerate(items):
        try:
            rows.append({"id": iid, "native": text, **romanize(client, text)})
        except DailyQuotaExceeded as e:
            stopped = str(e)[:300]
            print(f"stopped at {k}/{len(items)}: daily quota; re-run later (cached items are kept)")
            break
        if k % 100 == 0:
            print(f"{k}/{len(items)}", flush=True)
    out = REPO / "data" / "processed" / f"natural_romanization_{args.corpus}_{PROMPT_VERSION.split('_')[-1]}.jsonl"
    with out.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    n = len(rows)
    summary = {"n_done": n, "n_total": len(items), "stopped": stopped,
               "n_flagged": sum(r["flag"] for r in rows), "n_with_non_ascii": sum(r["non_ascii_chars"] > 0 for r in rows),
               "mean_word_ratio": sum(r["word_ratio"] for r in rows) / max(n, 1),
               "examples": rows[:5]}
    write_json(results_dir("e02_translit") / f"natural_{args.corpus}.json", summary,
               {"model": MODEL, "prompt_version": PROMPT_VERSION, "temperature": 0, "corpus": args.corpus})
    if n == len(items):  # hand-check sheet once everything is done
        sample = random.Random(0).sample(rows, min(50, n))
        path = REPO / "data" / "annotation" / "natural_romanization_check_v1.csv"
        with path.open("w", encoding="utf-8", newline="") as f:
            w = csv.writer(f)
            w.writerow(["id", "native", "natural", "itrans_reference", "faithful_yn", "natural_looking_1to5",
                        "annotator", "notes"])
            for r in sample:
                w.writerow([r["id"], r["native"], r["natural"], to_itrans(r["native"]), "", "", "", ""])
        print("wrote", path)
    print({k: v for k, v in summary.items() if k != "examples"})


if __name__ == "__main__":
    main()
