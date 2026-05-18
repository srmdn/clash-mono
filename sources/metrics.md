# Metrics

Draft metrics for first draw pass:

- unitsPerEm: `1000`
- ascender: `800`
- descender: `-200`
- capHeight: `700`
- xHeight: `500`
- baseline: `0`
- monospaced advance width: `600`

Optical rules:
- lowercase should feel centered in the cell
- caps should not crowd top line
- descenders should stay inside safe terminal range
- overshoot on round glyphs should be small and consistent

Spacing targets:
- `I`, `l`, `1`: same advance width as all glyphs
- round glyphs: optically centered, not mathematically centered
- punctuation: compact, but never clipped

