"""X9b training streams and the registered exclusion scan (Amendment 2, X9b).

Streams (equal token budget B under each model's own tokenizer, cut later): (i) ITRANS Kannada, (ii) native Kannada, (iii) English. Kannada Wikipedia
20231101 articles (the same articles in the same order for (i) and (ii), rendered with the project's ITRANS scheme for (i)); English Wikipedia 20231101
shard 0. Order: `default_rng(9).permutation` of the retained articles sorted by id, per language.

Exclusion (hard rule): every article that contains a FLORES+ sentence (Kannada or English; dev and devtest) or a SIB-200 sentence (Kannada or English) is
removed before sampling, by exact match (sentences under 20 characters: equal to a whole line of the article) or containment (20 characters or more;
whitespace-collapsed, NFC). The ITRANS renderings of the Kannada evaluation sentences are also searched in the ITRANS stream. The final streams are
re-scanned with the same function; overlap must be 0 for every stream or the run does not start (`assert_zero`).

The same module is used on the laptop (CPU report, `scripts/x9b_streams.py`) and in the Kaggle kernel (`scripts/kaggle_x9b.py`), which recomputes the
retained-id order and checks its sha256 against the CPU report.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import unicodedata
from pathlib import Path

import numpy as np

from ..runlog import REPO

WIKI_REPO, WIKI_REV = "wikimedia/wikipedia", "b04c8d1ceb2f5cd4588862100d08de323dccfbaa"
SIB_REPO, SIB_REV = "Davlan/sib200", "38977a667f6fc264d5c26ec57a01e16db040b358"
PREFIX = 20
SEED = 9
_WORD = re.compile(r"\w+")
_TOKEN = re.compile(r"\S+")


def norm(t: str) -> str:
    return " ".join(unicodedata.normalize("NFC", t).split())


def load_wiki(lang: str) -> list[tuple[str, str]]:
    """(id, text) of the Kannada (single shard) or English (shard 0) Wikipedia 20231101 parquet, sorted by id (as strings)."""
    import pyarrow.parquet as pq
    from huggingface_hub import hf_hub_download
    fn = "20231101.kn/train-00000-of-00001.parquet" if lang == "kn" else "20231101.en/train-00000-of-00041.parquet"
    p = hf_hub_download(WIKI_REPO, fn, repo_type="dataset", revision=WIKI_REV, token=os.environ.get("HF_TOKEN"))
    t = pq.read_table(p, columns=["id", "text"])
    rows = list(zip(t.column("id").to_pylist(), t.column("text").to_pylist()))
    return sorted(rows, key=lambda r: r[0])


def flores_private() -> dict:
    for p in (Path("/kaggle/input/shattered-flores-private/flores_private.json"), REPO / "build" / "kaggle" / "flores_private" / "flores_private.json"):
        if p.exists():
            return json.loads(p.read_text(encoding="utf-8"))
    for p in Path("/kaggle/input").glob("**/flores_private.json") if Path("/kaggle/input").exists() else []:
        return json.loads(p.read_text(encoding="utf-8"))
    raise FileNotFoundError("flores_private.json (private FLORES+ file) not found")


def eval_sentences() -> dict[str, list[str]]:
    """The evaluation sentences that must not occur in any stream: {'flores_kn','flores_en','sib_kn','sib_en'} (NFC, whitespace-collapsed)."""
    import pandas as pd
    from huggingface_hub import hf_hub_download
    fl = flores_private()
    out = {"flores_kn": [norm(s) for s in fl["kn"]], "flores_en": [norm(s) for s in fl["en"]]}
    for key, cfg in (("sib_kn", "kan_Knda"), ("sib_en", "eng_Latn")):
        sents = []
        for sp in ("train", "dev", "test"):
            p = hf_hub_download(SIB_REPO, f"data/{cfg}/{sp}.tsv", repo_type="dataset", revision=SIB_REV, token=os.environ.get("HF_TOKEN"))
            sents += [norm(t) for t in pd.read_csv(p, sep="\t").text]
        out[key] = sents
    return out


def render_itrans(text: str) -> str:
    from ..translit import to_itrans
    return "\n".join(" ".join(to_itrans(w) for w in ln.split()) for ln in text.split("\n"))


class Index:
    """Sentences with >= 20 characters indexed by their first 20 characters; shorter ones kept for whole-line equality."""

    def __init__(self, sets: dict[str, list[str]]) -> None:
        self.long: dict[str, list[tuple[str, str]]] = {}
        self.short: dict[str, str] = {}
        for name, sents in sets.items():
            for s in sents:
                if len(s) >= PREFIX:
                    self.long.setdefault(s[:PREFIX], []).append((s, name))
                elif s:
                    self.short[s] = name

    def hits(self, text: str) -> set[str]:
        """Names of the evaluation sets with a sentence contained in (or, if short, equal to a line of) the article."""
        found: set[str] = set()
        lines = [norm(ln) for ln in text.split("\n")]
        for ln in lines:
            if ln in self.short:
                found.add(self.short[ln])
        nt = " ".join(ln for ln in lines if ln)
        starts = {m.start() for m in _TOKEN.finditer(nt)} | {m.start() for m in _WORD.finditer(nt)}
        for i in starts:
            cand = self.long.get(nt[i:i + PREFIX])
            if cand:
                for s, name in cand:
                    if nt.startswith(s, i):
                        found.add(name)
        return found


_IDX: Index | None = None


def _init(sets: dict[str, list[str]]) -> None:
    global _IDX
    _IDX = Index(sets)


def _scan_chunk(args: tuple[list[tuple[str, str]], bool]) -> list[tuple[str, list[str]]]:
    rows, itrans = args
    out = []
    for aid, text in rows:
        t = render_itrans(text) if itrans else text
        h = _IDX.hits(t)
        if h:
            out.append((aid, sorted(h)))
    return out


def scan(rows: list[tuple[str, str]], sets: dict[str, list[str]], itrans: bool = False, workers: int = 6, chunk: int = 400) -> dict[str, list[str]]:
    """{article id: sorted names of the evaluation sets it contains}, for the articles (rendered to ITRANS first if `itrans`) that contain any."""
    import multiprocessing as mp
    chunks = [(rows[i:i + chunk], itrans) for i in range(0, len(rows), chunk)]
    res: dict[str, list[str]] = {}
    if workers <= 1:
        _init(sets)
        for c in chunks:
            res.update(dict(_scan_chunk(c)))
        return res
    with mp.get_context("spawn").Pool(workers, initializer=_init, initargs=(sets,)) as pool:
        for part in pool.imap_unordered(_scan_chunk, chunks):
            res.update(dict(part))
    return res


def retained_order(rows: list[tuple[str, str]], removed: set[str]) -> list[str]:
    """Retained article ids in the registered seeded order (`default_rng(9).permutation` over the retained ids sorted by id)."""
    ids = [r[0] for r in rows if r[0] not in removed]
    perm = np.random.default_rng(SEED).permutation(len(ids))
    return [ids[j] for j in perm]


def order_hash(order: list[str]) -> str:
    return hashlib.sha256("\n".join(map(str, order)).encode()).hexdigest()


def assert_zero(report: dict) -> None:
    bad = {k: v for k, v in report.items() if isinstance(v, dict) and v.get("final_overlap", 0) != 0}
    if bad:
        raise RuntimeError(f"X9b exclusion scan: overlap is not 0 for {bad}; the run does not start")
