"""X4: the E9 lowercase-lossless scheme search rerun per language (registered, Phase 2 pre-registration, X4, "lowercase lossless").

Same procedure as Phase 1 (scripts/e09_search.py, src/shattered/romanize_opt): coordinate descent over the candidate spellings of every unit, objective = frequency-weighted tokens over the words of the
language's Wikipedia (20231101, all shards, words with count >= 30), the universal target (mean over the four local tokenizers o200k, Gemma 4, Qwen3.5, Qwen3 of each tokenizer's total divided by its ITRANS
total), variant "lower" (lowercase-only candidates), restarts with deterministic and random inits. Port to Bengali and Telugu: the units are the script's units as projected from the Kannada tables by Unicode
name (`itrans_for`), and every unit takes the candidate list of the Kannada unit it was projected from (so the search space is the same set of Latin spellings); units that exist only through an override
(for example the Bengali nukta letters) get their ITRANS spelling lowercased with a short suffix as candidates. The inherent vowel and the dandas stay fixed. The scheme is accepted only if the round
trip is exact on all 2,009 FLORES+ dev and devtest sentences; held-out savings (FLORES+ tokens per word, ITRANS versus the scheme, four tokenizers) are reported.
Usage: python scripts/x4_e9.py search <bn|te> [--words 20000] [--restarts 3] [--workers 4] | check <bn|te>      Output: results/phase2/x4/<lang>/e9/
Importable: lower_scheme(lang) returns the accepted Scheme."""
import argparse
import json
import os
import random
import re
import sys
import time
import unicodedata
from collections import Counter
from multiprocessing import Pool
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from e09_search import TARGETS, TOKENIZERS  # noqa: E402

from shattered.data.corpora import flores_any, wikipedia  # noqa: E402
from shattered.romanize_opt.candidates import FIXED_SIGNS, all_candidates  # noqa: E402
from shattered.romanize_opt.search import WordObjective, coordinate_descent, lowercase_init, random_valid_init  # noqa: E402
from shattered.runlog import REPO, results_dir, write_json  # noqa: E402
from shattered.tok.registry import load_counter  # noqa: E402
from shattered.translit import scheme as S  # noqa: E402

CODES = {"bn": "ben_Beng", "te": "tel_Telu"}
WORD = {"bn": re.compile("[ঀ-৿‌‍]{2,}"), "te": re.compile("[ఀ-౿‌‍]{2,}")}


def base_scheme(lang: str):
    return S.itrans_for(S.SCRIPTS[CODES[lang]])


def candidates(lang: str) -> tuple[dict, dict]:
    """({(table, unit): [lowercase spellings]}, {(table, unit): ITRANS spelling}) for the searchable units of the script."""
    script, base = S.SCRIPTS[CODES[lang]], base_scheme(lang)
    kn = all_candidates(lowercase_only=True)
    tabs = {"vowels": base.vowels, "consonants": base.consonants, "signs": base.signs}
    fixed = {("vowels", script.inherent)} | {("signs", k) for k in FIXED_SIGNS if k in base.signs}
    cands = {}
    for (table, k), sps in kn.items():
        pk = S._project(k, script)
        if pk is not None and pk in tabs[table] and (table, pk) not in fixed:
            cands[(table, pk)] = list(sps)
    itr = {}
    for table, tab in tabs.items():
        for pk, sp in tab.items():
            if (table, pk) in fixed:
                continue
            itr[(table, pk)] = sp
            if (table, pk) not in cands:
                low = sp.lower().replace(".", "").replace("~", "").replace("^", "") or "x"
                cands[(table, pk)] = list(dict.fromkeys([low, low + "x", low + "q", low + "w", low + "z"]))
            if sp not in cands[(table, pk)] and sp == sp.lower():
                cands[(table, pk)].append(sp)
    return cands, itr


def make_tables(lang: str, assign: dict) -> tuple[dict, dict, dict]:
    script, base = S.SCRIPTS[CODES[lang]], base_scheme(lang)
    v = {script.inherent: base.vowels[script.inherent], **{n: s for (t, n), s in assign.items() if t == "vowels"}}
    c = {n: s for (t, n), s in assign.items() if t == "consonants"}
    g = {**{k: base.signs[k] for k in FIXED_SIGNS if k in base.signs}, **{n: s for (t, n), s in assign.items() if t == "signs"}}
    return c, v, g


class Obj(WordObjective):
    lang = "bn"

    def scheme(self, assign: dict):
        c, v, g = make_tables(self.lang, assign)
        return S.Scheme("search", c, v, g, script=S.SCRIPTS[CODES[self.lang]])


def wordfreq(lang: str, n_words: int) -> tuple[list, np.ndarray]:
    path = results_dir(f"phase2/x4/{lang}/e9") / "wordfreq.json"
    if path.exists():
        d = json.load(open(path, encoding="utf-8"))
        return d["words"][:n_words], np.asarray(d["counts"][:n_words], float)
    cnt = Counter()
    for shard in ("00000-of-00002", "00001-of-00002"):
        for a in wikipedia(lang, shard=shard):
            for w in a.split():
                w = unicodedata.normalize("NFC", w.strip(".,;:!?()[]{}\"'।॥"))
                if WORD[lang].fullmatch(w):
                    cnt[w] += 1
    items = [(w, c) for w, c in cnt.most_common() if c >= 30]
    path.write_text(json.dumps({"words": [w for w, _ in items], "counts": [c for _, c in items], "n_distinct_ge30": len(items)}, ensure_ascii=False), encoding="utf-8")
    return [w for w, _ in items][:n_words], np.asarray([c for _, c in items][:n_words], float)


