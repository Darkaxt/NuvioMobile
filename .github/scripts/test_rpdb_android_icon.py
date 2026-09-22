#!/usr/bin/env python3
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[2]
ANDROID_PAINTER = ROOT / "composeApp/src/androidMain/kotlin/com/nuvio/app/features/settings/IntegrationLogoPainter.android.kt"
IOS_PAINTER = ROOT / "composeApp/src/iosMain/kotlin/com/nuvio/app/features/settings/IntegrationLogoPainter.ios.kt"
ANDROID_DRAWABLE = ROOT / "composeApp/src/androidMain/res/drawable/rpdb_logo.xml"


class RpdbAndroidIconTest(unittest.TestCase):
    def test_android_uses_native_drawable_instead_of_compose_svg(self):
        source = ANDROID_PAINTER.read_text(encoding="utf-8")
        branch = source[source.index("IntegrationLogo.Rpdb") : source.index("IntegrationLogo.Trakt")]

        self.assertIn("painterResource(id = R.drawable.rpdb_logo)", branch)
        self.assertNotIn("composePainterResource", branch)

    def test_android_rpdb_drawable_is_a_vector_resource(self):
        root = ET.parse(ANDROID_DRAWABLE).getroot()
        self.assertEqual("vector", root.tag.rsplit("}", 1)[-1])

    def test_ios_keeps_shared_rpdb_svg_path(self):
        source = IOS_PAINTER.read_text(encoding="utf-8")
        branch = source[source.index("IntegrationLogo.Rpdb") : source.index("IntegrationLogo.Trakt")]

        self.assertIn("painterResource(Res.drawable.rpdb_logo)", branch)


if __name__ == "__main__":
    unittest.main()
