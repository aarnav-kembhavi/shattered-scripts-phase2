"""Step 2 full run: M1 (MDL probe, plain probe, erasure probe, Patchscopes) and M4 (retrieval + CKA vs English).
Pre-registered in RESULTS.md (2026-10-15, H1-H3). Forms: English, native, ITRANS.

Data
- M1 Kannada: Kannada Wikipedia 20231101 sentences (5-25 whitespace words, <= 250 chars; articles in a fixed
  seed-0 order). The N_WORDS most frequent Kannada letter-only words (>= 2 chars) with >= OCC occurrences; OCC
  occurrences each (first in scan order). ITRANS sentences are built word by word, so every occurrence has an ITRANS
  twin (checked). English: same procedure on English Wikipedia shard 0 (alphabetic words, >= 3 letters).
- M1 is also reported on the subset of words that occur in the E0 items (flag `in_e0`).
- M4: FLORES+ dev+devtest (2,009 sentences), sentence vectors = mean residual over tokens (BOS excluded).
Each (model, form, corpus) gets one forward pass; activations are cached in cache/activations/m14full/.

Usage: python scripts/m14_full.py --models qwen2.5-1.5b qwen3.5-2b sarvam-1 gemma4-e2b
Outputs (results/m14_full/): words.json, <model>/<form>.json (curves, detok layers),
         <model>/items_<form>.npz (per-item MDL costs, probe correctness, erasure, retrieval correctness),
         <model>/patchscopes_<form>.parquet, timing.json
"""
import argparse
import json
import random
import re
import time
from collections import Counter

import numpy as np
import pandas as pd
import torch

from shattered.data import tasks
from shattered.data.corpora import flores_any, wikipedia
from shattered.interp import patchscopes as ps
from shattered.interp.collect import Sentence, collect
from shattered.interp.load import load, n_layers
from shattered.interp.probes import (MDL_FRACS, PROBE, bootstrap_detok, bootstrap_mdl_detok, erasure_curve,
                                     layer_curve, mdl_curve, split_by_word)
from shattered.runlog import REPO, results_dir, write_json
from shattered.translit import to_itrans

N_WORDS, OCC = 300, 30
KN_WORD = re.compile(r"[ಀ-೥೰-೿‌‍]{2,}")  # Kannada letters/marks, no digits
EN_WORD = re.compile(r"[A-Za-z]{3,}")
SENT_SPLIT = re.compile(r"(?<=[.!?।])\s+")
FORMS = ["english", "native", "itrans"]
ACT = REPO / "cache" / "activations" / "m14full"


def wiki_sentences(lang: str) -> list[str]:
    import unicodedata
    arts = wikipedia(lang) if lang == "kn" else wikipedia("en", shard="00000-of-00041")
    random.Random(0).shuffle(arts)
    out = []
    for a in arts:
        for para in a.split("\n"):
            for s in SENT_SPLIT.split(para.strip()):
                s = unicodedata.normalize("NFC", s.strip())
                if 5 <= len(s.split()) <= 25 and len(s) <= 250:
                    out.append(s)
        if len(out) > 400_000:
            break
    return out


def select(sents: list[str], pattern) -> tuple[list[str], list[tuple[int, list[str]]]]:
    """Top N_WORDS words with >= OCC occurrences; first OCC occurrences each. Returns (words, [(sentence idx,
    targets)]) where a sentence contributes every occurrence of a still-needed word (each counted)."""
    freq = Counter(w for s in sents for w in s.split() if pattern.fullmatch(w))
    words = [w for w, n in freq.most_common() if n >= OCC][:N_WORDS]
    need, chosen = {w: OCC for w in words}, []
    for i, s in enumerate(sents):
        toks = s.split()
        hit = sorted({w for w in toks if need.get(w, 0) > 0})
        if not hit:
            continue
        # take the sentence only if it does not overshoot any word's quota
        if any(toks.count(w) > need[w] for w in hit):
            continue
        for w in hit:
            need[w] -= toks.count(w)
        chosen.append((i, hit))
        if not any(need.values()):
            break
    words = [w for w in words if need[w] == 0]
    chosen = [(i, [w for w in ws if w in set(words)]) for i, ws in chosen]
    return words, [(i, ws) for i, ws in chosen if ws]


def build_words() -> dict:
    kn, en = wiki_sentences("kn"), wiki_sentences("en")
    kn_words, kn_sel = select(kn, KN_WORD)
    en_words, en_sel = select(en, EN_WORD)
    e0_kn, e0_en = set(), set()
    for t in ("xnli", "sentiment"):
        for it in tasks.stratified_sample(tasks.load_task(t), 200, seed=0):
            for v in it["forms"]["native"].values():
                e0_kn.update(v.split())
            for v in it["forms"]["english"].values():
                e0_en.update(v.split())
    return {"kn_words": kn_words, "en_words": en_words,
            "kn_sentences": [kn[i] for i, _ in kn_sel], "kn_targets": [ws for _, ws in kn_sel],
            "en_sentences": [en[i] for i, _ in en_sel], "en_targets": [ws for _, ws in en_sel],
            "kn_in_e0": [w for w in kn_words if w in e0_kn], "en_in_e0": [w for w in en_words if w in e0_en],
            "params": {"n_words": N_WORDS, "occ": OCC, "sentence_words": [5, 25], "max_chars": 250}}


