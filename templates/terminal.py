"""terminal template — dark cyberpunk terminal aesthetic.

Matches the HexFoc-Xp profile README style:
  • dark background with subtle dot grid
  • monospace typography
  • yellow accent stripe on left
  • fake terminal chrome (traffic lights + titlebar)
  • tag badge top-right
"""
from html import escape

BG, BG2, LINE = "#0b0d10", "#11151b", "#1d232c"
TXT, DIM, MUTE = "#d7dde5", "#7b8594", "#4a5361"
YEL, BLU, GRN, RED, VIO = "#ffd23f", "#4c9aff", "#5cff9d", "#ff5c6c", "#b28cff"
MONO = ("ui-monospace,'JetBrains Mono','Fira Code','Cascadia Code',SFMono-Regular,"
        "Menlo,Consolas,'Liberation Mono',monospace")


def render(
    *,
    title: str,
    subtitle: str = "",
    author: str = "HexFoc-Xp",
    date: str = "",
    tag: str = "",
    accent: str | None = None,
    width: int = 1200,
    height: int = 630,
) -> str:
    """Render terminal-style OG image SVG."""
    acc = accent or YEL
    title_esc = escape(title)
    sub_esc = escape(subtitle)
    tag_esc = escape(tag.upper()) if tag else ""
    date_esc = escape(date)

    # Tag color by category
    tag_color = {"kernel": GRN, "security": RED, "android": YEL, "backend": BLU,
                 "ai": VIO, "tutorial": BLU}.get(tag.lower(), acc)

    # Truncate title if very long (visual heuristic)
    max_chars = 70
    if len(title) > max_chars:
        title_esc = escape(title[:max_chars - 1]) + "…"

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<defs>
  <pattern id="dots" width="20" height="20" patternUnits="userSpaceOnUse">
    <circle cx="1" cy="1" r="1" fill="{LINE}"/>
  </pattern>
  <linearGradient id="scanG" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{acc}" stop-opacity="0"/>
    <stop offset=".5" stop-color="{acc}" stop-opacity=".05"/>
    <stop offset="1" stop-color="{acc}" stop-opacity="0"/>
  </linearGradient>
</defs>
<rect width="{width}" height="{height}" fill="{BG}"/>
<rect width="{width}" height="{height}" fill="url(#dots)"/>

<!-- accent stripe (left) -->
<rect x="0" y="0" width="8" height="{height}" fill="{acc}"/>

<!-- terminal title bar -->
<rect x="40" y="40" width="{width-80}" height="48" rx="8" fill="{BG2}" stroke="{LINE}"/>
<circle cx="65" cy="64" r="6" fill="{RED}" opacity=".85"/>
<circle cx="85" cy="64" r="6" fill="{YEL}" opacity=".85"/>
<circle cx="105" cy="64" r="6" fill="{GRN}" opacity=".85"/>
<text x="{width//2}" y="69" text-anchor="middle" font-family="{MONO}" font-size="14" fill="{MUTE}">~/hexfoc-xp/blog — bash — 1200×630</text>

<!-- prompt + tag row -->
<text x="60" y="180" font-family="{MONO}" font-size="20" fill="{GRN}">magic@hexos</text>
<text x="220" y="180" font-family="{MONO}" font-size="20" fill="{MUTE}">:</text>
<text x="232" y="180" font-family="{MONO}" font-size="20" fill="{BLU}">~/posts</text>
<text x="320" y="180" font-family="{MONO}" font-size="20" fill="{MUTE}">$</text>
<text x="348" y="180" font-family="{MONO}" font-size="20" fill="{TXT}">cat post.md</text>

<!-- tag badge (top right) -->
<g transform="translate({width-220}, 145)">
  <rect width="170" height="34" rx="6" fill="{BG2}" stroke="{tag_color}" stroke-width="1.5"/>
  <circle cx="20" cy="17" r="4" fill="{tag_color}"/>
  <text x="38" y="22" font-family="{MONO}" font-size="13" font-weight="700" fill="{tag_color}">#{tag_esc}</text>
</g>

<!-- title (large, wrapped) -->
<text x="60" y="280" font-family="{MONO}" font-size="44" font-weight="800" fill="{TXT}">{title_esc}</text>

<!-- subtitle -->
<text x="60" y="340" font-family="{MONO}" font-size="20" fill="{DIM}">{sub_esc}</text>

<!-- divider line -->
<line x1="60" y1="430" x2="{width-60}" y2="430" stroke="{LINE}" stroke-dasharray="4 6"/>

<!-- metadata footer -->
<text x="60" y="490" font-family="{MONO}" font-size="16" fill="{MUTE}">// author</text>
<text x="60" y="520" font-family="{MONO}" font-size="22" font-weight="700" fill="{acc}">{escape(author)}</text>

<text x="60" y="555" font-family="{MONO}" font-size="14" fill="{DIM}">📅 {date_esc if date_esc else 'recently'}</text>
<text x="200" y="555" font-family="{MONO}" font-size="14" fill="{DIM}">·</text>
<text x="220" y="555" font-family="{MONO}" font-size="14" fill="{DIM}">☕ 5 min read</text>

<!-- blink cursor (static in PNG, but conceptually alive) -->
<rect x="{width-100}" y="495" width="14" height="32" fill="{acc}"/>

<!-- scanline overlay -->
<rect x="0" y="0" width="{width}" height="{height}" fill="url(#scanG)" opacity=".5"/>

<!-- border -->
<rect x=".5" y=".5" width="{width-1}" height="{height-1}" fill="none" stroke="{LINE}"/>
</svg>"""
