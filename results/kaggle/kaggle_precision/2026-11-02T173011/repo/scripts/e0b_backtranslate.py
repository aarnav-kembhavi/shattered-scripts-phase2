"""Automatic meaning check for E0 natural romanization: back-translate every romanized text into English with a
different free model (Groq, openai/gpt-oss-120b, temperature 0, cached, prompt backtranslate_v1) and compare it with
the original English source by sentence-embedding cosine (sentence-transformers/all-mpnet-base-v2, mean pooling).
The bottom 5% are flagged for a human glance.

Usage: python scripts/e0b_backtranslate.py   (resumes from the cache; covers whatever natural texts exist)
Outputs: results/e0b_natural_check/{backtranslation.csv, flagged_bottom5.csv, summary.json}
"""
import json

import numpy as np
import pandas as pd
import torch

from shattered.data import tasks
from shattered.llm.client import LLMClient
from shattered.llm.ratelimit import DailyQuotaExceeded
from shattered.runlog import REPO, results_dir, write_json
from shattered.translit.natural import defective

MODEL, PROMPT = "openai/gpt-oss-120b", "backtranslate_v1"
EMB, EMB_REV = "sentence-transformers/all-mpnet-base-v2", "e8c3b32edf"


def embed(texts: list[str]) -> np.ndarray:
    from transformers import AutoModel, AutoTokenizer
    tok = AutoTokenizer.from_pretrained(EMB)
    m = AutoModel.from_pretrained(EMB).eval()
    out = []
    with torch.no_grad():
        for i in range(0, len(texts), 64):
            b = tok(texts[i:i + 64], padding=True, truncation=True, max_length=384, return_tensors="pt")
            h = m(**b).last_hidden_state
            v = (h * b.attention_mask[..., None]).sum(1) / b.attention_mask.sum(1, keepdim=True)
            out.append(torch.nn.functional.normalize(v, dim=-1).numpy())
    return np.concatenate(out)


def main() -> None:
    template = (REPO / "src" / "shattered" / "llm" / "templates" / f"{PROMPT}.txt").read_text(encoding="utf-8")
    rows = [json.loads(x) for x in open(REPO / "data" / "processed" / "natural_e0_v1.jsonl", encoding="utf-8")]
    eng = {}
    for t in ("xnli", "sentiment"):
        for it in tasks.stratified_sample(tasks.load_task(t), 200, seed=0):
            for k, v in it["forms"]["native"].items():
                eng.setdefault(v, (it["id"], k, it["forms"]["english"][k]))
    client = LLMClient("groq", MODEL, rpm=20, rpd=950)
    out, stopped = [], None
    for k, r in enumerate(rows):
        try:
            resp = client.generate(template.format(text=r["natural"]), max_tokens=1024, temperature=0.0,
                                   reasoning_effort="low")
        except DailyQuotaExceeded as e:
            stopped = str(e)[:200]
            print(f"stopped at {k}/{len(rows)} (daily quota)")
            break
        iid, field, en = eng[r["native"]]
        out.append({"item": iid, "field": field, "native": r["native"], "natural": r["natural"],
                    "defective": defective(r), "english_source": en, "back_translation": resp.text.strip()})
        if k % 100 == 0:
            print(f"{k}/{len(rows)}", flush=True)
    df = pd.DataFrame(out)
    a, b = embed(df.english_source.tolist()), embed(df.back_translation.tolist())
    df["cosine"] = (a * b).sum(1)
    cut = df.cosine.quantile(0.05)
    df["flag_bottom5"] = df.cosine <= cut
    od = results_dir("e0b_natural_check")
    df.to_csv(od / "backtranslation.csv", index=False, encoding="utf-8")
    df[df.flag_bottom5].sort_values("cosine").to_csv(od / "flagged_bottom5.csv", index=False, encoding="utf-8")
    summ = {"n": len(df), "n_natural_total": len(rows), "stopped": stopped, "cosine_mean": float(df.cosine.mean()),
            "cosine_median": float(df.cosine.median()), "cosine_p05": float(cut), "n_flagged": int(df.flag_bottom5.sum()),
            "n_defective_in_set": int(df.defective.sum())}
    write_json(od / "summary.json", summ, {"model": MODEL, "prompt": PROMPT, "temperature": 0,
                                          "reasoning_effort": "low", "embedding": EMB, "embedding_rev": EMB_REV})
    print(summ)


if __name__ == "__main__":
    main()
