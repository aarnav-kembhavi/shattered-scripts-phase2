"""X1 T3 (exploratory): the T2 instruction translated into Kannada script, label words and field names kept in English.

Registered in RESULTS.md (2026-11-01, X1): drafted with gemini-3.5-flash-lite, temperature 0, cached; about 3 requests; written to
src/shattered/llm/templates/e0_*_v3.txt; sha256 recorded in results/phase2/x1/t3_templates.json; flagged for one native-speaker
annotator to verify; frozen before any T3 scoring. If the annotator has not verified it before T3 is scored, every T3 result is
labelled "instruction not verified".

Usage: python scripts/x1_t3_draft.py   (API; 3 requests, cached; refuses to overwrite an existing v3 template)
"""
import hashlib
import json
import sys

from shattered.llm.client import LLMClient
from shattered.runlog import REPO, write_json

TEMPL = REPO / "src" / "shattered" / "llm" / "templates"
MODEL = "gemini-3.5-flash-lite"
LABEL_WORDS = {"sentiment": ["negative", "positive"], "xnli": ["no", "maybe", "yes"],
               "sib": ["geography", "entertainment", "health", "sports", "politics", "travel", "science"]}
PROMPT = ("Translate the following English instruction into Kannada (Kannada script). Keep the English words {words} exactly as "
          "written in English, do not translate or transliterate them. Output only the Kannada sentence, with no quotation marks "
          "and no explanation.\n\nInstruction: {instr}")


def t2_question(task: str) -> str:
    line = (TEMPL / f"e0_{task}_v2.txt").read_text(encoding="utf-8").split("\n")[-2]
    assert line.startswith("Question: ")
    return line[len("Question: "):]


def main() -> None:
    client = LLMClient("gemini", MODEL, rpm=12, rpd=1000)
    out = {}
    for task, words in LABEL_WORDS.items():
        path = TEMPL / f"e0_{task}_v3.txt"
        if path.exists():
            raise SystemExit(f"{path.name} exists; T3 is frozen, not overwriting")
        v2 = (TEMPL / f"e0_{task}_v2.txt").read_text(encoding="utf-8")
        instr = t2_question(task)
        r = client.generate(PROMPT.format(words=", ".join(f'"{w}"' for w in words), instr=instr), max_tokens=512, temperature=0.0)
        kn = r.text.strip()
        has_kn = any("ಀ" <= c <= "೿" for c in kn)
        missing = [w for w in words if w not in kn]
        out[task] = {"t2_instruction": instr, "kannada_draft": kn, "contains_kannada_script": has_kn,
                     "label_words_missing_from_draft": missing, "cached": r.cached, "finish_reason": r.finish_reason}
        if not has_kn or missing or "\n" in kn:
            out[task]["status"] = "REJECTED: not written (check the draft; no silent retry)"
            continue
        text = v2.replace("Question: " + instr, "Question: " + kn)
        assert text != v2 and text.count("Question: ") == 1
        path.write_bytes(text.encode("utf-8"))  # no trailing newline, as the v1 and v2 files
        out[task]["status"] = "written"
        out[task]["sha256_prefix"] = hashlib.sha256(path.read_bytes()).hexdigest()[:16]
        out[task]["file"] = path.name
    write_json(REPO / "results" / "phase2" / "x1" / "t3_templates.json",
               {"templates": out, "verified_by_native_speaker": False,
                "label": "instruction not verified (until a native-speaker annotator verifies it; see RESULTS.md)"},
               {"model": MODEL, "temperature": 0.0, "prompt": PROMPT, "registered": "RESULTS.md 2026-11-01 (X1, T3)"})
    print(json.dumps(out, indent=1, ensure_ascii=False))
    if any(v["status"] != "written" for v in out.values()):
        sys.exit(1)


if __name__ == "__main__":
    main()
