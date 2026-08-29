#!/usr/bin/env python3
"""Render Teamulate Open Graph share images from the official purple T mark.

Produces:
  assets/og/teamulate-og-1536x1024.png  — source composition (3:2)
  assets/og/teamulate-og.png            — 1200x630 used by share tags
"""

from __future__ import annotations

import io
import math
from pathlib import Path

import cairosvg
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "assets" / "og"
SVG_PATH = Path("/tmp/tm-assets/icon.svg")
if not SVG_PATH.exists():
    SVG_PATH = OUT_DIR / "teamulate-mark-source.svg"

PURPLE = (90, 69, 255)  # #5A45FF
PURPLE_SOFT = (123, 108, 255)  # #7B6CFF
PURPLE_DEEP = (67, 48, 212)
INK = (17, 17, 20)
WHITE = (255, 255, 255)

FONT_BOLD = "/usr/share/fonts/truetype/macos/Inter-Bold.ttf"
FONT_SEMI = "/usr/share/fonts/truetype/macos/Inter-SemiBold.ttf"
FONT_MED = "/usr/share/fonts/truetype/macos/Inter-Medium.ttf"

NODES = [
    ("STRATEGY", "target"),
    ("PERFORMANCE", "bars"),
    ("CONTENT", "pencil"),
    ("AUDIENCE", "person"),
    ("SEO & GEO", "globe"),
    ("CAMPAIGNS", "megaphone"),
    ("GROWTH", "growth"),
    ("ANALYTICS", "pie"),
]


def font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size)


def raster_mark(size: int) -> Image.Image:
    png = cairosvg.svg2png(url=str(SVG_PATH), output_width=size, output_height=size)
    im = Image.open(io.BytesIO(png)).convert("RGBA")
    return im