def flores_forms() -> dict:
    kn = flores_any("kan_Knda", "dev", "flores_plus", nfc=True) + flores_any("kan_Knda", "devtest", "flores_plus",
                                                                             nfc=True)
    en = flores_any("eng_Latn", "dev", "flores_plus") + flores_any("eng_Latn", "devtest", "flores_plus")
    return {"native": kn, "itrans": [" ".join(to_itrans(w) for w in s.split()) for s in kn], "english": en}


def wiki_inputs(W: dict, form: str) -> list[Sentence]:
    if form == "english":
        return [Sentence(f"en{i}", s, t) for i, (s, t) in enumerate(zip(W["en_sentences"], W["en_targets"]))]
    out = []
    for i, (s, t) in enumerate(zip(W["kn_sentences"], W["kn_targets"])):
        if form == "itrans":
            s, t = " ".join(to_itrans(w) for w in s.split()), [to_itrans(w) for w in t]
        out.append(Sentence(f"kn{i}", s, t))
    return out


def forward_pass(model, tok, W, F, form, tag) -> dict:
    path = ACT / tag / f"{form}.npz"
    if path.exists():
        z = np.load(path, allow_pickle=False)
        return {k: z[k] for k in z.files}
    path.parent.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    a = collect(model, tok, wiki_inputs(W, form))
    t1 = time.time()
    f = collect(model, tok, [Sentence(str(i), s, []) for i, s in enumerate(F[form])])
    meta = np.asarray([json.dumps(m, ensure_ascii=False) for m in a["word_meta"]])
    np.savez(path, word_states=a["word_states"], word_meta=meta, flores_states=f["sent_states"],
             wiki_n_tokens=a["n_tokens"], flores_n_tokens=f["n_tokens"],
             seconds=np.asarray([t1 - t0, time.time() - t1]))
    z = np.load(path, allow_pickle=False)
    return {k: z[k] for k in z.files}


def measures(acts: dict, form: str, W: dict, kn_ref_meta=None) -> tuple[dict, dict]:
    meta = [json.loads(m) for m in acts["word_meta"]]
    words = W["en_words"] if form == "english" else W["kn_words"]
    inv = {to_itrans(w): w for w in W["kn_words"]} if form == "itrans" else {w: w for w in words}
    labels = np.array([words.index(inv[m[1]]) for m in meta])
    S = acts["word_states"]
    ntok = np.array([m[2] for m in meta])
    e0 = set(W["en_in_e0"] if form == "english" else W["kn_in_e0"])
    in_e0 = np.array([inv[m[1]] in e0 for m in meta])
    t0 = time.time()
    train = split_by_word(labels, 0.3, seed=0)
    cur = layer_curve(S, labels, train, seed=0)
    mdl = mdl_curve(S, labels, seed=0)
    order = np.random.default_rng(0).permutation(len(labels))  # mdl_curve's item order
    K = len(words)
    er = {str(-d): erasure_curve(S, np.array([m[2 + d] for m in meta]), np.array([m[2 + d] for m in meta]) >= 0,
                                 labels, seed=0) for d in (1, 2)}
    res = {"n_occ": len(labels), "n_words": K, "tokens_per_word_mean": float(ntok.mean()),
           "frac_multitoken": float((ntok > 1).mean()), "frac_ge3": float((ntok >= 3).mean()),
           "probe_acc": cur["acc"].tolist(), "probe_acc_control": cur["acc_control"].tolist(),
           "probe_detok": bootstrap_detok(cur["correct"]),
           "mdl": bootstrap_mdl_detok(mdl["costs"], K), "mdl_codelength": mdl["codelength"].tolist(),
           "mdl_e0_subset": bootstrap_mdl_detok(mdl["costs"], K, subset=in_e0[order]) if in_e0.sum() >= 100 else None,
           "probe_detok_e0_subset": (bootstrap_detok(cur["correct"], subset=in_e0[~train])
                                     if in_e0[~train].sum() >= 30 else None),
           "n_e0_words": len(e0), "erasure": er, "seconds_probes": time.time() - t0}
    items = {"mdl_costs": mdl["costs"].astype(np.float32), "mdl_order": order, "labels": labels,
             "probe_correct": cur["correct"], "probe_train_mask": train, "in_e0": in_e0, "n_tokens": ntok}
    return res, items


def cka(X, Y) -> float:
    X, Y = X - X.mean(0), Y - Y.mean(0)
    return float(np.linalg.norm(X.T @ Y) ** 2 / (np.linalg.norm(X.T @ X) * np.linalg.norm(Y.T @ Y)))


