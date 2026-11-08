# Phase 2 cleanup list (nothing is deleted until Aarnav says so)

Written 2026-11-08. Delete only after Phase 2 is closed; log every deletion in RESULTS.md.

## Kaggle (private datasets and kernels; all private)
- Account 1 (aarnavkembhavi1): datasets shattered-pkg, shattered-flores-private, shattered-ambari-instruct-v0-1, shattered-llama-3-1-8b, shattered-llama-2-7b-hf; kernels shattered-x-score, shattered-kaggle-x9b, shattered-kaggle-mdl, shattered-kaggle-precision, shattered-kaggle-gate, shattered-kaggle-retrieval-gate.
- Account 2 (a teammate's): datasets shattered-pkg, shattered-flores-private, shattered-ambari-instruct-v0-1, shattered-llama-3-1-8b; the same six kernels.
- Account 3 (a teammate's, current): datasets shattered-pkg, shattered-flores-private, shattered-x10-inputs; kernels shattered-kaggle-gate, shattered-kaggle-retrieval-gate, shattered-x-score, shattered-kaggle-x10, shattered-nettest.
- Earlier third-account attempt (a different teammate login, no internet): dataset shattered-flores-private and shattered-pkg; kernels shattered-kaggle-gate, shattered-kaggle-retrieval-gate, shattered-nettest.

## Tokens to revoke (the first two and the third were pasted in chat)
- Account 2's Kaggle token (KAGGLE2_API_TOKEN).
- The first third-account token (KAGGLE3_API_TOKEN_PREVIOUS) and the current one (KAGGLE3_API_TOKEN).
- Remove the lines from `.env` after revocation; delete `build/kaggle_config_*`.

## Other
- Keep: GitHub private repo and its backup release, the Drive folder (README and manifest; the zip files are still to be dragged in), the local backup folder C:\PROJECTS\PROMPT\backup_phase2_2026-11-08.
- Local: Hugging Face cache and model weights are not backed up and are not part of the project record; `cache/llm_cache.sqlite` is never deleted.
