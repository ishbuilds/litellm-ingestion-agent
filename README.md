# litellm-ingestion-agent

One place to manage your LLM trial accounts. Paste unstructured trial posts
from X/Threads, extract structured offer details with an LLM, and export a
ready-to-use [LiteLLM](https://github.com/BerriAI/litellm) config — with limit
tracking so trials never silently die.

## Quickstart

```bash
pip install -e ".[dev]"

# Capture a trial from a post (paste text or pipe it in)
litellm-ingestion-agent add-post "🚀 AcmeAI: $25 free credits for 30 days! Sign up: https://acme.ai/trial" \
  --source-url https://x.com/somepost

# Review, confirm, then manage lifecycle
litellm-ingestion-agent list
litellm-ingestion-agent set-status 1 active

# Export to LiteLLM (keys referenced via env vars — never written to disk)
export ACMEAI_API_KEY=sk-...
litellm-ingestion-agent export-config
```

Point LiteLLM at the generated `litellm.config.yaml` and you're routed.

## How it works

```
post text → LLM extraction (via LiteLLM) → human review → SQLite store → config.yaml
```

See [`docs/SPEC.md`](docs/SPEC.md) (source of truth),
[`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md), and
[`docs/EXTRACTION_CONTRACT.md`](docs/EXTRACTION_CONTRACT.md).

## Project tracking

Milestones and the build order live in [`docs/MILESTONES.md`](docs/MILESTONES.md),
tracked on the GitHub Project board. Setup: [`docs/GITHUB_SETUP.md`](docs/GITHUB_SETUP.md).

## Contributing

PRs welcome — start with [`CONTRIBUTING.md`](CONTRIBUTING.md).

## License

MIT — see [`LICENSE`](LICENSE).
