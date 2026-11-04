"""X4 R4 (registered, Phase 2 pre-registration, X4): the MDL word-assembly layer for native versus ITRANS on Bengali and Telugu Wikipedia words, the Phase 1 protocol (scripts/m14_full.py: the 300 most frequent
letter-only words with at least 30 occurrences, the first 30 occurrences each, sentences of 5 to 25 words and at most 250 characters, articles in the seed-0 order of Wikipedia 20231101), the Phase 1 functions
(`mdl_curve`, `bootstrap_mdl_detok`, word-clustered paired bootstrap of `m14_gate2.paired_mdl`). Models: Qwen3-1.7B, Qwen3.5-2B, Sarvam-1, Gemma 4 E2B, Qwen2.5-1.5B (all five).
R4 (Phase 1 H3 text): the sign of (ITRANS - native MDL detok layer) matches the sign of (ITRANS - native tokens per word), with the CI excluding 0, applied only in models where native and ITRANS tokens per word
differ by at least 1 on that language's probe words; effect in all such models but one and at least two; fewer than three qualifying models: uninformative; models that drop out are reported with their difference.
Usage: python scripts/x4_mdl.py score <bn|te> | analyse        Output: results/phase2/x4/<lang>/mdl/ and r4.json"""
import json
import random
import re
import sys
import time
import unicodedata
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import m14_full as M  # noqa: E402
import m14_gate2 as G  # noqa: E402

from shattered.data.corpora import wikipedia  # noqa: E402
from shattered.interp.collect import Sentence, collect  # noqa: E402
from shattered.interp.load import load  # noqa: E402
from shattered.interp.probes import bootstrap_mdl_detok, mdl_curve  # noqa: E402
from shattered.runlog import REPO, results_dir, write_json  # noqa: E402
from shattered.translit.scheme import SCRIPTS, itrans_for  # noqa: E402

CODES = {"bn": "ben_Beng", "te": "tel_Telu"}
WORD = {"bn": re.compile("[ঀ-৿‌‍]{2,}"), "te": re.compile("[ఀ-౿‌‍]{2,}")}
MODELS = ["qwen3-1.7b", "qwen3.5-2b", "sarvam-1", "gemma4-e2b", "qwen2.5-1.5b"]


def build(lang: str) -> dict:
    arts = wikipedia(lang, shard="00000-of-00002") + wikipedia(lang, shard="00001-of-00002")  # Bengali and Telugu Wikipedia have two shards; both are used (as x4_fetch.py)
    random.Random(0).shuffle(arts)
    sents = []
    for a in arts:
        for para in a.split("\n"):
            for s in M.SENT_SPLIT.split(para.strip()):
                s = unicodedata.normalize("NFC", s.strip())
                if 5 <= len(s.split()) <= 25 and len(s) <= 250:
                    sents.append(s)
        if len(sents) > 400_000:
            break
    words, sel = M.select(sents, WORD[lang])
    return {"words": words, "sentences": [sents[i] for i, _ in sel], "targets": [ws for _, ws in sel], "params": {"n_words": M.N_WORDS, "occ": M.OCC, "articles": len(arts)}}


def inputs(W: dict, lang: str, form: str) -> list[Sentence]:
    it = itrans_for(SCRIPTS[CODES[lang]])
    out = []
    for i, (s, t) in enumerate(zip(W["sentences"], W["targets"])):
        if form == "itrans":
            s, t = " ".join(it.encode(w) for w in s.split()), [it.encode(w) for w in t]
        out.append(Sentence(f"{lang}{i}", s, t))
    return out


def measure(acts: dict, W: dict, lang: str, form: str) -> tuple[dict, dict]:
    it = itrans_for(SCRIPTS[CODES[lang]])
    meta = [json.loads(m) for m in acts["word_meta"]]
    inv = {it.encode(w): w for w in W["words"]} if form == "itrans" else {w: w for w in W["words"]}
    labels = np.array([W["words"].index(inv[m[1]]) for m in meta])
    S = acts["word_states"]
    ntok = np.array([m[2] for m in meta])
    mdl = mdl_curve(S, labels, seed=0)
    order = np.random.default_rng(0).permutation(len(labels))
    res = {"n_occ": len(labels), "n_words": len(W["words"]), "tokens_per_word_mean": float(ntok.mean()), "mdl": bootstrap_mdl_detok(mdl["costs"], len(W["words"])), "n_layers": int(S.shape[1])}
    return res, {"mdl_costs": mdl["costs"].astype(np.float32), "mdl_order": order, "labels": labels, "probe_train_mask": np.zeros(len(labels), bool), "in_e0": np.zeros(len(labels), bool)}


