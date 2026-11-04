"""X14 model choice (Amendment 2, rule applied and logged on the day of the first call): list the free text models of Groq and OpenRouter,
take up to 3 with the largest STATED parameter counts (a number followed by b in the model id or name; mixture-of-experts: the total) from
different families. No Gemini-family model is used for natural text (all X14 forms involving natural text exclude the Gemini family; the
family is also excluded from every other form, so one model set serves all). Writes results/phase2/x14/model_choice.json (the full listing).
Usage: python scripts/x14_models.py
"""
import json
import os
import re
import urllib.request

from dotenv import load_dotenv

from shattered.runlog import REPO, results_dir, write_json

load_dotenv(REPO / ".env")


def get(url: str, key: str) -> dict:
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {key}", "User-Agent": "shattered-x14"})
    return json.load(urllib.request.urlopen(req, timeout=60))


def params_b(s: str) -> float | None:
    m = [float(x) for x in re.findall(r"(?<![\w.])(\d+(?:\.\d+)?)\s*[bB](?![a-zA-Z])", s.replace("-", " ").replace("_", " "))]
    return max(m) if m else None


def family(mid: str) -> str:
    s = mid.lower()
    for k in ("gemini", "gemma", "llama", "qwen", "deepseek", "mistral", "mixtral", "gpt", "kimi", "glm", "nemotron", "phi", "hermes", "minimax",
              "command", "yi", "olmo", "granite", "arcee", "trinity", "step", "ling", "ring"):
        if k in s:
            return "meta-llama" if k == "llama" else k
    return s.split("/")[-1].split("-")[0]


def main() -> None:
    rows = []
    g = get("https://api.groq.com/openai/v1/models", os.environ["GROQ_API_KEY"])
    for m in g["data"]:
        mid = m["id"]
        if any(x in mid.lower() for x in ("whisper", "tts", "guard", "embed", "orpheus", "playai", "distil-whisper")):
            continue
        rows.append({"provider": "groq", "id": mid, "stated_params_b": params_b(mid), "context": m.get("context_window"), "active": m.get("active")})
    o = get("https://openrouter.ai/api/v1/models", os.environ["OPENROUTER_API_KEY"])
    for m in o["data"]:
        p = m.get("pricing", {})
        if float(p.get("prompt", 1)) == 0 and float(p.get("completion", 1)) == 0 and "text" in (m.get("architecture", {}).get("output_modalities") or ["text"]):
            rows.append({"provider": "openrouter", "id": m["id"], "stated_params_b": params_b(m["id"] + " " + m.get("name", "")),
                         "context": m.get("context_length"), "active": True})
    for r in rows:
        r["family"] = family(r["id"])
    keys = {"groq": bool(os.environ.get("GROQ_API_KEY")), "openrouter": bool(os.environ.get("OPENROUTER_API_KEY"))}
    for r in rows:
        r["callable"] = keys[r["provider"]]  # a provider without a key in .env cannot be called on the day of the first call
    ok = [r for r in rows if r["callable"] and r["stated_params_b"] and r["family"] != "gemini" and r.get("active", True)]
    ok.sort(key=lambda r: -r["stated_params_b"])
    chosen, fams = [], set()
    for r in ok:
        if r["family"] in fams:
            continue
        chosen.append(r)
        fams.add(r["family"])
        if len(chosen) == 3:
            break
    write_json(results_dir("phase2/x14") / "model_choice.json", {"chosen": chosen, "listing": rows, "n_listed": len(rows)},
               {"rule": "up to 3 largest stated parameter counts from different families; Gemini family excluded; Gemma is not Gemini-family under the literal rule and is eligible (flagged: same lab as the natural-romanization generator)",
                "registered": "RESULTS.md Amendment 2 X14"})
    print(json.dumps(chosen, indent=1))
    print(len(rows), "listed;", sum(1 for r in rows if r["stated_params_b"] is None), "without a stated parameter count")


if __name__ == "__main__":
    main()
