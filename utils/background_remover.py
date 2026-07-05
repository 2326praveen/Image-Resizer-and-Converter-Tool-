"""
utils/background_remover.py
AI-powered background removal utilities using rembg (u2net model).

Functions:
    remove_background()   — strip image background, return transparent RGBA PNG bytes
    get_file_size()       — human-readable byte count string
    generate_download_btn_params() — produce kwargs for st.download_button
"""

from __future__ import annotations

import io
import time
from typing import Tuple

from PIL import Image

# ── rembg is imported lazily so the app doesn't crash if it isn't installed yet ──
try:
    from rembg import remove as _rembg_remove, new_session as _rembg_new_session
    REMBG_AVAILABLE = True
except ImportError:
    REMBG_AVAILABLE = False


# ══════════════════════════════════════════════
#  SESSION CACHE HELPERS
# ══════════════════════════════════════════════

def get_rembg_session():
    """
    Return a cached rembg Session object.
    The model (u2net, ~170 MB) is downloaded on first call and reused
    for all subsequent calls within the Streamlit app session.

    Raises:
        RuntimeError: If rembg is not installed.
    """
    if not REMBG_AVAILABLE:
        raise RuntimeError(
            "rembg is not installed. Run: pip install rembg"
        )
    # We use a module-level dict as a simple in-process cache so that the
    # heavy model is loaded only once, even across Streamlit reruns.
    if not hasattr(get_rembg_session, "_session"):
        get_rembg_session._session = _rembg_new_session("u2net")
    return get_rembg_session._session


# ══════════════════════════════════════════════
#  CORE FUNCTIONS
# ══════════════════════════════════════════════

def remove_background(
    img_bytes: bytes,
) -> Tuple[bytes, float]:
    """
    Remove the background from image bytes using the rembg u2net AI model.

    Args:
        img_bytes: Raw bytes of the input image (JPG / PNG / WEBP).

    Returns:
        A tuple of:
          - output_bytes (bytes): PNG-encoded RGBA image with transparent background.
          - elapsed (float): Processing time in seconds.

    Raises:
        RuntimeError: If rembg is unavailable.
        ValueError:   If the input bytes cannot be decoded as an image.
    """
    if not REMBG_AVAILABLE:
        raise RuntimeError(
            "rembg is not installed. Please run: pip install rembg"
        )

    # Validate input is a recognisable image before passing to AI model
    try:
        Image.open(io.BytesIO(img_bytes)).verify()
    except Exception as exc:
        raise ValueError(f"Could not decode image: {exc}") from exc

    session = get_rembg_session()

    start = time.perf_counter()
    output_bytes: bytes = _rembg_remove(img_bytes, session=session)
    elapsed = time.perf_counter() - start

    return output_bytes, elapsed


def get_file_size(data: bytes) -> str:
    """
    Convert raw byte length into a human-readable string.

    Args:
        data: Any bytes object.

    Returns:
        Formatted string, e.g. "245.3 KB" or "1.02 MB".
    """
    n = len(data)
    if n < 1024:
        return f"{n} B"
    if n < 1024 ** 2:
        return f"{n / 1024:.1f} KB"
    return f"{n / 1024 ** 2:.2f} MB"


def generate_download_btn_params(
    output_bytes: bytes,
    original_filename: str,
) -> dict:
    """
    Build keyword-argument dict suitable for ``st.download_button(**params)``.

    Args:
        output_bytes:       PNG RGBA bytes from remove_background().
        original_filename:  Original uploaded filename (used to derive download name).

    Returns:
        Dict with keys: label, data, file_name, mime, use_container_width.
    """
    stem = original_filename.rsplit(".", 1)[0]
    download_name = f"{stem}_no_bg.png"
    size_label = get_file_size(output_bytes)

    return {
        "label": f"⬇️  Download Transparent PNG — {size_label}",
        "data": output_bytes,
        "file_name": download_name,
        "mime": "image/png",
        "use_container_width": True,
    }
