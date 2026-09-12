import tempfile
import unittest
from pathlib import Path

from advance_nuviodv_version import advance_version_file, compute_next_version


class AdvanceNuvioDvVersionTest(unittest.TestCase):
    def test_advances_base_patch_when_upstream_is_behind(self) -> None:
        self.assertEqual(
            compute_next_version(
                current_name="0.4.18-nuviodv.1",
                current_code=12203,
                upstream_name="0.4.17",
                upstream_code=122,
            ),
            ("0.4.19-nuviodv.1", 12204),
        )

    def test_adopts_newer_upstream_base_and_advances_code_past_both(self) -> None:
        self.assertEqual(
            compute_next_version(
                current_name="0.4.18-nuviodv.1",
                current_code=12203,
                upstream_name="0.5.0",
                upstream_code=13000,
            ),
            ("0.5.0-nuviodv.1", 13001),
        )

    def test_rejects_a_non_nuviodv_current_version(self) -> None:
        with self.assertRaisesRegex(ValueError, "NuvioDV"):
            compute_next_version(
                current_name="0.4.18",
                current_code=12203,
                upstream_name="0.4.19",
                upstream_code=123,
            )

    def test_updates_only_version_values_in_xcconfig(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fork_config = root / "fork.xcconfig"
            upstream_config = root / "upstream.xcconfig"
            fork_config.write_text(
                "CURRENT_PROJECT_VERSION=12203\nMARKETING_VERSION=0.4.18-nuviodv.1\n",
                encoding="utf-8",
            )
            upstream_config.write_text(
                "CURRENT_PROJECT_VERSION=122\nMARKETING_VERSION=0.4.17\n",
                encoding="utf-8",
            )

            result = advance_version_file(fork_config, upstream_config)

            self.assertEqual(result, ("0.4.19-nuviodv.1", 12204))
            self.assertEqual(
                fork_config.read_text(encoding="utf-8"),
                "CURRENT_PROJECT_VERSION=12204\nMARKETING_VERSION=0.4.19-nuviodv.1\n",
            )


if __name__ == "__main__":
    unittest.main()
