"""Shared pieces of the annotation importers (import_x8.py, import_x15.py, import_t3.py): one command each over annotation/returned/.

Returned files are identified by the `File id: ...` line of their Instructions sheet (not by their name; people rename attachments). Cross-file checks (all identity
comparisons use a hash of the file's creator / last-modified-by fields, which Excel fills with the user's name when a file is saved; the names themselves are never printed
or written, only "the same hash occurs in files A and B"):
  - no file id twice (two returned copies of the same task), no two returned files byte-identical;
  - X15: no person (same hash) behind two X15 files; X8: P and Q come from two different files and two different persons, and their answers are not copies of each other;
  - no returned file matches a private key: its sha256 equals a file of annotation/private/, its name is a key file's name, or (X15) its answers equal the gold labels on every row.
"""
import hashlib
import json
import re
import zipfile
from pathlib import Path

from openpyxl import load_workbook

from shattered.runlog import REPO

RETURNED = REPO / "annotation" / "returned"
PRIVATE = REPO / "annotation" / "private"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def person_hash(path: Path) -> str | None:
    """Hash of the creator and last-modified-by fields (None when both are blank): identifies a person across files without storing a name."""
    core = zipfile.ZipFile(path).read("docProps/core.xml").decode("utf-8", "replace")
    parts = []
    for tag in ("creator", "lastModifiedBy"):
        m = re.search(rf"<(?:dc|cp):{tag}>([^<]*)</", core)
        if m and m.group(1).strip():
            parts.append(m.group(1).strip().lower())
    return hashlib.sha256("|".join(sorted(set(parts))).encode()).hexdigest()[:12] if parts else None


def file_id(path: Path) -> str | None:
    try:
        wb = load_workbook(path, read_only=True)
        ins = "\n".join(str(r[0]) for r in wb["Instructions"].iter_rows(values_only=True) if r and r[0])
        m = re.search(r"File id: (\S+)", ins)
        return m.group(1) if m else None
    except Exception:  # noqa: BLE001 - reported as an unreadable file by the caller
        return None


def returned_files(prefix: str, folder: Path = RETURNED) -> list[Path]:
    """Returned workbooks whose file id starts with `prefix` (X8_, X15_, T3_); unreadable or unidentifiable .xlsx files are reported by `orphans`."""
    return sorted(p for p in folder.glob("*.xlsx") if not p.name.startswith("~$") and (file_id(p) or "").startswith(prefix))


def orphans(folder: Path = RETURNED) -> list[str]:
    return sorted(p.name for p in folder.glob("*.xlsx") if not p.name.startswith("~$") and not file_id(p))


def private_hashes() -> dict[str, str]:
    return {sha256(p): p.name for p in PRIVATE.glob("*") if p.is_file()} if PRIVATE.exists() else {}


def cross_checks(paths: list[Path], ids: dict[Path, str | None], kind: str) -> list[str]:
    """Blockers over a set of returned files of one kind (see the module docstring)."""
    out = []
    seen_id: dict[str, Path] = {}
    seen_sha: dict[str, Path] = {}
    seen_person: dict[str, Path] = {}
    priv = private_hashes()
    key_names = {p.name.lower() for p in PRIVATE.glob("*")} if PRIVATE.exists() else set()
    for p in paths:
        fid = ids[p]
        if fid in seen_id:
            out.append(f"file id {fid} appears in two returned files: {seen_id[fid].name} and {p.name}")
        seen_id.setdefault(fid, p)
        h = sha256(p)
        if h in priv:
            out.append(f"{p.name} is byte-identical to the private key file {priv[h]}")
        if p.name.lower() in key_names:
            out.append(f"{p.name} has the name of a private key file")
        if h in seen_sha:
            out.append(f"{p.name} is byte-identical to {seen_sha[h].name}")
        seen_sha.setdefault(h, p)
        ph = person_hash(p)
        if ph and ph in seen_person and kind in ("X15", "X8"):
            out.append(f"the same person (matching author fields, hash {ph}) is behind {seen_person[ph].name} and {p.name}")
        if ph:
            seen_person.setdefault(ph, p)
    return out


def write_md(path: Path, title: str, reports: list[dict], cross: list[str], extra: list[str] | None = None) -> None:
    L = [f"# {title}", "", f"Files checked: {len(reports)}. Cross-file blockers: {len(cross)}.", ""]
    for c in cross:
        L.append(f"- BLOCKER (cross-file): {c}")
    for r in reports:
        L += ["", f"## {r.get('file')}  ({'OK' if r.get('ok') else 'BLOCKED'})"]
        for b in r.get("blockers", []):
            L.append(f"- BLOCKER: {b}")
        for w in r.get("warnings", []):
            L.append(f"- warning: {w}")
        for k, v in r.items():
            if k.startswith(("share_", "n_", "mean_", "choice_", "unexpected")) and not isinstance(v, dict):
                L.append(f"- {k}: {round(v, 4) if isinstance(v, float) else v}")
            elif k in ("choice_counts", "unexpected_characters"):
                L.append(f"- {k}: {v}")
    for e in extra or []:
        L.append(e)
    path.write_text("\n".join(L) + "\n", encoding="utf-8")
