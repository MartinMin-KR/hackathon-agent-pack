# Hackathon Codex Agents Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a Codex-based GitHub-installable hackathon agent package with one leader workflow, seven generalist teammate agents, Ouroboros-style clarification, automatic validation, and GitHub sync guardrails.

**Architecture:** This is a self-contained repository scaffold. Codex behavior is carried by `AGENTS.md` plus local `.codex/skills`; operational safety is provided by a dependency-free Python harness that creates isolated teammate/role folders, runs verification, commits, and pushes safe changes.

**Tech Stack:** Codex instructions, Markdown skills, Python 3 standard library, shell install script, unittest.

## Global Constraints

- Runtime target is Codex.
- Teammates are first-year university students, so interaction must be natural language and beginner-friendly.
- Every teammate request must pass through Ouroboros-style clarification before execution.
- Code verification is harness-driven; teammates should not need to review code.
- Work types include idea, planning, UX, code, debugging, research, presentation, and QA.
- The collaboration model is shared branch plus teammate/role folder isolation.
- Harness manages folder creation, verification, commits, and pushes.
- Destructive Git operations are forbidden.
- Common/shared-file edits are restricted or escalated.

---

### Task 1: Repository Contract And Codex Skills

**Files:**
- Create: `AGENTS.md`
- Create: `.codex/skills/hackathon-leader/SKILL.md`
- Create: `.codex/skills/hackathon-teammate/SKILL.md`

**Interfaces:**
- Produces: Codex-readable operating rules and two named skills.
- Consumes: Interview spec at `.omx/specs/deep-interview-hackathon-codex-agents.md`.

- [ ] **Step 1: Add repository-level Codex instructions**
- [ ] **Step 2: Add leader skill**
- [ ] **Step 3: Add teammate execution skill**
- [ ] **Step 4: Verify the files exist**

Run: `test -f AGENTS.md && test -f .codex/skills/hackathon-leader/SKILL.md && test -f .codex/skills/hackathon-teammate/SKILL.md`
Expected: exit code 0.

### Task 2: Harness CLI

**Files:**
- Create: `bin/hackathon-harness`
- Create: `harness/hackathon_harness.py`
- Create: `harness/__init__.py`
- Create: `.hackathon/config.json`

**Interfaces:**
- Produces CLI commands: `init`, `task`, `verify`, `sync`, `status`.
- Produces Python functions: `load_config`, `ensure_member_workspace`, `verify_workspace`, `sync_changes`.

- [ ] **Step 1: Implement dependency-free Python harness**
- [ ] **Step 2: Add executable wrapper**
- [ ] **Step 3: Add default config**
- [ ] **Step 4: Run `python3 -m harness.hackathon_harness status`**
Expected: prints configured members and workspace root.

### Task 3: Tests

**Files:**
- Create: `tests/test_hackathon_harness.py`

**Interfaces:**
- Consumes harness functions from `harness.hackathon_harness`.
- Verifies workspace creation, path guardrails, and verification behavior.

- [ ] **Step 1: Add unittest tests**
- [ ] **Step 2: Run `python3 -m unittest discover -s tests`**
Expected: all tests pass.

### Task 4: Install And Usage Documentation

**Files:**
- Create: `README.md`
- Create: `scripts/install.sh`
- Create: `docs/task-type-skill-map.md`

**Interfaces:**
- Produces one-command local install path and human-readable operating guide.

- [ ] **Step 1: Add README**
- [ ] **Step 2: Add install script**
- [ ] **Step 3: Add task-type skill mapping doc**
- [ ] **Step 4: Run shell syntax check**

Run: `bash -n scripts/install.sh`
Expected: exit code 0.

### Task 5: Final Verification

**Files:**
- All created files.

**Interfaces:**
- Consumes all previous tasks.

- [ ] **Step 1: Run tests**
Run: `python3 -m unittest discover -s tests`
Expected: OK.

- [ ] **Step 2: Run harness status**
Run: `python3 -m harness.hackathon_harness status`
Expected: lists leader and seven teammates.

- [ ] **Step 3: Run install syntax check**
Run: `bash -n scripts/install.sh`
Expected: exit code 0.
