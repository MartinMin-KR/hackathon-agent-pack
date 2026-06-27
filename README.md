# Hackathon Codex Agent Pack

One leader agent and seven teammate agents for a first-year university hackathon team.

Teammates use natural language. The agent clarifies the request, researches automatically, simulates Korean persona customer interviews, creates a seed-like spec, executes, evaluates, asks for local approval, and then proposes product changes to the leader.

GitHub repo: https://github.com/MartinMin-KR/hackathon-agent-pack

Vercel dashboard: https://dashboard-xi-lime-40.vercel.app

## Quick Start

```bash
git clone <your-github-repo-url> hackathon-agent-pack
cd hackathon-agent-pack
bash scripts/install.sh
```

During install, choose your name. The selection is local to your laptop and is not pushed to GitHub.

## Team Members

- `member-1`: 고윤재
- `member-2`: 권이루
- `member-3`: 백지원
- `member-4`: 유준우
- `member-5`: 이동건
- `member-6`: 이승환
- `member-7`: 이윤재

## Workflow

```text
request
→ Ouroboros interview
→ automatic web research
→ Korean persona simulated interview
→ product psychology check
→ seed-like task spec
→ run
→ evaluate
→ local teammate review
→ feedback/evolve loop
→ teammate approval
→ leader proposal
→ leader integration
```

## Roles

Use one of four visible task roles:

- `planning`
- `building`
- `validation`
- `presentation`

## Leader Dashboard

Generate the dashboard:

```bash
python3 -m harness.hackathon_harness dashboard
```

Open:

```text
dashboard/index.html
```

The same folder is Vercel-ready. Vercel can deploy `dashboard/` as the public output.

Current production dashboard:

```text
https://dashboard-xi-lime-40.vercel.app
```

## Core Commands

```bash
python3 -m harness.hackathon_harness init
python3 -m harness.hackathon_harness status
python3 -m harness.hackathon_harness task --title "landing page draft" --type building
python3 -m harness.hackathon_harness verify
python3 -m harness.hackathon_harness review --title "landing page draft"
python3 -m harness.hackathon_harness approve --title "landing page draft"
python3 -m harness.hackathon_harness propose --title "landing page draft"
python3 -m harness.hackathon_harness sync --dry-run --title "landing page draft"
python3 -m harness.hackathon_harness sync --title "landing page draft"
```

## Safety Model

- Teammate work stays under `team-work/member-N/`.
- Product files live under `product/`.
- Teammates do not edit `product/` directly.
- Product changes go through `integration-proposals/`.
- Existing product files are not overwritten automatically.
- Destructive Git commands are not part of the harness.
- Simulated persona interviews are hypothesis support, not real market validation.

## Included Skills

- `.codex/skills/hackathon-teammate/SKILL.md`
- `.codex/skills/hackathon-leader/SKILL.md`
- `.codex/skills/ouroboros-interview/SKILL.md`
- `.codex/skills/ouroboros-all/`

## Docs

- `docs/final-design-spec.md`
- `docs/implementation-plan.md`
- `docs/team-onboarding.md`
- `docs/leader-operations.md`
- `docs/github-vercel-setup.md`
- `docs/task-type-skill-map.md`

## Verification

```bash
python3 -m unittest discover -s tests -v
python3 -m harness.hackathon_harness verify --all
bash -n scripts/install.sh
```
