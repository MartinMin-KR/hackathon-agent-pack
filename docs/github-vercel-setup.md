# GitHub and Vercel Setup

## GitHub

1. Create or use the public repo.
2. Invite teammates if they need direct push access.
3. Make sure everyone can clone the repo.
4. Avoid force pushes during the hackathon.

Recommended repo name: `hackathon-agent-pack`.

Current public repo:

```text
https://github.com/MartinMin-KR/hackathon-agent-pack
```

## Vercel

1. Import the GitHub repo into Vercel.
2. Use the repo root as the project root.
3. Set the output directory to `dashboard` if Vercel asks.
4. The dashboard entry file is `dashboard/index.html`.
5. Every GitHub push can redeploy the dashboard.

Current production dashboard:

```text
https://dashboard-xi-lime-40.vercel.app
```

## Local Check

Run:

```bash
python3 -m harness.hackathon_harness dashboard
```

Then open `dashboard/index.html`.
