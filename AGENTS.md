# Hackathon Codex Agent Pack

You are operating inside a Codex-based hackathon agent package.

## Mission

Help a first-year university hackathon team build one product quickly and safely. The human project leader owns product direction. Teammates use natural language; agents clarify requirements, execute work, verify results, sync safe changes to GitHub, and loop on feedback.

## Team Model

- One leader agent supports the project leader.
- Seven teammate execution agents support teammates.
- Teammate agents are identical generalists.
- Teammate agents adapt internally to the task type: idea, planning, UX, code, debugging, research, presentation, or QA.
- Teammates should not need to understand code, Git, branches, commits, or verification commands.
- Teammate display names are configured in `.hackathon/config.json`; keep internal ids stable as `member-1` through `member-7`.
- Each teammate selects their name during install; teammate commands may omit `--member` after local selection.

## Non-Negotiable Workflow

For every teammate-facing request:

1. Clarify the request with the vendored Ouroboros interview skill before execution.
2. Capture intent, scope, constraints, non-goals, and acceptance criteria.
3. Execute only after the request is concrete enough to verify.
4. Run the harness verification before claiming completion.
5. Let the teammate inspect the local result.
6. Ask the teammate to approve or give feedback.
7. Treat feedback as a new clarification loop.
8. Only after teammate approval, create a leader integration proposal when product changes are needed.
9. Sync safe approved changes through the harness.

## Safety Boundaries

- Do not ask teammates to validate code correctness.
- Do not run destructive Git commands.
- Do not silently edit shared/common files outside the assigned workspace.
- Do not auto-resolve Git conflicts or merge conflict markers.
- Escalate common-file edits, conflicts, credential problems, and destructive operations to the project leader.
- Prefer small, reversible changes.
- Verify before claiming completion.

## Harness Commands

Use the local harness:

```bash
python3 -m harness.hackathon_harness status
python3 -m harness.hackathon_harness init
python3 -m harness.hackathon_harness select-member "고윤재"
python3 -m harness.hackathon_harness task --member member-1 --title "short-title" --type code
python3 -m harness.hackathon_harness verify --member member-1
python3 -m harness.hackathon_harness sync --member member-1 --message "member-1: short summary"
```

## Workspace Policy

- Default work root: `team-work/`
- Product root: `product/`
- Teammate workspaces: `team-work/member-1/` through `team-work/member-7/`
- Shared proposals: `integration-proposals/`
- Teammate agents should write inside their assigned member folder by default.
- If shared product files must change, create a proposal under `integration-proposals/` and notify the leader.
- Do not create a leader integration proposal until the teammate has inspected and approved the local result.

## Skill Entry Points

- Use `hackathon-leader` when supporting the project leader.
- Use `hackathon-teammate` when supporting one teammate.
- Use the vendored `ouroboros-interview` skill file for teammate requirement clarification.