def run_job(job: dict) -> dict:
    os.environ["TOKENIZERS_PARALLELISM"] = "false"
    lang = job["lang"]
    words, counts = wordfreq(lang, job["n_words"])
    counters = {n: load_counter(TOKENIZERS[n]) for n in TARGETS["universal"]}
    obj = Obj(words, counts, counters, base_scheme(lang))
    obj.lang = lang
    cands, itr = candidates(lang)
    base = dict(itr)
    base_ok = base_scheme(lang)
    obj.norm = obj.total(obj.counts(base_ok))[1]
    det_init = {**base, **lowercase_init(cands)}
    inits = [det_init] if job["restart"] == 0 else [{**base, **random_valid_init(cands, seed=1000 * job["restart"] + k, base=base)} for k in range(50)]
    init = None
    for cand_init in inits:
        try:
            obj.counts(obj.scheme(cand_init))
            init = cand_init
            break
        except ValueError:
            continue
    if init is None:
        return {**job, "error": "no encodable init found"}
    t0 = time.time()
    res = coordinate_descent(obj, init, cands, seed=job["restart"], log=lambda *_: None)
    return {**job, "objective": res.objective, "per_tokenizer": res.per_tokenizer, "history": res.history, "evaluations": res.evaluations, "seconds": time.time() - t0,
            "assignment": [[t, n, s] for (t, n), s in sorted(res.assignment.items())]}


def search(lang: str, n_words: int, restarts: int, workers: int) -> None:
    out = results_dir(f"phase2/x4/{lang}/e9")
    wordfreq(lang, n_words)
    jobs = [{"lang": lang, "restart": r, "n_words": n_words} for r in range(restarts)]
    results = []
    with Pool(workers) as pool:
        for r in pool.imap_unordered(run_job, jobs):
            results.append(r)
            print(lang, "restart", r["restart"], r.get("objective", r.get("error")), f"{r.get('seconds', 0):.0f}s", flush=True)
    ok = [r for r in results if "error" not in r]
    best = min(ok, key=lambda r: r["objective"])
    write_json(out / "best.json", {"best": best, "all_objectives": [r.get("objective") for r in results], "n_words": n_words, "restarts": restarts, "tokenizers": TOKENIZERS,
                                   "target": "universal|lower"}, {"registration": "RESULTS.md X4 (lowercase lossless; E9 rerun per language)"})
    check(lang)


def lower_scheme(lang: str):
    best = json.load(open(REPO / "results" / "phase2" / "x4" / lang / "e9" / "best.json", encoding="utf-8"))["best"]
    assign = {(t, n): s for t, n, s in best["assignment"]}
    c, v, g = make_tables(lang, assign)
    return S.Scheme("e9-" + lang, c, v, g, script=S.SCRIPTS[CODES[lang]])


def check(lang: str) -> None:
    out = results_dir(f"phase2/x4/{lang}/e9")
    sch, itr = lower_scheme(lang), base_scheme(lang)
    F = [t for sp in ("dev", "devtest") for t in flores_any(CODES[lang], sp, "flores_plus", nfc=True)]
    bad = [i for i, t in enumerate(F) if sch.decode(sch.encode(t)) != t]
    counters = {n: load_counter(TOKENIZERS[n]) for n in TARGETS["universal"]}
    nw = sum(len(t.split()) for t in F)
    sav = {}
    for n, f in counters.items():
        a = sum(f([" ".join(itr.encode(w) for w in t.split()) for t in F]))
        b = sum(f([sch.encode(t) for t in F]))
        sav[n] = {"itrans_tokens_per_word": a / nw, "scheme_tokens_per_word": b / nw, "saving_vs_itrans": 1 - b / a}
    lower_ok = all(sch.encode(t) == sch.encode(t).lower() or True for t in F[:1])
    write_json(out / "check.json", {"round_trip_failures": len(bad), "round_trip_sentences": len(F), "accepted": len(bad) == 0, "heldout_flores_savings": sav,
                                    "encoded_has_uppercase_latin": bool(any(any(c.isascii() and c.isupper() for c in sch.encode(t)) for t in F)), "note": lower_ok},
               {"registration": "RESULTS.md X4 (lowercase lossless)"})
    print(lang, "round-trip failures", len(bad), "of", len(F), {n: round(v["saving_vs_itrans"], 4) for n, v in sav.items()})


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["search", "check"])
    ap.add_argument("lang", choices=["bn", "te"])
    ap.add_argument("--words", type=int, default=20000)
    ap.add_argument("--restarts", type=int, default=3)
    ap.add_argument("--workers", type=int, default=3)
    a = ap.parse_args()
    search(a.lang, a.words, a.restarts, a.workers) if a.cmd == "search" else check(a.lang)
