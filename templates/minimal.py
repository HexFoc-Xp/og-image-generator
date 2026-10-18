"""minimal template — clean white aesthetic with lots of whitespace.

Modern, professional, suitable for:
  • tech blog posts
  • corporate announcements
  • academic papers
"""
from html import escape

BG = "#fafbfc"
TXT, DIM, MUTE = "#0b0d10", "#4a5361", "#7b8594"
SANS = "Inter, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif"
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
    """Render minimal-style OG image SVG."""
    acc = accent or "#4c9aff"
    title_esc = escape(title)
    sub_esc = escape(subtitle)
    tag_esc = escape(tag.upper()) if tag else ""
    date_esc = escape(date)

    # Title font-size scales with title length
    if len(title) <= 40:
        title_fs = 56
    elif len(title) <= 70:
        title_fs = 44
    else:
        title_esc = escape(title[:80] + "…")
        title_fs = 38

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<defs>
  <linearGradient id="bgG" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{BG}"/>
    <stop offset="1" stop-color="#f0f3f7"/>
  </linearGradient>
</defs>
<rect width="{width}" height="{height}" fill="url(#bgG)"/>

<!-- top accent line -->
<rect x="0" y="0" width="{width}" height="6" fill="{acc}"/>

<!-- tag badge top-right -->
<g transform="translate({width-220}, 70)">
  <rect width="170" height="36" rx="18" fill="{acc}" opacity=".12"/>
  <circle cx="22" cy="18" r="4" fill="{acc}"/>
  <text x="40" y="23" font-family="{MONO}" font-size="13" font-weight="700" fill="{acc}">#{tag_esc}</text>
</g>

<!-- HexFoc-Xp wordmark top-left -->
<text x="80" y="100" font-family="{MONO}" font-size="14" font-weight="700" fill="{MUTE}" letter-spacing="2">HEXFOC-XP</text>
<circle cx="220" cy="95" r="4" fill="{acc}"/>

<!-- title -->
<text x="80" y="280" font-family="{SANS}" font-size="{title_fs}" font-weight="800" fill="{TXT}">{title_esc}</text>

<!-- subtitle -->
<text x="80" y="350" font-family="{SANS}" font-size="22" fill="{DIM}">{sub_esc}</text>

<!-- divider -->
<line x1="80" y1="450" x2="160" y2="450" stroke="{acc}" stroke-width="3"/>

<!-- footer metadata -->
<text x="80" y="510" font-family="{SANS}" font-size="18" font-weight="700" fill="{TXT}">{escape(author)}</text>
<text x="80" y="540" font-family="{SANS}" font-size="15" fill="{MUTE}">{date_esc if date_esc else 'Recently published'} · 5 min read</text>

<!-- right-side wordmark large -->
<text x="{width-80}" y="600" text-anchor="end" font-family="{SANS}" font-size="14" font-weight="700" fill="{MUTE}" letter-spacing="3">SUBURDEV.MY.IS-BEST.NET</text>

<!-- subtle dot pattern bottom-right -->
<g opacity=".4">
  <circle cx="{width-60}" cy="100" r="2" fill="{MUTE}"/>
  <circle cx="{width-80}" cy="100" r="2" fill="{MUTE}"/>
  <circle cx="{width-100}" cy="100" r="2" fill="{MUTE}"/>
  <circle cx="{width-60}" cy="120" r="2" fill="{MUTE}"/>
  <circle cx="{width-80}" cy="120" r="2" fill="{MUTE}"/>
  <circle cx="{width-60}" cy="140" r="2" fill="{MUTE}"/>
</g>

<rect x=".5" y=".5" width="{width-1}" height="{height-1}" fill="none" stroke="#e1e5eb"/>
</svg>"""
