from pathlib import Path
import sys
import tempfile
import unittest


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from verify_kit import broken_local_references  # noqa: E402


class LocalReferenceTests(unittest.TestCase):
    def test_reports_only_missing_local_assets(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "present.svg").write_text("<svg/>", encoding="utf-8")
            page = root / "page.html"
            page.write_text(
                '<link href="https://example.com/font.css">'
                '<img src="present.svg"><img src="missing.svg">',
                encoding="utf-8",
            )

            self.assertEqual(broken_local_references(page), ["missing.svg"])


if __name__ == "__main__":
    unittest.main()
