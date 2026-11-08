"""Second backup (2026-11-09), read-only on the repo. Stage 'scan': inventory of what the 2026-11-08 backup does not hold. Stage 'build': zip parts under 1.9 GB each into the backup folder.
Nothing is deleted or changed. Secrets (.env, tokens, Kaggle config, annotation/private, annotation/returned) are never included.
Usage: python scripts/backup2.py scan <out.json> | python scripts/backup2.py build <scan.json> <out_dir>"""
import hashlib
import json
import os
import re
import subprocess
import sys
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
os.chdir(REPO)
OLD = REPO.parent / "backup_phase2_2026-11-08" / "results.zip"
PART_MAX = int(1.9 * 1024 ** 3)
NEVER = (".env", "build/kaggle_config_", "annotation/private/", "annotation/returned/", "kaggle.json", ".venv/", ".git/")
SECRET = re.compile(r"KGAT_[0-9a-f]{10,}|hf_[A-Za-z0-9]{25,}|AIza[0-9A-Za-z_-]{30,}|gsk_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9]{20,}|KAGGLE\d?_API_TOKEN\s*=\s*\S{8,}|GEMINI_API_KEY\s*=\s*\S{8,}|GROQ_API_KEY\s*=\s*\S{8,}|Bearer [A-Za-z0-9._-]{20,}|password\s*[=:]\s*\S{4,}", re.I)


def sha(p, buf=8 * 1024 * 1024):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(buf), b""):
            h.update(b)
    return h.hexdigest()


def never(p):
    return any(p == x or p.startswith(x) for x in NEVER) or p.endswith(".pyc") or "/__pycache__/" in p


def scan(out):
    z = zipfile.ZipFile(OLD)
    old = {i.filename: i for i in z.infolist() if not i.is_dir()}
    cur = []
    for r, ds, fs in os.walk("results"):
        for f in fs:
            cur.append(os.path.join(r, f).replace(chr(92), "/"))
    A_new, A_changed = [], []
    for p in cur:
        if never(p):
            continue
        if p not in old:
            A_new.append(p)
        elif os.path.getsize(p) != old[p].file_size or sha(p) != hashlib.sha256(z.read(p)).hexdigest():
            A_changed.append(p)
    untracked = [p for p in subprocess.run(["git", "ls-files", "--others", "--exclude-standard"], capture_output=True, text=True, encoding="utf-8").stdout.split("\n") if p and not never(p)]
    modified = [p for p in subprocess.run(["git", "ls-files", "-m"], capture_output=True, text=True, encoding="utf-8").stdout.split("\n") if p and not never(p)]
    final = sorted(p.replace(chr(92), "/") for p in map(str, Path("checkpoints").rglob("final.safetensors")))
    arch_root = REPO.parent / "cleanup_archive_2026-11-09"
    arch = sorted(str(p.relative_to(REPO.parent)).replace(chr(92), "/") for p in arch_root.rglob("*") if p.is_file())
    out_d = dict(new_since_old_archive=sorted(A_new), changed_since_old_archive=sorted(A_changed), untracked=sorted(untracked), modified=sorted(modified), final_safetensors=final, cleanup_archive=arch)
    Path(out).write_text(json.dumps(out_d), encoding="utf-8")
    for k, v in out_d.items():
        base = REPO.parent if k == "cleanup_archive" else REPO
        print(f"{k}: {len(v)} files, {sum(os.path.getsize(base / x) for x in v) / 1048576:,.1f} MB")


def build(scanf, out_dir):
    d = json.loads(Path(scanf).read_text(encoding="utf-8"))
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    items = {}  # arcname -> (source path, group)
    for k in ("new_since_old_archive", "changed_since_old_archive", "untracked", "modified"):
        for p in d[k]:
            items.setdefault("repo/" + p, (REPO / p, k))
    for p in d["cleanup_archive"]:
        items["cleanup_archive_2026-11-09/" + p.split("/", 1)[1]] = (REPO.parent / p, "cleanup_archive")
    for p in d["final_safetensors"]:
        items["repo/" + p] = (REPO / p, "final_safetensors")
    order = sorted(items, key=lambda a: (items[a][1] == "final_safetensors", items[a][1] == "cleanup_archive", a))
    parts, cur_i, cur_sz, zf = [], 0, 0, None
    manifest = []

    def open_part(i):
        name = f"phase2_backup2_part{i:02d}.zip"
        return name, zipfile.ZipFile(out / name, "w", zipfile.ZIP_DEFLATED, compresslevel=6)
    cur_name, zf = open_part(1)
    for a in order:
        src, grp = items[a]
        sz = src.stat().st_size
        if cur_sz + sz > PART_MAX and cur_sz > 0:
            zf.close()
            cur_i += 1
            cur_name, zf = open_part(cur_i + 1)
            cur_sz = 0
        zf.write(src, a)
        cur_sz += sz
        manifest.append(dict(path=a, group=grp, bytes=sz, part=cur_name))
    zf.close()
    (out / "MANIFEST2.json").write_text(json.dumps(manifest, indent=0), encoding="utf-8")
    res = {}
    for f in sorted(out.glob("phase2_backup2_part*.zip")):
        res[f.name] = dict(bytes=f.stat().st_size, sha256=sha(f), files=len(zipfile.ZipFile(f).namelist()))
    (out / "HASHES2.json").write_text(json.dumps(res, indent=1), encoding="utf-8")
    for k, v in res.items():
        print(k, v["files"], "files", f"{v['bytes'] / 1048576:,.1f} MB", v["sha256"])


if __name__ == "__main__":
    scan(sys.argv[2]) if sys.argv[1] == "scan" else build(sys.argv[2], sys.argv[3])
