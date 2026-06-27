import tempfile
import unittest
from pathlib import Path

from harness.hackathon_harness import (
    HarnessConfig,
    HarnessError,
    approve_review,
    assert_no_conflict_markers,
    assert_safe_changes,
    create_dashboard,
    create_leader_decision,
    create_integration_proposal,
    dry_run_integrate,
    integrate_proposal,
    create_review_request,
    create_session_wrap,
    create_task,
    dry_run_sync,
    generate_commit_message,
    ensure_inside,
    ensure_member_workspace,
    resolve_member,
    resolve_leader_decision,
    select_member,
    verify_workspace,
)


def config_for(root: Path) -> HarnessConfig:
    return HarnessConfig(
        workspace_root=root / "team-work",
        product_root=root / "product",
        integration_proposals=root / "integration-proposals",
        local_member_path=root / ".hackathon" / "local-member.json",
        members=("member-1", "member-2"),
        member_names={"member-1": "고윤재", "member-2": "권이루"},
        roles=("code", "qa"),
        checklist_templates=Path.cwd() / "docs" / "checklists",
        verification_commands=("python3 --version",),
        push_remote="origin",
        push_branch="HEAD",
        allow_common_file_edits=False,
        dashboard_root=root / "dashboard",
        dashboard_data_file="dashboard-data.json",
        dashboard_html_file="index.html",
        hermes_target="discord:#hackathon-leader",
        decision_log=root / "leader-decisions" / "decision-log.jsonl",
        notifications_root=root / "leader-notifications",
        persona_dataset="nvidia/Nemotron-Personas-Korea",
        fallback_persona_dataset="NLPBada/korean-persona-chat-dataset",
    )


