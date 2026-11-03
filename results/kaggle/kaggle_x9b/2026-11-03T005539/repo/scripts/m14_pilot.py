"""Step 2 pilot: M1 (Patchscopes + linear word-identity probes) and M4 (cross-lingual retrieval + linear CKA vs
English) on one model, sharing one forward pass per (form, sentence). Timing only until Gate 1 clears: the summary is
written to disk but must not be interpreted before Aarnav has seen Gate 1.

Corpus: FLORES+ dev+devtest Kannada (NFC) with its English side; ITRANS sentences are built word by word
(" ".join(to_itrans(w))) so every Kannada word occurrence has an ITRANS twin at the same index.
M1 words: the n most frequent Kannada letter-only whitespace words (>= 2 chars) and, separately, the n most frequent
English alphabetic words (>= 3 letters); up to `max_occ` occurrences each (first occurrences in corpus order).
M1a Patchscopes: FragMend setup (shattered.interp.patchscopes), per-layer identification rate over words.
M1b probes: shattered.interp.probes (held-out occurrences, permuted-label control).
Detokenization layer (both methods) = first layer reaching 90% of that form's maximum; 95% CI by bootstrap (words for
Patchscopes, test occurrences for probes).
M4: sentence vectors = mean residual over tokens (BOS excluded) per layer; retrieval accuracy@1 of the English
translation among `n_sent` candidates (cosine after per-form mean-centering), and linear CKA. Alignment layer = first
layer reaching 90% of the maximum retrieval accuracy; CI by bootstrapping sentences. Lag = alignment - detok.

Usage: python scripts/m14_pilot.py --model qwen2.5-1.5b [--n-words 50 --n-sent 50 --max-occ 20]
Outputs: cache/activations/m14/<model>/<form>_<tag>.npz (activations; not results),
         results/m14_pilot/<model>/{patchscopes_<tag>.parquet, summary_<tag>.json, timing_<tag>.json}
"""
import argparse
import json
import re
import time
from collections import Counter

import numpy as np
import pandas as pd
import torch

from shattered.data.corpora import flores_any
from shattered.interp import patchscopes as ps
from shattered.interp.collect import Sentence, collect
from shattered.interp.load import load, n_layers
from shattered.interp.probes import PROBE, bootstrap_detok, detok_layer, layer_curve, split_by_word
from shattered.runlog import REPO, results_dir, write_json
from shattered.translit import to_itrans

KN_WORD = re.compile(r"[ಀ-೿‌‍]{2,}")
EN_WORD = re.compile(r"[A-Za-z]{3,}")
FULL = {"n_words": 300, "n_sent_m4": 1012, "n_corpus_sentences": 2009, "forms": 4}  # for the extrapolation


def corpus() -> dict:
    kn = flores_any("kan_Knda", "dev", "flores_plus", nfc=True) + flores_any("kan_Knda", "devtest", "flores_plus",
                                                                             nfc=True)
    en = flores_any("eng_Latn", "dev", "flores_plus") + flores_any("eng_Latn", "devtest", "flores_plus")
    itr = [" ".join(to_itrans(w) for w in s.split()) for s in kn]
    return {"native": kn, "itrans": itr, "english": en}


def pick_words(sents: list[str], pattern, n: int) -> list[str]:
    c = Counter(w for s in sents for w in s.split() if pattern.fullmatch(w))
    return [w for w, _ in c.most_common(n)]


def occurrences(sents: list[str], words: list[str], max_occ: int) -> dict[int, list[str]]:
    """sentence index -> target words (first max_occ occurrences of each word in corpus order)."""
    left, out = {w: max_occ for w in words}, {}
    for i, s in enumerate(sents):
        for w in set(s.split()):
            if left.get(w, 0) > 0:
                out.setdefault(i, []).append(w)
                left[w] -= s.split().count(w)
    return out


def cka(X: np.ndarray, Y: np.ndarray) -> float:
    X, Y = X - X.mean(0), Y - Y.mean(0)
    hsic = np.linalg.norm(X.T @ Y) ** 2
    return float(hsic / (np.linalg.norm(X.T @ X) * np.linalg.norm(Y.T @ Y)))


