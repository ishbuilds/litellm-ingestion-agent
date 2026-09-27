"""Post text -> TrialOffer via an LLM called through LiteLLM (dogfooding)."""

from __future__ import annotations

import json

from .models import TrialOffer

SYSTEM_PROMPT = """You extract LLM trial offers from social media posts.
Return ONLY valid JSON matching this schema:
{
  "provider": "string",
  "model": "string",
  "offer_url": "string or null",
  "terms": {"credits_usd": number|null, "max_requests": number|null,
            "duration_days": number|null, "notes": "string"},
  "auth": {"type": "api_key|oauth|unknown", "signup_steps": ["..."]},
  "api_base": "string or null"
}
If a field is not in the post, use null ("" for notes). Never invent URLs."""


def extract_offer(
    post_text: str,
    *,
    model: str = "gpt-4o-mini",
    source_url: str | None = None,
) -> TrialOffer:
    """Extract a TrialOffer from raw post text using ``model`` via LiteLLM."""
    import litellm  # local import: the package imports without the dep installed

    resp = litellm.completion(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": post_text},
        ],
        response_format={"type": "json_object"},
        temperature=0,
    )
    data = json.loads(resp.choices[0].message.content)
    return TrialOffer(source_text=post_text, source_post_url=source_url, **data)
