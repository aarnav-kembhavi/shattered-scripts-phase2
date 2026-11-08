"""Backup manifest and archives (2026-11-08): what goes off this machine, what is excluded and why. Never included: .env, any token or credential file, the Hugging Face cache, model weights
(adapter_model.safetensors, ckpt.pt, any .safetensors/.bin/.gguf/.ckpt), the virtual environment, caches (cache/), build/ (account configuration folders hold login state), data/raw, .git.
Usage: python scripts/backup_manifest.py list              prints sizes
       python scripts/backup_manifest.py zip OUTDIR        writes results_*.zip (below 1.8 GB each), annotation.zip, root_docs.zip and MANIFEST.json (file count, size, sha256 per archive)"""
import hashlib
import json
import os
import sys
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
EXC_NAMES = {"adapter_model.safetensors", "ckpt.pt", "ckpt.tmp"}
EXC_SUFFIX = (".safetensors", ".bin", ".gguf", ".ckpt")
SKIP_TOP = (".git", ".venv", "cache", "build", "data/raw")
LIMIT = 1_800_000_000


def why_excluded(name: str) -> str | None:
    low = name.lower()
    if name in EXC_NAMES or low.endswith(EXC_SUFFIX):
        return "model weights / checkpoints"
    if name == ".env" or (name.startswith(".env.") and name != ".env.example") or low == "kaggle.json" or low in ("access_token", "credentials.json", "token.json"):
        return "credentials"
    return None


def walk(top: str):
    base = REPO / top
    if base.is_file():
        yield base, None
        return
    for root, dirs, files in os.walk(base):
        rel = Path(root).relative_to(REPO).as_posix()
        if any(rel == s or rel.startswith(s + "/") for s in SKIP_TOP):
            dirs[:] = []
            continue
        for f in files:
            yield Path(root) / f, why_excluded(f)


def collect(tops: list[str]):
    inc, exc = [], {}
    for t in tops:
        for p, why in walk(t):
            sz = p.stat().st_size
            if why:
                exc.setdefault(why, [0, 0])
                exc[why][0] += 1
                exc[why][1] += sz
            else:
                inc.append((p, sz))
    return inc, exc


def main() -> None:
    cmd = sys.argv[1]
    groups = {"results": ["results"], "annotation": ["annotation"], "root_docs": ["RESULTS.md", "CLAUDE.md", "DATA_CARD.md", "docs", "paper2", "configs", "scripts", "src", "pyproject.toml"]}
    if cmd == "list":
        for g, tops in groups.items():
            inc, exc = collect(tops)
            print(g, len(inc), "files", round(sum(s for _, s in inc) / 1e6, 1), "MB", {k: (v[0], round(v[1] / 1e6, 1)) for k, v in exc.items()})
        return
    out = Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    manifest = {}
    for g, tops in groups.items():
        inc, exc = collect(tops)
        parts, cur, cur_sz = [], [], 0
        for p, sz in sorted(inc):
            if cur and cur_sz + sz > LIMIT:
                parts.append(cur)
                cur, cur_sz = [], 0
            cur.append((p, sz))
            cur_sz += sz
        parts.append(cur)
        for i, part in enumerate(parts):
            name = f"{g}_{i + 1}.zip" if len(parts) > 1 else f"{g}.zip"
            with zipfile.ZipFile(out / name, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
                for p, _ in part:
                    z.write(p, p.relative_to(REPO).as_posix())
            h = hashlib.sha256((out / name).read_bytes()).hexdigest()
            manifest[name] = {"files": len(part), "uncompressed_bytes": sum(s for _, s in part), "zip_bytes": (out / name).stat().st_size, "sha256": h}
            print(name, manifest[name], flush=True)
        manifest[g + "_excluded"] = {k: {"files": v[0], "bytes": v[1]} for k, v in exc.items()}
    (out / "MANIFEST.json").write_text(json.dumps(manifest, indent=1))


if __name__ == "__main__":
    main()
