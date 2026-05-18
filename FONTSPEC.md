# Font Spec

Working target:
- clean-room monospace coding font
- CoC-inspired mood only
- no proprietary outline reuse
- open-source redistribution safe

Base direction:
- draw from open-source coding font metrics and proportions
- use `Iosevka` as engineering reference
- keep final outlines original

v1 glyph scope:
- ASCII letters `A-Z`, `a-z`
- digits `0-9`
- punctuation and coding symbols
- arrows and common operators
- later: extended Latin, ligatures, emoji fallback policy

Shape rules:
- monospaced advance width everywhere
- clear `I/l/1` separation
- clear `O/0` separation
- sturdy braces, brackets, parens
- terminal-friendly at small sizes

Style notes:
- softer, rounder, stout forms
- readable counters
- restrained flair, no game-art ornament
- flavor from proportions and terminals, not tracing

Build target:
- source in `sources/`
- generated intermediates in `build/`
- releases in `dist/`

