# Spacing

General spacing policy:
- one cell width for all glyphs
- sidebearings tuned by optical balance, not raw symmetry
- avoid collision in dense symbol runs
- preserve readability at small terminal sizes

Suggested starting points:
- cell width: `600`
- left/right sidebearing: `60` to `90` depending on glyph shape
- punctuation can be narrower visually, but advance stays fixed

Adjustment order:
1. set control glyph widths
2. verify `I/l/1`
3. verify `O/0`
4. verify brackets and braces
5. verify symbol runs like `==`, `!=`, `<=`, `>=`

