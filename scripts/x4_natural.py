"""X4 natural romanization drafts for Bengali and Telugu (registered in RESULTS.md, Phase 2 pre-registration, X4 "natural").

Model gemini-3.5-flash-lite, temperature 0, cached, prompt natural_romanization_v1 with only the language name changed (templates
natural_romanization_bn_v1.txt / _te_v1.txt, generated here by replacing "Kannada" with "Bengali" / "Telugu", three occurrences), defect check =
shattered.translit.natural.defective (any Indic-script character U+0900-U+0DFF or a new non-ASCII character), attempts 2-3, then excluded and
counted. Sentences: the same 500 FLORES+ dev+devtest indices as the Kannada M4c sample (default_rng(0) choice of 2,009); the 496 that were
retained for Kannada are the primary set, the 4 Kannada-defective ids are kept only if clean here (n reported).
Batching is used only if the registered pilot (30 Kannada sentences with cached unbatched outputs, 10 per request) reproduces at least 28 of 30
exactly; the decision is logged either way (results/phase2/x4/natural/batching_pilot.json).
Usage: python scripts/x4_natural.py pilot | romanize bn|te | status
"""
import json
import re
import sys

import numpy as np

from shattered.data.corpora import flores_any
from shattered.llm.ratelimit import DailyQuotaExceeded
from shattered.runlog import REPO, commit, results_dir, tmp_path, write_json
from shattered.translit.natural import MODEL, PROMPT_VERSION, TEMPLATE_DIR, defective, make_client, romanize

KN_OUT = REPO / "data" / "processed" / "natural_flores_m4_500_v1.jsonl"
LANG = {"bn": ("Bengali", "ben_Beng"), "te": ("Telugu", "tel_Telu")}
RPD = 6000  # own daily cap; raised from 480 on 2026-11-04 (billing enabled on the Gemini key, the lead author); rpm raised to 60 in make_client call below
BATCH = 10
OUTD = REPO / "results" / "phase2" / "x4" / "natural"


def template(lang: str) -> str:
    name = LANG[lang][0]
    base = (TEMPLATE_DIR / f"{PROMPT_VERSION}.txt").read_text(encoding="utf-8")
    assert base.count("Kannada") == 3, base.count("Kannada")
    ver = f"natural_romanization_{lang}_v1"
    (TEMPLATE_DIR / f"{ver}.txt").write_text(base.replace("Kannada", name), encoding="utf-8", newline="\n")
    return ver


def sample_idx() -> np.ndarray:
    return np.sort(np.random.default_rng(0).choice(2009, 500, replace=False))


def batch_prompt(sents: list[str], name: str) -> str:
    head = (f"Romanize the following {name} sentences the way an ordinary {name} speaker would type them in Latin script on a phone: informal spelling, no diacritics, "
            "no special symbols.\nKeep every word and the original word order of each sentence. Do not translate, explain, add or remove anything. Keep numbers, "
            "punctuation and any English words as they are.\nOutput only the romanized sentences, one per line, each starting with its number and a period, in the same order.\n\n"
            f"{name} sentences:\n")
    return head + "\n".join(f"{i + 1}. {s}" for i, s in enumerate(sents))


def parse_batch(text: str, n: int) -> list[str] | None:
    rows = {}
    for line in text.strip().splitlines():
        m = re.match(r"\s*(\d+)\.\s*(.*)$", line)
        if m:
            rows[int(m.group(1))] = m.group(2).strip()
    return [rows[i + 1] for i in range(n)] if all(i + 1 in rows for i in range(n)) else None


