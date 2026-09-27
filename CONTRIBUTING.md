# Contributing

## Spec-driven workflow

1. **Read `docs/SPEC.md` first.** It is the source of truth. If the behavior
   you want contradicts the spec, propose the spec change first.
2. **One issue = one branch = one PR.** Reference the issue number
   (`Closes #12`).
3. Keep PRs small and focused; describe the *why*, not just the *what*.

## Development setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest
ruff check .
```

## Standards

- `ruff` and `pytest` must be green (CI enforces this).
- New behavior needs tests. Bug fixes need a regression test.
- Never commit secrets, API keys, or `.env` files — see `SECURITY.md`.
- Follow the extraction contract in `docs/EXTRACTION_CONTRACT.md` when
  touching offer data shapes.

## Release process

Milestones in `docs/MILESTONES.md` define the release train. Tag releases as
`vX.Y.Z` with GitHub Release notes summarizing user-facing changes.
