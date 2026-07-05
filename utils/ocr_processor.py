"""
utils/ocr_processor.py
OCR text extraction utilities powered by EasyOCR.

Functions:
    extract_text()         — run OCR on a PIL image, return structured result dict
    calculate_confidence() — compute weighted average confidence from raw EasyOCR output
    export_text_file()     — encode extracted text as UTF-8 bytes for download
"""

from __future__ import annotations

import io
from typing import Any

from PIL import Image

# ── EasyOCR is imported lazily so missing install gives a clear error message ──
try:
    import easyocr as _easyocr
    EASYOCR_AVAILABLE = True
except ImportError:
    EASYOCR_AVAILABLE = False


# ══════════════════════════════════════════════
#  MODEL CACHE
# ══════════════════════════════════════════════

def get_ocr_reader(languages: list[str] | None = None) -> Any:
    """
    Return a cached EasyOCR Reader instance.

    The Reader object downloads language model files (~100–200 MB) on the
    very first call and caches them locally. Subsequent calls reuse the
    already-loaded model without any network activity.

    Args:
        languages: List of ISO-639-1 language codes. Defaults to ["en"].

    Returns:
        easyocr.Reader instance.

    Raises:
        RuntimeError: If easyocr is not installed.
    """
    if not EASYOCR_AVAILABLE:
        raise RuntimeError(
            "easyocr is not installed. Run: pip install easyocr"
        )
    if languages is None:
        languages = ["en"]

    cache_key = "_reader_" + "_".join(sorted(languages))
    if not hasattr(get_ocr_reader, cache_key):
        # gpu=True will be attempted automatically; falls back to CPU if unavailable
        reader = _easyocr.Reader(languages, gpu=True, verbose=False)
        setattr(get_ocr_reader, cache_key, reader)
    return getattr(get_ocr_reader, cache_key)


# ══════════════════════════════════════════════
#  CORE FUNCTIONS
# ══════════════════════════════════════════════

def extract_text(img: Image.Image, languages: list[str] | None = None) -> dict:
    """
    Run OCR on a PIL Image and return a structured result dictionary.

    Args:
        img:       Input PIL Image (any mode; converted internally to RGB).
        languages: EasyOCR language list. Defaults to ["en"].

    Returns:
        A dict with the following keys:
          - ``text``        (str):   Full extracted text, newline-separated.
          - ``confidence``  (float): Weighted average confidence (0–100 %).
          - ``word_count``  (int):   Number of whitespace-separated words.
          - ``char_count``  (int):   Total character count excluding newlines.
          - ``raw``         (list):  Raw EasyOCR result tuples for advanced use.
          - ``line_count``  (int):   Number of detected text regions.

    Raises:
        RuntimeError: If EasyOCR is not installed.
        ValueError:   If the image cannot be processed.
    """
    if not EASYOCR_AVAILABLE:
        raise RuntimeError(
            "easyocr is not installed. Please run: pip install easyocr"
        )

    if languages is None:
        languages = ["en"]

    # EasyOCR works with numpy arrays; PIL → bytes → reader is most reliable
    buf = io.BytesIO()
    img.convert("RGB").save(buf, format="PNG")
    img_bytes = buf.getvalue()

    reader = get_ocr_reader(languages)

    # detail=1 returns [[bbox, text, confidence], ...]
    raw_results: list = reader.readtext(img_bytes, detail=1)

    if not raw_results:
        return {
            "text": "",
            "confidence": 0.0,
            "word_count": 0,
            "char_count": 0,
            "raw": [],
            "line_count": 0,
        }

    lines = [item[1] for item in raw_results]
    full_text = "\n".join(lines)
    confidence = calculate_confidence(raw_results)

    return {
        "text": full_text,
        "confidence": confidence,
        "word_count": len(full_text.split()),
        "char_count": len(full_text.replace("\n", "")),
        "raw": raw_results,
        "line_count": len(raw_results),
    }


def calculate_confidence(raw_results: list) -> float:
    """
    Compute a weighted-average confidence score from EasyOCR raw output.

    Each region's confidence is weighted by the length of its text, giving
    longer, more meaningful detections more influence on the final score.

    Args:
        raw_results: List of (bbox, text, confidence) tuples from EasyOCR.

    Returns:
        Weighted average confidence as a float in [0, 100].
        Returns 0.0 if the list is empty.
    """
    if not raw_results:
        return 0.0

    total_weight = 0.0
    weighted_sum = 0.0

    for _bbox, text, conf in raw_results:
        weight = max(len(text), 1)          # avoid zero-weight for single chars
        weighted_sum += conf * weight * 100  # conf is 0–1; scale to percentage
        total_weight += weight

    return round(weighted_sum / total_weight, 1) if total_weight > 0 else 0.0


def export_text_file(text: str) -> bytes:
    """
    Encode extracted text as UTF-8 bytes suitable for ``st.download_button``.

    Args:
        text: The plain-text string to export.

    Returns:
        UTF-8-encoded bytes with a BOM for maximum editor compatibility.
    """
    # BOM prefix ensures proper encoding detection in Notepad and similar apps
    return ("\ufeff" + text).encode("utf-8")
