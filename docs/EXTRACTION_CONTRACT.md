# Extraction contract — TrialOffer

The JSON the extractor must produce, and the shape stored in SQLite.
`src/litellm_ingestion_agent/models.py` is the executable version of this document.

## Schema

```jsonc
{
  "provider": "string, required — e.g. \"AcmeAI\"",
  "model": "string, required — model id as exposed, e.g. \"acme-1\"",
  "offer_url": "string|null — signup URL from the post",
  "source_post_url": "string|null — where the offer was found",
  "source_text": "string — raw post text, kept for audit",
  "discovered_at": "ISO-8601 datetime",
  "terms": {
    "credits_usd": "number|null, >= 0",
    "max_requests": "integer|null, >= 0",
    "duration_days": "integer|null, >= 0",
    "notes": "string — anything else (\"card required\", \"rate limits\", ...)"
  },
  "auth": {
    "type": "\"api_key\" | \"oauth\" | \"unknown\"",
    "signup_steps": ["string — ordered steps to claim the trial"]
  },
  "api_base": "string|null — custom OpenAI-compatible endpoint, if given",
  "status": "\"discovered\" | \"signed_up\" | \"active\" | \"expired\" | \"exhausted\"",
  "env_key_name": "string|null — env var that will hold the API key, e.g. \"ACMEAI_API_KEY\""
}
```

## Rules

- Never invent URLs. If the post has no signup link, `offer_url` is `null`.
- Missing numeric limits are `null`, not `0` (`0` means "none granted").
- `notes` captures everything that doesn't fit the numeric fields —
  card requirements, region locks, "first 100 users", etc.
- The extractor returns everything except `source_text`, `source_post_url`,
  `discovered_at`, `status`, and `env_key_name`; the CLI fills those in.

## Example

```json
{
  "provider": "AcmeAI",
  "model": "acme-1",
  "offer_url": "https://acme.ai/trial",
  "terms": {
    "credits_usd": 25,
    "max_requests": null,
    "duration_days": 30,
    "notes": "credit card required; resets monthly"
  },
  "auth": {
    "type": "api_key",
    "signup_steps": ["Sign up with email", "Verify email", "Copy API key from dashboard"]
  },
  "api_base": "https://api.acme.ai/v1"
}
```
