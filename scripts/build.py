#!/usr/bin/env python3
from __future__ import annotations

import os
import shutil
import subprocess
import sys
import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DESIGNSPACE_PATH = ROOT / "sources" / "ClashMono.designspace"
BUILD_DIR = ROOT / "build"
DIST_DIR = ROOT / "dist"


def run(cmd: list[str]) -> None:
    print("+ " + " ".join(cmd), flush=True)
    subprocess.run(cmd, check=True)


def main() -> int:
    run([sys.executable, str(ROOT / "scripts" / "check.py")])

    fontmake = os.environ.get("FONTMAKE")
    if fontmake:
        fontmake_cmd = [fontmake]
    elif importlib.util.find_spec("fontmake") is not None:
        fontmake_cmd = [sys.executable, "-m", "fontmake"]
    elif shutil.which("fontmake") is not None:
        fontmake_cmd = ["fontmake"]
    else:
        print(
            "build: missing fontmake. Install deps with `pip install -r requirements.txt`.",
            file=sys.stderr,
        )
        return 1

    ttf_dir = BUILD_DIR / "ttf"
    otf_dir = BUILD_DIR / "otf"
    for path in (BUILD_DIR, DIST_DIR, ttf_dir, otf_dir):
        path.mkdir(parents=True, exist_ok=True)

    run(
        [
            *fontmake_cmd,
            "-m",
            str(DESIGNSPACE_PATH),
            "-o",
            "ttf",
            "--output-dir",
            str(ttf_dir),
        ]
    )
    run(
        [
            *fontmake_cmd,
            "-m",
            str(DESIGNSPACE_PATH),
            "-o",
            "otf",
            "--output-dir",
            str(otf_dir),
        ]
    )

    built: list[Path] = []
    for directory in (ttf_dir, otf_dir):
        for path in sorted(directory.glob("*")):
            if path.suffix.lower() not in {".ttf", ".otf"}:
                continue
            target = DIST_DIR / path.name
            shutil.copy2(path, target)
            built.append(target)

    if not built:
        print("build: no font binaries produced", file=sys.stderr)
        return 1

    print("build: ok")
    for path in built:
        print(f"build: {path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
