#!/usr/bin/env python3
"""Generate example OG images for all templates.

Usage:
    python scripts/demo.py

Outputs:
    examples/terminal-blog.png
    examples/minimal-tutorial.png
    examples/gradient-launch.png

This script is shipped in the source distribution. After cloning the repo,
you can run it to regenerate the example images.
"""
import sys
from pathlib import Path

# Allow running from a checkout without installing the package
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from og_image_hexfoc import generate

# Example 1: Terminal template — for technical blog post
generate(
    title="Booting Linux on Android without root",
    subtitle="A deep dive into User-Mode Linux on aarch64",
    author="HexFoc-Xp",
    date="Oct 2026",
    tag="kernel",
    template="terminal",
    output=ROOT / "examples" / "terminal-blog.png",
)
print("  ✓ terminal-blog.png")

# Example 2: Minimal template — for tutorial
generate(
    title="Building LLM Backends at Scale",
    subtitle="A practical guide to FastAPI + LangGraph + Redis",
    author="HexFoc-Xp",
    date="Oct 2026",
    tag="backend",
    template="minimal",
    output=ROOT / "examples" / "minimal-tutorial.png",
)
print("  ✓ minimal-tutorial.png")

# Example 3: Gradient template — for product launch
generate(
    title="Stryker 2.0 is here",
    subtitle="The pentest lab in 150K+ pockets — now with BLE + HID support",
    author="HexFoc-Xp",
    date="Oct 2026",
    tag="security",
    template="gradient",
    output=ROOT / "examples" / "gradient-launch.png",
)
print("  ✓ gradient-launch.png")

print("\nAll examples generated in /examples/")
