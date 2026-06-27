# Task Role Skill Map

This policy tells teammate agents how to route natural-language requests after the Ouroboros interview loop. Visible task roles are intentionally simple: planning, building, validation, and presentation.

## Universal Intake

Every request follows the same base loop:

1. Use the vendored Ouroboros interview skill.
2. Search the web automatically when current or external facts can help.
3. Run a Korean persona simulated customer interview.
4. Apply product psychology checks.
5. Create a seed-like task spec.
6. Execute inside the member workspace.
7. Evaluate mechanically and semantically.
8. Ask the teammate to inspect the local result.
9. Evolve on feedback.
10. Create a leader proposal only after teammate approval.

The checklist is a hard gate. If it is incomplete, the harness blocks local review and leader proposal creation.

## Routing Table

| Role | Use When | Helpful Skills | Verification |
| --- | --- | --- | --- |
| planning | Problem framing, feature selection, scope, research direction, product decisions | Ouroboros interview, seed, pm, best-practice-research, product psychology | Clear target user, problem, non-goals, acceptance criteria |
| building | Screens, copy, code, assets, prototype pieces, product files | Ouroboros run, implement, imagegen, chromux, product psychology | Local checks pass, output matches seed, product path goes through proposal |
| validation | QA, debugging, review, risk checks, usability checks | Ouroboros evaluate, qa, code-review, ultraqa, check-harness | Mechanical checks, semantic requirement match, persona/product psychology risks |
| presentation | Pitch, slides, demo script, final submission narrative | tightened-slide, pdf-to-ppt, content-digest, product psychology | Story matches product, claims are grounded, peak/end moments are clear |

## Shared File Rule

If the task needs files outside `team-work/member-N/`, do not edit them directly by default. Create a proposal under `integration-proposals/` after teammate approval.

## Product Psychology

Use `CuriousPaul/product-psychology-for-vibe-coding` ideas as a quality check:

- 6P storyboard
- BMAP
- BIAS
- Peak-End
- Ethics checks

## Simulated Customer Interview

Use Korean persona data as hypothesis support, not proof of real market validation. Default dataset:

- `nvidia/Nemotron-Personas-Korea`
- fallback: `NLPBada/korean-persona-chat-dataset`

