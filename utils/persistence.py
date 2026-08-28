"""
Persists history and settings to Supabase for logged-in users only.

Guests keep working exactly as today: history/settings live in
st.session_state and disappear when the tab closes. Nothing here changes
that path — these functions are no-ops when there's no logged-in user,
so you can call them unconditionally from app.py without extra branching
in most places.
"""

from datetime import datetime
from utils.auth import get_supabase_client, get_current_user


# ── Field-name mapping helpers ─────────────────────────────────────────────
# app.py history dicts use:  name, orig_fmt, out_fmt, orig_sz, out_sz, dims, ts
# Supabase user_history uses: original_name, original_size_kb, new_size_kb,
#                              format, dimensions, compression_pct, created_at
# orig_fmt is NOT stored in the DB schema (no column for it).

def to_supabase_shape(entry: dict) -> dict:
    """Convert an app-shape history dict to Supabase user_history column names.

    Called internally by save_history_entry() so app.py never has to deal
    with Supabase column names directly.
    """
    orig_sz = entry.get("orig_sz", 0) or 0
    out_sz  = entry.get("out_sz",  0) or 0
    pct     = (1 - out_sz / orig_sz) * 100 if orig_sz > 0 else 0.0
    return {
        "original_name":    entry.get("name", ""),
        "original_size_kb": round(orig_sz / 1024, 2),
        "new_size_kb":      round(out_sz  / 1024, 2),
        "format":           entry.get("out_fmt", ""),
        "dimensions":       entry.get("dims", ""),
        "compression_pct":  round(max(0.0, pct), 1),
    }


def to_app_shape(row: dict) -> dict:
    """Convert a Supabase user_history row back to an app-shape history dict.

    Used in app.py's one-time seeding block to translate persisted rows into
    the same shape that st.session_state.history already uses, so render_history()
    needs zero changes.
    """
    orig_kb = row.get("original_size_kb") or 0
    new_kb  = row.get("new_size_kb")      or 0
    return {
        "name":     row.get("original_name", ""),
        "orig_fmt": "",                                       # not stored in DB
        "out_fmt":  row.get("format", ""),
        "orig_sz":  int(orig_kb * 1024),
        "out_sz":   int(new_kb  * 1024),
        "dims":     row.get("dimensions", ""),
        "ts":       row.get("created_at", datetime.now().isoformat()),
    }


# ── Persistence functions ──────────────────────────────────────────────────

def save_history_entry(entry: dict) -> bool:
    """
    Persist one history record for the logged-in user.
    Accepts an app-shape dict (keys: name, orig_fmt, out_fmt, orig_sz, out_sz,
    dims, ts) and converts to Supabase column names internally via
    to_supabase_shape().
    Returns True if saved, False if skipped (guest) or failed.
    """
    user = get_current_user()
    if not user:
        return False
    supabase = get_supabase_client()
    try:
        payload = {**to_supabase_shape(entry), "user_id": user["id"]}
        supabase.table("user_history").insert(payload).execute()
        return True
    except Exception:
        return False


def load_history(limit: int = 200):
    """Return the logged-in user's saved history rows, most recent first.

    Rows are in Supabase shape; call to_app_shape() on each row before
    merging into st.session_state.history.
    """
    user = get_current_user()
    if not user:
        return []
    supabase = get_supabase_client()
    try:
        res = (
            supabase.table("user_history")
            .select("*")
            .eq("user_id", user["id"])
            .order("created_at", desc=True)
            .limit(limit)
            .execute()
        )
        return res.data or []
    except Exception:
        return []


def save_settings(settings: dict) -> bool:
    """
    Upsert the logged-in user's settings, e.g.
      {"theme": "dark", "default_format": "WEBP", "preferences": {...}}
    """
    user = get_current_user()
    if not user:
        return False
    supabase = get_supabase_client()
    try:
        payload = {"user_id": user["id"], **settings}
        supabase.table("user_settings").upsert(payload).execute()
        return True
    except Exception:
        return False


def load_settings():
    """Return the logged-in user's saved settings dict, or None."""
    user = get_current_user()
    if not user:
        return None
    supabase = get_supabase_client()
    try:
        res = (
            supabase.table("user_settings")
            .select("*")
            .eq("user_id", user["id"])
            .execute()
        )
        return res.data[0] if res.data else None
    except Exception:
        return None
