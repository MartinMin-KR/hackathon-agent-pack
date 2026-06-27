# Leader Operations

## Daily Loop

1. Pull the latest GitHub changes.
2. Run `python3 -m harness.hackathon_harness dashboard`.
3. Open the Vercel dashboard: `https://dashboard-xi-lime-40.vercel.app`.
4. Check pending decisions, risks, and proposal queue.
5. Use Hermes Discord for urgent decisions.
6. Integrate only accepted proposals.

## Decision Commands

Create a pending leader decision:

```bash
python3 -m harness.hackathon_harness decision create --title "Approve onboarding change" --urgency urgent --reason "Existing product file would change" --recommendation "Approve after copy edit"
```

Resolve it after the leader decides:

```bash
python3 -m harness.hackathon_harness decision resolve <decision-id> --status approved --notes "Approved by leader"
```

Resolved items leave the pending dashboard list and stay in `leader-decisions/decision-log.jsonl`.

## Decision Items

A decision item leaves the dashboard pending list once the leader decides. The decision should be logged as approved, rejected, changes requested, deferred, or executed.

## Hermes Discord

Use Hermes for urgent or blocking items:

- Existing product file modification
- Team conflict
- Repeated evaluate failure
- Final submission blocker
- Deployment or external service issue

Configured target: `discord:#hackathon-leader`.

The harness writes pending decision payloads under `leader-notifications/`. The leader agent uses those payloads when sending Hermes Discord alerts.

## Vercel

Deploy the repo root as a static project. The dashboard lives in `dashboard/`.

The public dashboard must not include API keys, credentials, secrets, or private personal information.
