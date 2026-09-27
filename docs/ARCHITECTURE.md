# Architecture — litellm-ingestion-agent

## Pipeline

```
X/Threads post (pasted text)
        │
        ▼
┌──────────────┐   LLM via LiteLLM    ┌──────────────┐
│  extract.py  │ ───────────────────▶ │ TrialOffer   │
│  (prompt +   │   JSON-mode output   │ (pydantic)   │
│  JSON parse) │                      └──────┬───────┘
└──────────────┘                             │ user confirms
                                             ▼
                                      ┌──────────────┐
                                      │  store.py    │
                                      │  SQLite      │
                                      │  ~/.trial-   │
                                      │  agent/      │
                                      └──────┬───────┘
                                             │
                    ┌────────────────────────┼────────────────────────┐
                    ▼                        ▼                        ▼
            ┌──────────────┐          ┌──────────────┐         ┌──────────────┐
            │ litellm_     │          │  cli.py      │         │  limit       │
            │ config.py    │          │  list /      │         │  warnings    │
            │ config.yaml  │          │  set-status  │         │  (7-day      │
            │ for LiteLLM  │          │              │         │  expiry)     │
            └──────────────┘          └──────────────┘         └──────────────┘
```

## Modules (`src/litellm_ingestion_agent/`)

| Module            | Responsibility                                              |
|-------------------|-------------------------------------------------------------|
| `models.py`       | Pydantic schemas: `TrialOffer`, `TrialTerms`, `AuthInfo`, enums |
| `extract.py`      | Post text → `TrialOffer` via LiteLLM JSON-mode completion   |
| `store.py`        | SQLite persistence, status transitions                      |
| `litellm_config.py` | `TrialOffer[]` → LiteLLM `config.yaml` dict + YAML writer |
| `cli.py`          | Typer CLI: `add-post`, `list`, `set-status`, `export-config` |

## Key decisions

1. **Dogfood LiteLLM for extraction.** The extractor calls whatever model the
   user already configured — the tool manages LLM access using LLM access.
2. **Pydantic as the contract.** `docs/EXTRACTION_CONTRACT.md` is the human
   spec; `models.py` is the executable version. They must match.
3. **Secrets by reference.** The exported YAML contains
   `api_key: os.environ/<NAME>` — LiteLLM resolves these at load time. Raw
   keys never touch disk outside the user's env.
4. **SQLite, not a server.** Single-user CLI tool; zero-ops storage under
   `~/.litellm-ingestion-agent/`.
5. **Confirm before write.** Extraction is LLM-guessy; the user reviews every
   record before it is stored (FR-3).

## Data flow example

1. `litellm-ingestion-agent add-post "🚀 New: AcmeAI gives $25 credits..." --source-url <url>`
2. Extractor returns JSON → validated into `TrialOffer` → printed for review.
3. User confirms → stored with status `discovered`.
4. User signs up, runs `litellm-ingestion-agent set-status 1 active`.
5. `litellm-ingestion-agent export-config` writes `litellm.config.yaml`; user sets
   `ACMEAI_API_KEY` in env and points LiteLLM at the file.
