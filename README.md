# clash-mono

Clean-room monospace coding font inspired by Clash of Clans UI flavor.

Goal:
- same energy, no proprietary asset reuse
- coding-first, editor-safe, redistribution-safe
- open source under `OFL-1.1`

Hard rules:
- no import of `Supercell-Magic_5.ttf`
- no trace, edit, or reuse of Supercell outlines
- use only open-source or self-drawn source material

Planned structure:
- `sources/` font source files
- `scripts/` build helpers
- `build/` generated intermediates
- `dist/` release binaries

Initial scope:
- ASCII letters, digits, punctuation
- core coding symbols
- later: ligatures, extended Latin, hinting, specimen

Status:
- source tree scaffolded
- partial glyph set in place
- build wiring added

Build:
- `make check` validates UFO structure and glyph map
- `make build` runs `fontmake` when installed and copies binaries to `dist/`
- `make specimen` writes `dist/specimen.html` after a successful build
- install deps with `pip install -r requirements.txt` in your own env
