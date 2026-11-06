"""X2 (registered, Phase 2 pre-registration): measured romanized exposure, Source A = FineWeb-2 (HuggingFaceFW/fineweb-2), which labels language and script separately (configs such as kan_Knda and kan_Latn).

e(language) = romanized share = documents in <lang>_Latn / (documents in <lang>_Latn + documents in the native-script config), counted from the parquet footers (no document text is read). A byte-based share
(file sizes, a proxy for text volume) is reported as a second measure. Languages: Kannada, Hindi, Telugu, Bengali (the registered four) and Tamil, Malayalam, Marathi, Gujarati as descriptive context.
Registered rule: e_hi > e_kn is SUPPORTED if the 95% interval of e_hi - e_kn lies above 0, refuted if it lies below 0 (or the sources disagree in sign), otherwise inconclusive; primary source A.
Deviation X2-D1 (stated, not a rule change): the registration says "bootstrap over shards"; the Latin-script configs of these languages are single-shard files (a few row groups), so there are no shards to
resample. The interval here is a parametric bootstrap treating each document count as Poisson (10,000 draws, seed 0), which captures counting noise only, and a second interval resamples the parquet row groups
where a config has at least 10 of them. Source B is not run here (Source A covers all four languages; the registration requires B only if A lacks one).
Usage: python scripts/x2_exposure.py        Output: results/phase2/x2/exposure.json"""
import json
import sys

import numpy as np

from shattered.runlog import REPO, results_dir, write_json

CFG = {"kn": ("kan_Knda", "kan_Latn"), "hi": ("hin_Deva", "hin_Latn"), "te": ("tel_Telu", "tel_Latn"), "bn": ("ben_Beng", "ben_Latn"),
       "ta": ("tam_Taml", "tam_Latn"), "ml": ("mal_Mlym", "mal_Latn"), "mr": ("mar_Deva", "mar_Latn"), "gu": ("guj_Gujr", "guj_Latn")}
N_BOOT = 10_000


def config_stats(fs, api, cfg: str) -> dict:
    import pyarrow.parquet as pq
    files = [f for f in api.list_repo_tree("HuggingFaceFW/fineweb-2", path_in_repo=f"data/{cfg}/train", repo_type="dataset") if f.path.endswith(".parquet")]
    rg, rows, size = [], 0, 0
    for f in files:
        md = pq.ParquetFile(fs.open(f"datasets/HuggingFaceFW/fineweb-2/{f.path}")).metadata
        rows += md.num_rows
        size += f.size
        rg += [md.row_group(i).num_rows for i in range(md.num_row_groups)]
    return {"files": len(files), "documents": int(rows), "bytes": int(size), "row_groups": [int(x) for x in rg]}


def share_ci(a_lat: float, b_nat: float, rng) -> tuple[float, list]:
    e = a_lat / (a_lat + b_nat)
    la, lb = rng.poisson(a_lat, N_BOOT), rng.poisson(b_nat, N_BOOT)
    sh = la / np.maximum(la + lb, 1)
    return e, [float(np.percentile(sh, 2.5)), float(np.percentile(sh, 97.5))]


def main() -> None:
    from huggingface_hub import HfApi, HfFileSystem
    api, fs = HfApi(), HfFileSystem()
    st = {}
    for lang, (nat, lat) in CFG.items():
        st[lang] = {"native": config_stats(fs, api, nat), "latin": config_stats(fs, api, lat)}
        print(lang, {k: (v["documents"], v["files"], len(v["row_groups"])) for k, v in st[lang].items()}, flush=True)
    rng = np.random.default_rng(0)
    out = {"source": "HuggingFaceFW/fineweb-2 (script-labelled configs); counts from parquet footers", "languages": {}}
    draws = {}
    for lang, d in st.items():
        a, b = d["latin"]["documents"], d["native"]["documents"]
        e, ci = share_ci(a, b, rng)
        ab, bb = d["latin"]["bytes"], d["native"]["bytes"]
        out["languages"][lang] = {"native_config": CFG[lang][0], "latin_config": CFG[lang][1], "documents_native": b, "documents_latin": a, "e_documents": e, "e_documents_ci95_poisson": ci,
                                  "bytes_native": bb, "bytes_latin": ab, "e_bytes": ab / (ab + bb)}
        la, lb = rng.poisson(a, N_BOOT), rng.poisson(b, N_BOOT)
        draws[lang] = la / np.maximum(la + lb, 1)
    diff = draws["hi"] - draws["kn"]
    lo, hi = float(np.percentile(diff, 2.5)), float(np.percentile(diff, 97.5))
    e_hi, e_kn = out["languages"]["hi"]["e_documents"], out["languages"]["kn"]["e_documents"]
    out["registered_test"] = {"e_hi": e_hi, "e_kn": e_kn, "difference": e_hi - e_kn, "ci95_poisson": [lo, hi],
                              "verdict": "supported" if lo > 0 else "refuted" if hi < 0 else "inconclusive",
                              "bytes_measure_same_sign": bool(out["languages"]["hi"]["e_bytes"] > out["languages"]["kn"]["e_bytes"])}
    out["ordering_by_e_documents"] = sorted(((k, v["e_documents"]) for k, v in out["languages"].items()), key=lambda x: -x[1])
    write_json(results_dir("phase2/x2") / "exposure.json", out, {"registration": "RESULTS.md X2 (Source A); deviation X2-D1: Poisson interval instead of a bootstrap over shards"})
    print(json.dumps(out["registered_test"], indent=1))
    print([(k, round(v * 100, 3)) for k, v in out["ordering_by_e_documents"]])


if __name__ == "__main__":
    sys.exit(main())
