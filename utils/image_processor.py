"""
Image processing utilities — PIL-based backend
"""
import io
import base64
from PIL import Image, ImageOps

# ── Resize presets ──
PRESETS = {
    "Custom Size":          None,
    "Instagram Post":       (1080, 1080),
    "Instagram Story":      (1080, 1920),
    "YouTube Thumbnail":    (1280, 720),
    "WhatsApp DP":          (512,  512),
    "HD Wallpaper":         (1920, 1080),
    "Twitter Header":       (1500, 500),
    "Facebook Cover":       (820,  312),
}

FORMAT_MIME = {"JPEG": "image/jpeg", "PNG": "image/png", "WEBP": "image/webp"}
FORMAT_EXT  = {"JPEG": "jpg", "PNG": "png", "WEBP": "webp"}


def format_bytes(n: int) -> str:
    if n < 1024:        return f"{n} B"
    if n < 1024 ** 2:  return f"{n / 1024:.1f} KB"
    return f"{n / 1024 ** 2:.2f} MB"


def load_image(data: bytes) -> Image.Image:
    img = Image.open(io.BytesIO(data))
    img.load()
    return img


def _to_rgb_if_needed(img: Image.Image, fmt: str) -> Image.Image:
    """Convert RGBA/P → RGB for JPEG."""
    if fmt == "JPEG" and img.mode in ("RGBA", "P", "LA"):
        bg = Image.new("RGB", img.size, (255, 255, 255))
        alpha = img.convert("RGBA").split()[-1]
        bg.paste(img.convert("RGBA"), mask=alpha)
        return bg
    return img


def resize_image(img: Image.Image, width: int, height: int, keep_aspect: bool) -> Image.Image:
    """Resize using Lanczos for best quality."""
    w = max(1, min(width,  10000))
    h = max(1, min(height, 10000))
    if keep_aspect:
        out = img.copy()
        out.thumbnail((w, h), Image.LANCZOS)
        return out
    return img.resize((w, h), Image.LANCZOS)


def save_image(img: Image.Image, fmt: str, quality: int = 85) -> bytes:
    """Save image to bytes with given format & quality."""
    fmt = fmt.upper()
    buf = io.BytesIO()
    out = _to_rgb_if_needed(img, fmt)
    kw = {"optimize": True}
    if fmt in ("JPEG", "WEBP"):
        kw["quality"] = quality
    out.save(buf, format=fmt, **kw)
    return buf.getvalue()


def image_to_b64(img: Image.Image, fmt: str = "PNG") -> str:
    """Return base64-encoded data URL for an image (for HTML embeds)."""
    fmt = fmt.upper()
    buf = io.BytesIO()
    out = _to_rgb_if_needed(img, fmt)
    out.save(buf, format=fmt)
    encoded = base64.b64encode(buf.getvalue()).decode()
    mime = FORMAT_MIME.get(fmt, "image/png")
    return f"data:{mime};base64,{encoded}"


def compression_pct(original: int, compressed: int) -> int:
    if original <= 0:
        return 0
    pct = (1 - compressed / original) * 100
    return max(0, int(pct))
