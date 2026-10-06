"""Round-trip native -> ITRANS -> native on a whole corpus and report failures.

Usage: python scripts/translit_roundtrip.py --corpus wikipedia|flores
Output: results/e02_translit/roundtrip_<corpus>.json
"""
import argparse
import collections
import time

from tqdm import tqdm

from shattered.data import corpora
from shattered.runlog import results_dir, write_json
from shattered.translit import ITRANS


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", choices=["wikipedia", "flores"], required=True)
    args = ap.parse_args()
    config = {"corpus": args.corpus, "scheme": ITRANS.name}
    if args.corpus == "flores":
        texts = [r["text"] for split in ("dev", "devtest") for r in corpora.flores("kan_Knda", split)]
        config.update(repo=corpora.FLORES_REPO, revision=corpora.FLORES_REV, splits=["dev", "devtest"])
    else:
        texts = corpora.wikipedia("kn")
        config.update(repo=corpora.WIKI_REPO, revision=corpora.WIKI_REV, dump="20231101.kn")

    t0 = time.time()
    failures, non_ascii, units = [], collections.Counter(), collections.Counter()
    n_chars = n_sep = n_raw = 0
    for i, text in enumerate(tqdm(texts, mininterval=10)):
        enc = ITRANS.encode(text)
        if ITRANS.decode(enc) != text:
            failures.append({"index": i, "text": text[:300]})
        n_chars += len(text)
        n_sep += enc.count(ITRANS.separator)
        for u in ITRANS.units(text):
            units[u.kind] += 1
            if u.kind == "RAW":
                n_raw += 1
                non_ascii.update(c for c in u.native if not c.isascii())
    payload = {
        "n_texts": len(texts), "n_chars": n_chars, "n_exact": len(texts) - len(failures),
        "exact_rate": (len(texts) - len(failures)) / len(texts),
        "n_separators": n_sep, "n_raw_runs": n_raw, "unit_counts": dict(units),
        "non_ascii_chars_in_raw_runs": {f"U+{ord(c):04X}": n for c, n in non_ascii.most_common()},
        "failures": failures[:50], "seconds": round(time.time() - t0, 1),
    }
    out = write_json(results_dir("e02_translit") / f"roundtrip_{args.corpus}.json", payload, config)
    print(f"{payload['n_exact']}/{payload['n_texts']} exact ({payload['exact_rate']:.4%}); "
          f"{n_sep} separators, {n_raw} raw runs; wrote {out}")


if __name__ == "__main__":
    main()
