"""Read-only: compare the backup archive results.zip (GitHub release asset, local copy) with the current results/ tree, file by file (sha256)."""
import collections
import hashlib
import os
import sys
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
os.chdir(REPO)
zp = REPO.parent / "backup_phase2_2026-11-08" / "results.zip"
z = zipfile.ZipFile(zp)
names = [i for i in z.infolist() if not i.is_dir()]
inzip = {i.filename for i in names}
same = []
diff = []
miss = []
for i in names:
    if not os.path.exists(i.filename):
        miss.append(i.filename)
        continue
    h1 = hashlib.sha256(z.read(i)).hexdigest()
    h2 = hashlib.sha256(open(i.filename, "rb").read()).hexdigest()
    (same if h1 == h2 else diff).append(i.filename)
cur = []
for r, d, f in os.walk("results"):
    for x in f:
        cur.append(os.path.join(r, x).replace(chr(92), "/"))
new = sorted(c for c in cur if c not in inzip)
print("archive files", len(names), "bytes", sum(i.file_size for i in names))
print("identical", len(same), "| changed since archive", len(diff), "| in archive but missing now", len(miss), "| current files", len(cur), "| new since archive", len(new))
print("changed:", diff[:20])
print("missing:", miss[:10])
print("new by folder:", collections.Counter("/".join(n.split("/")[:3]) for n in new).most_common(12))
sys.stdout.flush()
