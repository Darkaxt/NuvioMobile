import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
WORKFLOW = REPOSITORY_ROOT / ".github" / "workflows" / "nuviodv-upstream-sync.yml"
RELEASE_WORKFLOW = REPOSITORY_ROOT / ".github" / "workflows" / "nuviodv-android-release.yml"


class NuvioDvUpstreamSyncWorkflowTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.workflow = WORKFLOW.read_text(encoding="utf-8")
        cls.release_workflow = RELEASE_WORKFLOW.read_text(encoding="utf-8")

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
        self.assertIn(": > local.properties", self.workflow)
        self.assertIn(":androidApp:assembleFullDebug", self.workflow)
        self.assertIn("dovi_parse_rpu", self.workflow)
        self.assertIn("id: sync_commit", self.workflow)
        self.assertIn('echo "sha=$(git rev-parse HEAD)" >> "${GITHUB_OUTPUT}"', self.workflow)
        self.assertIn("git push origin HEAD:cmp-rewrite", self.workflow)
        self.assertIn('-f source_sha="${SOURCE_SHA}"', self.workflow)

    def test_release_checks_out_the_exact_synced_commit(self) -> None:
        self.assertIn("source_sha:", self.release_workflow)
        self.assertIn("ref: ${{ inputs.source_sha || github.sha }}", self.release_workflow)
        self.assertIn("REQUESTED_SOURCE_SHA: ${{ inputs.source_sha }}", self.release_workflow)
        self.assertIn('[[ "${source_sha}" == "${REQUESTED_SOURCE_SHA}" ]]', self.release_workflow)
        self.assertIn("SOURCE_SHA: ${{ steps.release.outputs.source_sha }}", self.release_workflow)
        self.assertIn('--target "${SOURCE_SHA}"', self.release_workflow)


if __name__ == "__main__":
    unittest.main()