def retrieval_correct(X, Y) -> np.ndarray:
    X, Y = X - X.mean(0), Y - Y.mean(0)
    X = X / (np.linalg.norm(X, axis=1, keepdims=True) + 1e-8)
    Y = Y / (np.linalg.norm(Y, axis=1, keepdims=True) + 1e-8)
    return (X @ Y.T).argmax(1) == np.arange(len(X))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", nargs="+", required=True)
    ap.add_argument("--forms", nargs="+", default=FORMS)
    ap.add_argument("--smoke", action="store_true", help="20 words per language, 100 FLORES sentences, separate dirs")
    args = ap.parse_args()
    global ACT
    wpath = results_dir("m14_full") / "words.json"
    if not wpath.exists():
        wpath.write_text(json.dumps(build_words(), ensure_ascii=False), encoding="utf-8")
    W = json.load(open(wpath, encoding="utf-8"))
    F = flores_forms()
    root = results_dir("m14_full")
    if args.smoke:
        root, ACT = results_dir("m14_smoke"), ACT.parent / "m14smoke"
        for lang in ("kn", "en"):
            keep = set(W[f"{lang}_words"][:20])
            pairs = [(s, [w for w in t if w in keep]) for s, t in zip(W[f"{lang}_sentences"], W[f"{lang}_targets"])]
            pairs = [(s, t) for s, t in pairs if t]
            W[f"{lang}_words"] = W[f"{lang}_words"][:20]
            W[f"{lang}_sentences"], W[f"{lang}_targets"] = [p[0] for p in pairs], [p[1] for p in pairs]
        F = {k: v[:100] for k, v in F.items()}
    print(f"kn words {len(W['kn_words'])} ({len(W['kn_sentences'])} sentences, {len(W['kn_in_e0'])} in E0); "
          f"en words {len(W['en_words'])} ({len(W['en_sentences'])} sentences, {len(W['en_in_e0'])} in E0)", flush=True)
    timing_path = root / "timing.json"
    timing = json.load(open(timing_path)) if timing_path.exists() else {}
    for name in args.models:
        out = root / name
        out.mkdir(exist_ok=True)
        todo = [f for f in args.forms if not (out / f"{f}.json").exists()]
        if not todo and (out / "m4.json").exists():
            continue
        t0 = time.time()
        model, tok = load(name, "cuda")
        L = n_layers(model)
        template = ps.build_template(tok)
        timing[f"{name}/load"] = time.time() - t0
        acts = {}
        for f in args.forms:
            t1 = time.time()
            acts[f] = forward_pass(model, tok, W, F, f, name)
            timing[f"{name}/{f}/forward"] = time.time() - t1
            pq = out / f"patchscopes_{f}.parquet"
            if not pq.exists():
                t1 = time.time()
                targets = W["en_words"] if f == "english" else [to_itrans(w) if f == "itrans" else w
                                                                 for w in W["kn_words"]]
                rows = []
                for w in targets:
                    outs = ps.decode_states(model, tok, ps.word_states(model, tok, w), template)
                    rows.append({"word": w, "n_tokens": len(tok(w, add_special_tokens=False)["input_ids"]),
                                 "first_id_layer": ps.detok_layer(w, outs),
                                 "identified": [ps.identifies(w, o) for o in outs], "outputs": outs})
                pd.DataFrame(rows).to_parquet(pq)
                timing[f"{name}/{f}/patchscopes"] = time.time() - t1
            timing_path.write_text(json.dumps(timing, indent=1))
            print(f"{name}/{f}: forward + patchscopes done ({time.time() - t0:.0f}s since load)", flush=True)
        del model
        torch.cuda.empty_cache()
        if acts["native"]["word_meta"].shape != acts["itrans"]["word_meta"].shape:
            raise SystemExit("native/ITRANS occurrences are not paired")
        for f in todo:
            res, items = measures(acts[f], f, W)
            res["n_layers"] = L
            np.savez_compressed(out / f"items_{f}.npz", **items)
            write_json(out / f"{f}.json", res, {"model": name, "form": f, "probe": PROBE, "mdl_fracs": MDL_FRACS,
                                                "frac": 0.9})
            timing[f"{name}/{f}/probes"] = res["seconds_probes"]
            print(f"{name}/{f}: MDL detok {res['mdl']['detok_layer']} [{res['mdl']['ci_low']}, "
                  f"{res['mdl']['ci_high']}] of {L}", flush=True)
        E = acts["english"]["flores_states"].astype(np.float32)
        m4, m4_items = {}, {}
        for f in [f for f in args.forms if f != "english"]:
            X = acts[f]["flores_states"].astype(np.float32)
            correct = np.stack([retrieval_correct(X[:, l], E[:, l]) for l in range(X.shape[1])])
            m4[f] = {"retrieval_acc": correct.mean(1).tolist(),
                     "cka": [cka(X[:, l], E[:, l]) for l in range(X.shape[1])]}
            m4_items[f] = correct
        np.savez_compressed(out / "m4_items.npz", **m4_items)
        write_json(out / "m4.json", {"n_sentences": int(E.shape[0]), "n_layers": L, **m4}, {"model": name})
        timing_path.write_text(json.dumps(timing, indent=1))
        print(f"{name}: done in {(time.time() - t0) / 60:.1f} min", flush=True)


if __name__ == "__main__":
    main()