class HarnessTests(unittest.TestCase):
    def test_ensure_member_workspace_creates_expected_folders(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            config = config_for(Path(tmp))
            workspace = ensure_member_workspace(config, "member-1")

            self.assertTrue((workspace / "requests").is_dir())
            self.assertTrue((workspace / "outputs").is_dir())
            self.assertTrue((workspace / "notes").is_dir())
            self.assertTrue((workspace / "patches").is_dir())
            self.assertTrue((workspace / "src").is_dir())
            self.assertTrue((workspace / "tests").is_dir())
            self.assertTrue((workspace / "interviews").is_dir())
            self.assertTrue((workspace / "specs").is_dir())
            self.assertTrue((workspace / "customer-interviews").is_dir())
            self.assertTrue((workspace / "README.md").is_file())
            self.assertIn("고윤재", (workspace / "README.md").read_text(encoding="utf-8"))

    def test_create_task_writes_ouroboros_brief(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            config = config_for(Path(tmp))
            path = create_task(config, "member-1", "Landing Page Draft", "code")

            text = path.read_text(encoding="utf-8")
            self.assertIn("## Ouroboros Clarification", text)
            self.assertIn("## Korean Persona Simulated Interview", text)
            self.assertIn("## Product Psychology Check", text)
            self.assertIn("## Seed-like Task Spec", text)
            self.assertIn("- Name: 고윤재", text)
            self.assertIn("- Task type: code", text)
            self.assertIn("- Intent:", text)
            self.assertIn("- Acceptance criteria:", text)
            self.assertIn("## Execution Plan", text)
            self.assertIn("## Stop Gates", text)
            self.assertTrue((path.parents[1] / "tests" / "landing-page-draft-checklist.md").exists())
            self.assertTrue((path.parents[1] / "specs" / "landing-page-draft-seed.md").exists())

    def test_unknown_member_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            config = config_for(Path(tmp))
            with self.assertRaises(HarnessError):
                ensure_member_workspace(config, "member-99")

    def test_ensure_inside_rejects_path_escape(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with self.assertRaises(HarnessError):
                ensure_inside(root / "outside.txt", root / "team-work")

    def test_safe_changes_allow_member_and_proposals(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            config = config_for(Path(tmp))
            assert_safe_changes(
                config,
                "member-1",
                [
                    "team-work/member-1/outputs/result.md",
                    "integration-proposals/member-1-shared-change/proposal.md",
                ],
            )

    def test_safe_changes_reject_other_member_proposal(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            config = config_for(Path(tmp))
            with self.assertRaises(HarnessError):
                assert_safe_changes(config, "member-1", ["integration-proposals/member-2-demo/proposal.md"])

    def test_safe_changes_reject_common_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            config = config_for(Path(tmp))
            with self.assertRaises(HarnessError):
                assert_safe_changes(config, "member-1", ["src/app.py"])

    def test_verify_workspace_runs_commands(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            config = config_for(Path(tmp))
            verify_workspace(config, "member-1")

    def test_proposal_requires_teammate_approval(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            config = config_for(Path(tmp))
            write_complete_checklist(config, "member-1", "Landing Page Draft")
            create_review_request(config, "member-1", "Landing Page Draft")

            with self.assertRaises(HarnessError):
                create_integration_proposal(config, "member-1", "Landing Page Draft")

    def test_approved_review_can_become_proposal(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            config = config_for(Path(tmp))
            write_complete_checklist(config, "member-1", "Landing Page Draft")
            approve_review(config, "member-1", "Landing Page Draft")
            proposal = create_integration_proposal(config, "member-1", "Landing Page Draft")

            text = proposal.read_text(encoding="utf-8")
            self.assertIn("Teammate local approval: yes", text)
            self.assertIn("waiting-for-leader-review", text)

    def test_member_can_be_selected_by_name(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            config = config_for(Path(tmp))
            select_member(config, "권이루")

            self.assertEqual(resolve_member(config, None), "member-2")

    def test_review_requires_completed_checklist(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            config = config_for(Path(tmp))
            create_task(config, "member-1", "Landing Page Draft", "code")

            with self.assertRaises(HarnessError):
                create_review_request(config, "member-1", "Landing Page Draft")

    def test_review_writes_verification_summary_and_learning_prompt(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            config = config_for(Path(tmp))
            write_complete_checklist(config, "member-1", "Landing Page Draft")
            create_review_request(config, "member-1", "Landing Page Draft")

            summary = config.workspace_root / "member-1" / "notes" / "landing-page-draft-verify.md"
            learnings = config.workspace_root / "member-1" / "notes" / "learnings.md"
            self.assertIn("Verification Summary", summary.read_text(encoding="utf-8"))
            self.assertIn("Reusable Learnings", learnings.read_text(encoding="utf-8"))

    def test_dry_run_sync_reports_safe_and_blocked_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            config = config_for(Path(tmp))
            report = dry_run_sync(
                config,
                "member-1",
                [
                    "team-work/member-1/outputs/result.md",
                    "product/app.py",
                ],
            )

            self.assertIn("Would sync", report)
            self.assertIn("Blocked", report)
            self.assertIn("product/app.py", report)

    def test_product_changes_have_specific_block_message(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            config = config_for(Path(tmp))
            with self.assertRaisesRegex(HarnessError, "Product files cannot be synced directly"):
                assert_safe_changes(config, "member-1", ["product/app.py"])

    def test_commit_message_can_be_generated_from_member_and_title(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            config = config_for(Path(tmp))

            message = generate_commit_message(config, "member-1", "Landing Page Draft", None)

            self.assertEqual(message, "고윤재: landing page draft")

    def test_conflict_markers_are_blocked(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            conflict = root / "team-work" / "member-1" / "outputs" / "result.md"
            conflict.parent.mkdir(parents=True)
            conflict.write_text("<<<<<<< HEAD\nours\n=======\ntheirs\n>>>>>>> branch\n", encoding="utf-8")

            with self.assertRaisesRegex(HarnessError, "Merge conflict markers"):
                assert_no_conflict_markers(root, ["team-work/member-1/outputs/result.md"])

    def test_dashboard_and_session_wrap_are_created(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            config = config_for(Path(tmp))
            write_complete_checklist(config, "member-1", "Landing Page Draft")
            approve_review(config, "member-1", "Landing Page Draft")
            create_integration_proposal(config, "member-1", "Landing Page Draft")

            dashboard = create_dashboard(config)
            wrap = create_session_wrap(config)

            self.assertIn("Leader Dashboard", dashboard.read_text(encoding="utf-8"))
            self.assertTrue((config.dashboard_root / "dashboard-data.json").exists())
            self.assertIn("Session Wrap", wrap.read_text(encoding="utf-8"))

    def test_integrate_requires_leader_acceptance(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            config = config_for(Path(tmp))
            proposal = make_proposal_with_product_file(config)

            with self.assertRaisesRegex(HarnessError, "Leader must accept"):
                integrate_proposal(config, proposal.parent.name)

    def test_dry_run_integrate_lists_product_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            config = config_for(Path(tmp))
            proposal = make_proposal_with_product_file(config)
            mark_proposal_accepted(proposal)

            report = dry_run_integrate(config, proposal.parent.name)

            self.assertIn("Would integrate", report)
            self.assertIn("product/demo.md", report)

    def test_integrate_copies_accepted_product_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            config = config_for(Path(tmp))
            proposal = make_proposal_with_product_file(config)
            mark_proposal_accepted(proposal)

            report = integrate_proposal(config, proposal.parent.name)

            product_file = config.product_root / "demo.md"
            self.assertEqual(product_file.read_text(encoding="utf-8"), "demo\n")
            self.assertIn("Integrated", report)

    def test_integrate_refuses_to_overwrite_existing_product_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            config = config_for(Path(tmp))
            proposal = make_proposal_with_product_file(config)
            mark_proposal_accepted(proposal)
            existing = config.product_root / "demo.md"
            existing.parent.mkdir(parents=True)
            existing.write_text("existing\n", encoding="utf-8")

            with self.assertRaisesRegex(HarnessError, "Refusing to overwrite"):
                integrate_proposal(config, proposal.parent.name)

    def test_review_requires_completed_workflow_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            config = config_for(Path(tmp))
            create_task(config, "member-1", "Landing Page Draft", "code")
            checklist = config.workspace_root / "member-1" / "tests" / "landing-page-draft-checklist.md"
            text = checklist.read_text(encoding="utf-8").replace("- Status: incomplete", "- Status: complete")
            text = text.replace("- [ ]", "- [x]")
            checklist.write_text(text, encoding="utf-8")

            with self.assertRaisesRegex(HarnessError, "workflow artifacts are incomplete"):
                create_review_request(config, "member-1", "Landing Page Draft")

    def test_review_rejects_status_only_artifact_completion(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            config = config_for(Path(tmp))
            create_task(config, "member-1", "Landing Page Draft", "code")
            checklist = config.workspace_root / "member-1" / "tests" / "landing-page-draft-checklist.md"
            text = checklist.read_text(encoding="utf-8").replace("- Status: incomplete", "- Status: complete")
            text = text.replace("- [ ]", "- [x]")
            checklist.write_text(text, encoding="utf-8")
            flip_artifact_status_only(config, "member-1")

            with self.assertRaisesRegex(HarnessError, "needs concrete"):
                create_review_request(config, "member-1", "Landing Page Draft")

    def test_review_rejects_filler_artifact_content(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            config = config_for(Path(tmp))
            create_task(config, "member-1", "Landing Page Draft", "code")
            checklist = config.workspace_root / "member-1" / "tests" / "landing-page-draft-checklist.md"
            text = checklist.read_text(encoding="utf-8").replace("- Status: incomplete", "- Status: complete")
            text = text.replace("- [ ]", "- [x]")
            checklist.write_text(text, encoding="utf-8")
            write_filler_artifacts(config, "member-1")

            with self.assertRaisesRegex(HarnessError, "needs concrete"):
                create_review_request(config, "member-1", "Landing Page Draft")

    def test_review_accepts_concise_substantive_scope(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            config = config_for(Path(tmp))
            write_complete_checklist(config, "member-1", "Landing Page Draft")
            brief = config.workspace_root / "member-1" / "requests" / "landing-page-draft.md"
            text = brief.read_text(encoding="utf-8")
            text = replace_line(text, "- Scope:", "- Scope: Copy edits only.")
            brief.write_text(text, encoding="utf-8")

            review = create_review_request(config, "member-1", "Landing Page Draft")

            self.assertTrue(review.exists())

    def test_leader_decision_lifecycle_updates_dashboard(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            config = config_for(Path(tmp))
            decision = create_leader_decision(
                config,
                "Approve onboarding proposal",
                "Existing product file would change",
                "Approve after copy edit",
                "urgent",
                "member-1",
                "member-1-landing-page-draft",
            )
            dashboard = create_dashboard(config)
            data = (config.dashboard_root / "dashboard-data.json").read_text(encoding="utf-8")
            self.assertIn("Approve onboarding proposal", data)
            self.assertIn("pending_decision", data)

            resolve_leader_decision(config, decision.stem, "approved", "Leader approved")
            create_dashboard(config)
            data = (config.dashboard_root / "dashboard-data.json").read_text(encoding="utf-8")
            self.assertNotIn('"status": "pending_decision"', data)
            self.assertIn("Leader Dashboard", dashboard.read_text(encoding="utf-8"))

    def test_leader_decision_ids_do_not_collide_for_same_title(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            config = config_for(Path(tmp))
            first = create_leader_decision(config, "Same Title", "reason", "recommendation")
            second = create_leader_decision(config, "Same Title", "reason", "recommendation")

            self.assertNotEqual(first.name, second.name)
            self.assertTrue(first.exists())
            self.assertTrue(second.exists())


def write_complete_checklist(config: HarnessConfig, member: str, title: str) -> None:
    create_task(config, member, title, "code")
    path = config.workspace_root / member / "tests" / "landing-page-draft-checklist.md"
    text = path.read_text(encoding="utf-8")
    text = text.replace("- Status: incomplete", "- Status: complete")
    text = text.replace("- [ ]", "- [x]")
    path.write_text(text, encoding="utf-8")
    write_complete_artifacts(config, member, title)


def write_complete_artifacts(config: HarnessConfig, member: str, title: str) -> None:
    safe_title = "landing-page-draft"
    workspace = config.workspace_root / member
    brief = workspace / "requests" / f"{safe_title}.md"
    brief_text = brief.read_text(encoding="utf-8")
    brief_text = brief_text.replace("- Status: clarifying", "- Status: ready-for-review")
    brief_text = brief_text.replace("- Intent:", "- Intent: Help first-time users understand the landing page quickly.")
    brief_text = brief_text.replace("- Outcome:", "- Outcome: A locally reviewable landing page draft.")
    brief_text = brief_text.replace("- Scope:", "- Scope: Draft content and structure only.")
    brief_text = brief_text.replace("- Acceptance criteria:", "- Acceptance criteria: Teammate can inspect the result locally.")
    brief.write_text(brief_text, encoding="utf-8")

    (workspace / "specs" / f"{safe_title}-seed.md").write_text(
        "# Seed-like Task Spec\n\n"
        "- Status: complete\n\n"
        "## Goal\n\nBuild a locally reviewable landing page draft for first-time user understanding.\n\n"
        "## Acceptance Criteria\n\n- The teammate can inspect the draft locally and confirm it matches the request.\n\n"
        "## Non-goals\n\n- Do not overwrite existing product files or bypass the leader proposal flow.\n\n"
        "## Inputs\n\n- Teammate request.\n\n"
        "## Output Contract\n\n- A proposal-ready draft with clear scope, evidence, and local review instructions.\n\n"
        "## Evaluate Plan\n\n1. Mechanical verification\n2. Semantic requirement check\n",
        encoding="utf-8",
    )
    (workspace / "interviews" / f"{safe_title}-ouroboros.md").write_text(
        "# Ouroboros Interview Transcript\n\n- Status: complete\n\n## Result\n\nIntent, scope, non-goals, and acceptance criteria are clear.\n",
        encoding="utf-8",
    )
    (workspace / "research" / f"{safe_title}-research.md").write_text(
        "# Automatic Web Research Log\n\n- Status: complete\n- Source: local test fixture with dated product context\n- Applied findings: none\n",
        encoding="utf-8",
    )
    (workspace / "customer-interviews" / f"{safe_title}-personas.md").write_text(
        "# Korean Persona Simulated Interview\n\n- Status: complete\n- Insight: first-time users need a clear next action.\n",
        encoding="utf-8",
    )


def flip_artifact_status_only(config: HarnessConfig, member: str) -> None:
    workspace = config.workspace_root / member
    safe_title = "landing-page-draft"
    replacements = {
        workspace / "requests" / f"{safe_title}.md": ("- Status: clarifying", "- Status: ready-for-review"),
        workspace / "specs" / f"{safe_title}-seed.md": ("- Status: draft", "- Status: complete"),
        workspace / "interviews" / f"{safe_title}-ouroboros.md": ("- Status: draft", "- Status: complete"),
        workspace / "research" / f"{safe_title}-research.md": ("- Status: draft", "- Status: complete"),
        workspace / "customer-interviews" / f"{safe_title}-personas.md": ("- Status: draft", "- Status: complete"),
    }
    for path, (old, new) in replacements.items():
        path.write_text(path.read_text(encoding="utf-8").replace(old, new), encoding="utf-8")


def write_filler_artifacts(config: HarnessConfig, member: str) -> None:
    safe_title = "landing-page-draft"
    workspace = config.workspace_root / member
    brief = workspace / "requests" / f"{safe_title}.md"
    brief_text = brief.read_text(encoding="utf-8")
    brief_text = brief_text.replace("- Status: clarifying", "- Status: ready-for-review")
    brief_text = brief_text.replace("- Intent:", "- Intent: ok")
    brief_text = brief_text.replace("- Outcome:", "- Outcome: done")
    brief_text = brief_text.replace("- Scope:", "- Scope: fine")
    brief_text = brief_text.replace("- Acceptance criteria:", "- Acceptance criteria: yes")
    brief.write_text(brief_text, encoding="utf-8")
    (workspace / "specs" / f"{safe_title}-seed.md").write_text(
        "# Seed-like Task Spec\n\n"
        "- Status: complete\n\n"
        "## Goal\n\nmeaningful??\n\n"
        "## Acceptance Criteria\n\nmeaningful??\n\n"
        "## Non-goals\n\nmeaningful??\n\n"
        "## Inputs\n\nmeaningful??\n\n"
        "## Output Contract\n\nmeaningful??\n\n"
        "## Evaluate Plan\n\nmeaningful??\n",
        encoding="utf-8",
    )
    (workspace / "interviews" / f"{safe_title}-ouroboros.md").write_text(
        "# Ouroboros Interview Transcript\n\n- Status: complete\n\n## Result\n\nmeaningful??\n",
        encoding="utf-8",
    )
    (workspace / "research" / f"{safe_title}-research.md").write_text(
        "# Automatic Web Research Log\n\n- Status: complete\n- Source: ok\n",
        encoding="utf-8",
    )
    (workspace / "customer-interviews" / f"{safe_title}-personas.md").write_text(
        "# Korean Persona Simulated Interview\n\n- Status: complete\n- Insight: done\n",
        encoding="utf-8",
    )


def replace_line(text: str, prefix: str, replacement: str) -> str:
    return "\n".join(replacement if line.startswith(prefix) else line for line in text.splitlines()) + "\n"


def make_proposal_with_product_file(config: HarnessConfig) -> Path:
    write_complete_checklist(config, "member-1", "Landing Page Draft")
    approve_review(config, "member-1", "Landing Page Draft")
    proposal = create_integration_proposal(config, "member-1", "Landing Page Draft")
    proposed_file = proposal.parent / "files" / "product" / "demo.md"
    proposed_file.parent.mkdir(parents=True)
    proposed_file.write_text("demo\n", encoding="utf-8")
    return proposal


def mark_proposal_accepted(proposal: Path) -> None:
    text = proposal.read_text(encoding="utf-8")
    text = text.replace("- Accepted: no", "- Accepted: yes")
    text = text.replace("- Decision status: pending_decision", "- Decision status: approved")
    proposal.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
