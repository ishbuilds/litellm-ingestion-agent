# Milestones → GitHub Projects

Each milestone below maps to **one GitHub Milestone** and a set of issues on
the **"LiteLLM Ingestion Agent" GitHub Project board**. Board columns:
`Backlog → Ready → In progress → In review → Done`.

Create them with the commands in `docs/GITHUB_SETUP.md`.

---

## M0 — Spec & repo bootstrap ✅ (done)

- [x] SPEC, architecture, extraction contract written
- [x] Repo scaffold with OSS standards (README, LICENSE, CONTRIBUTING,
      CODE_OF_CONDUCT, SECURITY, CI, issue/PR templates)
- [x] Cursor rules pointing at the spec as source of truth

## M1 — Extraction pipeline

**Goal:** pasted post text → validated `TrialOffer`, tested.

Issues:
- #1 `models.py`: pydantic schemas matching `EXTRACTION_CONTRACT.md`
- #2 `extract.py`: LiteLLM JSON-mode extractor + prompt
- #3 Unit tests for models + extractor (mocked LLM)
- #4 `store.py`: SQLite persistence + status transitions

Acceptance: `add-post` flow works end-to-end with `--yes` on a fixture post;
`pytest` green.

## M2 — LiteLLM config generation

**Goal:** one-command export to a loadable LiteLLM config.

Issues:
- #5 `litellm_config.py`: `TrialOffer[]` → `config.yaml` dict
- #6 Secrets-by-reference (`os.environ/<NAME>`), never raw keys
- #7 Test: exported YAML loads and contains only active offers

Acceptance: output file loads in LiteLLM with zero hand-edits.

## M3 — Tracking CLI

**Goal:** full lifecycle management from the terminal.

Issues:
- #8 `cli.py`: `add-post`, `list`, `set-status`, `export-config`, `--help` polish
- #9 7-day expiry warnings in `list`
- #10 README quickstart verified on a fresh machine

Acceptance: SPEC §6 acceptance criteria all checked.

## M4 — OSS polish & v0.1.0 release

**Goal:** repo meets the "proper OSS standards" bar.

Issues:
- #11 CI: ruff + pytest on 3.11/3.12, secret-scan check
- #12 Issue/PR templates, changelog, release notes
- #13 Tag `v0.1.0`, GitHub Release with install instructions

Acceptance: a stranger can install, run, and contribute in <15 minutes.

## M5 — Launch

**Goal:** portfolio artifact is public and explained.

Issues:
- #14 Medium article: problem → spec → build → lessons
- #15 Demo: 2-minute terminal recording (asciinema) in README
- #16 Post to X/Threads; link from portfolio

Acceptance: article published, repo public, demo embedded.
