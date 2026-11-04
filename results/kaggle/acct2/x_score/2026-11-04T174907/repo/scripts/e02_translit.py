"""E2 step 1: native <-> ITRANS round trip and controlled lossy scheme information loss.

Usage:
  python scripts/e02_translit.py --corpus flores200        # all FLORES Kannada sentences (dev + devtest)
  python scripts/e02_translit.py --corpus wikipedia --no-lossy
Outputs: results/e02_translit/roundtrip_<corpus>.json, lossy_<corpus>.json, examples_<corpus>.jsonl
"""
import argparse
import collections
import json
import random
import time
import unicodedata

from tqdm import tqdm

from shattered.data import corpora
from shattered.runlog import results_dir, write_json
from shattered.translit import ITRANS, LossyBackMapper, char_error_rate, to_lossy


def load(corpus: str) -> tuple[list[str], dict]:
    if corpus in ("flores200", "flores_plus"):
        texts = [t for split in ("dev", "devtest") for t in corpora.flores_any("kan_Knda", split, corpus)]
        return texts, {"splits": ["dev", "devtest"], "lang": "kan_Knda"}
    return corpora.wikipedia("kn"), {"repo": corpora.WIKI_REPO, "revision": corpora.WIKI_REV, "dump": "20231101.kn"}


def roundtrip(texts: list[str]) -> dict:
    failures, non_ascii, units = [], collections.Counter(), collections.Counter()
    n_chars = n_sep = n_raw = 0
    for i, text in enumerate(tqdm(texts, mininterval=10)):
        enc = ITRANS.encode(text)
        dec = ITRANS.decode(enc)
        if dec != text:
            bad = sorted({c for c in set(text) ^ set(dec)})
            failures.append({"index": i, "text": text[:300], "chars": [f"U+{ord(c):04X}" for c in bad]})
        n_chars += len(text)
        n_sep += enc.count(ITRANS.separator)
        for u in ITRANS.units(text):
            units[u.kind] += 1
            if u.kind == "RAW":
                n_raw += 1
                non_ascii.update(c for c in u.native if not c.isascii())
    return {"n_texts": len(texts), "n_chars": n_chars, "n_exact": len(texts) - len(failures),
            "exact_rate": (len(texts) - len(failures)) / len(texts), "n_separators": n_sep,
            "separators_per_text": n_sep / len(texts), "n_raw_runs": n_raw, "unit_counts": dict(units),
            "non_ascii_chars_in_raw_runs": {f"U+{ord(c):04X}": n for c, n in non_ascii.most_common()},
            "failing_chars": collections.Counter(c for f in failures for c in f["chars"]).most_common(),
            "failures": failures[:50]}


def lossy(texts: list[str], train_texts: list[str]) -> dict:
    """CER of the best word-level inversion of the lossy scheme, trained on a disjoint corpus."""
    bm = LossyBackMapper().fit(train_texts)
    norm = [" ".join(unicodedata.normalize("NFC", t).split()) for t in texts]
    lossy_texts = [to_lossy(t) for t in norm]
    inv = [bm.invert(lt) for lt in lossy_texts]
    fallback = [" ".join(LossyBackMapper._fallback(w) for w in lt.split()) for lt in lossy_texts]
    edits = sum(char_error_rate(h, r) * len(r) for h, r in zip(inv, norm))
    edits_fb = sum(char_error_rate(h, r) * len(r) for h, r in zip(fallback, norm))
    total = sum(len(r) for r in norm)
    words = [(w, lw) for t, lt in zip(norm, lossy_texts) for w, lw in zip(t.split(), lt.split())]
    inv_words = [w for i in inv for w in i.split()]
    # ambiguity of the lossy map itself: share of distinct native word types (in training) that collide
    by_lossy = collections.defaultdict(set)
    for t in train_texts:
        for w in t.split():
            by_lossy[to_lossy(w)].add(w)
    n_types = sum(len(s) for s in by_lossy.values())
    return {
        "n_sentences": len(texts), "n_ref_chars": total,
        "cer_corpus_backmap": edits / total, "cer_itrans_decode_only": edits_fb / total,
        "word_accuracy_backmap": sum(a == b for (a, _), b in zip(words, inv_words)) / len(words),
        "backmap_coverage_tokens": sum(bm.coverage(lt) * len(lt.split()) for lt in lossy_texts) / len(words),
        "train_native_word_types": n_types, "train_lossy_word_types": len(by_lossy),
        "train_types_merged_frac": 1 - len(by_lossy) / n_types,
        "examples": [{"native": n, "lossy": l, "inverted": i} for n, l, i in list(zip(norm, lossy_texts, inv))[:5]],
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", choices=["flores200", "flores_plus", "wikipedia"], required=True)
    ap.add_argument("--no-lossy", action="store_true")
    ap.add_argument("--lossy-train-articles", type=int, default=0, help="0 = all Kannada Wikipedia")
    args = ap.parse_args()
    texts, src = load(args.corpus)
    out_dir = results_dir("e02_translit")
    config = {"corpus": args.corpus, "scheme": ITRANS.name, **src}

    t0 = time.time()
    rt = roundtrip(texts)
    rt["seconds"] = round(time.time() - t0, 1)
    # Experiments use NFC-normalized text; report the round trip on that too.
    nfc = [unicodedata.normalize("NFC", t) for t in texts]
    rt["n_texts_not_nfc"] = sum(a != b for a, b in zip(texts, nfc))
    rt["nfc"] = {k: v for k, v in roundtrip(nfc).items() if k != "failures"}
    write_json(out_dir / f"roundtrip_{args.corpus}.json", rt, config)
    print(f"round trip: {rt['n_exact']}/{rt['n_texts']} exact ({rt['exact_rate']:.4%}), "
          f"{rt['n_separators']} separators, {rt['n_raw_runs']} raw runs, failing chars: {rt['failing_chars'][:10]}; "
          f"{rt['n_texts_not_nfc']} texts not NFC; after NFC: {rt['nfc']['n_exact']}/{rt['nfc']['n_texts']} exact, "
          f"{rt['nfc']['n_raw_runs']} raw runs, non-ASCII in raw: {rt['nfc']['non_ascii_chars_in_raw_runs']}")

    with (out_dir / f"examples_{args.corpus}.jsonl").open("w", encoding="utf-8") as f:
        for t in random.Random(0).sample(texts, min(20, len(texts))):
            f.write(json.dumps({"native": t, "itrans": ITRANS.encode(t), "lossy": to_lossy(t)},
                               ensure_ascii=False) + "\n")

    if not args.no_lossy:
        train = corpora.wikipedia("kn")
        if args.lossy_train_articles:
            train = train[:args.lossy_train_articles]
        lo = lossy(texts, train)
        cfg = {**config, "backmap_train": "wikipedia kn 20231101", "backmap_train_articles": len(train)}
        write_json(out_dir / f"lossy_{args.corpus}.json", lo, cfg)
        print(f"lossy: CER backmap {lo['cer_corpus_backmap']:.4f}, ITRANS-decode-only {lo['cer_itrans_decode_only']:.4f}"
              f", word acc {lo['word_accuracy_backmap']:.4f}, coverage {lo['backmap_coverage_tokens']:.4f}")


if __name__ == "__main__":
    main()
