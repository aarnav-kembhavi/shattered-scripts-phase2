"""X4 data fetch (registered in RESULTS.md, 2026-11-01, item "Data"; run 2026-11-02 after the lead author's go-ahead). Network and CPU only.

Steps (each resumable, each writes to results/phase2/x4/fetch/):
  sib     SIB-200 ben_Beng and tel_Telu (Davlan/sib200 at the pinned Phase 1 revision): counts, index ids and labels against
          the Kannada and English files.
  sent    IndicSentiment bn and te test files (ai4bharat/IndicSentiment at the Phase 1 revision): counts, labels.
  wiki    Wikipedia 20231101 bn, te (and hi, only for the collision-rate comparison) at the pinned Phase 1 revision, all shards.
  dak     Dakshina v1.0 official tarball re-streamed once; MD5 of the full stream is compared with the published hash; only
          bn/romanized/*, te/romanized/* are kept (data/raw/dakshina_official/, not committed).
  coll    Lossy collision rate per language: share of distinct native word types of that language's Wikipedia that merge with
          another type under to_lossy. The same procedure as scripts/e02_translit.py (whitespace words, 1 - lossy types / native
          types), run for Kannada as a check against the Phase 1 value 0.1038, and for Hindi, Bengali and Telugu.
Usage: python scripts/x4_fetch.py <step> [<step> ...]
"""
import base64
import collections
import hashlib
import json
import os
import sys
import tarfile
import time
import unicodedata
import urllib.request

from shattered.data import corpora
from shattered.runlog import REPO, results_dir, write_json

sys.path.insert(0, str(REPO / "scripts"))

OUT = results_dir("phase2/x4/fetch")
RAW = REPO / "data" / "raw"
SENT_REV = "dc8f3f66886531c6897fedffca1e938a68fc5013"
DAK_URL = "https://storage.googleapis.com/gresearch/dakshina/dakshina_dataset_v1.0.tar"
DAK_MD5_B64 = "pWCGix1nAmAsTqToN5T6Jg=="  # published x-goog-hash, as in DATA_CARD.md
LANGS = {"bn": "ben_Beng", "te": "tel_Telu", "hi": "hin_Deva", "kn": "kan_Knda"}


