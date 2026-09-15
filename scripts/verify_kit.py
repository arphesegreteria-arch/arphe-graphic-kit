#!/usr/bin/env python3
"""Verify that the public ARPHE graphic kit is complete and portable."""

from __future__ import annotations

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
        "tokens/colors.txt", "logos/svg/arphe-logo-ink.svg",
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

    return errors


if __name__ == "__main__":
    failures = verify()
    if failures:
        print("ARPHE GRAPHIC KIT: FAIL")
        for failure in failures:
            print(f"- {failure}")
        sys.exit(1)
    print("ARPHE GRAPHIC KIT: PASS")
