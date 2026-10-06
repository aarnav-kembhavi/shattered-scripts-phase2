import pytest

from shattered.llm import ratelimit
from shattered.llm.cache import ResponseCache, request_key
from shattered.llm.client import LLMClient, LLMResponse
from shattered.llm.ratelimit import DailyQuotaExceeded, RetryableError, TokenBucket, with_backoff


class FakeClient(LLMClient):
    def __init__(self, *a, fail_times=0, **kw):
        super().__init__("fake", "m", rpm=6000, **kw)
        self.calls = 0
        self.fail_times = fail_times

    def _call_fake(self, prompt, p):
        self.calls += 1
        if self.calls <= self.fail_times:
            raise RetryableError("429", retry_after=0.01)
        return LLMResponse(text=f"echo:{prompt}", input_tokens=3, output_tokens=1, finish_reason="stop",
                           cached=False, extra={})


@pytest.fixture
def cache(tmp_path):
    return ResponseCache(tmp_path / "c.sqlite")


def test_cache_hit_does_not_call_api(cache):
    c = FakeClient(cache=cache)
    r1 = c.generate("hi")
    r2 = c.generate("hi")
    assert (r1.text, r1.cached, r2.cached, c.calls) == ("echo:hi", False, True, 1)
    c.generate("hi", max_tokens=5)  # different params -> different key
    assert c.calls == 2
    assert cache.requests_today("fake", "m") == 2


def test_cache_persists_across_instances(cache):
    FakeClient(cache=cache).generate("x")
    c2 = FakeClient(cache=cache)
    assert c2.generate("x").cached and c2.calls == 0


def test_daily_cap(cache):
    c = FakeClient(cache=cache, rpd=1)
    c.generate("a")
    with pytest.raises(DailyQuotaExceeded):
        c.generate("b")
    assert c.generate("a").cached  # cached items still served after the cap


def test_backoff_retries(cache, monkeypatch):
    monkeypatch.setattr(ratelimit.random, "uniform", lambda a, b: 0)
    c = FakeClient(cache=cache, fail_times=2)
    assert c.generate("z").text == "echo:z" and c.calls == 3


def test_backoff_gives_up():
    def always():
        raise RetryableError("x", retry_after=0.001)
    with pytest.raises(RetryableError):
        with_backoff(always, max_retries=2)


def test_request_key_stable_and_sensitive():
    k = request_key("p", "m", "hello", {"a": 1, "b": 2})
    assert k == request_key("p", "m", "hello", {"b": 2, "a": 1})
    assert k != request_key("p", "m", "hello ", {"a": 1, "b": 2})


def test_token_bucket_rate():
    b = TokenBucket(rate_per_min=600, burst=1)  # 10/s
    b.acquire()
    assert 0.05 < b.acquire() < 0.3
