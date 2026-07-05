"""
utils/analytics.py
Session-scoped analytics tracking, metric computation, chart creation, and CSV export.

Functions:
    log_operation()    — append a processing record to st.session_state.analytics
    generate_metrics() — compute summary KPIs from the analytics DataFrame
    create_charts()    — return a dict of Plotly figure objects
    export_csv()       — serialise the DataFrame to UTF-8 CSV bytes
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

import pandas as pd

# ── Plotly imported lazily for a clear error if missing ──
try:
    import plotly.express as px
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

import streamlit as st


# ══════════════════════════════════════════════
#  CONSTANTS
# ══════════════════════════════════════════════

# Canonical operation-type labels used across the app
OP_RESIZE      = "Resize / Convert"
OP_BATCH       = "Batch Convert"
OP_BG_REMOVE   = "Background Removal"
OP_OCR         = "OCR"
OP_WATERMARK   = "Watermark"

# Colour palette (matches project green theme)
_COLOURS = [
    "#16a34a", "#4ade80", "#86efac", "#22c55e",
    "#15803d", "#14532d", "#dcfce7", "#bbf7d0",
]


# ══════════════════════════════════════════════
#  LOGGING
# ══════════════════════════════════════════════

def log_operation(
    op_type: str,
    orig_sz: int,
    out_sz: int,
    out_fmt: str,
    filename: str = "",
) -> None:
    """
    Append a single processing record to ``st.session_state.analytics``.

    This function is safe to call from any render function; it initialises
    the analytics list in session state if it doesn't exist yet.

    Args:
        op_type:  One of the OP_* constants defined in this module.
        orig_sz:  Original file size in bytes.
        out_sz:   Output file size in bytes.
        out_fmt:  Output format string, e.g. "JPEG", "PNG", "WEBP", "Transparent PNG".
        filename: Optional original filename for reference.
    """
    if "analytics" not in st.session_state:
        st.session_state.analytics = []

    space_saved = max(0, orig_sz - out_sz)
    saved_pct = round((space_saved / orig_sz * 100), 1) if orig_sz > 0 else 0.0

    record = {
        "Timestamp":    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Operation":    op_type,
        "File":         filename or "—",
        "Original (B)": orig_sz,
        "Output (B)":   out_sz,
        "Saved (B)":    space_saved,
        "Saved (%)":    saved_pct,
        "Format":       out_fmt,
    }
    st.session_state.analytics.insert(0, record)


# ══════════════════════════════════════════════
#  METRICS
# ══════════════════════════════════════════════

def _fmt_bytes(n: int) -> str:
    """Human-readable byte count (mirrors image_processor.format_bytes)."""
    if n < 1024:
        return f"{n} B"
    if n < 1024 ** 2:
        return f"{n / 1024:.1f} KB"
    return f"{n / 1024 ** 2:.2f} MB"


def generate_metrics(df: pd.DataFrame) -> dict[str, Any]:
    """
    Compute summary KPI metrics from the analytics DataFrame.

    Args:
        df: DataFrame produced from ``st.session_state.analytics``.
            Expected columns: Operation, Format, Original (B), Saved (B).

    Returns:
        Dict with keys:
          - total_images   (int)
          - total_saved    (str) — human-readable
          - top_format     (str)
          - top_operation  (str)
          - total_saved_bytes (int)
    """
    if df.empty:
        return {
            "total_images": 0,
            "total_saved": "0 B",
            "top_format": "—",
            "top_operation": "—",
            "total_saved_bytes": 0,
        }

    total_saved_bytes = int(df["Saved (B)"].sum())

    top_format = (
        df["Format"].value_counts().idxmax()
        if not df["Format"].empty
        else "—"
    )
    top_operation = (
        df["Operation"].value_counts().idxmax()
        if not df["Operation"].empty
        else "—"
    )

    return {
        "total_images":    len(df),
        "total_saved":     _fmt_bytes(total_saved_bytes),
        "top_format":      top_format,
        "top_operation":   top_operation,
        "total_saved_bytes": total_saved_bytes,
    }


# ══════════════════════════════════════════════
#  CHARTS
# ══════════════════════════════════════════════

def _plotly_theme(dark: bool) -> dict:
    """Return common Plotly layout kwargs for the current theme."""
    bg = "rgba(30,40,55,0.0)" if dark else "rgba(255,255,255,0.0)"
    font_color = "#f0faf0" if dark else "#0f3d1a"
    grid_color = "rgba(74,222,128,0.15)"
    return {
        "paper_bgcolor": bg,
        "plot_bgcolor":  bg,
        "font":          {"color": font_color, "family": "Inter, sans-serif"},
        "xaxis":         {"gridcolor": grid_color, "showgrid": True},
        "yaxis":         {"gridcolor": grid_color, "showgrid": True},
        "margin":        {"t": 40, "b": 40, "l": 40, "r": 20},
        "legend":        {"font": {"color": font_color}},
    }


def create_charts(df: pd.DataFrame, dark: bool = False) -> dict[str, Any]:
    """
    Generate all four Plotly charts for the Analytics Dashboard.

    Args:
        df:   Analytics DataFrame (may be empty).
        dark: Whether the app is in dark mode.

    Returns:
        Dict with keys:
          - ``operations_pie``   — Operations distribution (Pie)
          - ``format_bar``       — Format usage (Bar)
          - ``daily_line``       — Daily activity trend (Line)
          - ``space_saved_bar``  — Space saved per operation (Bar)
        All values are Plotly Figure objects or None if data is insufficient.
    """
    if not PLOTLY_AVAILABLE:
        return {}

    theme = _plotly_theme(dark)
    charts: dict[str, Any] = {}

    # ── 1. Operations Pie ──
    if not df.empty:
        op_counts = df["Operation"].value_counts().reset_index()
        op_counts.columns = ["Operation", "Count"]
        fig_pie = px.pie(
            op_counts,
            names="Operation",
            values="Count",
            title="Operations Distribution",
            color_discrete_sequence=_COLOURS,
            hole=0.40,
        )
        fig_pie.update_layout(**theme)
        fig_pie.update_traces(textfont_color=theme["font"]["color"])
        charts["operations_pie"] = fig_pie
    else:
        charts["operations_pie"] = None

    # ── 2. Format Bar ──
    if not df.empty:
        fmt_counts = df["Format"].value_counts().reset_index()
        fmt_counts.columns = ["Format", "Count"]
        fig_bar = px.bar(
            fmt_counts,
            x="Format",
            y="Count",
            title="Format Usage",
            color="Format",
            color_discrete_sequence=_COLOURS,
            text_auto=True,
        )
        fig_bar.update_layout(**theme)
        charts["format_bar"] = fig_bar
    else:
        charts["format_bar"] = None

    # ── 3. Daily Activity Line ──
    if not df.empty:
        df_copy = df.copy()
        df_copy["Date"] = pd.to_datetime(df_copy["Timestamp"]).dt.date
        daily = df_copy.groupby("Date").size().reset_index(name="Count")
        fig_line = px.line(
            daily,
            x="Date",
            y="Count",
            title="Daily Activity Trend",
            markers=True,
            color_discrete_sequence=["#4ade80"],
        )
        fig_line.update_traces(
            line={"width": 3},
            marker={"size": 8, "color": "#16a34a"},
        )
        fig_line.update_layout(**theme)
        charts["daily_line"] = fig_line
    else:
        charts["daily_line"] = None

    # ── 4. Space Saved per Operation ──
    if not df.empty:
        saved_by_op = (
            df.groupby("Operation")["Saved (B)"]
            .sum()
            .reset_index()
            .rename(columns={"Saved (B)": "Saved (bytes)"})
        )
        # Convert to KB for readability
        saved_by_op["Saved (KB)"] = (saved_by_op["Saved (bytes)"] / 1024).round(1)
        fig_saved = px.bar(
            saved_by_op,
            x="Operation",
            y="Saved (KB)",
            title="Space Saved per Operation (KB)",
            color="Operation",
            color_discrete_sequence=_COLOURS,
            text_auto=True,
        )
        fig_saved.update_layout(**theme)
        charts["space_saved_bar"] = fig_saved
    else:
        charts["space_saved_bar"] = None

    return charts


# ══════════════════════════════════════════════
#  EXPORT
# ══════════════════════════════════════════════

def export_csv(df: pd.DataFrame) -> bytes:
    """
    Serialise the analytics DataFrame to a UTF-8 CSV byte string.

    Args:
        df: Analytics DataFrame.

    Returns:
        UTF-8 encoded bytes of the CSV representation.
    """
    return df.to_csv(index=False).encode("utf-8")
