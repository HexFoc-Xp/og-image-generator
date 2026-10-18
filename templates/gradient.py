"""gradient template — vibrant gradient bg with glassmorphism card.

Modern startup-style OG image. Suitable for:
  • product launches
  • announcements
  • portfolio highlights
"""
from html import escape

BG = "#0b0d10"
TXT, DIM, MUTE = "#ffffff", "#d7dde5", "#7b8594"
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
    """Render gradient-style OG image SVG."""
    acc = accent or "#b28cff"
    title_esc = escape(title)
    sub_esc = escape(subtitle)
    tag_esc = escape(tag.upper()) if tag else ""
    date_esc = escape(date)

    # Title font-size scales with length
    if len(title) <= 40:
        title_fs = 52
    elif len(title) <= 70:
        title_fs = 40
    else:
        title_esc = escape(title[:80] + "…")
        title_fs = 36

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<defs>
  <linearGradient id="bgG" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#1a1f3a"/>
    <stop offset=".5" stop-color="#2d1b4e"/>
    <stop offset="1" stop-color="#0b0d10"/>
  </linearGradient>
  <radialGradient id="glow1" cx=".2" cy=".3" r=".5">
    <stop offset="0" stop-color="{acc}" stop-opacity=".4"/>
    <stop offset="1" stop-color="{acc}" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="glow2" cx=".9" cy=".8" r=".5">
    <stop offset="0" stop-color="#4c9aff" stop-opacity=".3"/>
    <stop offset="1" stop-color="#4c9aff" stop-opacity="0"/>
  </radialGradient>
  <filter id="blur1"><feGaussianBlur stdDeviation="40"/></filter>
</defs>

<!-- background -->
<rect width="{width}" height="{height}" fill="url(#bgG)"/>
<rect width="{width}" height="{height}" fill="url(#glow1)"/>
<rect width="{width}" height="{height}" fill="url(#glow2)"/>

<!-- floating gradient orbs (decorative) -->
<circle cx="100" cy="100" r="80" fill="{acc}" opacity=".15" filter="url(#blur1)"/>
<circle cx="{width-150}" cy="{height-100}" r="120" fill="#4c9aff" opacity=".15" filter="url(#blur1)"/>
<circle cx="{width-200}" cy="80" r="60" fill="#ff5c6c" opacity=".12" filter="url(#blur1)"/>

<!-- glassmorphism card -->
<rect x="60" y="60" width="{width-120}" height="{height-120}" rx="20"
      fill="#ffffff" opacity=".04" stroke="#ffffff" stroke-width="1" stroke-opacity=".15"/>

<!-- tag badge top-left -->
<g transform="translate(100, 110)">
  <rect width="180" height="40" rx="20" fill="{acc}" opacity=".25" stroke="{acc}" stroke-width="1" stroke-opacity=".5"/>
  <circle cx="24" cy="20" r="5" fill="{acc}"/>
  <text x="44" y="26" font-family="{MONO}" font-size="14" font-weight="700" fill="{TXT}">#{tag_esc}</text>
</g>

<!-- wordmark top-right -->
<text x="{width-100}" y="135" text-anchor="end" font-family="{MONO}" font-size="14" font-weight="700"
      fill="{MUTE}" letter-spacing="3">HEXFOC-XP</text>

<!-- title (large, bold, white) -->
<text x="100" y="300" font-family="{SANS}" font-size="{title_fs}" font-weight="800" fill="{TXT}">{title_esc}</text>

<!-- subtitle -->
<text x="100" y="370" font-family="{SANS}" font-size="22" fill="{DIM}">{sub_esc}</text>

<!-- divider -->
<line x1="100" y1="430" x2="180" y2="430" stroke="{acc}" stroke-width="3"/>

<!-- footer metadata -->
<g transform="translate(100, 470)">
  <circle cx="20" cy="20" r="20" fill="{acc}" opacity=".2"/>
  <text x="20" y="26" text-anchor="middle" font-family="{SANS}" font-size="16" font-weight="800" fill="{acc}">H</text>
  <text x="60" y="20" font-family="{SANS}" font-size="18" font-weight="700" fill="{TXT}">{escape(author)}</text>
  <text x="60" y="44" font-family="{SANS}" font-size="14" fill="{MUTE}">{date_esc if date_esc else 'Recently'} · 5 min read</text>
</g>

<!-- decorative grid pattern (bottom right) -->
<g opacity=".15" transform="translate({width-260}, 460)">
  <line x1="0" y1="0" x2="200" y2="0" stroke="#ffffff" stroke-width=".5"/>
  <line x1="0" y1="40" x2="200" y2="40" stroke="#ffffff" stroke-width=".5"/>
  <line x1="0" y1="80" x2="200" y2="80" stroke="#ffffff" stroke-width=".5"/>
  <line x1="0" y1="0" x2="0" y2="80" stroke="#ffffff" stroke-width=".5"/>
  <line x1="100" y1="0" x2="100" y2="80" stroke="#ffffff" stroke-width=".5"/>
  <line x1="200" y1="0" x2="200" y2="80" stroke="#ffffff" stroke-width=".5"/>
</g>

<rect x=".5" y=".5" width="{width-1}" height="{height-1}" fill="none" stroke="#1d232c"/>
</svg>"""
