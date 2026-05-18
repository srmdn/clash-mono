#!/usr/bin/env python3
from __future__ import annotations

from html import escape
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
DIST_DIR = ROOT / "dist"
OUTPUT_PATH = DIST_DIR / "specimen.html"


SAMPLES = [
    ("Core", "I l 1 O 0 [] {} () <> = - + * / \\ | _ ~ ^ # @ $ % &"),
    ("Quotes", '\' " ` single double backtick'),
    ("Punctuation", "! ? : ; , ."),
    ("Digits", "0123456789"),
    (
        "Code",
        "const value = items[0] + items[1];\nif (value >= 10) {\n  console.log(`ok: ${value}`);\n}",
    ),
]


def find_font() -> Path | None:
    for candidate in sorted(DIST_DIR.glob("*.ttf")) + sorted(DIST_DIR.glob("*.otf")):
        return candidate
    return None


def render(font_name: str) -> str:
    blocks = []
    for title, sample in SAMPLES:
        blocks.append(
            f"""
      <section class="card">
        <div class="label">{escape(title)}</div>
        <pre>{escape(sample)}</pre>
      </section>
            """.strip()
        )

    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Clash Mono Specimen</title>
    <style>
      @font-face {{
        font-family: "Clash Mono";
        src: url("./{escape(font_name)}");
      }}

      :root {{
        color-scheme: dark;
        --bg: #0f1115;
        --panel: #171b22;
        --panel-soft: #1e2430;
        --text: #eff3f8;
        --muted: #a8b2c0;
        --accent: #7ad4ff;
        --accent-2: #8bf5c8;
      }}

      * {{
        box-sizing: border-box;
      }}

      body {{
        margin: 0;
        min-height: 100vh;
        font-family: "Clash Mono", monospace;
        background:
          radial-gradient(circle at top left, rgba(122, 212, 255, 0.18), transparent 34%),
          radial-gradient(circle at top right, rgba(139, 245, 200, 0.14), transparent 28%),
          var(--bg);
        color: var(--text);
      }}

      main {{
        max-width: 1080px;
        margin: 0 auto;
        padding: 48px 24px 72px;
      }}

      h1 {{
        margin: 0 0 10px;
        font-size: clamp(40px, 7vw, 78px);
        line-height: 0.92;
        letter-spacing: -0.04em;
      }}

      .lede {{
        margin: 0 0 32px;
        max-width: 760px;
        color: var(--muted);
        font-size: 18px;
        line-height: 1.6;
      }}

      .grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
        gap: 16px;
      }}

      .card {{
        background: linear-gradient(180deg, rgba(255,255,255,0.04), transparent), var(--panel);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 18px;
        padding: 18px 18px 16px;
        box-shadow: 0 18px 60px rgba(0, 0, 0, 0.22);
      }}

      .label {{
        margin-bottom: 10px;
        color: var(--accent);
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 0.16em;
      }}

      pre {{
        margin: 0;
        white-space: pre-wrap;
        word-break: break-word;
        font-size: 18px;
        line-height: 1.55;
        color: var(--text);
      }}

      .footer {{
        margin-top: 18px;
        color: var(--muted);
        font-size: 13px;
      }}
    </style>
  </head>
  <body>
    <main>
      <h1>Clash Mono</h1>
      <p class="lede">
        Clean-room monospace coding font. This specimen is for small-size readability,
        symbol contrast, and code rhythm after build.
      </p>
      <section class="grid">
        {''.join(blocks)}
      </section>
      <p class="footer">
        Font file: {escape(font_name)}
      </p>
    </main>
  </body>
</html>
"""


def main() -> int:
    font = find_font()
    if font is None:
        print("specimen: missing built font in dist/. Run `make build` first.", file=sys.stderr)
        return 1

    DIST_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(render(font.name), encoding="utf-8")
    print(f"specimen: wrote {OUTPUT_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