def rounded_rect(draw: ImageDraw.ImageDraw, box, radius, fill, width=0, outline=None):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def draw_icon(draw: ImageDraw.ImageDraw, kind: str, cx: int, cy: int, s: int, color):
    """Simple purple line icons, centered at (cx, cy). s is half-size."""
    w = max(3, s // 7)

    if kind == "target":
        draw.ellipse((cx - s, cy - s, cx + s, cy + s), outline=color, width=w)
        draw.ellipse((cx - s * 0.55, cy - s * 0.55, cx + s * 0.55, cy + s * 0.55), outline=color, width=w)
        draw.ellipse((cx - s * 0.16, cy - s * 0.16, cx + s * 0.16, cy + s * 0.16), fill=color)
        draw.line((cx, cy - s - 2, cx, cy - s * 0.55), fill=color, width=w)
        draw.line((cx, cy + s * 0.55, cx, cy + s + 2), fill=color, width=w)
        draw.line((cx - s - 2, cy, cx - s * 0.55, cy), fill=color, width=w)
        draw.line((cx + s * 0.55, cy, cx + s + 2, cy), fill=color, width=w)
    elif kind == "bars":
        gap = s * 0.55
        bw = max(3, int(s * 0.42))
        heights = [s * 0.55, s * 0.85, s * 1.15]
        xs = [cx - gap, cx, cx + gap]
        base = cy + s * 0.85
        for x, h in zip(xs, heights):
            draw.rounded_rectangle((x - bw / 2, base - h, x + bw / 2, base), radius=bw / 2, fill=color)
    elif kind == "pencil":
        # angled pencil
        draw.line((cx - s * 0.7, cy + s * 0.7, cx + s * 0.55, cy - s * 0.55), fill=color, width=w + 1)
        draw.polygon(
            [
                (cx + s * 0.55, cy - s * 0.55),
                (cx + s * 0.85, cy - s * 0.25),
                (cx + s * 0.72, cy - s * 0.72),
            ],
            fill=color,
        )
        draw.line((cx - s * 0.85, cy + s * 0.85, cx - s * 0.55, cy + s * 0.55), fill=color, width=w)
    elif kind == "person":
        draw.ellipse((cx - s * 0.38, cy - s * 0.95, cx + s * 0.38, cy - s * 0.18), outline=color, width=w)
        draw.arc((cx - s * 0.95, cy - 2, cx + s * 0.95, cy + s * 1.35), 200, 340, fill=color, width=w + 1)
    elif kind == "globe":
        draw.ellipse((cx - s, cy - s, cx + s, cy + s), outline=color, width=w)
        draw.ellipse((cx - s * 0.42, cy - s, cx + s * 0.42, cy + s), outline=color, width=max(2, w - 1))
        draw.arc((cx - s, cy - s * 0.45, cx + s, cy + s * 0.15), 200, 340, fill=color, width=max(2, w - 1))
        draw.arc((cx - s, cy - s * 0.15, cx + s, cy + s * 0.45), 20, 160, fill=color, width=max(2, w - 1))
        draw.line((cx - s, cy, cx + s, cy), fill=color, width=max(2, w - 1))
    elif kind == "megaphone":
        draw.polygon(
            [
                (cx - s * 0.85, cy - s * 0.25),
                (cx + s * 0.15, cy - s * 0.85),
                (cx + s * 0.15, cy + s * 0.85),
                (cx - s * 0.85, cy + s * 0.25),
            ],
            outline=color,
        )
        draw.line((cx - s * 0.85, cy - s * 0.25, cx - s * 0.85, cy + s * 0.25), fill=color, width=w)
        draw.arc((cx + s * 0.2, cy - s * 0.55, cx + s * 0.95, cy + s * 0.55), 300, 60, fill=color, width=w)
        draw.line((cx - s * 0.55, cy + s * 0.25, cx - s * 0.35, cy + s * 0.95), fill=color, width=w)
        draw.line((cx - s * 0.35, cy + s * 0.95, cx - s * 0.05, cy + s * 0.7), fill=color, width=w)
    elif kind == "growth":
        pts = [
            (cx - s, cy + s * 0.55),
            (cx - s * 0.35, cy + s * 0.1),
            (cx + s * 0.05, cy + s * 0.45),
            (cx + s * 0.85, cy - s * 0.75),
        ]
        draw.line(pts, fill=color, width=w, joint="curve")
        draw.polygon(
            [
                (cx + s * 0.85, cy - s * 0.75),
                (cx + s * 0.25, cy - s * 0.7),
                (cx + s * 0.75, cy - s * 0.15),
            ],
            fill=color,
        )
    elif kind == "pie":
        box = (cx - s, cy - s, cx + s, cy + s)
        draw.ellipse(box, outline=color, width=w)
        draw.pieslice(box, start=270, end=40, outline=color, width=w)
        draw.line((cx, cy, cx, cy - s), fill=color, width=w)
        draw.line((cx, cy, cx + s * 0.72, cy + s * 0.55), fill=color, width=w)


def draw_waves(img: Image.Image, purple, scale: float):
    """Translucent flowing waves along the bottom edge."""
    w, h = img.size
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    base = h * 0.86

    def wave_poly(amp, y0, phase, thick):
        pts_top = []
        pts_bot = []
        steps = 80
        for i in range(steps + 1):
            x = w * i / steps
            y = y0 + amp * math.sin((i / steps) * math.pi * 2 + phase)
            pts_top.append((x, y))
            pts_bot.append((x, y + thick))
        return pts_top + list(reversed(pts_bot))

    d.polygon(wave_poly(18 * scale, base, 0.2, 70 * scale), fill=(*purple, 28))
    d.polygon(wave_poly(22 * scale, base + 18 * scale, 1.4, 80 * scale), fill=(*PURPLE_SOFT, 36))
    d.polygon(wave_poly(14 * scale, base + 36 * scale, 2.6, 90 * scale), fill=(*purple, 22))
    blurred = overlay.filter(ImageFilter.GaussianBlur(radius=6 * scale))
    img.alpha_composite(blurred)


def compose(width: int, height: int, scale: float) -> Image.Image:
    img = Image.new("RGBA", (width, height), (*WHITE, 255))
    draw = ImageDraw.Draw(img)

    # --- left branding ---
    mark_px = int(72 * scale)
    mark = raster_mark(mark_px * 2)
    mark = mark.resize((mark_px, mark_px), Image.Resampling.LANCZOS)
    logo_x = int(72 * scale)
    logo_y = int(72 * scale)
    img.paste(mark, (logo_x, logo_y), mark)

    word_font = font(FONT_BOLD, int(36 * scale))
    word = "Teamulate"
    word_x = logo_x + mark_px + int(16 * scale)
    # vertically center wordmark against the mark
    bbox = word_font.getbbox(word)
    word_h = bbox[3] - bbox[1]
    word_y = logo_y + (mark_px - word_h) // 2 - bbox[1]
    draw.text((word_x, word_y), word, font=word_font, fill=INK)

    # headline — three lines, matching the attached graphic
    h1 = font(FONT_BOLD, int(72 * scale))
    h2 = font(FONT_BOLD, int(72 * scale))
    hx = logo_x
    hy = logo_y + mark_px + int(56 * scale)
    line_gap = int(78 * scale)
    draw.text((hx, hy), "Your", font=h1, fill=INK)
    draw.text((hx, hy + line_gap), "AI Marketing", font=h2, fill=PURPLE)
    draw.text((hx, hy + line_gap * 2), "Team", font=h1, fill=INK)

    # --- circular diagram on the right ---
    # center of the ring
    if width / height > 1.7:
        ring_cx = int(width * 0.70)
        ring_cy = int(height * 0.48)
        ring_r = int(min(width, height) * 0.32)
    else:
        ring_cx = int(width * 0.68)
        ring_cy = int(height * 0.48)
        ring_r = int(min(width, height) * 0.30)

    node_r = int(36 * scale)
    # dashed spokes
    for i in range(len(NODES)):
        angle = -math.pi / 2 + i * (2 * math.pi / len(NODES))
        x2 = ring_cx + math.cos(angle) * (ring_r - node_r - 4)
        y2 = ring_cy + math.sin(angle) * (ring_r - node_r - 4)
        # dashed line
        x1 = ring_cx + math.cos(angle) * (int(58 * scale))
        y1 = ring_cy + math.sin(angle) * (int(58 * scale))
        segs = 18
        for s in range(segs):
            if s % 2 == 1:
                continue
            t0 = s / segs
            t1 = min(1, (s + 1) / segs)
            draw.line(
                (
                    x1 + (x2 - x1) * t0,
                    y1 + (y2 - y1) * t0,
                    x1 + (x2 - x1) * t1,
                    y1 + (y2 - y1) * t1,
                ),
                fill=(210, 208, 220),
                width=max(2, int(2 * scale)),
            )

    # center glowing plate + official T
    glow = Image.new("RGBA", img.size, (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    glow_r = int(78 * scale)
    gd.ellipse(
        (ring_cx - glow_r, ring_cy - glow_r, ring_cx + glow_r, ring_cy + glow_r),
        fill=(90, 69, 255, 28),
    )
    img.alpha_composite(glow.filter(ImageFilter.GaussianBlur(radius=18 * scale)))
    plate_r = int(52 * scale)
    draw.ellipse(
        (ring_cx - plate_r, ring_cy - plate_r, ring_cx + plate_r, ring_cy + plate_r),
        fill=WHITE,
        outline=(236, 234, 246),
        width=max(2, int(2 * scale)),
    )
    center_mark = raster_mark(int(64 * scale))
    cm = center_mark.resize((int(56 * scale), int(56 * scale)), Image.Resampling.LANCZOS)
    img.paste(cm, (ring_cx - cm.size[0] // 2, ring_cy - cm.size[1] // 2), cm)

    label_font = font(FONT_BOLD, int(13 * scale))
    for i, (label, kind) in enumerate(NODES):
        angle = -math.pi / 2 + i * (2 * math.pi / len(NODES))
        nx = int(ring_cx + math.cos(angle) * ring_r)
        ny = int(ring_cy + math.sin(angle) * ring_r)
        # white node circle with light ring
        draw.ellipse(
            (nx - node_r, ny - node_r, nx + node_r, ny + node_r),
            fill=WHITE,
            outline=(232, 230, 242),
            width=max(2, int(2 * scale)),
        )
        draw_icon(draw, kind, nx, ny - int(2 * scale), int(14 * scale), PURPLE)
        # label under the node, nudged outward
        tb = label_font.getbbox(label)
        tw = tb[2] - tb[0]
        # push labels slightly outward from center
        lx = nx - tw // 2
        ly = ny + node_r + int(8 * scale)
        # keep labels on canvas
        lx = max(8, min(width - tw - 8, lx))
        ly = max(8, min(height - int(28 * scale), ly))
        draw.text((lx, ly), label, font=label_font, fill=INK)

    draw_waves(img, PURPLE, scale)
    return img


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # Render at 2x then downscale for clean edges
    src = compose(1536 * 2, 1024 * 2, scale=2.0)
    src = src.resize((1536, 1024), Image.Resampling.LANCZOS).convert("RGB")
    src_path = OUT_DIR / "teamulate-og-1536x1024.png"
    src.save(src_path, "PNG", optimize=True)

    wide = compose(1200 * 2, 630 * 2, scale=1.72)
    wide = wide.resize((1200, 630), Image.Resampling.LANCZOS).convert("RGB")
    og_path = OUT_DIR / "teamulate-og.png"
    wide.save(og_path, "PNG", optimize=True)

    print(f"wrote {src_path} {src.size}")
    print(f"wrote {og_path} {wide.size}")


if __name__ == "__main__":
    main()
