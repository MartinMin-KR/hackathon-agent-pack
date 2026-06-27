# Final Design Spec

## Goal

Build one hackathon agent package for a first-year university team: one leader agent and seven identical teammate agents. Teammates speak naturally; agents clarify, execute, verify, and propose changes without requiring teammates to understand code or Git.

## Core Workflow

Every teammate task follows this loop:

1. Ouroboros interview
2. Automatic web research
3. Korean persona simulated customer interview
4. Product psychology check
5. Seed-like task spec
6. Run/execute
7. Evaluate
8. Local teammate review
9. Evolve loop on feedback
10. Teammate approval
11. Leader proposal

## Teammate Agent

The teammate agent is a generalist. It can handle planning, building, validation, and presentation tasks. It works only inside the selected teammate workspace unless creating a leader proposal.

The teammate never asks the student to judge code correctness. The teammate only asks whether the result matches the student's intended outcome.

## Leader Agent

The leader agent manages product direction, team state, proposal review, integration safety, final submission readiness, Hermes Discord alerts, and the Vercel dashboard.

The leader agent teaches onboarding to teammates in plain language:

1. Sign in to GitHub.
2. Install Git if needed.
3. Install or open Codex.
4. Clone or download the repo.
5. Run `bash scripts/install.sh`.
6. Select your name.
7. Tell the agent what you want to make.

## Dashboard

The dashboard is a static web dashboard under `dashboard/` and is Vercel-ready. The harness writes:

- `dashboard/index.html`
- `dashboard/dashboard-data.json`

The dashboard shows team status, pending leader decisions, proposal queue, risks, and final submission checks.

## Notifications

Leader notifications use Hermes Discord. Dashboard shows all decision items. Discord is used for urgent or blocking decisions only.

The configured target is `discord:#hackathon-leader`; the leader can change it in `.hackathon/config.json`.

## GitHub

The repo is public and meant to be cloned by teammates. Teammates push their work; product integration is leader-controlled.

Recommended branches:

- `main`: stable product and package
- `team/member-1` through `team/member-7`: optional teammate branches
- `leader/integration`: optional integration branch

## Safety Rules

- Team work stays under `team-work/member-N/`.
- Direct product sync by teammate agents is blocked.
- Product changes move through `integration-proposals/`.
- Existing product files are not overwritten automatically.
- Destructive Git commands are outside the harness.
- Deletions should move files to `archive/` instead of removing them.

