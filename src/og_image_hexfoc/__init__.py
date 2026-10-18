#!/usr/bin/env python3
"""
og-image-generator — Generate beautiful Open Graph (OG) images for your blog posts,
tutorials, and announcements.

Usage (CLI):
    python og_image.py \\
        --title   "Booting Linux on Android without root" \\
        --subtitle "A deep dive into User-Mode Linux on aarch64" \\
        --author  "HexFoc-Xp" \\
        --date    "Oct 2026" \\
        --tag     "kernel" \\
        --template terminal \\
        --output   examples/blog-post.png

Usage (library):
    from og_image import generate
    generate(title="...", subtitle="...", template="terminal", output="out.png")

Templates:
    terminal   — dark cyberpunk terminal (matches HexFoc-Xp profile aesthetic)
    minimal    — clean white/light, lots of whitespace, sans-serif
    gradient   — vibrant gradient background, glassmorphism card, modern

Author:    HexFoc-Xp
License:   MIT
"""
from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path
from typing import Optional

# ── package metadata ──────────────────────────────────────────────────────
__version__ = "0.1.1"
__author__ = "HexFoc-Xp"
__license__ = "MIT"

# ── palette (shared with HexFoc-Xp profile README) ─────────────────────────
BG, BG2, LINE = "#0b0d10", "#11151b", "#1d232c"
TXT, DIM, MUTE = "#d7dde5", "#7b8594", "#4a5361"
YEL, BLU, GRN, RED, VIO = "#ffd23f", "#4c9aff", "#5cff9d", "#ff5c6c", "#b28cff"
SAW = "#fa6f30"

MONO = ("ui-monospace,'JetBrains Mono','Fira Code','Cascadia Code',SFMono-Regular,"
        "Menlo,Consolas,'Liberation Mono',monospace")
SANS = "Inter, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif"

# OG image standard dimensions (recommended by Twitter/Facebook)
OG_W, OG_H = 1200, 630

# Templates ship inside the package (src/og_image_hexfoc/templates/)
TEMPLATE_DIR = Path(__file__).resolve().parent / "templates"

AVAILABLE_TEMPLATES = ["terminal", "minimal", "gradient"]


def _load_template_module(name: str):
    """Dynamically load a template module from templates/<name>.py."""
    path = TEMPLATE_DIR / f"{name}.py"
    if not path.exists():
        raise FileNotFoundError(
            f"Template '{name}' not found. Available: {AVAILABLE_TEMPLATES}"
        )
    spec = importlib.util.spec_from_file_location(
        f"og_image_hexfoc.templates.{name}", path
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def render_svg(svg: str, output: Path, width: int = OG_W, height: int = OG_H) -> None:
    """Render an SVG string to a PNG file.

    Renderer priority:
      1. cairosvg (default — works on ALL platforms including Termux/Android)
      2. playwright + chromium (optional high-quality fallback, desktop only)

    Set env var OG_IMAGE_RENDERER=playwright to force the playwright path,
    or OG_IMAGE_RENDERER=cairosvg to force cairosvg.
    """
    import os
    output.parent.mkdir(parents=True, exist_ok=True)
    output = output.resolve()

    forced = os.environ.get("OG_IMAGE_RENDERER", "").lower().strip()

    # Default path: cairosvg (always available, works everywhere)
    if forced != "playwright":
        try:
            import cairosvg
            cairosvg.svg2png(bytestring=svg.encode("utf-8"),
                             write_to=str(output),
                             output_width=width * 2,
                             output_height=height * 2)
            return
        except ImportError:
            if forced == "cairosvg":
                raise RuntimeError(
                    "OG_IMAGE_RENDERER=cairosvg was set, but cairosvg is not "
                    "installed. Run: pip install cairosvg"
                )
            # else: fall through to playwright

    # Optional high-quality path: playwright + chromium (desktop only)
    try:
        from playwright.sync_api import sync_playwright
        svg_path = output.with_suffix(".svg")
        svg_path.write_text(svg, encoding="utf-8")
        svg_url = svg_path.resolve().as_uri()
        html = (
            f"<!doctype html><html><head><meta charset='utf-8'>"
            f"<style>html,body{{margin:0;padding:0;background:transparent}}"
            f"img{{display:block;width:{width}px;height:{height}px}}</style>"
            f"</head><body><img src='{svg_url}' width='{width}' height='{height}'/></body></html>"
        )
        html_path = output.with_suffix(".preview.html")
        html_path.write_text(html, encoding="utf-8")
        with sync_playwright() as p:
            b = p.chromium.launch()
            pg = b.new_page(viewport={"width": width, "height": height}, device_scale_factor=2)
            pg.goto(html_path.resolve().as_uri())
            pg.wait_for_timeout(400)  # let fonts settle
            pg.screenshot(path=str(output), full_page=False, omit_background=False)
            b.close()
        # cleanup intermediate files
        svg_path.unlink(missing_ok=True)
        html_path.unlink(missing_ok=True)
        return
    except ImportError:
        pass

    raise RuntimeError(
        "No renderer available. Install one of:\n"
        "  pip install cairosvg               (default, works everywhere)\n"
        "  pip install og-image-hexfoc[playwright] && playwright install chromium\n"
        "    (higher quality, desktop only — does not work on Termux/Android)"
    )


def generate(
    *,
    title: str,
    subtitle: str = "",
    author: str = "HexFoc-Xp",
    date: str = "",
    tag: str = "",
    template: str = "terminal",
    output: Path | str = "og.png",
    accent: Optional[str] = None,
    width: int = OG_W,
    height: int = OG_H,
) -> Path:
    """Generate a single OG image. Returns the output Path."""
    if template not in AVAILABLE_TEMPLATES:
        raise ValueError(f"Unknown template '{template}'. Available: {AVAILABLE_TEMPLATES}")

    mod = _load_template_module(template)
    if not hasattr(mod, "render"):
        raise AttributeError(f"Template '{template}' has no render() function")

    svg = mod.render(
        title=title,
        subtitle=subtitle,
        author=author,
        date=date,
        tag=tag,
        accent=accent,
        width=width,
        height=height,
    )
    out = Path(output)
    render_svg(svg, out, width=width, height=height)
    return out


# ── CLI ────────────────────────────────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser(
        prog="og_image",
        description="Generate an OG (Open Graph) image from a title + metadata.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    ap.add_argument("--title",    required=True, help="Main title (required)")
    ap.add_argument("--subtitle", default="",    help="Optional subtitle / description")
    ap.add_argument("--author",  default="HexFoc-Xp", help="Author name (default: HexFoc-Xp)")
    ap.add_argument("--date",    default="",    help="Date string, e.g. 'Oct 2026'")
    ap.add_argument("--tag",     default="",    help="Optional tag, e.g. 'kernel', 'security'")
    ap.add_argument("--template", choices=AVAILABLE_TEMPLATES, default="terminal",
                    help="Template name (default: terminal)")
    ap.add_argument("--accent",  default=None,  help="Override accent color (hex, e.g. #ffd23f)")
    ap.add_argument("--width",   type=int, default=OG_W, help=f"Width in px (default {OG_W})")
    ap.add_argument("--height",  type=int, default=OG_H, help=f"Height in px (default {OG_H})")
    ap.add_argument("--output", "-o", required=True, help="Output PNG path")
    args = ap.parse_args()

    out = generate(
        title=args.title,
        subtitle=args.subtitle,
        author=args.author,
        date=args.date,
        tag=args.tag,
        template=args.template,
        output=args.output,
        accent=args.accent,
        width=args.width,
        height=args.height,
    )
    print(f"wrote {out} ({out.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
