"""Fail if any timestamped RESULTS.md entry is later than the time of the commit that wrote it (rule of 2026-11-02: times in logs come from the
system clock or the commit, never typed).

An entry is a line that starts with `- **YYYY-MM-DD HH:MM IST` (or `UTC`). Its stamp is compared, at minute resolution, with the author time of the
commit that last touched that line (`git blame`); a line that is not committed yet is compared with the system clock now. The project clock is IST
(UTC+05:30); the stamp's zone is honoured. Usage: python scripts/check_results_times.py [--file RESULTS.md] [--since 2026-11-02]
Exit code 1 and a list of the offending lines if any stamp is in the future of its commit. Also run by the git pre-commit hook (scripts/pre-commit-times.sh).
"""
import argparse
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
ZONES = {"IST": timezone(timedelta(hours=5, minutes=30)), "UTC": timezone.utc}
ENTRY = re.compile(r"^- \*\*(\d{4}-\d{2}-\d{2}) (\d{2}):(\d{2}) (IST|UTC)\b")


def blame_times(path: str) -> dict[int, datetime | None]:
    """line number (1-based) -> author time of the commit that last changed it (None = not committed yet)."""
    out = subprocess.run(["git", "blame", "--line-porcelain", "--", path], cwd=REPO, capture_output=True, text=True, encoding="utf-8", check=True).stdout
    res, cur, ts, sha = {}, None, None, None
    for ln in out.split("\n"):
        m = re.match(r"^([0-9a-f]{40}) \d+ (\d+)", ln)
        if m:
            sha, cur = m.group(1), int(m.group(2))
        elif ln.startswith("author-time "):
            ts = int(ln.split()[1])
        elif ln.startswith("\t") and cur is not None:
            res[cur] = None if set(sha) == {"0"} else datetime.fromtimestamp(ts, timezone.utc)
    return res


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", default="RESULTS.md")
    ap.add_argument("--since", default="0000-00-00", help="only entries dated on or after this day")
    a = ap.parse_args()
    now = datetime.now(timezone.utc)
    blame = blame_times(a.file)
    lines = (REPO / a.file).read_text(encoding="utf-8").split("\n")
    bad, n = [], 0
    for i, ln in enumerate(lines, 1):
        m = ENTRY.match(ln)
        if not m or m.group(1) < a.since:
            continue
        n += 1
        stamp = datetime(int(m.group(1)[:4]), int(m.group(1)[5:7]), int(m.group(1)[8:]), int(m.group(2)), int(m.group(3)), tzinfo=ZONES[m.group(4)])
        ref = blame.get(i) or now
        if stamp > ref.replace(second=0, microsecond=0) + timedelta(minutes=0) and stamp > ref:
            bad.append((i, stamp.isoformat(), ref.astimezone(ZONES["IST"]).isoformat(timespec="minutes"), ln[:90]))
    print(f"{n} timestamped entries checked in {a.file}; {len(bad)} later than their commit (or the clock)")
    for b in bad:
        print(f"  line {b[0]}: stamp {b[1]} > commit/clock {b[2]}: {b[3]}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