def pilot() -> None:
    client = make_client(rpm=60, rpd=RPD)
    kn = [json.loads(l) for l in KN_OUT.open(encoding="utf-8")]
    kn = [r for r in kn if not r["defective"] and r["attempt"] == 1][:30]
    assert len(kn) == 30
    matches, outs = 0, []
    for b in range(0, 30, BATCH):
        grp = kn[b:b + BATCH]
        r = client.generate(batch_prompt([g["native"] for g in grp], "Kannada"), max_tokens=2048, temperature=0.0)
        parsed = parse_batch(r.text, len(grp))
        for k, g in enumerate(grp):
            hit = parsed is not None and parsed[k].strip() == g["natural"].strip()
            matches += int(hit)
            outs.append({"index": g["index"], "unbatched": g["natural"], "batched": parsed[k] if parsed else None, "exact": hit})
    decision = "batched" if matches >= 28 else "unbatched"
    write_json(results_dir("phase2/x4/natural") / "batching_pilot.json",
               {"exact_matches": matches, "of": 30, "threshold": 28, "decision": decision, "rows": outs},
               {"model": MODEL, "batch_size": BATCH, "registered": "RESULTS.md X4 batching rule"})
    print({"exact_matches": matches, "decision": decision})


def decision() -> str:
    p = OUTD / "batching_pilot.json"
    return json.loads(p.read_text(encoding="utf-8"))["decision"] if p.exists() else "unbatched"


def do_romanize(lang: str) -> None:
    name, code = LANG[lang]
    ver = template(lang)
    F = flores_any(code, "dev", "flores_plus", nfc=True) + flores_any(code, "devtest", "flores_plus", nfc=True)
    assert len(F) == 2009
    kn_ok = {r["index"]: not r["defective"] for r in map(json.loads, KN_OUT.open(encoding="utf-8"))}
    out = REPO / "data" / "processed" / f"natural_flores_{lang}_x4_v1.jsonl"
    client = make_client(rpm=60, rpd=RPD)
    done = {r["index"]: r for r in map(json.loads, out.open(encoding="utf-8"))} if out.exists() else {}
    stopped, mode = None, decision()
    todo = [int(i) for i in sample_idx() if not (int(i) in done and not done[int(i)]["defective"])]
    if mode == "batched":  # first attempt in batches; anything unparsed or defective continues unbatched below
        for b in range(0, len(todo), BATCH):
            grp = [i for i in todo[b:b + BATCH] if i not in done]
            if not grp:
                continue
            try:
                r = client.generate(batch_prompt([F[i] for i in grp], name), max_tokens=2048, temperature=0.0)
            except DailyQuotaExceeded as e:
                stopped = str(e)[:200]
                break
            parsed = parse_batch(r.text, len(grp))
            for k, i in enumerate(grp if parsed else []):
                row = {"index": i, "native": F[i], "natural": parsed[k], "attempt": 1, "batched": True}
                row["defective"] = defective(row)
                done[i] = row
    for i in todo:
        if stopped:
            break
        if i in done and not done[i]["defective"]:
            continue
        for attempt in range(done[i]["attempt"] + 1 if i in done else 1, 4):
            try:
                r = romanize(client, F[i], version=ver, attempt=attempt)
            except DailyQuotaExceeded as e:
                stopped = str(e)[:200]
                break
            row = {"index": i, "native": F[i], **r, "batched": False}
            row["defective"] = defective(row)
            done[i] = row
            if not row["defective"]:
                break
    with tmp_path(out).open("w", encoding="utf-8") as f:
        for i in sorted(done):
            f.write(json.dumps({**done[i], "kn_retained": kn_ok.get(i)}, ensure_ascii=False) + "\n")
    commit(tmp_path(out), out)
    n_def = sum(r["defective"] for r in done.values())
    s = {"lang": lang, "mode": mode, "n_done": len(done), "n_target": 500, "n_defective_after_retries": n_def,
         "primary_496_clean": sum(1 for i, r in done.items() if kn_ok.get(i) and not r["defective"]),
         "kn_defective_kept_if_clean": sum(1 for i, r in done.items() if not kn_ok.get(i) and not r["defective"]),
         "stopped": stopped, "complete": len(done) == 500 and stopped is None}
    (OUTD).mkdir(parents=True, exist_ok=True)
    (OUTD / f"status_{lang}.json").write_text(json.dumps(s, indent=1))
    print(s)


if __name__ == "__main__":
    cmd = sys.argv[1]
    {"pilot": pilot}.get(cmd, lambda: do_romanize(sys.argv[2]))()
