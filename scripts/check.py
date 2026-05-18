#!/usr/bin/env python3
from __future__ import annotations

import plistlib
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "sources"
MASTER_DIR = SOURCE_DIR / "masters" / "Regular.ufo"
GLYPH_DIR = MASTER_DIR / "glyphs"
CONTENTS_PATH = GLYPH_DIR / "contents.plist"
FONTINFO_PATH = MASTER_DIR / "fontinfo.plist"
LIB_PATH = MASTER_DIR / "lib.plist"
GLYPH_ORDER_PATH = SOURCE_DIR / "glyph-order.txt"
DESIGNSPACE_PATH = SOURCE_DIR / "ClashMono.designspace"
CELL_WIDTH = 600


def fail(errors: list[str]) -> int:
    for error in errors:
        print(f"check: {error}", file=sys.stderr)
    return 1


def check_exists(errors: list[str], path: Path, label: str) -> None:
    if not path.exists():
        errors.append(f"missing {label}: {path}")


def parse_plist(path: Path):
    with path.open("rb") as handle:
        return plistlib.load(handle)


def parse_text_lines(path: Path) -> list[str]:
    lines: list[str] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        lines.append(line)
    return lines


def check_designspace(errors: list[str]) -> None:
    try:
        root = ET.parse(DESIGNSPACE_PATH).getroot()
    except Exception as exc:  # pragma: no cover - structural check
        errors.append(f"cannot parse designspace: {exc}")
        return

    if root.tag != "designspace":
        errors.append(f"unexpected designspace root tag: {root.tag}")

    sources = root.findall("./sources/source")
    if not sources:
        errors.append("designspace has no sources")
        return

    for source in sources:
        filename = source.get("filename")
        if not filename:
            errors.append("designspace source missing filename")
            continue
        source_path = DESIGNSPACE_PATH.parent / filename
        if not source_path.exists():
            errors.append(f"designspace source missing: {source_path}")


def check_fontinfo(errors: list[str]) -> None:
    try:
        fontinfo = parse_plist(FONTINFO_PATH)
    except Exception as exc:  # pragma: no cover - structural check
        errors.append(f"cannot parse fontinfo: {exc}")
        return

    for key in ("familyName", "styleName", "unitsPerEm", "ascender", "descender"):
        if key not in fontinfo:
            errors.append(f"fontinfo missing key: {key}")

    if fontinfo.get("familyName") != "Clash Mono":
        errors.append("fontinfo familyName must be Clash Mono")
    if fontinfo.get("styleName") != "Regular":
        errors.append("fontinfo styleName must be Regular")
    if fontinfo.get("unitsPerEm") != 1000:
        errors.append("fontinfo unitsPerEm must be 1000")


def check_glyph_order(errors: list[str]) -> None:
    try:
        order = parse_text_lines(GLYPH_ORDER_PATH)
    except Exception as exc:  # pragma: no cover - structural check
        errors.append(f"cannot read glyph order: {exc}")
        return

    try:
        lib = parse_plist(LIB_PATH)
    except Exception as exc:  # pragma: no cover - structural check
        errors.append(f"cannot parse lib.plist: {exc}")
        return

    public_order = lib.get("public.glyphOrder")
    if not isinstance(public_order, list):
        errors.append("lib.plist missing public.glyphOrder")
        return

    if public_order != order:
        errors.append("public.glyphOrder does not match sources/glyph-order.txt")


def check_glyphs(errors: list[str]) -> None:
    try:
        contents = parse_plist(CONTENTS_PATH)
    except Exception as exc:  # pragma: no cover - structural check
        errors.append(f"cannot parse contents.plist: {exc}")
        return

    if not isinstance(contents, dict):
        errors.append("contents.plist is not a dictionary")
        return

    for glyph_name, rel_path in contents.items():
        if not isinstance(glyph_name, str):
            errors.append(f"non-string glyph name in contents: {glyph_name!r}")
            continue
        if not isinstance(rel_path, str):
            errors.append(f"non-string glyph path for {glyph_name}: {rel_path!r}")
            continue
        glyph_path = GLYPH_DIR / rel_path
        if not glyph_path.exists():
            errors.append(f"missing glyph file for {glyph_name}: {glyph_path}")
            continue
        try:
            tree = ET.parse(glyph_path)
        except Exception as exc:  # pragma: no cover - structural check
            errors.append(f"cannot parse glyph {glyph_name}: {exc}")
            continue

        advance = tree.find("./advance")
        if advance is None:
            errors.append(f"glyph missing advance width: {glyph_name}")
            continue

        width = advance.get("width")
        if width is None:
            errors.append(f"glyph missing advance width value: {glyph_name}")
            continue
        try:
            advance_width = int(width)
        except ValueError:
            errors.append(f"glyph has invalid advance width {width!r}: {glyph_name}")
            continue
        if advance_width != CELL_WIDTH:
            errors.append(
                f"glyph width must be {CELL_WIDTH}: {glyph_name} has {advance_width}"
            )

        parts = Path(rel_path).parts
        stem = Path(rel_path).stem
        if parts and parts[0] == "lower" and any(ch.isupper() for ch in stem):
            errors.append(f"uppercase glyph leaked into lower/: {rel_path}")
        if parts and parts[0] == "upper" and any(ch.islower() for ch in stem):
            errors.append(f"lowercase glyph leaked into upper/: {rel_path}")

    for required in ("core/.notdef.glif", "core/space.glif"):
        if required not in contents.values():
            errors.append(f"missing required glyph mapping: {required}")


def main() -> int:
    errors: list[str] = []

    for path, label in (
        (DESIGNSPACE_PATH, "designspace"),
        (FONTINFO_PATH, "fontinfo"),
        (LIB_PATH, "lib.plist"),
        (CONTENTS_PATH, "glyph contents"),
        (GLYPH_ORDER_PATH, "glyph order"),
    ):
        check_exists(errors, path, label)

    if errors:
        return fail(errors)

    check_designspace(errors)
    check_fontinfo(errors)
    check_glyph_order(errors)
    check_glyphs(errors)

    if errors:
        return fail(errors)

    print("check: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
