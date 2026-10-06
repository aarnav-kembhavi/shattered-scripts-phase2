"""Cached, rate-limited LLM clients for free-tier providers (Gemini, Groq, OpenRouter) and token counters.

Every call is keyed by sha256(provider, model, prompt, params) and stored in SQLite; re-running never re-calls the
API. Temperature defaults to 0. Provider-reported token usage is stored with each response.
"""
from __future__ import annotations

import os
import re
from dataclasses import dataclass

from dotenv import load_dotenv

from ..runlog import REPO
from .cache import ResponseCache, request_key
from .ratelimit import DailyQuotaExceeded, RetryableError, TokenBucket, with_backoff

load_dotenv(REPO / ".env")


@dataclass
class LLMResponse:
    text: str
    input_tokens: int | None
    output_tokens: int | None
    finish_reason: str | None
    cached: bool
    extra: dict  # provider-specific usage fields (e.g. thinking tokens)


def _messages(prompt, system: str | None) -> list[dict]:
    msgs = [{"role": "user", "content": prompt}] if isinstance(prompt, str) else list(prompt)
    return ([{"role": "system", "content": system}] if system else []) + msgs


def _classify_error(e: Exception):
    """Turn provider exceptions into RetryableError / DailyQuotaExceeded, or re-raise."""
    status = getattr(e, "status_code", None) or getattr(e, "code", None) or getattr(e, "status", None)
    msg = str(e)
    if isinstance(status, str) and status.isdigit():
        status = int(status)
    if status == 429 or "RESOURCE_EXHAUSTED" in msg or "rate limit" in msg.lower():
        if re.search(r"per.?day|PerDay|daily", msg, re.I):
            raise DailyQuotaExceeded(msg) from e
        m = re.search(r"retry.{0,20}?(\d+(?:\.\d+)?)\s*s", msg, re.I)
        raise RetryableError(msg, float(m.group(1)) if m else None) from e
    if isinstance(status, int) and status >= 500:
        raise RetryableError(msg) from e
    raise e


