#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys

from fontTools.ttLib import TTFont


ROOT = Path(__file__).resolve().parents[1]
DIST_DIR = ROOT / "dist"
SPECIMEN_PATH = DIST_DIR / "specimen.html"


def find_font() -> Path | None:
    for candidate in sorted(DIST_DIR.glob("*.ttf")) + sorted(DIST_DIR.glob("*.otf")):
        return candidate
    return None


def main() -> int:
    font_path = find_font()
    if font_path is None:
        print("smoke: missing built font in dist/. Run `make build` first.", file=sys.stderr)
        return 1

    if not SPECIMEN_PATH.exists():
        print("smoke: missing specimen.html. Run `make specimen` first.", file=sys.stderr)
        return 1

    specimen = SPECIMEN_PATH.read_text(encoding="utf-8")
    if "<html" not in specimen or "</html>" not in specimen:
        print("smoke: specimen.html does not look like HTML", file=sys.stderr)
        return 1
    if font_path.name not in specimen:
        print("smoke: specimen.html does not reference built font", file=sys.stderr)
        return 1

    font = TTFont(str(font_path))
    cmap = font.getBestCmap() or {}
    head = font["head"]
    hhea = font["hhea"]
    os2 = font["OS/2"]

    required = {
        0x0049: "I",
        0x006C: "l",
        0x0031: "one",
        0x004F: "O",
        0x0030: "zero",
    }
    missing = [name for code, name in required.items() if code not in cmap]
    if missing:
        print(f"smoke: missing cmap entries: {', '.join(missing)}", file=sys.stderr)
        return 1

    print(f"smoke: font {font_path.name}")
    print(f"smoke: unitsPerEm {head.unitsPerEm}")
    print(f"smoke: ascender {hhea.ascent}")
    print(f"smoke: descender {hhea.descent}")
    print(f"smoke: glyphs {len(font.getGlyphOrder())}")
    print(f"smoke: specimen {SPECIMEN_PATH.relative_to(ROOT)}")
    print("smoke: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
