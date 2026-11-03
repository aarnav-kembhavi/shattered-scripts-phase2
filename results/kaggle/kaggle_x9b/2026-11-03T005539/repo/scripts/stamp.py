"""Print the current time as a RESULTS.md entry stamp (system clock, IST): `2026-11-02 23:17 IST`. Use this, never a typed time."""
from datetime import datetime, timedelta, timezone

print(datetime.now(timezone(timedelta(hours=5, minutes=30))).strftime("%Y-%m-%d %H:%M IST"))
