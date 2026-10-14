"""Control for the back-translation check: back-translate the native-script Kannada of each E0 text with the same
model and settings, so that low natural-vs-English similarity can be attributed to the romanization (natural much
lower than native) or to the source translation / back-translator (both low). Flagged items first, then the rest, as
far as the daily quota allows (re-run to continue).

Usage: python scripts/e0b_backtranslate_control.py
Outputs: results/e0b_natural_check/{backtranslation_with_control.csv, summary_control.json}
"""
import pandas as pd

from shattered.llm.client import LLMClient
from shattered.llm.ratelimit import DailyQuotaExceeded
from shattered.runlog import REPO, results_dir, write_json

import sys
sys.path.insert(0, str(REPO / "scripts"))
from e0b_backtranslate import MODEL, embed  # noqa: E402

PROMPT = "backtranslate_native_v1"


def main() -> None:
    od = results_dir("e0b_natural_check")
    df = pd.read_csv(od / "backtranslation.csv")
    template = (REPO / "src" / "shattered" / "llm" / "templates" / f"{PROMPT}.txt").read_text(encoding="utf-8")
    client = LLMClient("groq", MODEL, rpm=20, rpd=990)
    order = list(df.index[df.flag_bottom5]) + list(df.index[~df.flag_bottom5])
    bt, stopped = {}, None
    for i in order:
        try:
            r = client.generate(template.format(text=df.native[i]), max_tokens=1024, temperature=0.0,
                                reasoning_effort="low")
        except DailyQuotaExceeded as e:
            stopped = str(e)[:200]
            break
        bt[i] = r.text.strip()
    df["back_translation_native"] = pd.Series(bt)
    done = df.back_translation_native.notna()
    a = embed(df.english_source[done].tolist())
    b = embed(df.back_translation_native[done].tolist())
    df.loc[done, "cosine_native"] = (a * b).sum(1)
    df["cosine_drop"] = df.cosine_native - df.cosine  # > 0: the romanized text lost meaning relative to native
    df.to_csv(od / "backtranslation_with_control.csv", index=False, encoding="utf-8")
    d = df[done]
    fl = d[d.flag_bottom5]
    summ = {"n_with_control": int(done.sum()), "stopped": stopped,
            "cosine_natural_mean": float(d.cosine.mean()), "cosine_native_mean": float(d.cosine_native.mean()),
            "flagged_n": int(len(fl)), "flagged_native_also_low_(<0.4)": int((fl.cosine_native < 0.4).sum()),
            "flagged_drop_gt_0.3": int((fl.cosine_drop > 0.3).sum()),
            "all_drop_gt_0.3": int((d.cosine_drop > 0.3).sum())}
    write_json(od / "summary_control.json", summ, {"model": MODEL, "prompt": PROMPT, "temperature": 0})
    print(summ)


if __name__ == "__main__":
    main()
