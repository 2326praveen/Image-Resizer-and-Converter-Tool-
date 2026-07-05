"""
utils/watermark_processor.py
Watermarking utilities — text and logo overlays with full opacity / position control.

Functions:
    add_text_watermark()  — render text onto an image at a chosen position
    add_logo_watermark()  — composite a logo image onto a base image
    apply_opacity()       — adjust alpha channel of an RGBA image
    position_watermark()  — translate a named position into pixel (x, y) coordinates
"""

from __future__ import annotations

import io
import math
from typing import Tuple

from PIL import Image, ImageDraw, ImageFont


# ══════════════════════════════════════════════
#  CONSTANTS
# ══════════════════════════════════════════════

POSITIONS = [
    "Top Left",
    "Top Right",
    "Center",
    "Bottom Left",
    "Bottom Right",
]

# Margin from the canvas edge when placing a watermark at a corner/edge
_MARGIN = 20


# ══════════════════════════════════════════════
#  HELPERS
# ══════════════════════════════════════════════

def position_watermark(
    canvas_size: Tuple[int, int],
    wm_size: Tuple[int, int],
    position: str,
) -> Tuple[int, int]:
    """
    Translate a named position into (x, y) pixel coordinates.

    Args:
        canvas_size: (width, height) of the base image.
        wm_size:     (width, height) of the watermark element.
        position:    One of POSITIONS constant values.

    Returns:
        (x, y) tuple for the top-left corner of the watermark placement.
    """
    cw, ch = canvas_size
    ww, wh = wm_size
    m = _MARGIN

    mapping = {
        "Top Left":     (m, m),
        "Top Right":    (cw - ww - m, m),
        "Center":       ((cw - ww) // 2, (ch - wh) // 2),
        "Bottom Left":  (m, ch - wh - m),
        "Bottom Right": (cw - ww - m, ch - wh - m),
    }
    return mapping.get(position, ((cw - ww) // 2, (ch - wh) // 2))


def apply_opacity(img: Image.Image, opacity: float) -> Image.Image:
    """
    Scale the alpha channel of an RGBA image by the given opacity factor.

    Args:
        img:     PIL Image. Converted to RGBA if not already.
        opacity: Float in [0.0, 1.0]. 1.0 = fully opaque, 0.0 = invisible.

    Returns:
        New RGBA PIL Image with adjusted transparency.
    """
    img = img.convert("RGBA")
    r, g, b, a = img.split()
    # Scale each alpha pixel value
    a = a.point(lambda px: int(px * max(0.0, min(1.0, opacity))))
    return Image.merge("RGBA", (r, g, b, a))


# ══════════════════════════════════════════════
#  CORE FUNCTIONS
# ══════════════════════════════════════════════

def add_text_watermark(
    img: Image.Image,
    text: str,
    font_size: int = 36,
    opacity: float = 0.5,
    angle: float = 0.0,
    position: str = "Bottom Right",
    color: Tuple[int, int, int] = (255, 255, 255),
) -> Image.Image:
    """
    Render a text watermark onto an image.

    Args:
        img:       Base PIL Image (any mode).
        text:      Watermark string to render.
        font_size: Point size of the watermark text.
        opacity:   Transparency of the text layer (0.0–1.0).
        angle:     Counter-clockwise rotation angle in degrees.
        position:  Named position string (see POSITIONS).
        color:     RGB tuple for the text colour. Default is white.

    Returns:
        New PIL Image (RGBA) with watermark composited onto the base image.
    """
    base = img.convert("RGBA")

    # ── Build the text layer ──
    try:
        # Try loading a system font; fall back to Pillow's default bitmap font
        font = ImageFont.truetype("arial.ttf", font_size)
    except (IOError, OSError):
        try:
            font = ImageFont.truetype("DejaVuSans.ttf", font_size)
        except (IOError, OSError):
            font = ImageFont.load_default()

    # Measure text bounding box to size the layer correctly
    dummy = Image.new("RGBA", (1, 1))
    draw_dummy = ImageDraw.Draw(dummy)
    bbox = draw_dummy.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]

    # Create transparent text canvas sized to the text
    txt_layer = Image.new("RGBA", (tw + 4, th + 4), (0, 0, 0, 0))
    draw = ImageDraw.Draw(txt_layer)

    # Draw a subtle shadow for readability
    shadow_opacity = int(opacity * 255 * 0.6)
    draw.text((2, 2), text, font=font, fill=(0, 0, 0, shadow_opacity))
    draw.text((0, 0), text, font=font, fill=(*color, int(opacity * 255)))

    # ── Rotate ──
    if angle != 0:
        txt_layer = txt_layer.rotate(
            angle, expand=True, resample=Image.BICUBIC
        )

    # ── Position ──
    x, y = position_watermark(base.size, txt_layer.size, position)

    # Clip to canvas bounds
    x = max(0, min(x, base.width - txt_layer.width))
    y = max(0, min(y, base.height - txt_layer.height))

    # ── Composite ──
    composite = base.copy()
    composite.paste(txt_layer, (x, y), txt_layer)

    return composite


def add_logo_watermark(
    img: Image.Image,
    logo: Image.Image,
    scale: float = 0.20,
    opacity: float = 0.80,
    position: str = "Bottom Right",
) -> Image.Image:
    """
    Composite a logo image onto a base image.

    Args:
        img:      Base PIL Image (any mode).
        logo:     Logo PIL Image. Transparency is preserved if available.
        scale:    Logo width as a fraction of the base image width (0.05–1.0).
        opacity:  Logo opacity (0.0–1.0).
        position: Named position string (see POSITIONS).

    Returns:
        New PIL Image (RGBA) with the logo composited onto the base image.
    """
    base = img.convert("RGBA")
    logo = logo.convert("RGBA")

    # ── Resize logo proportionally ──
    target_w = max(10, int(base.width * max(0.05, min(1.0, scale))))
    ratio = target_w / logo.width
    target_h = max(10, int(logo.height * ratio))
    logo = logo.resize((target_w, target_h), Image.LANCZOS)

    # ── Apply opacity ──
    logo = apply_opacity(logo, opacity)

    # ── Position ──
    x, y = position_watermark(base.size, logo.size, position)
    x = max(0, min(x, base.width - logo.width))
    y = max(0, min(y, base.height - logo.height))

    # ── Composite ──
    composite = base.copy()
    composite.paste(logo, (x, y), logo)

    return composite
