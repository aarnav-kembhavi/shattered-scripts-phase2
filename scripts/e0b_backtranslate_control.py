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
    import json
    import numpy as np
    noise = {(x["item"], x["field"]) for x in json.load(open(REPO / "data" / "annotation" / "source_noise_v1.json"))}
    df["source_noise"] = [(i, f) in noise for i, f in zip(df["item"], df["field"])]
    df.to_csv(od / "backtranslation_with_control.csv", index=False, encoding="utf-8")
    d = df[done & ~df.source_noise]
    rng = np.random.default_rng(0)
    idx = rng.integers(0, len(d), size=(10000, len(d)))
    nat, nav = d.cosine.to_numpy(), d.cosine_native.to_numpy()

    def ci(x):
        m = x[idx].mean(1)
        return [float(np.percentile(m, 2.5)), float(np.percentile(m, 97.5))]
    fl = d[d.flag_bottom5]
    summ = {"n_with_control": int(len(d)), "n_source_noise_excluded": int((done & df.source_noise).sum()),
            "stopped": stopped,
            "cosine_natural_mean": float(nat.mean()), "cosine_natural_ci": ci(nat),
            "cosine_native_mean": float(nav.mean()), "cosine_native_ci": ci(nav),
            "native_minus_natural_mean": float((nav - nat).mean()), "native_minus_natural_ci": ci(nav - nat),
            "flagged_n": int(len(fl)), "flagged_native_also_low_(<0.4)": int((fl.cosine_native < 0.4).sum()),
            "flagged_drop_gt_0.3": int((fl.cosine_drop > 0.3).sum()),
            "all_drop_gt_0.3": int((d.cosine_drop > 0.3).sum())}
    write_json(od / "summary_control.json", summ, {"model": MODEL, "prompt": PROMPT, "temperature": 0})
    print(summ)


if __name__ == "__main__":
    main()
