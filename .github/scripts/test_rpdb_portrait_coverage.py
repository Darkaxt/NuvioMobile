#!/usr/bin/env python3
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
CONTINUE_ROW = ROOT / "composeApp/src/commonMain/kotlin/com/nuvio/app/features/home/components/HomeContinueWatchingSection.kt"
CONTINUE_SHEET = ROOT / "composeApp/src/commonMain/kotlin/com/nuvio/app/core/ui/ContinueWatchingActionSheet.kt"
MAIN_APP = ROOT / "composeApp/src/commonMain/kotlin/com/nuvio/app/MainAppContent.kt"
FLOATING_PROMPT = ROOT / "composeApp/src/commonMain/kotlin/com/nuvio/app/core/ui/FloatingPrompt.kt"


class RpdbPortraitCoverageTest(unittest.TestCase):
    def test_continue_watching_portrait_row_uses_rpdb_with_fallback(self):
        source = CONTINUE_ROW.read_text(encoding="utf-8")
        poster_card = source[source.index("private fun ContinueWatchingPosterCard(") :]
        self.assertIn("rpdbPortraitSelection", poster_card)
        self.assertIn("rpdbPoster.fallbackUrl", poster_card)
        self.assertIn("onError =", poster_card)

    def test_continue_watching_wide_portrait_strip_uses_rpdb_with_fallback(self):
        source = CONTINUE_ROW.read_text(encoding="utf-8")
        wide_card = source[
            source.index("private fun ContinueWatchingWideCard(") :
            source.index("private fun ContinueWatchingPosterCard(")
        ]
        self.assertIn("continueWatchingPosterArtworkUrl", wide_card)
        self.assertIn("rpdbPortraitSelection", wide_card)
        self.assertIn("rpdbPoster.fallbackUrl", wide_card)
        self.assertIn("onError =", wide_card)

    def test_continue_watching_action_sheet_uses_rpdb_with_fallback(self):
        source = CONTINUE_SHEET.read_text(encoding="utf-8")
        header = source[source.index("private fun ContinueWatchingSheetHeader(") :]
        self.assertIn("rpdbPortraitSelection", header)
        self.assertIn("rpdbPoster.fallbackUrl", header)
        self.assertIn("onError =", header)

    def test_resume_prompt_uses_rpdb_with_fallback(self):
        main_source = MAIN_APP.read_text(encoding="utf-8")
        prompt_source = FLOATING_PROMPT.read_text(encoding="utf-8")
        self.assertIn("resumePromptPoster", main_source)
        self.assertIn("rpdbPortraitSelection", main_source)
        self.assertIn("fallbackImageUrl = resumePromptPoster", main_source)
        self.assertIn("fallbackImageUrl: String?", prompt_source)
        self.assertIn("onError =", prompt_source)


if __name__ == "__main__":
    unittest.main()
