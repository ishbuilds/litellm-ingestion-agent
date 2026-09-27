# GitHub setup — repo, Projects board, milestones

Run these once, on your local machine. Requires the GitHub CLI (`gh`):
`https://cli.github.com`.

## 1. Create the repo and push

```bash
cd litellm-ingestion-agent
git init -b main
git add .
git commit -m "M0: spec-driven scaffold"
gh repo create litellm-ingestion-agent --public --source=. --push --description "Manage LLM trial accounts from unstructured posts; export LiteLLM config."
```

## 2. Create the Project board

```bash
gh project create --owner="@me" --title="LiteLLM Ingestion Agent"
```

Then open the project in the browser and add the built-in **Status** field
columns (it ships with Todo / In Progress / Done — rename to
`Backlog → Ready → In progress → In review → Done`).

## 3. Create milestones (M1–M5)

```bash
REPO=$(gh repo view --json nameWithOwner -q .nameWithOwner)
for m in \
  "M1:Extraction pipeline" \
  "M2:LiteLLM config generation" \
  "M3:Tracking CLI" \
  "M4:OSS polish and v0.1.0" \
  "M5:Launch" ; do
  title="${m%%:*} — ${m#*:}"
  gh api "repos/$REPO/milestones" -f title="$title" >/dev/null
  echo "created: $title"
done

##powershell
$REPO = gh repo view --json nameWithOwner -q .nameWithOwner

$milestones = @(
    "M1:Extraction pipeline"
    "M2:LiteLLM config generation"
    "M3:Tracking CLI"
    "M4:OSS polish and v0.1.0"
    "M5:Launch"
)

foreach ($m in $milestones) {
    $parts = $m -split ":", 2
    $title = "$($parts[0]) — $($parts[1])"

    gh api "repos/$REPO/milestones" `
        -f "title=$title" | Out-Null

    Write-Host "created: $title"
}

```



## 4. Create the issues

Use the issue list in `docs/MILESTONES.md`. Quick way:

```bash
gh label create M1 --description "Milestone 1" --color 1D76DB


gh issue create --title "models.py: pydantic schemas" \
  --body "Implement schemas per docs/EXTRACTION_CONTRACT.md." \
  --milestone "M1 — Extraction pipeline" --label "M1"
# …repeat per issue, then drag them onto the project board

##powershell
gh issue create --title "models.py: pydantic schemas" --body "Implement schemas per docs/EXTRACTION_CONTRACT.md." --milestone "M1 — Extraction pipeline" --label "M1"


```

Tip: add issues to the project in bulk from the project page
(`... → Add items`), or set the repo's project as default and use
`gh issue create --project "LiteLLM Ingestion Agent"`.

## 5. Working agreement (Cursor)

- The spec is the source of truth: `docs/SPEC.md`.
- One issue = one branch = one PR. Reference the issue number.
- Every PR must keep `ruff` and `pytest` green.
- Update the spec first if behavior needs to change — never silently.

