"""X14 black-box hosted models (Amendment 2; exploratory, no verdict): SIB-200 classification by generation with the registered prompt,
temperature 0, 20 new tokens, exact (case-insensitive) category match, unparsed = wrong (share reported). Models: results/phase2/x14/model_choice.json
(rule applied 2026-11-02). Forms native, ITRANS, lossy on 1,004 items, natural on the 257 items with a clean natural romanization. Items are visited in a
fixed seeded order (default_rng(14)) and all forms of an item are asked together, so any prefix of the run is a paired sample. Every response is cached
(sqlite cache keyed by prompt); raw rows are appended to results/phase2/x14/raw/<model>.jsonl; failures and rate limits are logged, never silently retried
as results. Exit 3 = all models at their daily cap.
Usage: python scripts/x14_run.py pilot | run | report
"""
import json
import re
import sys
import time

import numpy as np

from shattered.llm.client import LLMClient
from shattered.llm.ratelimit import DailyQuotaExceeded
from shattered.runlog import REPO, results_dir, write_json

sys.path.insert(0, str(REPO / "scripts"))
import e0c_sib as e0c  # noqa: E402
import l_ladder as lad  # noqa: E402

PROMPT = ("Classify the topic of the following Kannada text. Answer with exactly one of: science/technology, travel, politics, sports, health, "
          "entertainment, geography.\n\nText: {text}\nTopic:")
CATS = e0c.CATS
OUT = REPO / "results" / "phase2" / "x14"
LIMITS = {"groq": {"rpm": 20, "rpd": 900}, "openrouter": {"rpm": 12, "rpd": 22}}  # own caps below the free tiers (OpenRouter free: about 50 a day per account)
FORMS = ["native", "itrans", "lossy", "natural"]
# Per-model call settings. Registered: 20 new tokens. gpt-oss-120b is a reasoning model whose reasoning consumes the 20 tokens (pilot 2026-11-02:
# 5 of 5 empty, finish "length"), so it is called with reasoning_effort "low" and 400 tokens; the answer is still parsed by the same exact match
# (deviation X14-D1, logged in RESULTS.md). The other models use the registered 20 tokens.
SETTINGS = {"openai/gpt-oss-120b": {"max_tokens": 400, "reasoning_effort": "low"}}


def parse(text: str) -> int | None:
    t = re.sub(r"[\s.\"'*`]+$", "", text.strip().lower())
    t = re.sub(r"^[\s\"'*`]+", "", t)
    return CATS.index(t) if t in CATS else None


def items() -> list[dict]:
    its = e0c.load_items()["sib"]
    nat = {it["id"]: it["forms"]["natural257"]["text"] for it in lad.sib257_items()["sib"]}
    order = np.random.default_rng(14).permutation(len(its))
    rows = []
    for j in order:
        it = its[int(j)]
        r = {"id": it["id"], "label": it["label"], "native": it["forms"]["native"]["text"], "itrans": it["forms"]["itrans"]["text"],
             "lossy": it["forms"]["lossy"]["text"]}
        if it["id"] in nat:
            r["natural"] = nat[it["id"]]
        rows.append(r)
    return rows


def models() -> list[dict]:
    return json.loads((OUT / "model_choice.json").read_text(encoding="utf-8"))["chosen"]


def clients() -> dict:
    return {m["id"]: (m, LLMClient(m["provider"], m["id"].replace(":free", "") if m["provider"] == "groq" else m["id"], rpm=LIMITS[m["provider"]]["rpm"],
                                   rpd=LIMITS[m["provider"]]["rpd"])) for m in models()}


def done_keys(mid: str) -> set:
    p = OUT / "raw" / (mid.replace("/", "__").replace(":", "_") + ".jsonl")
    return {(r["id"], r["form"]) for r in map(json.loads, p.open(encoding="utf-8"))} if p.exists() else set()


def run(limit_items: int | None, forms: list[str]) -> int:
    (OUT / "raw").mkdir(parents=True, exist_ok=True)
    its = items()[:limit_items]
    cl = clients()
    dead, log = set(), (OUT / "x14_errors.log").open("a", encoding="utf-8")
    progress = True
    while progress and len(dead) < len(cl):
        progress = False
        for mid, (m, c) in cl.items():
            if mid in dead:
                continue
            done = done_keys(mid)
            todo = [(it, f) for it in its for f in forms if f in it and (it["id"], f) not in done]
            if not todo:
                dead.add(mid)
                continue
            f_out = (OUT / "raw" / (mid.replace("/", "__").replace(":", "_") + ".jsonl")).open("a", encoding="utf-8")
            for it, f in todo[:10]:  # a few per round so the models advance together
                try:
                    r = c.generate(PROMPT.format(text=it[f]), temperature=0.0, **{"max_tokens": 20, **SETTINGS.get(mid, {})})
                except DailyQuotaExceeded as e:
                    log.write(f"{time.strftime('%F %T')} {mid} daily cap: {str(e)[:150]}\n")
                    dead.add(mid)
                    break
                except Exception as e:  # noqa: BLE001 - logged; the model is skipped for this run
                    log.write(f"{time.strftime('%F %T')} {mid} error: {repr(e)[:300]}\n")
                    log.flush()
                    dead.add(mid)
                    break
                pred = parse(r.text)
                f_out.write(json.dumps({"id": it["id"], "form": f, "label": it["label"], "response": r.text, "pred": pred,
                                        "finish": r.finish_reason, "cached": r.cached}, ensure_ascii=False) + "\n")
                f_out.flush()
                progress = True
            f_out.close()
    log.close()
    return 3 if dead and any(done_keys(mid) != set() for mid in cl) and any(
        len([1 for it in its for f in forms if f in it and (it["id"], f) not in done_keys(mid)]) for mid in cl) else 0


def report() -> None:
    rep = {}
    for m in models():
        p = OUT / "raw" / (m["id"].replace("/", "__").replace(":", "_") + ".jsonl")
        if not p.exists():
            continue
        R = [json.loads(l) for l in p.open(encoding="utf-8")]
        per = {}
        for f in FORMS:
            rf = [r for r in R if r["form"] == f]
            if rf:
                per[f] = {"n": len(rf), "acc": float(np.mean([r["pred"] == r["label"] for r in rf])), "unparsed_share": float(np.mean([r["pred"] is None for r in rf]))}
        rep[m["id"]] = per
    write_json(OUT / "x14_report_partial.json", rep, {"status": "partial until all items are done; exploratory, no verdict", "registered": "Amendment 2 X14"})
    print(json.dumps(rep, indent=1))


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "pilot":
        run(5, ["native"])
        report()
    elif cmd == "run":
        sys.exit(run(None, FORMS))
    else:
        report()
