"""Safety harness for Codex hackathon teammate agents.

The harness keeps teammate work isolated, runs local verification, and performs
non-destructive Git sync for safe changes.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import pathlib
import shutil
import subprocess
import sys
import uuid
from dataclasses import dataclass
from typing import Iterable


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
CONFIG_PATH = REPO_ROOT / ".hackathon" / "config.json"
LOCAL_MEMBER_PATH = REPO_ROOT / ".hackathon" / "local-member.json"


class HarnessError(RuntimeError):
    """Raised when the harness refuses an unsafe or invalid operation."""


@dataclass(frozen=True)
class HarnessConfig:
    workspace_root: pathlib.Path
    product_root: pathlib.Path
    integration_proposals: pathlib.Path
    local_member_path: pathlib.Path
    members: tuple[str, ...]
    member_names: dict[str, str]
    roles: tuple[str, ...]
    checklist_templates: pathlib.Path
    verification_commands: tuple[str, ...]
    push_remote: str
    push_branch: str
    allow_common_file_edits: bool
    dashboard_root: pathlib.Path
    dashboard_data_file: str
    dashboard_html_file: str
    hermes_target: str
    decision_log: pathlib.Path
    notifications_root: pathlib.Path
    persona_dataset: str
    fallback_persona_dataset: str


def _repo_path(value: str) -> pathlib.Path:
    return (REPO_ROOT / value).resolve()


def load_config(path: pathlib.Path = CONFIG_PATH) -> HarnessConfig:
    data = json.loads(path.read_text(encoding="utf-8"))
    git = data.get("git", {})
    verification = data.get("verification", {})
    dashboard = data.get("dashboard", {})
    leader = data.get("leader", {})
    research = data.get("research", {})
    member_ids: list[str] = []
    member_names: dict[str, str] = {}
    for member in data["members"]:
        if isinstance(member, str):
            member_ids.append(member)
            member_names[member] = member
        else:
            member_id = str(member["id"])
            member_ids.append(member_id)
            member_names[member_id] = str(member.get("name", member_id))
    return HarnessConfig(
        workspace_root=_repo_path(data["workspace_root"]),
        product_root=_repo_path(data["product_root"]),
        integration_proposals=_repo_path(data["integration_proposals"]),
        local_member_path=LOCAL_MEMBER_PATH,
        members=tuple(member_ids),
        member_names=member_names,
        roles=tuple(data["roles"]),
        checklist_templates=_repo_path(data["checklist_templates"]),
        verification_commands=tuple(verification.get("commands", ())),
        push_remote=str(git.get("push_remote", "origin")),
        push_branch=str(git.get("push_branch", "HEAD")),
        allow_common_file_edits=bool(git.get("allow_common_file_edits", False)),
        dashboard_root=_repo_path(str(dashboard.get("root", "dashboard"))),
        dashboard_data_file=str(dashboard.get("data_file", "dashboard-data.json")),
        dashboard_html_file=str(dashboard.get("html_file", "index.html")),
        hermes_target=str(leader.get("hermes_target", "discord:#hackathon-leader")),
        decision_log=_repo_path(str(leader.get("decision_log", "leader-decisions/decision-log.jsonl"))),
        notifications_root=_repo_path(str(leader.get("notifications", "leader-notifications"))),
        persona_dataset=str(research.get("persona_dataset", "nvidia/Nemotron-Personas-Korea")),
        fallback_persona_dataset=str(research.get("fallback_persona_dataset", "NLPBada/korean-persona-chat-dataset")),
    )


def run(command: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=REPO_ROOT,
        check=check,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def require_member(config: HarnessConfig, member: str) -> None:
    if member not in config.members:
        allowed = ", ".join(config.members)
        raise HarnessError(f"Unknown member '{member}'. Allowed: {allowed}")


def member_display_name(config: HarnessConfig, member: str) -> str:
    require_member(config, member)
    return config.member_names.get(member, member)


def resolve_member(config: HarnessConfig, member: str | None) -> str:
    if member:
        require_member(config, member)
        return member
    if not config.local_member_path.exists():
        raise HarnessError(
            "No member selected. Run `python3 -m harness.hackathon_harness select-member` "
            "or pass `--member member-N`."
        )
    data = json.loads(config.local_member_path.read_text(encoding="utf-8"))
    selected = str(data.get("id", ""))
    require_member(config, selected)
    return selected


def select_member(config: HarnessConfig, member_or_name: str) -> pathlib.Path:
    selected = None
    for member in config.members:
        if member_or_name == member or member_or_name == member_display_name(config, member):
            selected = member
            break
    if selected is None:
        allowed = ", ".join(f"{member} ({member_display_name(config, member)})" for member in config.members)
        raise HarnessError(f"Unknown teammate '{member_or_name}'. Allowed: {allowed}")
    config.local_member_path.parent.mkdir(parents=True, exist_ok=True)
    config.local_member_path.write_text(
        json.dumps(
            {"id": selected, "name": member_display_name(config, selected)},
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return config.local_member_path


def selected_member_label(config: HarnessConfig) -> str:
    if not config.local_member_path.exists():
        return "not selected"
    member = resolve_member(config, None)
    return f"{member} ({member_display_name(config, member)})"


def ensure_inside(path: pathlib.Path, parent: pathlib.Path) -> None:
    path = path.resolve()
    parent = parent.resolve()
    if path != parent and parent not in path.parents:
        raise HarnessError(f"Unsafe path outside allowed workspace: {path}")


def display_path(path: pathlib.Path, base: pathlib.Path = REPO_ROOT) -> str:
    try:
        return str(path.resolve().relative_to(base.resolve()))
    except ValueError:
        return str(path)


def member_workspace(config: HarnessConfig, member: str) -> pathlib.Path:
    require_member(config, member)
    return config.workspace_root / member


def safe_slug(value: str, fallback: str) -> str:
    slug = "".join(ch if ch.isalnum() or ch in ("-", "_") else "-" for ch in value.strip().lower())
    return "-".join(part for part in slug.split("-") if part)[:60] or fallback


def require_task_type(config: HarnessConfig, task_type: str) -> None:
    if task_type not in config.roles:
        allowed = ", ".join(config.roles)
        raise HarnessError(f"Unknown task type '{task_type}'. Allowed: {allowed}")


def checklist_path(config: HarnessConfig, member: str, title: str) -> pathlib.Path:
    workspace = ensure_member_workspace(config, member)
    return workspace / "tests" / f"{safe_slug(title, 'task')}-checklist.md"


def task_artifact_paths(config: HarnessConfig, member: str, title: str) -> dict[str, pathlib.Path]:
    workspace = ensure_member_workspace(config, member)
    safe_title = safe_slug(title, "task")
    return {
        "brief": workspace / "requests" / f"{safe_title}.md",
        "seed": workspace / "specs" / f"{safe_title}-seed.md",
        "interview": workspace / "interviews" / f"{safe_title}-ouroboros.md",
        "research": workspace / "research" / f"{safe_title}-research.md",
        "persona": workspace / "customer-interviews" / f"{safe_title}-personas.md",
    }


def checklist_template_path(config: HarnessConfig, task_type: str) -> pathlib.Path:
    require_task_type(config, task_type)
    path = config.checklist_templates / f"{task_type}.md"
    if not path.exists():
        raise HarnessError(f"Missing checklist template: {path.relative_to(REPO_ROOT)}")
    return path


def create_checklist(config: HarnessConfig, member: str, title: str, task_type: str) -> pathlib.Path:
    path = checklist_path(config, member, title)
    ensure_inside(path, member_workspace(config, member))
    if not path.exists():
        template = checklist_template_path(config, task_type).read_text(encoding="utf-8")
        path.write_text(
            "# Task Verification Checklist\n\n"
            f"- Member: {member}\n"
            f"- Name: {member_display_name(config, member)}\n"
            f"- Title: {title}\n"
            f"- Task type: {task_type}\n"
            "- Status: incomplete\n\n"
            f"{template}\n",
            encoding="utf-8",
        )
    return path


def assert_checklist_complete(config: HarnessConfig, member: str, title: str) -> None:
    path = checklist_path(config, member, title)
    if not path.exists():
        raise HarnessError("Missing task verification checklist.")
    text = path.read_text(encoding="utf-8")
    if "- Status: complete" not in text:
        raise HarnessError("Task verification checklist must be marked `- Status: complete` before review or proposal.")
    incomplete = [line for line in text.splitlines() if line.startswith("- [ ]")]
    if incomplete:
        joined = "\n".join(incomplete)
        raise HarnessError(f"Checklist still has incomplete items:\n{joined}")


def assert_required_artifacts_complete(config: HarnessConfig, member: str, title: str) -> None:
    paths = task_artifact_paths(config, member, title)
    missing: list[str] = []
    for key in ("brief", "seed", "interview", "research", "persona"):
        path = paths[key]
        if not path.exists():
            missing.append(f"{key}: missing {display_path(path)}")
            continue
        text = path.read_text(encoding="utf-8")
        if key == "brief":
            if "- Status: ready-for-review" not in text:
                missing.append(f"{key}: status is not ready-for-review in {display_path(path)}")
            bullet_requirements = {
                "- Intent:": (4, 24),
                "- Outcome:": (4, 24),
                "- Scope:": (3, 12),
                "- Acceptance criteria:": (4, 24),
            }
            for label, (min_words, min_chars) in bullet_requirements.items():
                if not bullet_has_value(text, label, min_words=min_words, min_chars=min_chars):
                    missing.append(f"{key}: {label} needs a concrete value in {display_path(path)}")
        elif key == "seed":
            if "- Status: complete" not in text:
                missing.append(f"{key}: status is not complete in {display_path(path)}")
            for heading in ("## Goal", "## Acceptance Criteria", "## Non-goals", "## Output Contract"):
                if not section_has_content(text, heading):
                    missing.append(f"{key}: {heading} needs concrete content in {display_path(path)}")
        elif key == "interview":
            if "- Status: complete" not in text:
                missing.append(f"{key}: status is not complete in {display_path(path)}")
            if not section_has_content(text, "## Result"):
                missing.append(f"{key}: ## Result needs concrete content in {display_path(path)}")
        elif key == "research":
            if "- Status: complete" not in text:
                missing.append(f"{key}: status is not complete in {display_path(path)}")
            if not bullet_has_value(text, "- Source:", min_words=4, min_chars=24):
                missing.append(f"{key}: - Source: needs a concrete source in {display_path(path)}")
        elif key == "persona":
            if "- Status: complete" not in text:
                missing.append(f"{key}: status is not complete in {display_path(path)}")
            if not bullet_has_value(text, "- Insight:", min_words=5, min_chars=32):
                missing.append(f"{key}: - Insight: needs a concrete insight in {display_path(path)}")
    if missing:
        raise HarnessError(
            "Task workflow artifacts are incomplete. Complete the Ouroboros/research/persona/seed loop before review:\n"
            + "\n".join(f"- {item}" for item in missing)
        )


def bullet_has_value(text: str, label: str, *, min_words: int, min_chars: int) -> bool:
    for line in text.splitlines():
        if line.startswith(label):
            value = line[len(label) :].strip()
            return is_substantive_text(value, min_words=min_words, min_chars=min_chars)
    return False


def section_has_content(text: str, heading: str) -> bool:
    lines = text.splitlines()
    capture = False
    content: list[str] = []
    for line in lines:
        if line.strip() == heading:
            capture = True
            continue
        if capture and line.startswith("## "):
            break
        if capture and line.strip():
            content.append(line.strip())
    joined = " ".join(content).strip()
    return is_substantive_text(joined, min_words=5, min_chars=32)


def is_substantive_text(value: str, *, min_words: int, min_chars: int) -> bool:
    stripped = value.strip()
    if len(stripped) < min_chars:
        return False
    lowered = stripped.lower().strip(" .?!:;,-_")
    filler_values = {
        "todo",
        "tbd",
        "none",
        "n/a",
        "placeholder",
        "ok",
        "done",
        "fine",
        "yes",
        "meaningful",
        "meaningful??",
        "complete",
        "completed",
    }
    if lowered in filler_values:
        return False
    words = [word for word in stripped.replace("/", " ").split() if any(ch.isalnum() for ch in word)]
    return len(words) >= min_words


def ensure_member_workspace(config: HarnessConfig, member: str) -> pathlib.Path:
    workspace = member_workspace(config, member)
    name = member_display_name(config, member)
    ensure_inside(workspace, config.workspace_root)
    for child in (
        "requests",
        "outputs",
        "notes",
        "patches",
        "src",
        "tests",
        "interviews",
        "specs",
        "research",
        "customer-interviews",
        "archive",
    ):
        (workspace / child).mkdir(parents=True, exist_ok=True)
    readme = workspace / "README.md"
    if not readme.exists():
        readme.write_text(
            f"# {name} Workspace\n\n"
            f"- Internal member id: `{member}`\n"
            f"- Display name: {name}\n\n"
            "Use this folder for isolated teammate work. Final product changes "
            "should be proposed under `integration-proposals/` for leader review.\n",
            encoding="utf-8",
        )
    return workspace


def init_workspaces(config: HarnessConfig) -> None:
    config.workspace_root.mkdir(parents=True, exist_ok=True)
    config.product_root.mkdir(parents=True, exist_ok=True)
    config.integration_proposals.mkdir(parents=True, exist_ok=True)
    config.dashboard_root.mkdir(parents=True, exist_ok=True)
    config.notifications_root.mkdir(parents=True, exist_ok=True)
    config.decision_log.parent.mkdir(parents=True, exist_ok=True)
    if not config.decision_log.exists():
        config.decision_log.write_text("", encoding="utf-8")
    product_readme = config.product_root / "README.md"
    if not product_readme.exists():
        product_readme.write_text(
            "# Product\n\n"
            "This folder contains the hackathon product that will be demoed or submitted. "
            "Teammate agents should not edit it directly unless the leader approves.\n",
            encoding="utf-8",
        )
    proposals_readme = config.integration_proposals / "README.md"
    if not proposals_readme.exists():
        proposals_readme.write_text(
            "# Integration Proposals\n\n"
            "Teammate agents place proposed product changes here. The leader agent reviews "
            "and integrates accepted proposals into `product/`.\n",
            encoding="utf-8",
        )
    for member in config.members:
        ensure_member_workspace(config, member)


def create_task(config: HarnessConfig, member: str, title: str, task_type: str) -> pathlib.Path:
    workspace = ensure_member_workspace(config, member)
    require_task_type(config, task_type)
    safe_title = safe_slug(title, "task")
    task_path = workspace / "requests" / f"{safe_title}.md"
    artifact_paths = task_artifact_paths(config, member, title)
    seed_path = artifact_paths["seed"]
    interview_path = artifact_paths["interview"]
    persona_path = artifact_paths["persona"]
    research_path = artifact_paths["research"]
    ensure_inside(task_path, workspace)
    if not task_path.exists():
        task_path.write_text(
            "# Task Brief\n\n"
            f"- Member: {member}\n"
            f"- Name: {member_display_name(config, member)}\n"
            f"- Title: {title}\n"
            f"- Task type: {task_type}\n"
            "- Status: clarifying\n\n"
            "## Workflow\n\n"
            "Ouroboros loop: interview -> automatic web research -> Korean persona simulated interview -> product psychology check -> seed -> run -> evaluate -> local review -> evolve on feedback -> leader proposal.\n\n"
            "## Ouroboros Clarification\n\n"
            "- Intent:\n"
            "- Outcome:\n"
            "- Scope:\n"
            "- Constraints:\n"
            "- Non-goals:\n"
            "- Acceptance criteria:\n"
            "\n## Automatic Web Research\n\n"
            "- Policy: always search for current external context when useful.\n"
            "- Sources:\n"
            "- Dates checked:\n"
            "- Applied findings:\n"
            "\n## Korean Persona Simulated Interview\n\n"
            f"- Primary dataset: {config.persona_dataset}\n"
            f"- Fallback dataset: {config.fallback_persona_dataset}\n"
            "- Persona sample:\n"
            "- Simulated customer objections:\n"
            "- Insights to reflect:\n"
            "\n## Product Psychology Check\n\n"
            "- 6P storyboard:\n"
            "- BMAP:\n"
            "- BIAS:\n"
            "- Peak-End:\n"
            "- Ethics:\n"
            "\n## Seed-like Task Spec\n\n"
            f"- Seed file: `{seed_path.relative_to(workspace.parent.parent)}`\n"
            "\n## Execution Plan\n\n"
            "- Step 1:\n"
            "- Step 2:\n"
            "- Step 3:\n"
            "\n## Stop Gates\n\n"
            "- [ ] Requirement interview is complete.\n"
            "- [ ] Automatic web research is recorded.\n"
            "- [ ] Korean persona simulated interview is recorded.\n"
            "- [ ] Product psychology check is recorded.\n"
            "- [ ] Seed-like spec is complete.\n"
            "- [ ] Ouroboros evaluate passed.\n"
            "- [ ] Teammate local review is complete.\n"
            "- [ ] Leader proposal is needed only after teammate approval.\n",
            encoding="utf-8",
        )
    if not seed_path.exists():
        seed_path.write_text(
            "# Seed-like Task Spec\n\n"
            f"- Member: {member}\n"
            f"- Name: {member_display_name(config, member)}\n"
            f"- Title: {title}\n"
            f"- Role tag: {task_type}\n"
            "- Status: draft\n\n"
            "## Goal\n\n"
            "## Acceptance Criteria\n\n"
            "## Non-goals\n\n"
            "## Inputs\n\n"
            "## Output Contract\n\n"
            "## Evaluate Plan\n\n"
            "1. Mechanical verification\n"
            "2. Semantic requirement check\n"
            "3. Leader escalation if uncertainty remains\n",
            encoding="utf-8",
        )
    if not interview_path.exists():
        interview_path.write_text("# Ouroboros Interview Transcript\n\n- Status: draft\n\n## Result\n\n", encoding="utf-8")
    if not persona_path.exists():
        persona_path.write_text(
            "# Korean Persona Simulated Interview\n\n"
            "- Status: draft\n"
            f"- Dataset: {config.persona_dataset}\n"
            "- This is simulated customer hypothesis work, not real market validation.\n\n"
            "## Insights\n\n"
            "- Insight:\n",
            encoding="utf-8",
        )
    if not research_path.exists():
        research_path.write_text(
            "# Automatic Web Research Log\n\n"
            "- Status: draft\n"
            "- Policy: always automatic\n"
            "- Source:\n",
            encoding="utf-8",
        )
    create_checklist(config, member, title, task_type)
    return task_path


def create_verification_summary(config: HarnessConfig, member: str, title: str) -> pathlib.Path:
    workspace = ensure_member_workspace(config, member)
    safe_title = safe_slug(title, "verify")
    summary_path = workspace / "notes" / f"{safe_title}-verify.md"
    checklist = checklist_path(config, member, title)
    if not summary_path.exists():
        summary_path.write_text(
            "# Verification Summary\n\n"
            f"- Member: {member}\n"
            f"- Name: {member_display_name(config, member)}\n"
            f"- Title: {title}\n"
            f"- Checklist: `{checklist.relative_to(config.workspace_root.parent)}`\n"
            "- Result: passed local checklist gate\n\n"
            "## Evidence\n\n"
            "- Checklist marked complete.\n"
            "- Harness verification required before sync.\n"
            "- Ouroboros evaluate should cover mechanical checks, semantic requirement match, and leader escalation risk.\n",
            encoding="utf-8",
        )
    return summary_path


def ensure_learning_log(config: HarnessConfig, member: str) -> pathlib.Path:
    workspace = ensure_member_workspace(config, member)
    path = workspace / "notes" / "learnings.md"
    if not path.exists():
        path.write_text(
            "# Reusable Learnings\n\n"
            "Record decisions, pitfalls, and reusable context that future teammate tasks should know.\n",
            encoding="utf-8",
        )
    return path


def create_review_request(config: HarnessConfig, member: str, title: str) -> pathlib.Path:
    assert_checklist_complete(config, member, title)
    assert_required_artifacts_complete(config, member, title)
    create_verification_summary(config, member, title)
    ensure_learning_log(config, member)
    workspace = ensure_member_workspace(config, member)
    safe_title = safe_slug(title, "review")
    review_path = workspace / "outputs" / f"{safe_title}-review.md"
    ensure_inside(review_path, workspace)
    if not review_path.exists():
        review_path.write_text(
            "# Local Teammate Review\n\n"
            f"- Member: {member}\n"
            f"- Name: {member_display_name(config, member)}\n"
            f"- Title: {title}\n"
            "- Status: waiting-for-teammate-approval\n\n"
            "## What changed\n\n"
            "Summarize the local result in beginner-friendly language.\n\n"
            "## How to check locally\n\n"
            "Explain the simplest way for the teammate to inspect the result.\n\n"
            "## Approval\n\n"
            "- Teammate approved: no\n"
            "- Feedback to address before proposing:\n",
            encoding="utf-8",
        )
    return review_path


def approve_review(config: HarnessConfig, member: str, title: str) -> pathlib.Path:
    review_path = create_review_request(config, member, title)
    text = review_path.read_text(encoding="utf-8")
    text = text.replace("- Teammate approved: no", "- Teammate approved: yes")
    text = text.replace(
        "- Status: waiting-for-teammate-approval",
        "- Status: teammate-approved",
    )
    review_path.write_text(text, encoding="utf-8")
    return review_path


def create_integration_proposal(config: HarnessConfig, member: str, title: str) -> pathlib.Path:
    assert_checklist_complete(config, member, title)
    assert_required_artifacts_complete(config, member, title)
    workspace = ensure_member_workspace(config, member)
    safe_title = safe_slug(title, "proposal")
    review_path = workspace / "outputs" / f"{safe_title}-review.md"
    if not review_path.exists():
        raise HarnessError("Create a local review request before proposing to the leader.")
    review_text = review_path.read_text(encoding="utf-8")
    if "- Teammate approved: yes" not in review_text:
        raise HarnessError("The teammate must approve the local result before leader proposal.")
    proposal_dir = config.integration_proposals / f"{member}-{safe_title}"
    ensure_inside(proposal_dir, config.integration_proposals)
    proposal_dir.mkdir(parents=True, exist_ok=True)
    proposal_path = proposal_dir / "proposal.md"
    display_base = config.workspace_root.parent.resolve()
    review_display_path = review_path.resolve().relative_to(display_base)
    if not proposal_path.exists():
        proposal_path.write_text(
            "# Leader Integration Proposal\n\n"
            f"- Member: {member}\n"
            f"- Name: {member_display_name(config, member)}\n"
            f"- Title: {title}\n"
            "- Status: waiting-for-leader-review\n"
            "- Teammate local approval: yes\n\n"
            "## Local review source\n\n"
            f"`{review_display_path}`\n\n"
            "## Proposed product change\n\n"
            "Explain what should move into `product/` and why.\n\n"
            "## Verification evidence\n\n"
            "Summarize harness checks and any local inspection performed.\n\n"
            "## Required leader review fields\n\n"
            "- Automatic web research recorded: yes/no\n"
            "- Korean persona simulated interview recorded: yes/no\n"
            "- Product psychology check recorded: yes/no\n"
            "- Ouroboros evaluate passed: yes/no\n"
            "- Product target path:\n"
            "- Risk level: info/warning/urgent\n"
            "- Leader recommendation:\n\n"
            "## Leader decision\n\n"
            "- Accepted: no\n"
            "- Decision status: pending_decision\n"
            "- Notes:\n",
            encoding="utf-8",
        )
    return proposal_path


def proposal_dir(config: HarnessConfig, proposal_name: str) -> pathlib.Path:
    path = config.integration_proposals / proposal_name
    ensure_inside(path, config.integration_proposals)
    if not path.is_dir():
        raise HarnessError(f"Unknown integration proposal: {proposal_name}")
    return path


def require_leader_acceptance(path: pathlib.Path) -> None:
    proposal = path / "proposal.md"
    if not proposal.exists():
        raise HarnessError("Integration proposal is missing proposal.md.")
    text = proposal.read_text(encoding="utf-8")
    if "- Accepted: yes" not in text:
        raise HarnessError("Leader must accept the proposal before product integration.")
    if "- Decision status: pending_decision" in text:
        raise HarnessError("Leader decision is still pending. Move it to approved before integration.")


def proposed_product_files(config: HarnessConfig, proposal_name: str) -> list[tuple[pathlib.Path, pathlib.Path]]:
    root = proposal_dir(config, proposal_name)
    source_root = root / "files" / "product"
    if not source_root.exists():
        raise HarnessError("Proposal has no `files/product/` directory to integrate.")
    pairs: list[tuple[pathlib.Path, pathlib.Path]] = []
    for source in sorted(path for path in source_root.rglob("*") if path.is_file()):
        relative = source.relative_to(source_root)
        target = config.product_root / relative
        ensure_inside(target, config.product_root)
        pairs.append((source, target))
    if not pairs:
        raise HarnessError("Proposal has no product files to integrate.")
    return pairs


def assert_no_product_overwrite(pairs: Iterable[tuple[pathlib.Path, pathlib.Path]]) -> None:
    existing = [target for _source, target in pairs if target.exists()]
    if existing:
        joined = "\n".join(f"- {display_path(target)}" for target in existing)
        raise HarnessError(
            "Refusing to overwrite existing product files automatically:\n"
            f"{joined}\n"
            "Create a leader decision item and integrate the change manually after review."
        )


def dry_run_integrate(config: HarnessConfig, proposal_name: str) -> str:
    path = proposal_dir(config, proposal_name)
    require_leader_acceptance(path)
    pairs = proposed_product_files(config, proposal_name)
    assert_no_product_overwrite(pairs)
    base = config.workspace_root.parent.resolve()
    lines = [f"Dry run integrate: {proposal_name}", "", "Would integrate:"]
    for _source, target in pairs:
        lines.append(f"- {target.resolve().relative_to(base)}")
    return "\n".join(lines)


def integrate_proposal(config: HarnessConfig, proposal_name: str) -> str:
    path = proposal_dir(config, proposal_name)
    require_leader_acceptance(path)
    pairs = proposed_product_files(config, proposal_name)
    assert_no_product_overwrite(pairs)
    report = dry_run_integrate(config, proposal_name)
    verify_workspace(config, None)
    for source, target in pairs:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    create_dashboard(config)
    create_session_wrap(config)
    integrated_marker = path / "integrated.md"
    integrated_marker.write_text(
        "# Integrated\n\n"
        f"- Proposal: {proposal_name}\n"
        "- Status: integrated into product\n\n"
        f"{report}\n",
        encoding="utf-8",
    )
    return f"{report}\n\nIntegrated proposal into product."


def dry_run_sync(config: HarnessConfig, member: str, files: Iterable[str] | None = None) -> str:
    require_member(config, member)
    candidates = list(changed_files() if files is None else files)
    prefixes = allowed_prefixes(config, member)
    safe = [path for path in candidates if path.startswith(prefixes)]
    blocked = [path for path in candidates if not path.startswith(prefixes)]
    lines = [f"Dry run for {member} ({member_display_name(config, member)})", ""]
    if safe:
        lines.append("Would sync:")
        lines.extend(f"- {path}" for path in safe)
    else:
        lines.append("Would sync: nothing")
    lines.append("")
    if blocked:
        lines.append("Blocked:")
        lines.extend(f"- {path}" for path in blocked)
    else:
        lines.append("Blocked: none")
    return "\n".join(lines)


def read_proposal_status(path: pathlib.Path) -> dict[str, str]:
    proposal = path / "proposal.md"
    result = {"status": "missing", "accepted": "no", "decision_status": "unknown", "risk": "info"}
    if not proposal.exists():
        return result
    text = proposal.read_text(encoding="utf-8")
    for line in text.splitlines():
        if line.startswith("- Status:"):
            result["status"] = line.split(":", 1)[1].strip()
        elif line.startswith("- Accepted:"):
            result["accepted"] = line.split(":", 1)[1].strip()
        elif line.startswith("- Decision status:"):
            result["decision_status"] = line.split(":", 1)[1].strip()
        elif line.startswith("- Risk level:"):
            result["risk"] = line.split(":", 1)[1].strip()
    return result


def read_json_file(path: pathlib.Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def pending_leader_decisions(config: HarnessConfig) -> list[dict[str, object]]:
    if not config.notifications_root.exists():
        return []
    decisions: list[dict[str, object]] = []
    for path in sorted(config.notifications_root.glob("*.json")):
        data = read_json_file(path)
        if data.get("status") == "pending_decision":
            decisions.append({**data, "file": display_path(path)})
    return decisions


def append_decision_log(config: HarnessConfig, data: dict[str, object]) -> None:
    config.decision_log.parent.mkdir(parents=True, exist_ok=True)
    entry = {**data, "logged_at": _dt.datetime.now(_dt.timezone.utc).isoformat()}
    with config.decision_log.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry, ensure_ascii=False, sort_keys=True) + "\n")


def create_leader_decision(
    config: HarnessConfig,
    title: str,
    reason: str,
    recommendation: str,
    urgency: str = "warning",
    member: str | None = None,
    proposal: str | None = None,
    choices: str | None = None,
) -> pathlib.Path:
    if urgency not in {"info", "warning", "urgent"}:
        raise HarnessError("Urgency must be one of: info, warning, urgent")
    decision_id = (
        f"{_dt.datetime.now(_dt.timezone.utc).strftime('%Y%m%d%H%M%S%f')}-"
        f"{safe_slug(title, 'decision')}-{uuid.uuid4().hex[:8]}"
    )
    path = config.notifications_root / f"{decision_id}.json"
    config.notifications_root.mkdir(parents=True, exist_ok=True)
    payload = {
        "id": decision_id,
        "title": title,
        "status": "pending_decision",
        "urgency": urgency,
        "reason": reason,
        "recommendation": recommendation,
        "choices": choices or "approve / request_changes / defer / reject",
        "member": member,
        "proposal": proposal,
        "hermes_target": config.hermes_target,
        "created_at": _dt.datetime.now(_dt.timezone.utc).isoformat(),
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    append_decision_log(config, {"event": "decision_created", **payload})
    return path


def resolve_leader_decision(config: HarnessConfig, decision_id: str, status: str, notes: str | None = None) -> pathlib.Path:
    if status not in {"approved", "rejected", "changes_requested", "deferred", "executed"}:
        raise HarnessError("Decision status must be approved, rejected, changes_requested, deferred, or executed.")
    path = config.notifications_root / f"{decision_id}.json"
    if not path.exists():
        raise HarnessError(f"Unknown leader decision: {decision_id}")
    data = read_json_file(path)
    data["status"] = status
    data["resolved_at"] = _dt.datetime.now(_dt.timezone.utc).isoformat()
    data["notes"] = notes or ""
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    append_decision_log(config, {"event": "decision_resolved", **data})
    return path


def dashboard_data(config: HarnessConfig) -> dict[str, object]:
    proposal_dirs = sorted(p for p in config.integration_proposals.iterdir() if p.is_dir()) if config.integration_proposals.exists() else []
    proposals = []
    pending_decisions = []
    risks = []
    for item in proposal_dirs:
        status = read_proposal_status(item)
        record = {"name": item.name, **status}
        proposals.append(record)
        if status["decision_status"] == "pending_decision":
            pending_decisions.append(record)
        if status["risk"] in {"warning", "urgent"}:
            risks.append(record)
    decision_items = pending_leader_decisions(config)
    pending_decisions.extend(
        {
            "name": str(item.get("title", item.get("id", "decision"))),
            "status": str(item.get("status", "pending_decision")),
            "accepted": "n/a",
            "decision_status": str(item.get("status", "pending_decision")),
            "risk": str(item.get("urgency", "warning")),
            "source": "leader-notification",
        }
        for item in decision_items
    )
    risks.extend(
        {
            "name": str(item.get("title", item.get("id", "decision"))),
            "status": str(item.get("status", "pending_decision")),
            "accepted": "n/a",
            "decision_status": str(item.get("status", "pending_decision")),
            "risk": str(item.get("urgency", "warning")),
            "source": "leader-notification",
        }
        for item in decision_items
        if item.get("urgency") in {"warning", "urgent"}
    )
    members = []
    for member in config.members:
        workspace = member_workspace(config, member)
        requests = sorted((workspace / "requests").glob("*.md")) if workspace.exists() else []
        outputs = sorted((workspace / "outputs").glob("*.md")) if workspace.exists() else []
        members.append(
            {
                "id": member,
                "name": member_display_name(config, member),
                "workspace": "ready" if workspace.exists() else "missing",
                "request_count": len(requests),
                "output_count": len(outputs),
            }
        )
    return {
        "generated_at": _dt.datetime.now(_dt.timezone.utc).isoformat(),
        "summary": {
            "members": len(config.members),
            "proposals": len(proposals),
            "pending_decisions": len(pending_decisions),
            "risks": len(risks),
            "submission_checks": [
                {"label": "Product runs locally", "status": "todo"},
                {"label": "Demo scenario exists", "status": "todo"},
                {"label": "Presentation matches product", "status": "todo"},
                {"label": "README is ready", "status": "todo"},
                {"label": "GitHub is current", "status": "todo"},
            ],
        },
        "members": members,
        "proposals": proposals,
        "pending_decisions": pending_decisions,
        "risks": risks,
        "decision_items": decision_items,
        "leader": {
            "hermes_target": config.hermes_target,
            "decision_log": display_path(config.decision_log),
        },
    }


def dashboard_html() -> str:
    return """<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Hackathon Leader Dashboard</title>
  <style>
    :root { color-scheme: light; --ink:#172026; --muted:#667085; --line:#d8dee4; --bg:#f6f8fa; --card:#ffffff; --accent:#2563eb; --warn:#b45309; --bad:#b42318; --ok:#067647; }
    * { box-sizing: border-box; }
    body { margin:0; font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; color:var(--ink); background:var(--bg); }
    header { padding:24px 28px 14px; background:#fff; border-bottom:1px solid var(--line); }
    h1 { margin:0 0 6px; font-size:28px; letter-spacing:0; }
    h2 { margin:0 0 12px; font-size:17px; }
    main { display:grid; grid-template-columns: 1fr 1.2fr 1fr; gap:16px; padding:16px; }
    section, .metric { background:var(--card); border:1px solid var(--line); border-radius:8px; padding:16px; }
    .metrics { display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:12px; padding:16px; }
    .metric strong { display:block; font-size:28px; }
    .muted { color:var(--muted); font-size:13px; }
    .item { border-top:1px solid var(--line); padding:11px 0; }
    .item:first-child { border-top:0; padding-top:0; }
    .badge { display:inline-flex; align-items:center; min-height:24px; padding:2px 8px; border-radius:999px; font-size:12px; background:#eef2ff; color:#1d4ed8; }
    .urgent { color:var(--bad); font-weight:700; }
    .warning { color:var(--warn); font-weight:700; }
    .ok { color:var(--ok); font-weight:700; }
    ul { margin:0; padding-left:18px; }
    @media (max-width: 980px) { main, .metrics { grid-template-columns:1fr; } }
  </style>
</head>
<body>
  <header>
    <h1>Hackathon Leader Dashboard</h1>
    <div class="muted" id="generated">Loading dashboard data...</div>
  </header>
  <div class="metrics" id="metrics"></div>
  <main>
    <section><h2>팀원별 현황</h2><div id="members"></div></section>
    <section><h2>리더 결정 대기</h2><div id="decisions"></div><h2 style="margin-top:22px">Proposal 큐</h2><div id="proposals"></div></section>
    <section><h2>위험/충돌</h2><div id="risks"></div><h2 style="margin-top:22px">최종 제출 준비도</h2><div id="submission"></div></section>
  </main>
  <script>
    const esc = (value) => String(value ?? "").replace(/[&<>"']/g, (ch) => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[ch]));
    const item = (body) => `<div class="item">${body}</div>`;
    fetch("./dashboard-data.json", {cache:"no-store"})
      .then((response) => response.json())
      .then((data) => {
        document.getElementById("generated").textContent = `Updated ${data.generated_at} · Hermes ${data.leader.hermes_target}`;
        document.getElementById("metrics").innerHTML = [
          ["팀원", data.summary.members],
          ["Proposal", data.summary.proposals],
          ["결정 대기", data.summary.pending_decisions],
          ["위험", data.summary.risks],
        ].map(([label,value]) => `<div class="metric"><strong>${esc(value)}</strong><span class="muted">${esc(label)}</span></div>`).join("");
        document.getElementById("members").innerHTML = data.members.map((m) => item(`<strong>${esc(m.name)}</strong> <span class="badge">${esc(m.id)}</span><br><span class="muted">workspace ${esc(m.workspace)} · tasks ${esc(m.request_count)} · outputs ${esc(m.output_count)}</span>`)).join("") || item("팀원 상태 없음");
        document.getElementById("decisions").innerHTML = data.pending_decisions.map((p) => item(`<strong>${esc(p.name)}</strong><br><span class="${esc(p.risk)}">${esc(p.risk)}</span> · ${esc(p.status)}<br><span class="muted">결정하면 대기함에서 사라지고 decision log로 이동</span>`)).join("") || item(`<span class="ok">대기 중인 결정 없음</span>`);
        document.getElementById("proposals").innerHTML = data.proposals.map((p) => item(`<strong>${esc(p.name)}</strong><br><span class="muted">${esc(p.status)} · accepted ${esc(p.accepted)} · ${esc(p.decision_status)}</span>`)).join("") || item("proposal 없음");
        document.getElementById("risks").innerHTML = data.risks.map((p) => item(`<strong>${esc(p.name)}</strong><br><span class="${esc(p.risk)}">${esc(p.risk)}</span>`)).join("") || item(`<span class="ok">현재 위험 없음</span>`);
        document.getElementById("submission").innerHTML = `<ul>${data.summary.submission_checks.map((c) => `<li>${esc(c.label)}: ${esc(c.status)}</li>`).join("")}</ul>`;
      })
      .catch((error) => { document.getElementById("generated").textContent = `Dashboard data failed to load: ${error}`; });
  </script>
</body>
</html>
"""


def create_dashboard(config: HarnessConfig) -> pathlib.Path:
    config.integration_proposals.mkdir(parents=True, exist_ok=True)
    config.dashboard_root.mkdir(parents=True, exist_ok=True)
    data_path = config.dashboard_root / config.dashboard_data_file
    html_path = config.dashboard_root / config.dashboard_html_file
    data_path.write_text(json.dumps(dashboard_data(config), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    html_path.write_text(dashboard_html(), encoding="utf-8")
    legacy_path = config.integration_proposals / "dashboard.md"
    legacy_path.write_text(
        "# Leader Dashboard\n\n"
        f"Open `{display_path(html_path)}` or the Vercel deployment for the visual dashboard.\n",
        encoding="utf-8",
    )
    return html_path


def create_session_wrap(config: HarnessConfig) -> pathlib.Path:
    base = config.workspace_root.parent.resolve()
    docs = base / "docs"
    docs.mkdir(parents=True, exist_ok=True)
    path = docs / "session-wrap.md"
    proposal_count = len([p for p in config.integration_proposals.iterdir() if p.is_dir()]) if config.integration_proposals.exists() else 0
    path.write_text(
        "# Session Wrap\n\n"
        "## Snapshot\n\n"
        f"- Product root: `{config.product_root.resolve().relative_to(base)}`\n"
        f"- Team workspace: `{config.workspace_root.resolve().relative_to(base)}`\n"
        f"- Integration proposals: {proposal_count}\n\n"
        "## Next Leader Checks\n\n"
        "- Review teammate-approved integration proposals.\n"
        "- Run harness verification before product integration.\n"
        "- Record reusable learnings after major decisions.\n",
        encoding="utf-8",
    )
    return path


def verify_workspace(config: HarnessConfig, member: str | None = None) -> None:
    if member is not None:
        ensure_member_workspace(config, member)
    for command in config.verification_commands:
        completed = subprocess.run(
            command,
            cwd=REPO_ROOT,
            shell=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if completed.returncode != 0:
            raise HarnessError(
                "Verification failed:\n"
                f"$ {command}\n"
                f"{completed.stdout}{completed.stderr}"
            )


def git_available() -> bool:
    return (REPO_ROOT / ".git").exists()


def changed_files() -> list[str]:
    if not git_available():
        return []
    completed = run(["git", "status", "--porcelain"], check=True)
    files: list[str] = []
    for line in completed.stdout.splitlines():
        if not line.strip():
            continue
        path = line[3:] if len(line) > 3 else line
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        files.append(path)
    return files


def allowed_prefixes(config: HarnessConfig, member: str) -> tuple[str, ...]:
    base = config.workspace_root.parent.resolve()
    workspace = member_workspace(config, member).resolve().relative_to(base).as_posix()
    proposals = config.integration_proposals.resolve().relative_to(base).as_posix()
    return (f"{workspace}/", f"{proposals}/{member}-")


def assert_safe_changes(config: HarnessConfig, member: str, files: Iterable[str]) -> None:
    prefixes = allowed_prefixes(config, member)
    unsafe = [path for path in files if not path.startswith(prefixes)]
    if unsafe and not config.allow_common_file_edits:
        base = config.workspace_root.parent.resolve()
        product_prefix = config.product_root.resolve().relative_to(base).as_posix()
        product_changes = [path for path in unsafe if path.startswith(f"{product_prefix}/")]
        if product_changes:
            joined = "\n".join(f"- {path}" for path in product_changes)
            raise HarnessError(
                "Product files cannot be synced directly by teammate agents:\n"
                f"{joined}\n"
                "Move the intended product change into `integration-proposals/` for leader review."
            )
        joined = "\n".join(f"- {path}" for path in unsafe)
        raise HarnessError(
            "Refusing to sync changes outside the member workspace or this member's integration proposals:\n"
            f"{joined}\n"
            "Move shared changes into this member's harness-created integration proposal or ask the leader."
        )


def assert_no_conflict_markers(base: pathlib.Path, files: Iterable[str]) -> None:
    marker_prefixes = ("<<<<<<< ", "=======", ">>>>>>> ")
    conflicts: list[str] = []
    for file_name in files:
        path = base / file_name
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if any(marker in text for marker in marker_prefixes):
            conflicts.append(file_name)
    if conflicts:
        joined = "\n".join(f"- {path}" for path in conflicts)
        raise HarnessError(
            "Merge conflict markers detected. The harness will not auto-resolve conflicts:\n"
            f"{joined}\n"
            "Escalate this to the project leader."
        )


def generate_commit_message(config: HarnessConfig, member: str, title: str | None, message: str | None) -> str:
    if message:
        return message
    if title:
        return f"{member_display_name(config, member)}: {title.strip().lower()}"
    return f"{member_display_name(config, member)}: sync approved hackathon work"


def sync_changes(config: HarnessConfig, member: str, message: str | None, title: str | None = None) -> str:
    require_member(config, member)
    files = changed_files()
    dry_run_report = dry_run_sync(config, member, files)
    if not git_available():
        return f"{dry_run_report}\n\nGit repository not initialized; skipped commit and push."
    verify_workspace(config, member)
    if not files:
        return f"{dry_run_report}\n\nNo changes to sync."
    assert_safe_changes(config, member, files)
    assert_no_conflict_markers(REPO_ROOT, files)
    run(["git", "add", *files], check=True)
    commit_message = generate_commit_message(config, member, title, message)
    run(["git", "commit", "-m", commit_message], check=True)
    push = run(["git", "push", config.push_remote, config.push_branch], check=False)
    if push.returncode != 0:
        raise HarnessError(
            "Commit succeeded but push failed. Ask the leader to check GitHub credentials.\n"
            f"{push.stdout}{push.stderr}"
        )
    return f"{dry_run_report}\n\nCommitted and pushed safe changes."


def print_status(config: HarnessConfig) -> None:
    print(f"Product root: {config.product_root.relative_to(REPO_ROOT)}")
    print(f"Workspace root: {config.workspace_root.relative_to(REPO_ROOT)}")
    print(f"Integration proposals: {config.integration_proposals.relative_to(REPO_ROOT)}")
    print(f"Selected local teammate: {selected_member_label(config)}")
    print("Members:")
    for member in config.members:
        exists = "ready" if member_workspace(config, member).exists() else "missing"
        print(f"- {member} ({member_display_name(config, member)}): {exists}")
    print(f"Git repository: {'yes' if git_available() else 'no'}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Hackathon Codex agent harness")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("init", help="Create teammate workspaces")
    subparsers.add_parser("status", help="Show harness status")
    subparsers.add_parser("dashboard", help="Write the leader integration dashboard")
    subparsers.add_parser("session-wrap", help="Write a session wrap summary")

    select = subparsers.add_parser("select-member", help="Select this machine's teammate")
    select.add_argument("member_or_name")

    task = subparsers.add_parser("task", help="Create a clarified task brief")
    task.add_argument("--member")
    task.add_argument("--title", required=True)
    task.add_argument("--type", required=True, choices=None)

    review = subparsers.add_parser("review", help="Create a local teammate review request")
    review.add_argument("--member")
    review.add_argument("--title", required=True)

    approve = subparsers.add_parser("approve", help="Record teammate local approval")
    approve.add_argument("--member")
    approve.add_argument("--title", required=True)

    propose = subparsers.add_parser("propose", help="Create a leader integration proposal after teammate approval")
    propose.add_argument("--member")
    propose.add_argument("--title", required=True)

    integrate = subparsers.add_parser("integrate", help="Leader-only integration from proposal files into product")
    integrate.add_argument("proposal_name")
    integrate.add_argument("--dry-run", action="store_true")

    verify = subparsers.add_parser("verify", help="Run harness verification")
    verify.add_argument("--member")
    verify.add_argument("--all", action="store_true")

    sync = subparsers.add_parser("sync", help="Verify, commit, and push safe changes")
    sync.add_argument("--member")
    sync.add_argument("--message")
    sync.add_argument("--title")
    sync.add_argument("--dry-run", action="store_true")

    decision = subparsers.add_parser("decision", help="Create or resolve leader decision items")
    decision_subparsers = decision.add_subparsers(dest="decision_command", required=True)
    decision_create = decision_subparsers.add_parser("create", help="Create a pending leader decision")
    decision_create.add_argument("--title", required=True)
    decision_create.add_argument("--urgency", default="warning", choices=("info", "warning", "urgent"))
    decision_create.add_argument("--reason", required=True)
    decision_create.add_argument("--recommendation", required=True)
    decision_create.add_argument("--member")
    decision_create.add_argument("--proposal")
    decision_create.add_argument("--choices")
    decision_resolve = decision_subparsers.add_parser("resolve", help="Resolve a pending leader decision")
    decision_resolve.add_argument("decision_id")
    decision_resolve.add_argument("--status", required=True, choices=("approved", "rejected", "changes_requested", "deferred", "executed"))
    decision_resolve.add_argument("--notes")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    config = load_config()
    try:
        if args.command == "init":
            init_workspaces(config)
            print("Initialized teammate workspaces.")
        elif args.command == "status":
            print_status(config)
        elif args.command == "dashboard":
            path = create_dashboard(config)
            print(path.relative_to(REPO_ROOT))
        elif args.command == "session-wrap":
            path = create_session_wrap(config)
            print(path.relative_to(REPO_ROOT))
        elif args.command == "select-member":
            path = select_member(config, args.member_or_name)
            print(path.relative_to(REPO_ROOT))
        elif args.command == "task":
            path = create_task(config, resolve_member(config, args.member), args.title, args.type)
            print(path.relative_to(REPO_ROOT))
        elif args.command == "review":
            path = create_review_request(config, resolve_member(config, args.member), args.title)
            print(path.relative_to(REPO_ROOT))
        elif args.command == "approve":
            path = approve_review(config, resolve_member(config, args.member), args.title)
            print(path.relative_to(REPO_ROOT))
        elif args.command == "propose":
            path = create_integration_proposal(config, resolve_member(config, args.member), args.title)
            print(path.relative_to(REPO_ROOT))
        elif args.command == "integrate":
            if args.dry_run:
                print(dry_run_integrate(config, args.proposal_name))
            else:
                print(integrate_proposal(config, args.proposal_name))
        elif args.command == "verify":
            verify_workspace(config, None if args.all else resolve_member(config, args.member))
            print("Verification passed.")
        elif args.command == "sync":
            member = resolve_member(config, args.member)
            if args.dry_run:
                print(dry_run_sync(config, member))
            else:
                print(sync_changes(config, member, args.message, args.title))
        elif args.command == "decision":
            if args.decision_command == "create":
                path = create_leader_decision(
                    config,
                    args.title,
                    args.reason,
                    args.recommendation,
                    args.urgency,
                    args.member,
                    args.proposal,
                    args.choices,
                )
                create_dashboard(config)
                print(path.relative_to(REPO_ROOT))
            elif args.decision_command == "resolve":
                path = resolve_leader_decision(config, args.decision_id, args.status, args.notes)
                create_dashboard(config)
                print(path.relative_to(REPO_ROOT))
        else:
            parser.error(f"Unknown command: {args.command}")
    except HarnessError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
