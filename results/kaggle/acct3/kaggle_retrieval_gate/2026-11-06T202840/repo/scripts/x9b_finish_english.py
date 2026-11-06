"""X9b secondary arm (Qwen3.5-2B): finish the English run after the Kaggle kernel hit its cap (account 2, 2026-11-05).

The kernel trained all three runs and finished the ITRANS and native runs; the English run finished training and the three SIB-200 evaluations but the cap hit during its retrieval step, so it has no
retrieval.json and no done.json. This script (laptop GPU) does exactly what the kernel's last step does: loads the fp16 base, merges the saved adapter, runs the Phase 1 retrieval scorer (x_score.score_retrieval),
rebuilds the English training stream on CPU to recover the consumed articles, words and tokens and to repeat the overlap scan, takes the loss log from the kernel's own stdout, and writes done.json marked
"reconstructed_after_timeout". Nothing about training or the other evaluations is re-run. Usage: python scripts/x9b_finish_english.py"""
import json
import re
import sys
import time
from pathlib import Path

import torch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kaggle_x9b as K  # noqa: E402
import x_score as XS  # noqa: E402

from shattered.interp.load import load  # noqa: E402
from shattered.runlog import REPO  # noqa: E402

RUN = REPO / "results" / "kaggle" / "acct2" / "kaggle_x9b" / "2026-11-04T214110"
TAG = "qwen3.5-2b+english+s0"


def main() -> None:
    rdir = RUN / "out" / TAG
    if (rdir / "done.json").exists():
        print("already done")
        return
    t0 = time.time()
    model, tok = load("qwen3.5-2b", "cuda", dtype=torch.float16)
    from peft import PeftModel
    model = PeftModel.from_pretrained(model, str(rdir / "adapter")).merge_and_unload()
    XS.score_retrieval(model, tok, TAG, rdir)
    del model
    K.free_gpu()
    pd_ = json.loads((K.REPORT / "pilot_done.json").read_text(encoding="utf-8"))
    B = pd_["models"]["qwen3.5-2b"]["B"]
    pool = K.Pool()
    sets = K.S.eval_sentences()
    sha = K.tok_hash(tok)
    seqs, st = K.build_stream(pool, "english", tok, B)
    overlap = K.scan_consumed(pool, "english", st["ids"], sets)
    log = []
    for line in open(RUN / "shattered-kaggle-x9b.log", encoding="utf-8"):
        m = re.search(r'"data":"' + re.escape(TAG) + r" (\{'step'.*?\})\\n", line)
        if m:
            log.append(eval(m.group(1)))  # noqa: S307 (a dict literal printed by our own kernel)
    done = {"tag": TAG, "model": "qwen3.5-2b", "condition": "english", "seed": 0, "B": B, "optimizer_steps": B // K.TOK_PER_STEP, "micro_batch": pd_["models"]["qwen3.5-2b"]["conditions"]["english"]["micro_batch"],
            "articles": st["articles"], "words": st["words"], "tokens": st["tokens"], "overlap_articles": overlap,
            "tokenizer_sha256_before": sha, "tokenizer_sha256_after": sha, "tokenizer_unchanged": True,
            "train_seconds": log[-1]["t"] if log else None, "seconds": None, "loss_log": log,
            "reconstructed_after_timeout": "the kernel's 10.2 h cap hit during this run's retrieval step; retrieval was run on the laptop from the saved adapter with the same scorer; stream statistics recomputed on CPU; "
                                           "tokenizer hash taken from the unmodified tokenizer (the kernel's own before/after hashes for this run were not written)"}
    (rdir / "done.json").write_text(json.dumps(done, indent=1))
    print("done", f"{time.time() - t0:.0f}s", "tokens", st["tokens"], "overlap", overlap)


if __name__ == "__main__":
    main()
