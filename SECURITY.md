# Security policy

## Supported versions

Only the latest `v0.x` release receives security fixes during the
pre-1.0 period.

## Reporting a vulnerability

Open a **private** vulnerability report via GitHub
(Security → Report a vulnerability) or contact the maintainer directly.
Please do not open public issues for security problems.

We aim to acknowledge reports within 72 hours.

## Secrets handling

This tool manages API keys by design. Rules:

- Keys live in environment variables or a local `.env` — never in code,
  config files, issues, or PRs.
- Exported LiteLLM configs reference keys as `os.environ/<NAME>`.
- `.env` is git-ignored; CI includes a secret-scan step.
- If you accidentally commit a key: revoke it at the provider immediately,
  then purge it from history.
