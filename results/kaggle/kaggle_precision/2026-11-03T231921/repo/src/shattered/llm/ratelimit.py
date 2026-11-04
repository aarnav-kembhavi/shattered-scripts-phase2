"""Token-bucket rate limiting and retry with exponential backoff."""
from __future__ import annotations

import random
import threading
import time


class TokenBucket:
    """Allows `rate_per_min` acquisitions per minute with bursts up to `burst`."""

    def __init__(self, rate_per_min: float, burst: int = 1) -> None:
        self.rate = rate_per_min / 60.0
        self.capacity = burst
        self.tokens = float(burst)
        self.updated = time.monotonic()
        self._lock = threading.Lock()

    def acquire(self) -> float:
        """Block until a token is available; return seconds waited."""
        waited = 0.0
        while True:
            with self._lock:
                now = time.monotonic()
                self.tokens = min(self.capacity, self.tokens + (now - self.updated) * self.rate)
                self.updated = now
                if self.tokens >= 1:
                    self.tokens -= 1
                    return waited
                need = (1 - self.tokens) / self.rate
            time.sleep(need)
            waited += need


class RetryableError(Exception):
    def __init__(self, msg: str, retry_after: float | None = None) -> None:
        super().__init__(msg)
        self.retry_after = retry_after


class DailyQuotaExceeded(Exception):
    """Raised when our own per-day cap (or the provider's daily quota) is reached. Not retried."""


def with_backoff(fn, max_retries: int = 6, base: float = 2.0, cap: float = 120.0):
    for attempt in range(max_retries + 1):
        try:
            return fn()
        except RetryableError as e:
            if attempt == max_retries:
                raise
            delay = e.retry_after if e.retry_after else min(cap, base * 2 ** attempt)
            time.sleep(delay + random.uniform(0, 1))
