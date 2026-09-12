import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
WORKFLOW = REPOSITORY_ROOT / ".github" / "workflows" / "nuviodv-upstream-sync.yml"


class NuvioDvUpstreamSyncWorkflowTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.workflow = WORKFLOW.read_text(encoding="utf-8")

    def test_runs_daily_and_can_be_dispatched_manually(self) -> None:
        self.assertIn("schedule:", self.workflow)
        self.assertIn("cron: '17 4 * * *'", self.workflow)
        self.assertIn("workflow_dispatch:", self.workflow)

    def test_has_permissions_to_push_and_dispatch_release(self) -> None:
        self.assertIn("contents: write", self.workflow)
        self.assertIn("actions: write", self.workflow)
        self.assertIn("gh workflow run nuviodv-android-release.yml", self.workflow)

    def test_syncs_only_the_authoritative_upstream_branch(self) -> None:
        self.assertIn("https://github.com/NuvioMedia/NuvioMobile.git", self.workflow)
        self.assertIn("git fetch --no-tags upstream cmp-rewrite", self.workflow)
        self.assertIn("git merge --no-commit --no-ff upstream/cmp-rewrite", self.workflow)

    def test_conflict_exception_is_limited_to_the_version_file(self) -> None:
        self.assertIn("allowed_conflict='iosApp/Configuration/Version.xcconfig'", self.workflow)
        self.assertIn('[[ "${conflicts[0]}" == "${allowed_conflict}" ]]', self.workflow)
        self.assertIn("git merge --abort", self.workflow)

    def test_verifies_the_fork_before_push(self) -> None:
        self.assertIn("test_advance_nuviodv_version.py", self.workflow)
        self.assertIn("test-configure-nuviodv-release.sh", self.workflow)
        self.assertIn(":androidApp:assembleFullDebug", self.workflow)
        self.assertIn("dovi_parse_rpu", self.workflow)
        self.assertIn("git push origin HEAD:cmp-rewrite", self.workflow)


if __name__ == "__main__":
    unittest.main()
