from pathlib import Path
import copy
import json
import shutil
import sys
import tempfile
import unittest


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from verify_kit import (  # noqa: E402
    broken_local_references,
    canonical_policy_digest,
    load_video_readability_policy,
    verify_story_reel_template_geometry,
)


VALID_POLICY = {
    "schema_version": 1,
    "policy_version": "ARPHE_VIDEO_READABILITY_V1",
    "canvases": {
        "story_reel_1080x1920": {
            "width": 1080,
            "height": 1920,
            "essential_safe_area": {
                "left": 0.08,
                "right": 0.84,
                "top": 0.10,
                "bottom": 0.82,
            },
        },
    },
    "reading": {
        "words_per_second": 4.0,
        "settle_seconds": 1,
        "minimum_seconds": 3,
        "standard_maximum_seconds": 12,
    },
    "review_body": {"size_tiers": [0.052, 0.047, 0.042], "maximum_lines": 7},
    "typography": {
        "heading": {"family": "Noto Serif Display", "weight": 300},
        "body": {"family": "Satoshi", "weight": 400},
        "label": {"family": "Satoshi", "weight": 500},
        "button": {"family": "Satoshi", "weight": 700},
    },
    "technical_fallback_is_final": False,
}


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


class VideoReadabilityPolicyTests(unittest.TestCase):
    def write_policy(self, root: Path, policy: dict) -> Path:
        path = root / "video-readability.json"
        path.write_text(json.dumps(policy), encoding="utf-8")
        return path

    def test_loads_the_exact_canonical_policy_and_stable_digest(self):
        policy_path = Path(__file__).resolve().parents[1] / "tokens" / "video-readability.json"

        policy = load_video_readability_policy(policy_path)

        self.assertEqual(policy, VALID_POLICY)
        self.assertEqual(
            canonical_policy_digest(policy),
            "68b240d727e23707b4b64e5da069c47519e166a25bce94e33cc3de5ae005c0fe",
        )

    def test_rejects_unknown_keys_at_every_schema_level(self):
        cases = []
        for location in (
            (),
            ("reading",),
            ("review_body",),
            ("typography", "body"),
            ("canvases", "story_reel_1080x1920", "essential_safe_area"),
        ):
            policy = copy.deepcopy(VALID_POLICY)
            target = policy
            for key in location:
                target = target[key]
            target["unexpected"] = 1
            cases.append(policy)

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for index, policy in enumerate(cases):
                with self.subTest(index=index), self.assertRaises(ValueError):
                    load_video_readability_policy(self.write_policy(root, policy))


    def test_rejects_boolean_numeric_values(self):
        numeric_paths = (
            ("schema_version",),
            ("reading", "words_per_second"),
            ("reading", "settle_seconds"),
            ("review_body", "maximum_lines"),
            ("typography", "body", "weight"),
        )
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for path in numeric_paths:
                policy = copy.deepcopy(VALID_POLICY)
                target = policy
                for key in path[:-1]:
                    target = target[key]
                target[path[-1]] = True
                with self.subTest(path=path), self.assertRaises(ValueError):
                    load_video_readability_policy(self.write_policy(root, policy))

    def test_rejects_unordered_or_changed_size_tiers(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for tiers in ([0.047, 0.052, 0.042], [0.052, 0.047, 0.041]):
                policy = copy.deepcopy(VALID_POLICY)
                policy["review_body"]["size_tiers"] = tiers
                with self.subTest(tiers=tiers), self.assertRaises(ValueError):
                    load_video_readability_policy(self.write_policy(root, policy))

    def test_rejects_out_of_range_or_inverted_safe_coordinates(self):
        invalid_areas = (
            {"left": -0.01, "right": 0.84, "top": 0.10, "bottom": 0.82},
            {"left": 0.90, "right": 0.84, "top": 0.10, "bottom": 0.82},
            {"left": 0.08, "right": 0.84, "top": 0.90, "bottom": 0.82},
            {"left": 0.08, "right": 1.01, "top": 0.10, "bottom": 0.82},
        )
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for area in invalid_areas:
                policy = copy.deepcopy(VALID_POLICY)
                policy["canvases"]["story_reel_1080x1920"]["essential_safe_area"] = area
                with self.subTest(area=area), self.assertRaises(ValueError):
                    load_video_readability_policy(self.write_policy(root, policy))


class StoryReelTemplateTests(unittest.TestCase):
    def setUp(self):
        self.root = Path(__file__).resolve().parents[1]
        self.policy = load_video_readability_policy(self.root / "tokens" / "video-readability.json")

    def test_essential_nodes_fit_the_canonical_safe_rectangle(self):
        self.assertEqual(
            verify_story_reel_template_geometry(self.root, self.policy),
            [],
        )

    def test_rejects_the_legacy_96_pixel_bottom_placement(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            shutil.copytree(self.root / "templates", root / "templates")
            html = root / "templates" / "social" / "story-1080x1920.html"
            text = html.read_text(encoding="utf-8").replace("bottom: 346px", "bottom: 96px")
            html.write_text(text, encoding="utf-8")

            errors = verify_story_reel_template_geometry(root, self.policy)

            self.assertTrue(any("bottom" in error for error in errors), errors)

    def test_rejects_missing_essential_or_font_status_markers(self):
        mutations = (
            ('data-essential="true"', ""),
            ('data-font-status="checking"', ""),
            ('id="font-fallback-badge"', ""),
            ("document.fonts.ready", "Promise.resolve()"),
            ('document.fonts.check("400 1em Satoshi")', "true"),
            ('document.fonts.check("500 1em Satoshi")', "true"),
            ('document.fonts.check("700 1em Satoshi")', "true"),
        )
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            shutil.copytree(self.root / "templates", root / "templates")
            html = root / "templates" / "social" / "story-1080x1920.html"
            original = html.read_text(encoding="utf-8")
            for needle, replacement in mutations:
                with self.subTest(needle=needle):
                    html.write_text(original.replace(needle, replacement, 1), encoding="utf-8")
                    self.assertTrue(
                        verify_story_reel_template_geometry(root, self.policy),
                        f"mutation unexpectedly accepted: {needle}",
                    )


if __name__ == "__main__":
    unittest.main()