def retrieval_correct(X: np.ndarray, Y: np.ndarray) -> np.ndarray:
    X, Y = X - X.mean(0), Y - Y.mean(0)
    X /= np.linalg.norm(X, axis=1, keepdims=True) + 1e-8
    Y /= np.linalg.norm(Y, axis=1, keepdims=True) + 1e-8
    return (X @ Y.T).argmax(1) == np.arange(len(X))


def boot_layer(correct: np.ndarray, n_boot: int = 2000, seed: int = 0) -> dict:
    """correct [L+1, n] (items as columns): first layer reaching 90% of max, with a bootstrap CI over items."""
    rng = np.random.default_rng(seed)
    boots = [detok_layer(correct[:, i].mean(1)) for i in rng.integers(0, correct.shape[1], (n_boot, correct.shape[1]))]
    return {"layer": detok_layer(correct.mean(1)), "ci_low": float(np.percentile(boots, 2.5)),
            "ci_high": float(np.percentile(boots, 97.5)), "curve": correct.mean(1).tolist(), "n": correct.shape[1]}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--forms", nargs="+", default=["english", "native", "itrans"])
    ap.add_argument("--n-words", type=int, default=50)
    ap.add_argument("--n-sent", type=int, default=50, help="M4 sentences (first n of FLORES+ devtest)")
    ap.add_argument("--max-occ", type=int, default=20)
    args = ap.parse_args()
    tag = f"w{args.n_words}_s{args.n_sent}_o{args.max_occ}"
    out = results_dir(f"m14_pilot/{args.model}")
    act_dir = REPO / "cache" / "activations" / "m14" / args.model
    act_dir.mkdir(parents=True, exist_ok=True)
    C = corpus()
    kn_words = pick_words(C["native"], KN_WORD, args.n_words)
    en_words = pick_words(C["english"], EN_WORD, args.n_words)
    kn_occ, en_occ = occurrences(C["native"], kn_words, args.max_occ), occurrences(C["english"], en_words, args.max_occ)
    m4_ids = list(range(997, 997 + args.n_sent))  # devtest starts at index 997 (dev has 997 sentences)
    timing = {}

    t0 = time.time()
    model, tok = load(args.model, "cuda")
    L = n_layers(model)
    timing["load"] = time.time() - t0

    # ---- one forward pass per (form, sentence): word states for M1b + sentence means for M4
    acts = {}
    for f in args.forms:
        occ = en_occ if f == "english" else kn_occ
        ids = sorted(set(occ) | set(m4_ids))
        sents = [Sentence(str(i), C[f][i], [w if f != "itrans" else to_itrans(w) for w in occ.get(i, [])])
                 for i in ids]
        t1 = time.time()
        a = collect(model, tok, sents)
        timing[f"forward_{f}"] = time.time() - t1
        timing[f"n_sentences_{f}"] = len(sents)
        np.savez(act_dir / f"{f}_{tag}.npz", word_states=a["word_states"], sent_states=a["sent_states"],
                 sent_ids=np.asarray(a["sent_ids"]), n_tokens=a["n_tokens"],
                 word_meta=np.asarray([json.dumps(m, ensure_ascii=False) for m in a["word_meta"]]))
        acts[f] = a

    # ---- M1b probes
    probes = {}
    for f in args.forms:
        a = acts[f]
        words = [m[1] for m in a["word_meta"]]
        vocab = sorted(set(words))
        labels = np.array([vocab.index(w) for w in words])
        train = split_by_word(labels, 0.3, seed=0)
        t1 = time.time()
        cur = layer_curve(a["word_states"].astype(np.float32), labels, train, seed=0)
        multi = np.array([m[2] for m in a["word_meta"]])[~train] > 1
        probes[f] = {"acc": cur["acc"].tolist(), "acc_control": cur["acc_control"].tolist(),
                     "detok": bootstrap_detok(cur["correct"]),
                     "detok_multi_token": bootstrap_detok(cur["correct"], subset=multi) if multi.sum() >= 30 else None,
                     "n_occ": len(labels), "n_words": len(vocab), "mean_tokens_per_word": float(np.mean(
                         [m[2] for m in a["word_meta"]]))}
        timing[f"probes_{f}"] = time.time() - t1

    # ---- M1a Patchscopes (words alone)
    template = ps.build_template(tok)
    rows = []
    for f in args.forms:
        targets = en_words if f == "english" else [to_itrans(w) if f == "itrans" else w for w in kn_words]
        t1 = time.time()
        for w in targets:
            outs = ps.decode_states(model, tok, ps.word_states(model, tok, w), template)
            rows.append({"form": f, "word": w, "n_tokens": len(tok(w, add_special_tokens=False)["input_ids"]),
                         "first_id_layer": ps.detok_layer(w, outs),
                         "identified": [ps.identifies(w, o) for o in outs], "outputs": outs})
        timing[f"patchscopes_{f}"] = time.time() - t1
        timing[f"n_patchscopes_words_{f}"] = len(targets)
    pdf = pd.DataFrame(rows)
    pdf.to_parquet(out / f"patchscopes_{tag}.parquet")
    patch = {}
    for f, g in pdf.groupby("form"):
        ident = np.stack(g.identified.to_list()).T  # [L+1, n_words]
        patch[f] = {"per_layer_rate": boot_layer(ident), "success_rate": float(g.first_id_layer.notna().mean()),
                    "median_first_id_layer": float(g.first_id_layer.median()) if g.first_id_layer.notna().any()
                    else None, "mean_tokens_per_word": float(g.n_tokens.mean())}

    # ---- M4 retrieval + CKA vs English on the shared forward pass
    t1 = time.time()
    m4 = {}
    if "english" in acts:
        def sent_matrix(f):
            pos = {s: k for k, s in enumerate(acts[f]["sent_ids"])}
            return acts[f]["sent_states"][[pos[str(i)] for i in m4_ids]].astype(np.float32)  # [n, L+1, d]
        E = sent_matrix("english")
        for f in [f for f in args.forms if f != "english"]:
            X = sent_matrix(f)
            correct = np.stack([retrieval_correct(X[:, layer], E[:, layer]) for layer in range(X.shape[1])])
            m4[f] = {"retrieval": boot_layer(correct),
                     "cka": [cka(X[:, layer], E[:, layer]) for layer in range(X.shape[1])]}
    timing["m4"] = time.time() - t1
    lag = {f: {"probe": m4[f]["retrieval"]["layer"] - probes[f]["detok"]["detok_layer"],
               "patchscopes": m4[f]["retrieval"]["layer"] - patch[f]["per_layer_rate"]["layer"]} for f in m4}

    # ---- timing extrapolation to the full run (this model; other models scaled in the Gate 2 report)
    n_sent_pilot = np.mean([timing[f"n_sentences_{f}"] for f in args.forms])
    fwd = np.mean([timing[f"forward_{f}"] for f in args.forms]) / n_sent_pilot
    psw = np.mean([timing[f"patchscopes_{f}"] / timing[f"n_patchscopes_words_{f}"] for f in args.forms])
    prb = np.mean([timing[f"probes_{f}"] for f in args.forms])
    full = {"forward_s": fwd * FULL["n_corpus_sentences"] * FULL["forms"],
            "patchscopes_s": psw * FULL["n_words"] * FULL["forms"],
            "probes_s": prb * FULL["forms"] * (FULL["n_words"] / args.n_words), "load_s": timing["load"]}
    full["total_min"] = sum(full.values()) / 60
    write_json(out / f"timing_{tag}.json", {"pilot": timing, "per_sentence_forward_s": fwd,
                                            "per_word_patchscopes_s": psw, "full_run_estimate": full,
                                            "full_run_assumptions": FULL}, vars(args))
    write_json(out / f"summary_{tag}.json", {"model": args.model, "n_layers": L, "kn_words": kn_words,
                                             "en_words": en_words, "probes": probes, "patchscopes": patch, "m4": m4,
                                             "lag": lag, "status": "PILOT - not to be interpreted before Gate 1"},
               {**vars(args), "probe": PROBE, "frac": 0.9})
    print(json.dumps({"timing": timing, "full_run_estimate": full}, indent=1))
    del model
    torch.cuda.empty_cache()


if __name__ == "__main__":
    main()
