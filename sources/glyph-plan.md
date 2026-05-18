# Glyph Plan

Priority glyph set:
- `I`, `l`, `1`
- `O`, `0`
- `{`, `}`, `[`, `]`, `(`, `)`
- `<`, `>`, `=`, `-`, `+`, `*`, `/`, `\`, `|`
- `_`, `~`, `^`, `#`, `@`, `$`, `%`, `&`
- quotes, backtick, punctuation

Design rules:
- one advance width for all glyphs
- keep `I` narrow but readable
- make `l` distinct from `I` by terminal shape
- give `1` foot or flag, not full serif overload
- make `0` visibly different from `O`
- make braces and brackets balanced and sturdy
- keep operators crisp at low size

Flavor target:
- soft industrial feel
- chunky but not cartoonish
- slightly rounded corners
- coding-first over display-first

Construction order:
1. set metrics
2. draw control set
3. draw uppercase
4. draw lowercase
5. draw punctuation and symbols
6. test in editor
7. add ligatures only after basic readability passes

