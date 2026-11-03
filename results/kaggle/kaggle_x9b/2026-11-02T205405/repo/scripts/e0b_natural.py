"""Natural romanization of all E0 items (200 sentiment + 200 XNLI; XNLI premise and hypothesis separately).

Same model, prompt (natural_romanization_v1), temperature 0 and cache as the FLORES run. Unique texts only; stops
cleanly on the daily quota (re-run to resume from the cache).

Outputs that violate the prompt (non-ASCII characters not present in the source: leftover Kannada/other Indic script,
diacritics, IPA) are re-asked with the same model, prompt and temperature (attempt 2, then 3; `attempt` changes only
the cache key). The first attempt is kept in the row. Rows still defective after attempt 3 are kept and marked.

Usage: python scripts/e0b_natural.py
Outputs: data/processed/natural_e0_v1.jsonl (native -> natural, one row per unique text),
         data/processed/natural_e0_regen_queue_v1.json, results/e00_gate/natural_e0.json
"""
import json

from shattered.data import tasks
from shattered.llm.ratelimit import DailyQuotaExceeded
from shattered.runlog import REPO, results_dir, write_json
from shattered.translit.natural import MODEL, PROMPT_VERSION, defective, make_client, romanize

OUT = REPO / "data" / "processed" / "natural_e0_v1.jsonl"
QUEUE = REPO / "data" / "processed" / "natural_e0_regen_queue_v1.json"
MAX_ATTEMPTS = 3


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
    previous = load_map()  # kept for texts not reached this run (e.g. after a quota stop), so nothing is truncated
    client = make_client(rpm=12, rpd=1000)
    rows, stopped = [], None
    for k, text in enumerate(texts):
        try:
            row = {"native": text, **romanize(client, text)}
            first = row
            while defective(row) and row["attempt"] < MAX_ATTEMPTS:
                row = {"native": text, **romanize(client, text, attempt=row["attempt"] + 1)}
            if row is not first:
                row["first_attempt_natural"] = first["natural"]
            row["defective"] = defective(row)
            rows.append(row)
        except DailyQuotaExceeded as e:
            stopped = str(e)[:200]
            print(f"stopped at {k}/{len(texts)} (daily quota); re-run later to resume from cache")
            rows += [previous[t] for t in texts[k:] if t in previous]
            break
        if k % 100 == 0:
            print(f"{k}/{len(texts)}", flush=True)
    with OUT.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    queue = [{"index": i, "native": r["native"], "natural": r["natural"], "attempt": r.get("attempt", 1),
              "bad_chars": "".join(sorted({c for c in r["natural"] if "ऀ" <= c <= "෿"
                                          or (not c.isascii() and c not in r["native"])}))} for i, r in enumerate(rows) if defective(r)]
    QUEUE.write_text(json.dumps(queue, ensure_ascii=False, indent=1), encoding="utf-8")
    done = stopped is None and len(rows) == len(texts)
    summary = {"n_unique_texts": len(texts), "n_done": len(rows), "complete": done, "stopped": stopped,
               "n_flagged": sum(r["flag"] for r in rows),
               "n_with_non_ascii": sum(r["non_ascii_chars"] > 0 for r in rows),
               "n_regenerated": sum("first_attempt_natural" in r for r in rows),
               "n_defective_after_retries": len(queue),
               "mean_word_ratio": sum(r["word_ratio"] for r in rows) / max(len(rows), 1)}
    write_json(results_dir("e00_gate") / "natural_e0.json", summary,
               {"model": MODEL, "prompt_version": PROMPT_VERSION, "temperature": 0, "max_attempts": MAX_ATTEMPTS})
    print(summary)


if __name__ == "__main__":
    main()
