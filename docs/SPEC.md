# SPEC — litellm-ingestion-agent

> Source of truth for this project. Code, tests, and docs must conform to this
> spec. If behavior and spec disagree, the spec wins until it is amended here.

## 1. Problem

Ish signs up for lots of LLM trial accounts discovered in X/Threads posts.
The details — provider, model, signup link, credit/request limits, expiry,
API keys — scatter across posts, emails, and provider dashboards. There is no
single place to manage them, and no pipeline to feed them into LiteLLM.

## 2. Users

- **Primary:** Ish, a solo developer building an FDE portfolio.
- **Secondary:** any developer juggling multiple LLM trial accounts who uses
  LiteLLM as a unified gateway.

## 3. Goals

- One CLI-first place to capture trial offers from unstructured post text.
- Structured trial records with limits, expiry, and status.
- One-command export of active trials to a valid LiteLLM `config.yaml`.
- Limit/expiry tracking so trials don't silently die or surprise-bill.

## 4. Non-goals (v1)

- Automatic scraping of X/Threads (ToS + API limits; v1 takes pasted text).
- Automatic account signup (the user signs up; the agent manages what exists).
- Real-time usage metering (limits are recorded and tracked manually in v1).
- Web UI (CLI first; a dashboard is a later milestone).

## 5. Functional requirements

- **FR-1 Ingest.** Accept raw post text via CLI argument or stdin, plus an
  optional source-post URL.
- **FR-2 Extract.** Produce a `TrialOffer` record conforming to
  `docs/EXTRACTION_CONTRACT.md`, using an LLM through LiteLLM itself
  (dogfood any configured model; default: cheapest available).
- **FR-3 Review.** Print the extracted record and require explicit user
  confirmation before saving. No silent writes.
- **FR-4 Store.** Persist offers in local SQLite
  (`~/.litellm-ingestion-agent/trials.db`). Statuses:
  `discovered → signed_up → active → expired | exhausted`.
- **FR-5 Export.** Generate a valid LiteLLM `config.yaml` `model_list` from
  active offers. API keys are referenced as `os.environ/<NAME>`; the key
  values are **never** written into the file.
- **FR-6 Track.** `list` shows every trial with status, limits, and expiry at
  a glance; warn about anything expiring within 7 days.
- **FR-7 Secrets.** Keys live in environment variables or a local `.env`.
  The repo never commits secrets; CI fails if a secret-looking value is
  committed (see `SECURITY.md`).

## 6. Acceptance criteria (v1)

- [ ] `litellm-ingestion-agent add-post` turns a pasted trial post into a confirmed,
      stored offer in under a minute.
- [ ] `litellm-ingestion-agent export-config` output loads in LiteLLM without hand-edits.
- [ ] `litellm-ingestion-agent list` shows every trial with status and limits at a glance.
- [ ] No secrets in the repo; `ruff` and `pytest` are green on CI.

## 7. Open questions

- Which model should be the default extractor (cheapest configured model)?
- Should expiry reminders stay CLI-only in v1, or also emit a cron ping?
- Do we want a `sync` command that re-checks offer URLs for changed terms?
