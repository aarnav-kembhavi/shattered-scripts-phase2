"""Natural romanization of all E0 items (200 sentiment + 200 XNLI; XNLI premise and hypothesis separately).

Same model, prompt (natural_romanization_v1), temperature 0 and cache as the FLORES run. Unique texts only; stops
cleanly on the daily quota (re-run to resume from the cache).

Usage: python scripts/e0b_natural.py
Outputs: data/processed/natural_e0_v1.jsonl (native -> natural, one row per unique text),
         data/annotation/natural_romanization_e0_check_v1.csv (50 random, once complete),
         results/e00_gate/natural_e0.json
"""
import csv
import json
import random

from shattered.data import tasks
from shattered.llm.ratelimit import DailyQuotaExceeded
from shattered.runlog import REPO, results_dir, write_json
from shattered.translit import to_itrans
from shattered.translit.natural import MODEL, PROMPT_VERSION, make_client, romanize

OUT = REPO / "data" / "processed" / "natural_e0_v1.jsonl"


def e0_texts() -> list[str]:
    texts = []
    for t in ("xnli", "sentiment"):
        for it in tasks.stratified_sample(tasks.load_task(t), 200, seed=0):
            texts += list(it["forms"]["native"].values())
    return list(dict.fromkeys(texts))  # unique, order-preserving


def load_map() -> dict:
    if not OUT.exists():
        return {}
    return {r["native"]: r for r in map(json.loads, OUT.open(encoding="utf-8"))}


def main() -> None:
    texts = e0_texts()
    client = make_client(rpm=12, rpd=1000)
    rows, stopped = [], None
    for k, text in enumerate(texts):
        try:
            rows.append({"native": text, **romanize(client, text)})
        except DailyQuotaExceeded as e:
            stopped = str(e)[:200]
            print(f"stopped at {k}/{len(texts)} (daily quota); re-run later to resume from cache")
            break
        if k % 100 == 0:
            print(f"{k}/{len(texts)}", flush=True)
    with OUT.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    done = len(rows) == len(texts)
    if done:
        sample = random.Random(0).sample(rows, 50)
        path = REPO / "data" / "annotation" / "natural_romanization_e0_check_v1.csv"
        with path.open("w", encoding="utf-8", newline="") as f:
            w = csv.writer(f)
            w.writerow(["native", "natural", "itrans_reference", "faithful_yn", "natural_looking_1to5", "annotator",
                        "notes"])
            for r in sample:
                w.writerow([r["native"], r["natural"], to_itrans(r["native"]), "", "", "", ""])
    summary = {"n_unique_texts": len(texts), "n_done": len(rows), "complete": done, "stopped": stopped,
               "n_flagged": sum(r["flag"] for r in rows),
               "n_with_non_ascii": sum(r["non_ascii_chars"] > 0 for r in rows),
               "mean_word_ratio": sum(r["word_ratio"] for r in rows) / max(len(rows), 1)}
    write_json(results_dir("e00_gate") / "natural_e0.json", summary,
               {"model": MODEL, "prompt_version": PROMPT_VERSION, "temperature": 0})
    print(summary)


if __name__ == "__main__":
    main()
