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
    # flagged texts first (already done), then the rest in a seeded random order, so that any prefix of the
    # remainder is a random subset; texts already controlled are cache hits whatever their position
    import numpy as np
    rest = df.index[~df.flag_bottom5].to_numpy()
    order = list(df.index[df.flag_bottom5]) + list(np.random.default_rng(0).permutation(rest))
    from shattered.llm.cache import request_key
    params = {"max_tokens": 1024, "temperature": 0.0, "system": None, "reasoning_effort": "low"}
    bt, stopped = {}, None
    for i in order:
        prompt = template.format(text=df.native[i])
        if stopped:  # after a quota stop, only read what is already cached
            hit = client.cache.get(request_key("groq", MODEL, prompt, params))
            if hit is not None:
                bt[i] = hit["text"].strip()
            continue
        try:
            r = client.generate(prompt, max_tokens=1024, temperature=0.0, reasoning_effort="low")
        except Exception as e:  # noqa: BLE001 - quota/rate errors end the API phase
            if not isinstance(e, DailyQuotaExceeded) and "rate limit" not in str(e).lower() and "429" not in str(e):
                raise
            stopped = str(e)[:200]
            continue
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

    def gap(sub):
        if len(sub) < 20:
            return None
        j = np.random.default_rng(0).integers(0, len(sub), size=(10000, len(sub)))
        x = (sub.cosine_native - sub.cosine).to_numpy()
        m = x[j].mean(1)
        return {"n": int(len(sub)), "n_xnli": int(sub["item"].str.startswith("xnli").sum()),
                "native": float(sub.cosine_native.mean()), "natural": float(sub.cosine.mean()),
                "gap": float(x.mean()), "gap_ci": [float(np.percentile(m, 2.5)), float(np.percentile(m, 97.5))]}
    rand_pos = {int(i): k for k, i in enumerate(order[len(df.index[df.flag_bottom5]):])}
    nonflag = d[~d.flag_bottom5]
    # random subset = the longest prefix of the random order that is fully controlled
    k = 0
    seq = sorted(rand_pos, key=rand_pos.get)
    while k < len(seq) and seq[k] in d.index:
        k += 1
    summ = {"complete_all_paired": bool(done.sum() == len(df)),
            "gap_all_controlled_BIASED_UPWARD_by_selection": gap(d),
            "gap_nonflagged_controlled_so_far": gap(nonflag),
            "gap_random_prefix": gap(d.loc[seq[:k]]),
            "n_with_control": int(len(d)), "n_source_noise_excluded": int((done & df.source_noise).sum()),
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
