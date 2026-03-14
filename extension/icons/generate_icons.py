"""Generate croissant PNG icons from an SVG template."""

import subprocess
import os

SVG_TEMPLATE = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128" width="{size}" height="{size}">
  <rect width="128" height="128" rx="20" fill="#F59E0B"/>
  <text x="64" y="88" text-anchor="middle" font-size="72" font-family="Arial, sans-serif" font-weight="bold" fill="white">C</text>
</svg>"""

SIZES = [16, 48, 128]

script_dir = os.path.dirname(os.path.abspath(__file__))

for size in SIZES:
    svg_path = os.path.join(script_dir, f"croissant-{size}.svg")
    png_path = os.path.join(script_dir, f"croissant-{size}.png")

    with open(svg_path, "w") as f:
        f.write(SVG_TEMPLATE.format(size=size))

    try:
        subprocess.run(
            ["rsvg-convert", "-w", str(size), "-h", str(size), svg_path, "-o", png_path],
            check=True,
        )
        os.remove(svg_path)
        print(f"Generated {png_path}")
    except FileNotFoundError:
        try:
            subprocess.run(
                ["sips", "-s", "format", "png", "-z", str(size), str(size), svg_path, "--out", png_path],
                check=True,
            )
            os.remove(svg_path)
            print(f"Generated {png_path} (via sips)")
        except Exception:
            print(f"Kept SVG at {svg_path} - install rsvg-convert or convert manually")
