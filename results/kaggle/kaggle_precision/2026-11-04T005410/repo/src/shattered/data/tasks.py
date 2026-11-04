"""E0/M-experiment task data: IndicXNLI (kn) with aligned English XNLI, IndicSentiment (kn) with its English review.

Each item carries an English, native Kannada and ITRANS form. Samples are stratified by label with a fixed seed; the
selected ids are written to results so later experiments (E2) can stay disjoint.
"""
from __future__ import annotations

import json
import random
import unicodedata
from pathlib import Path

import pandas as pd

from ..runlog import REPO
from ..translit import to_itrans

RAW = REPO / "data" / "raw"
XNLI_LABELS = ["entailment", "neutral", "contradiction"]  # 0, 1, 2 in both IndicXNLI and XNLI


def _nfc(s: str) -> str:
    return unicodedata.normalize("NFC", s.strip())


def load_xnli() -> list[dict]:
    kn = json.load(open(next((RAW / "indicxnli").rglob("forward/test/xnli_kn.json")), encoding="utf-8"))["test"]
    en = pd.read_parquet(next((RAW / "xnli").rglob("en/test-*.parquet")))
    assert list(en.label) == [r["label"] for r in kn], "IndicXNLI kn and XNLI en test are not aligned"
    items = []
    for i, (k, e) in enumerate(zip(kn, en.itertuples())):
        p, h = _nfc(k["premise"]), _nfc(k["hypothesis"])
        items.append({"task": "xnli", "id": f"xnli-test-{i}", "label": int(k["label"]),
                      "forms": {"english": {"premise": e.premise, "hypothesis": e.hypothesis},
                                "native": {"premise": p, "hypothesis": h},
                                "itrans": {"premise": to_itrans(p), "hypothesis": to_itrans(h)}}})
    return items


def load_sentiment() -> list[dict]:
    rows = [json.loads(line) for line in open(RAW / "indicsentiment" / "data" / "test" / "kn.json", encoding="utf-8")
            if line.strip()]
    items = []
    for i, r in enumerate(rows):
        if r.get("LABEL") not in ("Positive", "Negative"):
            continue
        t = _nfc(r["INDIC REVIEW"])
        items.append({"task": "sentiment", "id": f"indicsentiment-test-{i}", "label": int(r["LABEL"] == "Positive"),
                      "forms": {"english": {"text": r["ENGLISH REVIEW"].strip()}, "native": {"text": t},
                                "itrans": {"text": to_itrans(t)}}})
    return items


def stratified_sample(items: list[dict], n: int, seed: int = 0, exclude: set | None = None) -> list[dict]:
    rng = random.Random(seed)
    pool = [it for it in items if not exclude or it["id"] not in exclude]
    labels = sorted({it["label"] for it in pool})
    per = {lab: [it for it in pool if it["label"] == lab] for lab in labels}
    for v in per.values():
        rng.shuffle(v)
    k = n // len(labels)
    out = [it for lab in labels for it in per[lab][:k]]
    rest = [it for lab in labels for it in per[lab][k:]]
    rng.shuffle(rest)
    out += rest[: n - len(out)]
    rng.shuffle(out)
    return out


def load_task(task: str) -> list[dict]:
    return {"xnli": load_xnli, "sentiment": load_sentiment}[task]()


def save_ids(path: Path, items: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps([it["id"] for it in items], indent=0), encoding="utf-8")
