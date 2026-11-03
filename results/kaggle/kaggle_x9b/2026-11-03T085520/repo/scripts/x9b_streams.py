"""X9b step 1 (CPU): build the three training pools (ITRANS Kannada, native Kannada, English Wikipedia 20231101), run the registered exclusion scan against
FLORES+ (dev and devtest, Kannada and English) and SIB-200 (Kannada and English), re-scan the retained pools, and report overlap per stream. Overlap must be
0 for every stream or nothing runs (X9b registration). Output: results/phase2/x9b/streams_report.json (counts, sha256 of the retained seeded order per
language; the Kaggle job recomputes and compares). Usage: python scripts/x9b_streams.py [--workers 5] [--limit N]   (--limit only for a smoke test)"""
import argparse
import sys
import time

from shattered.data import x9b_streams as S
from shattered.runlog import REPO, results_dir, write_json
from shattered.translit import to_itrans


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=5)
    ap.add_argument("--limit", type=int, default=0)
    a = ap.parse_args()
    t0 = time.time()
    ev = S.eval_sentences()
    ev_itrans = {k + "_itrans": [" ".join(to_itrans(w) for w in s.split()) for s in v] for k, v in ev.items() if k.endswith("_kn")}
    print({k: len(v) for k, v in {**ev, **ev_itrans}.items()}, flush=True)
    kn = S.load_wiki("kn")
    en = S.load_wiki("en")
    if a.limit:
        kn, en = kn[:a.limit], en[:a.limit]
    print("articles", len(kn), len(en), f"{time.time() - t0:.0f}s", flush=True)
    rep: dict = {"eval_sentences": {k: len(v) for k, v in {**ev, **ev_itrans}.items()}, "wikipedia_revision": S.WIKI_REV, "sib_revision": S.SIB_REV,
                 "prefix_chars": S.PREFIX, "seed": S.SEED, "limit": a.limit or None}

    # Kannada: native scan against all evaluation sets; ITRANS scan of the rendered articles against the ITRANS renderings (and the English sets)
    sets_native = ev
    sets_itrans = {**ev_itrans, "flores_en": ev["flores_en"], "sib_en": ev["sib_en"]}
    h_nat = S.scan(kn, sets_native, itrans=False, workers=a.workers)
    print("kn native scan done", len(h_nat), f"{time.time() - t0:.0f}s", flush=True)
    h_itr = S.scan(kn, sets_itrans, itrans=True, workers=a.workers)
    print("kn itrans scan done", len(h_itr), f"{time.time() - t0:.0f}s", flush=True)
    removed_kn = set(h_nat) | set(h_itr)
    h_en = S.scan(en, ev, itrans=False, workers=a.workers)
    print("en scan done", len(h_en), f"{time.time() - t0:.0f}s", flush=True)
    removed_en = set(h_en)

    def by_set(h: dict) -> dict:
        c: dict = {}
        for names in h.values():
            for n in names:
                c[n] = c.get(n, 0) + 1
        return c

    kn_keep = [r for r in kn if r[0] not in removed_kn]
    en_keep = [r for r in en if r[0] not in removed_en]
    # re-scan of the retained pools with the same function (final overlap, per stream)
    f_nat = S.scan(kn_keep, sets_native, itrans=False, workers=a.workers)
    f_itr = S.scan(kn_keep, sets_itrans, itrans=True, workers=a.workers)
    f_en = S.scan(en_keep, ev, itrans=False, workers=a.workers)
    words = lambda rows: sum(len(t.split()) for _, t in rows)  # noqa: E731
    ok_kn, ok_en = S.retained_order(kn, removed_kn), S.retained_order(en, removed_en)
    rep["streams"] = {
        "native_kannada": {"pool_articles": len(kn), "removed_native_scan": len(h_nat), "removed_by_set": by_set(h_nat), "retained_articles": len(kn_keep),
                           "retained_words": words(kn_keep), "final_overlap": len(f_nat), "order_sha256": S.order_hash(ok_kn)},
        "itrans_kannada": {"pool_articles": len(kn), "removed_itrans_scan": len(h_itr), "removed_by_set": by_set(h_itr),
                           "removed_union_with_native": len(removed_kn), "retained_articles": len(kn_keep), "retained_words": words(kn_keep),
                           "final_overlap": len(f_itr), "order_sha256": S.order_hash(ok_kn)},
        "english": {"pool_articles": len(en), "removed": len(h_en), "removed_by_set": by_set(h_en), "retained_articles": len(en_keep),
                    "retained_words": words(en_keep), "final_overlap": len(f_en), "order_sha256": S.order_hash(ok_en)}}
    write_json(results_dir("phase2/x9b") / ("removed_ids.json" if not a.limit else "removed_ids_smoke.json"),
               {"kn": sorted(removed_kn), "en": sorted(removed_en), "kn_native_scan": sorted(h_nat), "kn_itrans_scan": sorted(h_itr)},
               {"experiment": "X9b removed article ids (the Kaggle job reproduces the seeded order from these and checks the sha256)"})
    rep["all_overlap_zero"] = all(v["final_overlap"] == 0 for v in rep["streams"].values())
    rep["seconds"] = time.time() - t0
    out = results_dir("phase2/x9b") / ("streams_report.json" if not a.limit else "streams_report_smoke.json")
    write_json(out, rep, {"experiment": "X9b exclusion scan (CPU)", "registration": "phase2-amendment-2"})
    print(out, {k: (v["retained_articles"], v["final_overlap"]) for k, v in rep["streams"].items()}, "ALL ZERO:", rep["all_overlap_zero"], flush=True)
    if not rep["all_overlap_zero"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
