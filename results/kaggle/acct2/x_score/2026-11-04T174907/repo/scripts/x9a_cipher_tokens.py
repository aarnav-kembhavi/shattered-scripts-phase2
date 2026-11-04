"""X9a / X9a-low: absolute number of cipher tokens in each exposure level's training stream (descriptive; for the report). Recomputes, from the stored story order and the fixed tokenizer, the
tokens (with the EOS after each story) that belong to cipher stories among the stories each stream consumed, truncated at the stream length (n_tokens + 1) exactly as `tokenize_until` cuts it.
Each story appears once, either as English or as its letter-cipher rendering (never both): the streams contain no parallel pairs. Output: results/phase2/x9a/cipher_tokens.json."""
import json
import random
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import x9a as X  # noqa: E402

from shattered.pretrain import data as D  # noqa: E402
from shattered.runlog import write_json  # noqa: E402

LEVELS = {"0": 0.0, "0p01": 0.01, "0p03": 0.03, "0p1": 0.1, "0p3": 0.3, "1": 1.0, "5": 5.0, "20": 20.0, "50": 50.0}


def main() -> None:
    meta = X.load_meta()
    n_tokens = meta["_x9a"]["tokens_per_run"]
    stories = D.read_stories("train")
    random.Random(X.CFG["data"]["data_seed"]).shuffle(stories)
    train, _ = X.take(stories, 0, X.CFG["data"]["train_bytes"])
    n_train = len(train)
    tok = D.load_tokenizer(X.PROC / "tokenizer_1024.json")
    order = np.random.default_rng(9).permutation(n_train)
    out = {}
    for key, pct in LEVELS.items():
        m = meta[f"x9a_p{key}"]
        used = m["stories_consumed"]
        cset = set(order[: int(round(n_train * pct / 100))].tolist())
        cip = sorted(i for i in cset if i < used)  # only the cipher stories among the consumed ones are tokenized (memory-light)
        cipher = 0
        for b in range(0, len(cip), 20000):
            cipher += sum(len(e.ids) + 1 for e in tok.encode_batch([train[i].translate(X.ENC) for i in cip[b:b + 20000]]))
        out[key] = {"exposure_percent": pct, "cipher_tokens_untruncated": cipher, "cipher_stories_consumed": len(cip), "stories_consumed": used, "stream_tokens": n_tokens + 1,
                    "cipher_token_share_of_stream": cipher / (n_tokens + 1), "last_story_is_cipher_so_count_may_exceed_by_less_than_one_story": bool((used - 1) in cset)}
        print(key, out[key], flush=True)
    write_json(X.OUT / "cipher_tokens.json", out, {"note": "descriptive; stream length n_tokens + 1 = %d" % (n_tokens + 1)})


if __name__ == "__main__":
    main()
