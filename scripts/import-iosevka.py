#!/usr/bin/env python3
"""Import Iosevka curved glyphs into Clash Mono UFO source.
Handles composite glyphs by following component references.
"""
from __future__ import annotations

import xml.etree.ElementTree as ET
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen, DecomposingRecordingPen

ROOT = Path(__file__).resolve().parents[1]
GLYPH_DIR = ROOT / "sources" / "masters" / "Regular.ufo" / "glyphs"
ET.register_namespace("", "http://www.w3.org/2000/svg")

CAP_CLASH = 700
CAP_IOSEVKA = 735
CELL_CLASH = 600
SCALE = CAP_CLASH / CAP_IOSEVKA


def draw_decomposed(font, glyph_name):
    """Draw a glyph fully decomposed to moveTo/lineTo/qCurveTo/curveTo."""
    glyf = font['glyf']
    glyph = glyf[glyph_name]
    if glyph.numberOfContours > 0:
        # Simple glyph - draw directly
        pen = RecordingPen()
        glyph.draw(pen, glyf)
        return pen.value
    elif glyph.numberOfContours < 0:
        # Composite - follow first component (Iosevka uses identity transforms)
        comp = glyph.components[0]
        return draw_decomposed(font, comp.glyphName)
    else:
        return []


def convert_to_cubic(pen_ops):
    contours = []
    current = []
    lon_x, lon_y = 0, 0
    
    for op, pts in pen_ops:
        if op == "moveTo":
            if current:
                contours.append(current)
            current = []
            x, y = pts[0]
            current.append((int(x), int(y), "move"))
            lon_x, lon_y = x, y
        elif op == "lineTo":
            x, y = pts[0]
            current.append((int(x), int(y), "line"))
            lon_x, lon_y = x, y
        elif op == "qCurveTo":
            for i in range(len(pts) - 1):
                cp_x, cp_y = pts[i]
                next_x, next_y = pts[i + 1]
                if i < len(pts) - 2:
                    end_x = (cp_x + next_x) / 2
                    end_y = (cp_y + next_y) / 2
                else:
                    end_x, end_y = next_x, next_y
                
                cp1_x = lon_x + 2/3 * (cp_x - lon_x)
                cp1_y = lon_y + 2/3 * (cp_y - lon_y)
                cp2_x = end_x + 2/3 * (cp_x - end_x)
                cp2_y = end_y + 2/3 * (cp_y - end_y)
                
                current.append((int(cp1_x), int(cp1_y), "offcurve"))
                current.append((int(cp2_x), int(cp2_y), "offcurve"))
                current.append((int(end_x), int(end_y), "curve"))
                lon_x, lon_y = end_x, end_y
        elif op == "curveTo":
            p1x, p1y = pts[0]; p2x, p2y = pts[1]; p3x, p3y = pts[2]
            current.append((int(p1x), int(p1y), "offcurve"))
            current.append((int(p2x), int(p2y), "offcurve"))
            current.append((int(p3x), int(p3y), "curve"))
            lon_x, lon_y = p3x, p3y
        elif op in ("closePath", "endPath"):
            if current:
                contours.append(current)
            current = []
    
    if current:
        contours.append(current)
    return contours


def transform(contours, scale, dx, dy):
    result = []
    for c in contours:
        nc = []
        for x, y, t in c:
            nc.append((int(x * scale + dx), int(y * scale + dy), t))
        result.append(nc)
    return result


def to_xml(contours):
    el = ET.Element("outline")
    for c in contours:
        ce = ET.SubElement(el, "contour")
        for x, y, t in c:
            attrs = {"x": str(x), "y": str(y)}
            if t != "offcurve":
                attrs["type"] = t
            ET.SubElement(ce, "point", attrs)
    return el


def update(path, contours):
    tree = ET.parse(path)
    root = tree.getroot()
    old = root.find("./outline")
    if old is not None:
        root.remove(old)
    root.append(to_xml(contours))
    ET.indent(tree, space="  ")
    tree.write(path, encoding="UTF-8", xml_declaration=True)


IMPORT_MAP = [
    ("O", "upper", "O"), ("C", "upper", "C"), ("G", "upper", "G"),
    ("Q", "upper", "Q"), ("S", "upper", "S"), ("B", "upper", "B"),
    ("D", "upper", "D"), ("P", "upper", "P"), ("R", "upper", "R"),
    ("zero", "core", "0"), ("two", "core", "2"), ("three", "core", "3"),
    ("five", "core", "5"), ("six", "core", "6"), ("eight", "core", "8"),
    ("nine", "core", "9"),
    ("a", "lower", "a"), ("c", "lower", "c"), ("e", "lower", "e"),
    ("g", "lower", "g"), ("o", "lower", "o"), ("s", "lower", "s"),
    ("at", "core", "@"), ("ampersand", "core", "&"),
]


def main():
    font = TTFont('/tmp/iosevka.woff2')
    cmap = font.getBestCmap()
    
    for our_name, subdir, ch in IMPORT_MAP:
        code = ord(ch)
        gname = cmap.get(code)
        if not gname:
            print(f"SKIP {our_name}: '{ch}' not in font")
            continue
        
        ops = draw_decomposed(font, gname)
        if not ops:
            print(f"SKIP {our_name}: no outline data")
            continue
        
        contours = convert_to_cubic(ops)
        
        all_x = []
        for c in contours:
            for x, y, t in c:
                if t != "offcurve":
                    all_x.append(x)
        if not all_x:
            print(f"SKIP {our_name}: no on-curve points")
            continue
        
        gx_min, gx_max = min(all_x), max(all_x)
        sw = (gx_max - gx_min) * SCALE
        dx = (CELL_CLASH - sw) / 2 - gx_min * SCALE
        
        transformed = transform(contours, SCALE, dx, 0)
        
        glif_path = GLYPH_DIR / subdir / f"{our_name}.glif"
        if not glif_path.exists():
            print(f"SKIP {our_name}: {glif_path} not found")
            continue
        
        update(glif_path, transformed)
        print(f"OK: {our_name} ({ch}) → {subdir}/{our_name}.glif [{len(transformed)}c]")
    
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
