#!/usr/bin/env python3
"""Verify that the public ARPHE graphic kit is complete and portable."""

from __future__ import annotations

import hashlib
import json
import re
import struct
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COLORS = {
    "cream": "#F8F4EE",
    "brown": "#614432",
    "burgundy": "#680C09",
    "red": "#8D0511",
    "ink": "#1B170E",
}
SIZES = (512, 1024, 2048, 4096)
TEMPLATES = {
    "templates/social/post-1080x1350": (1080, 1350),
    "templates/social/story-1080x1920": (1080, 1920),
    "templates/video/title-card-1920x1080": (1920, 1080),
}


def _require_keys(value: object, expected: set[str], location: str) -> dict:
    if not isinstance(value, dict):
        raise ValueError(f"{location} deve essere un oggetto")
    actual = set(value)
    if actual != expected:
        raise ValueError(
            f"chiavi non valide in {location}: attese {sorted(expected)}, trovate {sorted(actual)}"
        )
    return value


def _require_number(value: object, location: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{location} deve essere numerico")
    return float(value)


def load_video_readability_policy(path: Path) -> dict:
    """Load and strictly validate the versioned video readability policy."""
    try:
        policy = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"policy non valida: {exc}") from exc

    policy = _require_keys(
        policy,
        {
            "schema_version",
            "policy_version",
            "canvases",
            "reading",
            "review_body",
            "typography",
            "technical_fallback_is_final",
        },
        "policy",
    )
    schema_version = _require_number(policy["schema_version"], "schema_version")
    if schema_version != 1 or policy["schema_version"] != 1:
        raise ValueError("schema_version non supportata")
    if policy["policy_version"] != "ARPHE_VIDEO_READABILITY_V1":
        raise ValueError("policy_version non supportata")
    if policy["technical_fallback_is_final"] is not False:
        raise ValueError("technical_fallback_is_final deve essere false")

    canvases = _require_keys(
        policy["canvases"], {"story_reel_1080x1920"}, "canvases"
    )
    canvas = _require_keys(
        canvases["story_reel_1080x1920"],
        {"width", "height", "essential_safe_area"},
        "canvases.story_reel_1080x1920",
    )
    if _require_number(canvas["width"], "canvas.width") != 1080:
        raise ValueError("canvas.width deve essere 1080")
    if _require_number(canvas["height"], "canvas.height") != 1920:
        raise ValueError("canvas.height deve essere 1920")
    area = _require_keys(
        canvas["essential_safe_area"],
        {"left", "right", "top", "bottom"},
        "essential_safe_area",
    )
    left, right, top, bottom = (
        _require_number(area[key], f"essential_safe_area.{key}")
        for key in ("left", "right", "top", "bottom")
    )
    if not (0 <= left < right <= 1 and 0 <= top < bottom <= 1):
        raise ValueError("essential_safe_area deve essere ordinata e compresa tra 0 e 1")

    reading = _require_keys(
        policy["reading"],
        {
            "words_per_second",
            "settle_seconds",
            "minimum_seconds",
            "standard_maximum_seconds",
        },
        "reading",
    )
    for key in reading:
        value = _require_number(reading[key], f"reading.{key}")
        if value <= 0:
            raise ValueError(f"reading.{key} deve essere positivo")
    if reading["minimum_seconds"] > reading["standard_maximum_seconds"]:
        raise ValueError("minimum_seconds supera standard_maximum_seconds")

    review_body = _require_keys(
        policy["review_body"], {"size_tiers", "maximum_lines"}, "review_body"
    )
    tiers = review_body["size_tiers"]
    if not isinstance(tiers, list) or tiers != [0.052, 0.047, 0.042]:
        raise ValueError("review_body.size_tiers non canonici o non ordinati")
    for index, value in enumerate(tiers):
        _require_number(value, f"review_body.size_tiers[{index}]")
    if _require_number(review_body["maximum_lines"], "review_body.maximum_lines") != 7:
        raise ValueError("review_body.maximum_lines deve essere 7")

    typography = _require_keys(
        policy["typography"], {"heading", "body", "label", "button"}, "typography"
    )
    expected_typography = {
        "heading": ("Noto Serif Display", 300),
        "body": ("Satoshi", 400),
        "label": ("Satoshi", 500),
        "button": ("Satoshi", 700),
    }
    for role, (family, weight) in expected_typography.items():
        entry = _require_keys(typography[role], {"family", "weight"}, f"typography.{role}")
        if entry["family"] != family:
            raise ValueError(f"famiglia non valida per typography.{role}")
        if _require_number(entry["weight"], f"typography.{role}.weight") != weight:
            raise ValueError(f"peso non valido per typography.{role}")

    return policy