def sha(path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def do_sib() -> None:
    import e0c_sib as e0c
    out = {}
    K, E = e0c.sib("kan_Knda"), e0c.sib("eng_Latn")
    for lang in ("ben_Beng", "tel_Telu"):
        S = e0c.sib(lang)
        out[lang] = {"n": len(S), "unique_ids": int(S.index_id.nunique()),
                     "ids_equal_kn": bool((S.index_id.values == K.index_id.values).all()),
                     "labels_equal_kn": bool((S.category.values == K.category.values).all()),
                     "labels_equal_en": bool((S.category.values == E.category.values).all()),
                     "splits": S.split.value_counts().to_dict(), "categories": S.category.value_counts().to_dict(),
                     "n_empty_text": int((S.text.str.strip() == "").sum())}
    write_json(OUT / "sib.json", out, {"dataset": f"{e0c.SIB_REPO}@{e0c.SIB_REV}", "license": "CC-BY-SA-4.0 (SIB-200 card)"})
    print(json.dumps(out, indent=1))


def do_sent() -> None:
    from huggingface_hub import hf_hub_download
    out = {}
    for lang in ("bn", "te"):
        try:
            p = hf_hub_download("ai4bharat/IndicSentiment", f"data/test/{lang}.json", repo_type="dataset", revision=SENT_REV,
                                token=os.environ.get("HF_TOKEN"), local_dir=RAW / "indicsentiment")
        except Exception as e:  # skipped if IndicSentiment lacks the language (registered)
            out[lang] = {"available": False, "error": repr(e)[:200]}
            continue
        rows = [json.loads(x) for x in open(p, encoding="utf-8")]  # JSON lines, as the Kannada file
        kn = [json.loads(x) for x in open(RAW / "indicsentiment/data/test/kn.json", encoding="utf-8")]
        out[lang] = {"available": True, "n": len(rows), "sha256": sha(p), "labels": dict(collections.Counter(r["LABEL"] for r in rows)),
                     "n_kn": len(kn), "english_reviews_equal_kn": sum(a["ENGLISH REVIEW"].strip() == b["ENGLISH REVIEW"].strip() for a, b in zip(rows, kn)),
                     "labels_equal_kn": sum(a["LABEL"] == b["LABEL"] for a, b in zip(rows, kn))}
    write_json(OUT / "sentiment.json", out, {"dataset": f"ai4bharat/IndicSentiment@{SENT_REV}"})
    print(json.dumps(out, indent=1))


def wiki_texts(lang: str) -> list[str]:
    import pyarrow.parquet as pq
    from huggingface_hub import HfApi
    files = sorted(f for f in HfApi().list_repo_files(corpora.WIKI_REPO, repo_type="dataset", revision=corpora.WIKI_REV)
                   if f.startswith(f"20231101.{lang}/train-"))
    texts = []
    for f in files:
        p = corpora._download(corpora.WIKI_REPO, f, corpora.WIKI_REV, f"wikipedia_{lang}")
        texts += pq.read_table(p, columns=["text"]).column("text").to_pylist()
    return texts


def do_wiki() -> None:
    out = {}
    for lang in ("bn", "te", "hi"):
        t0 = time.time()
        T = wiki_texts(lang)
        out[lang] = {"n_articles": len(T), "n_chars": sum(map(len, T)), "seconds": round(time.time() - t0)}
        print(lang, out[lang], flush=True)
    write_json(OUT / "wikipedia.json", out, {"dataset": f"{corpora.WIKI_REPO}@{corpora.WIKI_REV}", "dump": "20231101",
                                             "license": "CC-BY-SA-3.0 / GFDL (Wikipedia)"})


class HashReader:
    def __init__(self, f):
        self.f, self.md5, self.n = f, hashlib.md5(), 0

    def read(self, k=-1):
        b = self.f.read(k)
        self.md5.update(b)
        self.n += len(b)
        return b


def do_dak() -> None:
    dest = RAW / "dakshina_official"
    resp = urllib.request.urlopen(DAK_URL)
    hdr = resp.headers.get("x-goog-hash", "")
    r = HashReader(resp)
    kept = []
    t0 = time.time()
    with tarfile.open(fileobj=r, mode="r|") as tf:
        for m in tf:
            if m.isfile() and any(f"/{l}/romanized/" in "/" + m.name for l in ("bn", "te")):
                tf.extract(m, dest)
                kept.append(m.name)
    while r.read(1 << 22):  # the tar end blocks and padding belong to the hashed stream
        pass
    md5 = base64.b64encode(r.md5.digest()).decode()
    ok = md5 == DAK_MD5_B64
    out = {"bytes": r.n, "md5_b64": md5, "published_md5_b64": DAK_MD5_B64, "x_goog_hash_header": hdr, "md5_matches_published": ok,
           "kept_files": kept, "seconds": round(time.time() - t0)}
    write_json(OUT / "dakshina.json", out, {"url": DAK_URL, "license": "CC BY-SA 4.0"})
    print(json.dumps({k: v for k, v in out.items() if k != "kept_files"}, indent=1), len(kept), "files kept")
    if not ok:
        raise SystemExit("Dakshina MD5 does not match the published hash; the kept files must not be used")


def types_of(texts):
    c = set()
    for t in texts:
        c.update(unicodedata.normalize("NFC", t).split())  # e02_translit.lossy(): t.split() on each article
    return c


def collision(types, lang: str) -> dict:
    from shattered.translit import to_lossy
    by = collections.defaultdict(set)
    unmapped = 0  # word types containing a character the ITRANS scheme cannot spell (rare letters): excluded and counted
    for w in types:
        try:
            by[to_lossy(w, lang)].add(w)
        except KeyError:
            unmapped += 1
    types = [w for s in by.values() for w in s]
    n = len(types)
    in_group = sum(len(s) for s in by.values() if len(s) > 1)
    return {"types_unmapped_excluded": unmapped, "native_types": n, "lossy_types": len(by), "merged_frac": 1 - len(by) / n,  # the Phase 1 definition (10.4% for Kannada)
            "share_of_types_in_a_collision_group": in_group / n, "max_group": max(len(s) for s in by.values())}


def do_coll() -> None:
    out = {}
    for short, lang in (("kn", "kan_Knda"), ("hi", "hin_Deva"), ("bn", "ben_Beng"), ("te", "tel_Telu")):
        t0 = time.time()
        T = corpora.wikipedia("kn") if short == "kn" else wiki_texts(short)
        types = types_of(T)
        out[lang] = {"n_articles": len(T), **collision(types, lang), "seconds": round(time.time() - t0)}
        print(lang, out[lang], flush=True)
    write_json(OUT / "collision_rates.json", out,
               {"definition": "merged_frac = 1 - (distinct lossy word types / distinct native word types), whitespace words of NFC-normalized "
                              "Wikipedia 20231101 articles, as scripts/e02_translit.py; share_of_types_in_a_collision_group = types that share their "
                              "lossy form with at least one other type (the registered wording 'merge with another type')",
                "phase1_kannada_value": 0.10382542681169316})


if __name__ == "__main__":
    for step in sys.argv[1:]:
        {"sib": do_sib, "sent": do_sent, "wiki": do_wiki, "dak": do_dak, "coll": do_coll}[step]()