def score(lang: str) -> None:
    import torch
    out = results_dir(f"phase2/x4/{lang}/mdl")
    wp = out / "words.json"
    if wp.exists():
        W = json.load(open(wp, encoding="utf-8"))
    else:
        W = build(lang)
        wp.write_text(json.dumps(W, ensure_ascii=False), encoding="utf-8")
    print(lang, "words", len(W["words"]), "contexts", len(W["sentences"]), flush=True)
    for m in MODELS:
        if all((out / m / f"{f}.json").exists() for f in ("native", "itrans")):
            continue
        model, tok = load(m, "cuda")
        for f in ("native", "itrans"):
            if (out / m / f"{f}.json").exists():
                continue
            t0 = time.time()
            a = collect(model, tok, inputs(W, lang, f))
            acts = {"word_states": a["word_states"], "word_meta": np.asarray([json.dumps(x, ensure_ascii=False) for x in a["word_meta"]])}
            res, items = measure(acts, W, lang, f)
            (out / m).mkdir(exist_ok=True)
            np.savez(out / m / f"items_{f}.npz", **items)
            (out / m / f"{f}.json").write_text(json.dumps(res), encoding="utf-8")
            print(lang, m, f, "detok layer", res["mdl"]["detok_layer"], "tokens/word", round(res["tokens_per_word_mean"], 2), f"{time.time() - t0:.0f}s", flush=True)
        del model
        torch.cuda.empty_cache()


def analyse() -> None:
    for lang in CODES:
        base = REPO / "results" / "phase2" / "x4" / lang / "mdl"
        rows = {}
        for m in MODELS:
            d = {"res": {f: json.load(open(base / m / f"{f}.json", encoding="utf-8")) for f in ("native", "itrans")},
                 "items": {f: dict(np.load(base / m / f"items_{f}.npz")) for f in ("native", "itrans")}}
            d["L"] = d["res"]["native"]["n_layers"]
            p = G.paired_mdl(d)
            tn, ti = d["res"]["native"]["tokens_per_word_mean"], d["res"]["itrans"]["tokens_per_word_mean"]
            lo, hi = p["diff_ci"]
            sign_ci = 1 if lo > 0 else -1 if hi < 0 else 0
            rows[m] = {"native_layer": p["native"], "itrans_layer": p["itrans"], "itrans_minus_native": p["diff"], "ci95": [float(lo), float(hi)],
                       "tokens_per_word": {"native": tn, "itrans": ti, "diff": ti - tn}, "qualifies": bool(abs(ti - tn) >= 1), "expected_sign": int(np.sign(ti - tn)), "ci_sign": sign_ci,
                       "effect": bool(abs(ti - tn) >= 1 and sign_ci == int(np.sign(ti - tn)) and sign_ci != 0)}
        q = [m for m, v in rows.items() if v["qualifies"]]
        e = [m for m in q if rows[m]["effect"]]
        verdict = "uninformative (fewer than three qualifying models)" if len(q) < 3 else "supported" if len(e) >= len(q) - 1 and len(e) >= 2 else "not supported"
        write_json(REPO / "results" / "phase2" / "x4" / lang / "r4.json", {"language": lang, "models": rows, "qualifying": q, "effect_in": e, "R4": verdict}, {"registration": "RESULTS.md X4 (R4)"})
        print(lang, verdict, {m: (v["native_layer"], v["itrans_layer"], round(v["tokens_per_word"]["diff"], 2), v["effect"]) for m, v in rows.items()})


if __name__ == "__main__":
    if sys.argv[1] == "score":
        score(sys.argv[2])
    else:
        analyse()
