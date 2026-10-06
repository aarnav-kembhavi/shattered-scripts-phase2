# Shattered Scripts

Code for "Shattered Scripts: How Tokenizer Fragmentation Taxes the Cost, Depth and Accuracy of Multilingual LLMs."
Project memory and rules: `CLAUDE.md`. Full experiment brief: `docs/BRIEF.md`. Results log: `RESULTS.md`.

## Setup (local, Windows/Linux)

```bash
uv venv --python 3.12 .venv
# CUDA build of torch (cu126 works with CUDA 12.x drivers >= 525)
uv pip install --python .venv/Scripts/python.exe torch --index-url https://download.pytorch.org/whl/cu126
uv pip install --python .venv/Scripts/python.exe -r requirements.txt -e .
cp .env.example .env   # then fill in keys
python scripts/env_check.py
```

## Setup (Kaggle / Colab)

Keep the platform's torch:

```bash
pip install -r requirements.in && pip install -e .
```

## Reproducing experiments

Each experiment has a thin entry point `scripts/eNN_*.py` driven by a YAML in `configs/`; outputs go to
`results/eNN_<name>/` together with the config and git commit hash. Sections are added here as experiments land.
