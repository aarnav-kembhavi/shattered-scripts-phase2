"""SQLite cache for API calls, plus persistent per-day usage counters (for free-tier caps)."""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import sqlite3
import threading
from pathlib import Path

from ..runlog import REPO

DEFAULT_DB = REPO / "cache" / "llm_cache.sqlite"


def request_key(provider: str, model: str, prompt, params: dict) -> str:
    """sha256 over (provider, model, prompt, params); prompt may be a string or a list of messages."""
    blob = json.dumps({"provider": provider, "model": model, "prompt": prompt, "params": params},
                      sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


class ResponseCache:
    def __init__(self, path: Path | str = DEFAULT_DB) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()
        self._db = sqlite3.connect(self.path, check_same_thread=False)
        self._db.execute("PRAGMA journal_mode=WAL")
        self._db.execute("""CREATE TABLE IF NOT EXISTS responses (
            key TEXT PRIMARY KEY, provider TEXT, model TEXT, request TEXT, response TEXT, created_utc TEXT)""")
        self._db.execute("""CREATE TABLE IF NOT EXISTS usage (
            day TEXT, provider TEXT, model TEXT, requests INTEGER, input_tokens INTEGER, output_tokens INTEGER,
            PRIMARY KEY (day, provider, model))""")
        self._db.commit()

    def get(self, key: str) -> dict | None:
        with self._lock:
            row = self._db.execute("SELECT response FROM responses WHERE key=?", (key,)).fetchone()
        return json.loads(row[0]) if row else None

    def put(self, key: str, provider: str, model: str, request: dict, response: dict) -> None:
        with self._lock:
            self._db.execute("INSERT OR REPLACE INTO responses VALUES (?,?,?,?,?,?)",
                             (key, provider, model, json.dumps(request, ensure_ascii=False),
                              json.dumps(response, ensure_ascii=False), _now()))
            self._db.commit()

    def record_usage(self, provider: str, model: str, input_tokens: int, output_tokens: int) -> None:
        with self._lock:
            self._db.execute("""INSERT INTO usage VALUES (?,?,?,1,?,?) ON CONFLICT(day, provider, model) DO UPDATE SET
                requests=requests+1, input_tokens=input_tokens+excluded.input_tokens,
                output_tokens=output_tokens+excluded.output_tokens""",
                             (_today(), provider, model, input_tokens or 0, output_tokens or 0))
            self._db.commit()

    def requests_today(self, provider: str, model: str) -> int:
        with self._lock:
            row = self._db.execute("SELECT requests FROM usage WHERE day=? AND provider=? AND model=?",
                                   (_today(), provider, model)).fetchone()
        return row[0] if row else 0

    def __len__(self) -> int:
        with self._lock:
            return self._db.execute("SELECT COUNT(*) FROM responses").fetchone()[0]


def _now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def _today() -> str:
    # Free-tier daily quotas reset at midnight Pacific for Gemini; UTC day is a conservative-enough bucket here
    # because we also stop on the provider's own 429.
    return dt.datetime.now(dt.timezone.utc).date().isoformat()