def canonical_policy_digest(policy: dict) -> str:
    """Return SHA-256 of the canonical UTF-8 JSON representation."""
    canonical = json.dumps(policy, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def verify_story_reel_template_geometry(root: Path, policy: dict) -> list[str]:
    """Verify machine-identifiable Story/Reel essentials and font observability."""
    errors: list[str] = []
    canvas = policy["canvases"]["story_reel_1080x1920"]
    width = canvas["width"]
    height = canvas["height"]
    safe = canvas["essential_safe_area"]
    left = round(width * safe["left"])
    right = round(width * safe["right"])
    top = round(height * safe["top"])
    bottom = round(height * safe["bottom"])
    right_margin = width - right
    bottom_margin = height - bottom

    html_path = root / "templates/social/story-1080x1920.html"
    svg_path = root / "templates/social/story-1080x1920.svg"
    try:
        html = html_path.read_text(encoding="utf-8")
    except OSError as exc:
        return [f"template Story/Reel HTML non leggibile: {exc}"]

    required_html = {
        'class="brand-logo" data-essential="true"': "logo HTML essenziale non marcato",
        'class="photo-placeholder" data-essential="true"': "media HTML essenziale non marcato",
        'class="copy" data-essential="true"': "contenitore HTML essenziale non marcato",
        'data-font-status="checking"': "stato font iniziale assente",
        'id="font-fallback-badge"': "badge fallback font assente",
        "document.fonts.ready": "attesa document.fonts.ready assente",
        'document.fonts.check("400 1em Satoshi")': "controllo Satoshi 400 assente",
        'document.fonts.check("500 1em Satoshi")': "controllo Satoshi 500 assente",
        'document.fonts.check("700 1em Satoshi")': "controllo Satoshi 700 assente",
    }
    for marker, message in required_html.items():
        if marker not in html:
            errors.append(message)

    copy_rule = re.search(r"\.copy\s*\{([^}]*)\}", html, re.DOTALL)
    if not copy_rule:
        errors.append("regola .copy assente")
    else:
        declarations = copy_rule.group(1)
        expected_declarations = {
            "left": left,
            "right": right_margin,
            "bottom": bottom_margin,
        }
        for property_name, expected in expected_declarations.items():
            match = re.search(rf"\b{property_name}\s*:\s*(-?\d+)px", declarations)
            if not match or int(match.group(1)) != expected:
                errors.append(
                    f".copy {property_name} deve essere {expected}px per la safe area"
                )

    try:
        svg_root = ET.parse(svg_path).getroot()
    except (OSError, ET.ParseError) as exc:
        errors.append(f"template Story/Reel SVG non leggibile: {exc}")
        return errors

    essential = [node for node in svg_root.iter() if node.get("data-essential") == "true"]
    if not essential:
        errors.append("nodi SVG essenziali non marcati")
    for node in essential:
        tag = node.tag.rsplit("}", 1)[-1]
        try:
            x = float(node.get("x", "nan"))
            y = float(node.get("y", "nan"))
            if tag == "rect":
                node_right = x + float(node.get("width", "nan"))
                node_bottom = y + float(node.get("height", "nan"))
                if not (left <= x and node_right <= right and top <= y and node_bottom <= bottom):
                    errors.append(f"rettangolo SVG essenziale fuori safe area: {node.get('id', tag)}")
            elif tag == "text" and not (left <= x <= right and top <= y <= bottom):
                errors.append(f"testo SVG essenziale fuori safe area: {node.get('id', tag)}")
        except (TypeError, ValueError):
            errors.append(f"geometria SVG essenziale non numerica: {node.get('id', tag)}")
    return errors


def broken_local_references(path: Path) -> list[str]:
    """Return relative file references that do not resolve beside an HTML/CSS file."""
    text = path.read_text(encoding="utf-8")
    candidates = re.findall(r'(?:src|href)=["\']([^"\']+)["\']', text)
    candidates.extend(re.findall(r"url\([\"']?([^\"')]+)", text))
    missing: list[str] = []
    for value in candidates:
        if value.startswith(("http://", "https://", "data:", "#", "mailto:")):
            continue
        if not (path.parent / value).resolve().is_file():
            missing.append(value)
    return sorted(set(missing))


def png_header(path: Path) -> tuple[int, int, int]:
    with path.open("rb") as handle:
        if handle.read(8) != b"\x89PNG\r\n\x1a\n":
            raise ValueError("firma PNG non valida")
        length = struct.unpack(">I", handle.read(4))[0]
        if handle.read(4) != b"IHDR" or length != 13:
            raise ValueError("IHDR PNG non valido")
        width, height, _, color_type, _, _, _ = struct.unpack(">IIBBBBB", handle.read(13))
    return width, height, color_type


def verify() -> list[str]:
    errors: list[str] = []

    required = [
        "README.md", "LICENSES.md", "tokens/colors.json", "tokens/colors.css",
        "tokens/colors.txt", "tokens/video-readability.json", "logos/svg/arphe-logo-ink.svg",
        "logos/svg/arphe-logo-cream.svg", "fonts/SATOSHI.md",
        "fonts/noto-serif-display/OFL.txt", "elements/README.md",
        "brand-guidelines/ISTRUZIONI-PER-AI.md",
    ]
    for relative in required:
        if not (ROOT / relative).is_file():
            errors.append(f"manca: {relative}")

    json_path = ROOT / "tokens/colors.json"
    if json_path.is_file():
        try:
            if json.loads(json_path.read_text(encoding="utf-8")) != COLORS:
                errors.append("tokens/colors.json non coincide con la palette canonica")
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"tokens/colors.json non valido: {exc}")

    for relative in ("tokens/colors.css", "tokens/colors.txt"):
        path = ROOT / relative
        if path.is_file():
            values = set(re.findall(r"#[0-9A-Fa-f]{6}", path.read_text(encoding="utf-8")))
            if {value.upper() for value in values} != set(COLORS.values()):
                errors.append(f"{relative} non contiene esattamente la palette canonica")

    policy_path = ROOT / "tokens/video-readability.json"
    if policy_path.is_file():
        try:
            load_video_readability_policy(policy_path)
        except ValueError as exc:
            errors.append(f"tokens/video-readability.json non valido: {exc}")

    for role, expected in (("ink", COLORS["ink"]), ("cream", COLORS["cream"])):
        svg = ROOT / f"logos/svg/arphe-logo-{role}.svg"
        if svg.is_file():
            try:
                ET.parse(svg)
                if expected.lower() not in svg.read_text(encoding="utf-8").lower():
                    errors.append(f"fill errato: {svg.relative_to(ROOT)}")
            except (ET.ParseError, OSError) as exc:
                errors.append(f"SVG non valido {svg.relative_to(ROOT)}: {exc}")
        for size in SIZES:
            png = ROOT / f"logos/png/arphe-logo-{role}-{size}.png"
            if not png.is_file():
                errors.append(f"manca: {png.relative_to(ROOT)}")
                continue
            try:
                width, height, color_type = png_header(png)
                if max(width, height) != size:
                    errors.append(f"dimensione errata: {png.relative_to(ROOT)} ({width}x{height})")
                if color_type not in (4, 6):
                    errors.append(f"canale alfa assente: {png.relative_to(ROOT)}")
            except (OSError, ValueError, struct.error) as exc:
                errors.append(f"PNG non valido {png.relative_to(ROOT)}: {exc}")

    satoshi_binaries = [
        path for path in ROOT.rglob("*")
        if path.is_file() and "satoshi" in path.name.lower()
        and path.suffix.lower() in {".ttf", ".otf", ".woff", ".woff2"}
    ]
    if satoshi_binaries:
        errors.append("binari Satoshi non redistribuibili presenti")

    for stem, (width, height) in TEMPLATES.items():
        for suffix in (".html", ".svg"):
            path = ROOT / f"{stem}{suffix}"
            if not path.is_file():
                errors.append(f"manca: {path.relative_to(ROOT)}")
                continue
            text = path.read_text(encoding="utf-8")
            if f"{width}" not in text or f"{height}" not in text:
                errors.append(f"canvas non dichiarato: {path.relative_to(ROOT)}")
            if "file://" in text or "/Users/" in text:
                errors.append(f"percorso assoluto vietato: {path.relative_to(ROOT)}")
            for reference in broken_local_references(path):
                errors.append(f"asset locale mancante in {path.relative_to(ROOT)}: {reference}")
            if suffix == ".svg":
                try:
                    ET.parse(path)
                except ET.ParseError as exc:
                    errors.append(f"template SVG non valido {path.relative_to(ROOT)}: {exc}")

    shared_css = ROOT / "templates/shared/brand.css"
    if shared_css.is_file():
        for reference in broken_local_references(shared_css):
            errors.append(f"asset locale mancante in templates/shared/brand.css: {reference}")

    policy_path = ROOT / "tokens/video-readability.json"
    if policy_path.is_file():
        try:
            policy = load_video_readability_policy(policy_path)
            errors.extend(verify_story_reel_template_geometry(ROOT, policy))
        except ValueError:
            pass

    return errors


if __name__ == "__main__":
    failures = verify()
    if failures:
        print("ARPHE GRAPHIC KIT: FAIL")
        for failure in failures:
            print(f"- {failure}")
        sys.exit(1)
    print("ARPHE GRAPHIC KIT: PASS")