class LLMClient:
    """One (provider, model) pair. `rpm`/`rpd` are our own conservative caps, set below the free-tier limits."""

    def __init__(self, provider: str, model: str, rpm: float = 10, rpd: int | None = None,
                 cache: ResponseCache | None = None) -> None:
        self.provider, self.model, self.rpd = provider, model, rpd
        self.cache = cache if cache is not None else ResponseCache()
        self.bucket = TokenBucket(rpm)
        self._sdk = None

    # ------------------------------------------------------------ public
    def generate(self, prompt, system: str | None = None, max_tokens: int = 16, temperature: float = 0.0,
                 **params) -> LLMResponse:
        params = {"max_tokens": max_tokens, "temperature": temperature, "system": system, **params}
        key = request_key(self.provider, self.model, prompt, params)
        hit = self.cache.get(key)
        if hit is not None:
            return LLMResponse(**{**hit, "cached": True})
        if self.rpd is not None and self.cache.requests_today(self.provider, self.model) >= self.rpd:
            raise DailyQuotaExceeded(f"{self.provider}/{self.model}: own daily cap {self.rpd} reached")

        def call():
            self.bucket.acquire()
            try:
                return getattr(self, f"_call_{self.provider}")(prompt, params)
            except (RetryableError, DailyQuotaExceeded):
                raise
            except Exception as e:  # noqa: BLE001 - classified below
                _classify_error(e)

        resp = with_backoff(call)
        self.cache.record_usage(self.provider, self.model, resp.input_tokens, resp.output_tokens)
        stored = {k: v for k, v in resp.__dict__.items() if k != "cached"}
        self.cache.put(key, self.provider, self.model, {"prompt": prompt, "params": params}, stored)
        return resp

    # ------------------------------------------------------------ providers
    def _call_gemini(self, prompt, p: dict) -> LLMResponse:
        from google import genai
        from google.genai import types
        if self._sdk is None:
            self._sdk = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
        cfg = {"temperature": p["temperature"], "max_output_tokens": p["max_tokens"]}
        if p.get("system"):
            cfg["system_instruction"] = p["system"]
        if p.get("thinking_budget") is not None:
            cfg["thinking_config"] = types.ThinkingConfig(thinking_budget=p["thinking_budget"])
        contents = prompt if isinstance(prompt, str) else [
            {"role": "model" if m["role"] == "assistant" else "user", "parts": [{"text": m["content"]}]}
            for m in prompt]
        r = self._sdk.models.generate_content(model=self.model, contents=contents,
                                              config=types.GenerateContentConfig(**cfg))
        u = r.usage_metadata
        cand = r.candidates[0] if r.candidates else None
        return LLMResponse(
            text=r.text or "", input_tokens=getattr(u, "prompt_token_count", None),
            output_tokens=getattr(u, "candidates_token_count", None),
            finish_reason=str(cand.finish_reason) if cand else None, cached=False,
            extra={"thoughts_tokens": getattr(u, "thoughts_token_count", None),
                   "total_tokens": getattr(u, "total_token_count", None)})

    def _openai_style(self, client, prompt, p: dict, extra_body: dict | None = None) -> LLMResponse:
        kwargs = {k: v for k, v in p.items() if k not in ("max_tokens", "temperature", "system")}
        r = client.chat.completions.create(model=self.model, messages=_messages(prompt, p.get("system")),
                                           temperature=p["temperature"], max_tokens=p["max_tokens"],
                                           extra_body=extra_body, **kwargs)
        c = r.choices[0]
        u = r.usage
        return LLMResponse(text=c.message.content or "", input_tokens=getattr(u, "prompt_tokens", None),
                           output_tokens=getattr(u, "completion_tokens", None), finish_reason=c.finish_reason,
                           cached=False, extra={"usage": u.model_dump() if u else None})

    def _call_groq(self, prompt, p: dict) -> LLMResponse:
        from groq import Groq
        if self._sdk is None:
            self._sdk = Groq(api_key=os.environ["GROQ_API_KEY"], max_retries=0)
        return self._openai_style(self._sdk, prompt, p)

    def _call_openrouter(self, prompt, p: dict) -> LLMResponse:
        from openai import OpenAI
        if self._sdk is None:
            self._sdk = OpenAI(api_key=os.environ["OPENROUTER_API_KEY"], base_url="https://openrouter.ai/api/v1",
                               max_retries=0)
        return self._openai_style(self._sdk, prompt, p)


class TokenCounter:
    """Free token-counting endpoints (no generation), cached like generation calls."""

    def __init__(self, provider: str, model: str, rpm: float = 60, cache: ResponseCache | None = None) -> None:
        self.provider, self.model = provider, model
        self.cache = cache if cache is not None else ResponseCache()
        self.bucket = TokenBucket(rpm)
        self._sdk = None

    def count(self, text: str) -> int:
        key = request_key(f"{self.provider}-count", self.model, text, {})
        hit = self.cache.get(key)
        if hit is not None:
            return hit["tokens"]

        def call():
            self.bucket.acquire()
            try:
                return getattr(self, f"_count_{self.provider}")(text)
            except Exception as e:  # noqa: BLE001
                _classify_error(e)

        n = with_backoff(call)
        self.cache.put(key, f"{self.provider}-count", self.model, {"text": text}, {"tokens": n})
        return n

    def _count_gemini(self, text: str) -> int:
        from google import genai
        if self._sdk is None:
            self._sdk = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
        return self._sdk.models.count_tokens(model=self.model, contents=text).total_tokens

    def _count_anthropic(self, text: str) -> int:
        import anthropic
        if self._sdk is None:
            self._sdk = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"], max_retries=0)
        return self._sdk.messages.count_tokens(model=self.model,
                                               messages=[{"role": "user", "content": text}]).input_tokens
