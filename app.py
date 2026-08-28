"""
Image Studio Pro — Streamlit App  (v3.0)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Stack : Python · Streamlit · Pillow · rembg · EasyOCR · Plotly
Logic : utils/image_processor.py
        utils/background_remover.py
        utils/ocr_processor.py
        utils/watermark_processor.py
        utils/analytics.py
Styling: utils/styles.py (dynamic Light/Dark CSS)
HTML  : only for CSS injection · JS comparison slider · ambient blobs
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import io
import base64
from datetime import datetime

import pandas as pd
import streamlit as st
from PIL import Image

# ── Existing utilities ──
from utils.image_processor import (
    load_image, resize_image, save_image,
    image_to_b64, format_bytes, compression_pct, PRESETS, FORMAT_EXT,
)
from utils.styles import get_css

# ── New feature utilities ──
from utils.background_remover import (
    remove_background, get_file_size, generate_download_btn_params,
    REMBG_AVAILABLE,
)
from utils.ocr_processor import (
    extract_text, export_text_file, EASYOCR_AVAILABLE,
)
from utils.watermark_processor import (
    add_text_watermark, add_logo_watermark, POSITIONS,
)
from utils.analytics import (
    log_operation, generate_metrics, create_charts, export_csv,
    OP_RESIZE, OP_BATCH, OP_BG_REMOVE, OP_OCR, OP_WATERMARK,
)

# ── Optional auth utilities (graceful degradation) ─────────────────────────
# If supabase is not installed, secrets are missing, or secrets are invalid,
# AUTH_AVAILABLE stays False and the login UI is never shown.  Guests are
# completely unaffected — every existing feature works as today.
AUTH_AVAILABLE = False
try:
    from utils.auth import sign_up, sign_in, sign_out, is_logged_in, get_current_user
    from utils.persistence import save_history_entry, load_history, to_app_shape
    # Confirm both secrets exist before marking auth as available
    _sb_url = st.secrets.get("SUPABASE_URL", "")
    _sb_key = st.secrets.get("SUPABASE_ANON_KEY", "")
    if _sb_url and _sb_key:
        AUTH_AVAILABLE = True
except Exception:
    pass

# ══════════════════════════════════════════════
#  PAGE CONFIG
# ══════════════════════════════════════════════
st.set_page_config(
    page_title="Image Studio Pro",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════
#  SESSION STATE — initialise all keys
# ══════════════════════════════════════════════
_defaults = {
    "section":        "upload",
    "dark":           False,
    "history":        [],
    "batch_results":  [],
    "analytics":      [],          # per-session analytics log
    "ocr_result":     None,        # cache last OCR result
    "wm_preview":     None,        # cache watermark preview bytes
    "history_seeded": False,       # auth: prevents double-loading persisted history
    "entered_app":    False,       # gating: landing page vs main tool
    "landing_auth":   None,        # landing auth drawer state: None | 'login' | 'signup'
}
for k, v in _defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

dark = st.session_state.dark
is_landing = not st.session_state.entered_app

# ── Seed session history from Supabase once per session (logged-in users only) ──
if AUTH_AVAILABLE and is_logged_in() and not st.session_state.history_seeded:
    try:
        _db_rows = load_history()
        if _db_rows:
            _seeded = [to_app_shape(r) for r in _db_rows]
            st.session_state.history = _seeded + st.session_state.history
            _analytics_from_db = []
            for _r, _e in zip(_db_rows, _seeded):
                _fmt = _e.get("out_fmt", "").upper()
                _op  = OP_OCR if _fmt == "TXT" else OP_RESIZE
                _ts  = _e.get("ts", "")
                _ts_str = _ts[:19].replace("T", " ") if "T" in _ts else _ts[:19]
                _analytics_from_db.append({
                    "Timestamp":    _ts_str,
                    "Operation":    _op,
                    "File":         _e.get("name", "—"),
                    "Original (B)": _e.get("orig_sz", 0),
                    "Output (B)":   _e.get("out_sz",  0),
                    "Saved (B)":    max(0, _e.get("orig_sz", 0) - _e.get("out_sz", 0)),
                    "Saved (%)":    round(_r.get("compression_pct", 0.0), 1),
                    "Format":       _fmt,
                })
            st.session_state.analytics = _analytics_from_db + st.session_state.analytics
    except Exception:
        pass
    st.session_state.history_seeded = True

# ══════════════════════════════════════════════
#  CSS + DECORATIONS
# ══════════════════════════════════════════════
st.markdown(get_css(dark, is_landing=is_landing), unsafe_allow_html=True)
# ── Minimal hero tilt (3°) — hero card only, no blobs/orbs/rings ──



# ══════════════════════════════════════════════
#  PURE-PYTHON HELPERS
# ══════════════════════════════════════════════
def time_ago(iso: str) -> str:
    """Return a human-readable 'time ago' string from an ISO timestamp."""
    dt = datetime.fromisoformat(iso)
    if dt.tzinfo is not None:          # strip tz-awareness (Supabase created_at)
        dt = dt.replace(tzinfo=None)
    diff = (datetime.now() - dt).total_seconds()
    if diff < 60:    return "Just now"
    if diff < 3600:  return f"{int(diff / 60)}m ago"
    if diff < 86400: return f"{int(diff / 3600)}h ago"
    return f"{int(diff / 86400)}d ago"


def section_header(icon: str, title: str, subtitle: str = "", badges: list = None) -> None:
    """Render a consistent, modern SaaS section header."""
    badges_html = ""
    if badges:
        items = "".join([f'<span class="app-pill-badge">{b}</span>' for b in badges])
        badges_html = f'<div class="app-badge-row">{items}</div>'

    st.markdown(f"""
<div class="app-header-wrap">
  <div class="app-header-title">{icon} {title}</div>
  {f'<div class="app-header-sub">{subtitle}</div>' if subtitle else ''}
  {badges_html}
</div>
    """, unsafe_allow_html=True)


def card(title: str = "", icon: str = "") -> None:
    """Render a labelled card title using native Streamlit subheader."""
    if title:
        st.markdown(f"**{icon} {title}**" if icon else f"**{title}**")


# Only unavoidable HTML: JavaScript-driven before/after slider
def comparison_slider(b64_before: str, b64_after: str) -> None:
    """Render an interactive before/after image comparison slider via HTML + JS."""
    st.markdown(f"""\
<div style="position:relative;width:100%;border-radius:20px;overflow:hidden;
            user-select:none;touch-action:none;margin-top:0.5rem;
            box-shadow:0 8px 32px rgba(0,0,0,0.25);" id="cmp">
  <img src="{b64_before}"
       style="display:block;width:100%;height:auto;max-height:340px;
              object-fit:contain;background:#0d1117;" />
  <div id="cmpAfter"
       style="position:absolute;top:0;left:0;width:50%;height:100%;
              overflow:hidden;border-right:3px solid rgba(74,222,128,0.90);
              filter:drop-shadow(0 0 8px rgba(74,222,128,0.50));">
    <img src="{b64_after}"
         style="display:block;width:100%;height:100%;
                object-fit:contain;background:#0d1117;position:absolute;
                top:0;left:0;" id="cmpAfterImg"/>
  </div>
  <div id="cmpHandle"
       style="position:absolute;top:0;bottom:0;left:50%;width:3px;
              background:linear-gradient(to bottom,rgba(74,222,128,0.3),rgba(74,222,128,1),rgba(0,229,255,0.8),rgba(74,222,128,1),rgba(74,222,128,0.3));
              cursor:col-resize;display:flex;align-items:center;justify-content:center;
              filter:drop-shadow(0 0 6px rgba(74,222,128,0.70));">
    <div class="cmp-handle-glass">&#8660;</div>
  </div>
  <span style="position:absolute;top:10px;left:10px;background:rgba(0,0,0,0.70);
               backdrop-filter:blur(8px);color:#fff;font-size:10px;font-weight:800;
               padding:3px 12px;border-radius:99px;letter-spacing:0.08em;
               border:1px solid rgba(255,255,255,0.12);">BEFORE</span>
  <span style="position:absolute;top:10px;right:10px;background:rgba(22,163,74,0.80);
               backdrop-filter:blur(8px);color:#fff;font-size:10px;font-weight:800;
               padding:3px 12px;border-radius:99px;letter-spacing:0.08em;
               border:1px solid rgba(74,222,128,0.40);
               box-shadow:0 0 12px rgba(74,222,128,0.40);">AFTER</span>
</div>
<input type="range" min="0" max="100" value="50" id="cmpSlider"
  style="width:100%;margin-top:0.6rem;accent-color:#16a34a;
         height:4px;border-radius:99px;"
  oninput="moveCmp(this.value)"/>
<script>
function moveCmp(v){{
  var pct = v + '%';
  document.getElementById('cmpAfter').style.width = pct;
  document.getElementById('cmpHandle').style.left = pct;
  var w = document.getElementById('cmp').offsetWidth;
  var aw = document.getElementById('cmpAfterImg');
  if(aw) aw.style.width = w + 'px';
}}
</script>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════
# ══════════════════════════════════════════════
#  TOP NAVIGATION BAR (Main App Mode)
# ══════════════════════════════════════════════
SECTIONS = [
    ("upload",    "📤", "Upload & Convert"),
    ("batch",     "📦", "Batch Processing"),
    ("bg_remove", "✂️", "Background Remover"),
    ("ocr",       "🔤", "Text Extractor"),
    ("watermark", "🖊️", "Watermark Studio"),
    ("analytics", "📊", "Analytics"),
    ("history",   "🕒", "History"),
    ("settings",  "⚙️", "Settings"),
]

def render_app_top_nav() -> None:
    """Render the top horizontal navigation bar for the inside app."""
    # ── 1. Top Bar: Logo + Brand on left, User Avatar / Auth on right ──
    top_col1, top_col2 = st.columns([1.2, 1])
    with top_col1:
        st.markdown("""
<div style="display:flex;align-items:center;gap:0.7rem;padding:0.4rem 0;">
  <span style="font-size:1.5rem;">🌿</span>
  <span style="font-weight:800;font-size:1.25rem;letter-spacing:-0.02em;">Image Studio Pro</span>
  <span style="background:rgba(16,185,129,0.12);color:#10B981;padding:2px 8px;border-radius:99px;font-size:0.75rem;font-weight:700;border:1px solid rgba(16,185,129,0.25);">v3.0</span>
</div>
        """, unsafe_allow_html=True)
    with top_col2:
        if AUTH_AVAILABLE and is_logged_in():
            user = get_current_user()
            email = user.get("email", "user@example.com")
            initials = (email[:2] if len(email) >= 2 else "US").upper()
            u_col1, u_col2 = st.columns([2.5, 1])
            with u_col1:
                st.markdown(f"""
<div style="display:flex;align-items:center;justify-content:flex-end;gap:0.6rem;padding-top:0.45rem;">
  <div style="width:30px;height:30px;border-radius:50%;background:#10B981;color:#FFFFFF;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:0.80rem;box-shadow:0 2px 6px rgba(16,185,129,0.3);">{initials}</div>
  <span style="font-size:0.86rem;font-weight:600;color:#94A3B8;">{email}</span>
</div>
                """, unsafe_allow_html=True)
            with u_col2:
                if st.button("Log out", key="app_top_logout", type="secondary", use_container_width=True):
                    sign_out()
                    st.session_state.history        = []
                    st.session_state.analytics      = []
                    st.session_state.history_seeded = False
                    st.session_state.entered_app    = True
                    st.rerun()
        elif AUTH_AVAILABLE:
            _, lg_btn_col, su_btn_col = st.columns([2, 1, 1.25])
            with lg_btn_col:
                st.markdown('<div class="nav-login-btn-anchor"></div>', unsafe_allow_html=True)
                if st.button("Log In", key="app_top_login", use_container_width=True):
                    st.session_state.app_auth = "login" if st.session_state.get("app_auth") != "login" else None
                    st.rerun()
            with su_btn_col:
                st.markdown('<div class="violet-outline-btn-anchor"></div>', unsafe_allow_html=True)
                if st.button("Sign Up Free", key="app_top_signup", use_container_width=True):
                    st.session_state.app_auth = "signup" if st.session_state.get("app_auth") != "signup" else None
                    st.rerun()

    # ── Optional Inline Auth Drawer for In-App ──
    if AUTH_AVAILABLE and not is_logged_in() and st.session_state.get("app_auth"):
        _, auth_col, _ = st.columns([1.2, 2.6, 1.2])
        with auth_col:
            if st.session_state.app_auth == "login":
                with st.form("app_login_form"):
                    st.markdown("""
<div class="auth-header">
  <div class="auth-header-title">🔑 Welcome Back</div>
  <div class="auth-header-caption">Log in to sync your conversion history and preferences.</div>
</div>
                    """, unsafe_allow_html=True)
                    l_email = st.text_input("Email Address", placeholder="name@example.com", key="a_login_email")
                    l_pw = st.text_input("Password", type="password", placeholder="••••••••", key="a_login_pw")
                    l_sub = st.form_submit_button("Sign In →", use_container_width=True)
                    if l_sub:
                        ok, msg = sign_in(l_email, l_pw)
                        if ok:
                            st.session_state.app_auth = None
                            st.rerun()
                        else:
                            st.error(msg)
            elif st.session_state.app_auth == "signup":
                with st.form("app_signup_form"):
                    st.markdown("""
<div class="auth-header">
  <div class="auth-header-title">✨ Create Free Account</div>
  <div class="auth-header-caption">No credit card required. Free forever with 100% local privacy.</div>
</div>
                    """, unsafe_allow_html=True)
                    s_uname = st.text_input("Choose Username", placeholder="creative_user", key="a_signup_username")
                    s_email = st.text_input("Email Address", placeholder="name@example.com", key="a_signup_email")
                    s_pw = st.text_input("Password", type="password", placeholder="••••••••", key="a_signup_pw")
                    s_sub = st.form_submit_button("Create Account →", use_container_width=True)
                    if s_sub:
                        ok, msg = sign_up(s_email, s_pw, s_uname)
                        if ok:
                            st.success(msg)
                            st.session_state.app_auth = None
                            st.rerun()
                        else:
                            st.error(msg)
            st.write("")

    st.markdown("""
<div style="border-bottom: 1px solid rgba(0,0,0,0.08); margin: 0.4rem 0 1rem;"></div>
    """, unsafe_allow_html=True)

    # ── 2. Top Navigation Bar (8 Pills in 2 clean rows of 4) ──
    row1 = SECTIONS[:4]
    row2 = SECTIONS[4:]
    for row in [row1, row2]:
        cols = st.columns(4)
        for idx, (sid, icon, label) in enumerate(row):
            with cols[idx]:
                is_active = (st.session_state.section == sid)
                btn_type = "primary" if is_active else "secondary"
                if st.button(f"{icon}  {label}", key=f"topnav_{sid}", type=btn_type, use_container_width=True):
                    st.session_state.section = sid
                    st.rerun()

    st.markdown("""
<div style="margin-bottom: 1.5rem;"></div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════
#  MARKETING LANDING PAGE
# ══════════════════════════════════════════════
#  MARKETING LANDING PAGE — STEP 1: NAV + HERO
# ══════════════════════════════════════════════
def render_landing_page() -> None:
    """Render the high-impact marketing landing page before entering the tool."""

    # ── 1. Dark Hero Banner Section (Navbar + Hero + CTAs + Trust Badges) ──
    with st.container():
        st.markdown('<div class="hero-banner-anchor"></div>', unsafe_allow_html=True)

        # ── Top Navbar ──
        # ── Top Navbar ──
        nav_col1, nav_col2, nav_col3 = st.columns([3.2, 3.8, 3.0])
        with nav_col1:
            st.markdown(
                '<div style="display:flex;align-items:center;gap:8px;height:40px;">'
                '<span style="font-size:1.35rem;">🌿</span>'
                '<span class="hero-brand-title" style="font-weight:800;font-size:1.18rem;letter-spacing:-0.025em;color:#0F172A;">Image Studio Pro</span>'
                '<span style="font-size:0.70rem;font-weight:700;padding:2px 8px;border-radius:99px;background:rgba(16,185,129,0.12);color:#10B981;border:1px solid rgba(16,185,129,0.25);">v3.0</span>'
                '</div>',
                unsafe_allow_html=True,
            )
        with nav_col2:
            st.markdown(
                '<div class="nav-links-center" style="display:flex;justify-content:center;align-items:center;gap:22px;height:40px;">'
                '<a href="#features" class="nav-link-item">Features</a>'
                '<a href="#workflows" class="nav-link-item">Workflows</a>'
                '<a href="#why-us" class="nav-link-item">Why Us</a>'
                '<a href="#faq" class="nav-link-item">FAQ</a>'
                '</div>',
                unsafe_allow_html=True,
            )
        with nav_col3:
            if AUTH_AVAILABLE:
                nc1, nc2 = st.columns([1, 1.25])
                with nc1:
                    st.markdown('<div class="nav-login-btn-anchor"></div>', unsafe_allow_html=True)
                    if st.button("Log In", key="nav_login_btn", use_container_width=True):
                        st.session_state.landing_auth = "login" if st.session_state.landing_auth != "login" else None
                        st.rerun()
                with nc2:
                    st.markdown('<div class="violet-outline-btn-anchor"></div>', unsafe_allow_html=True)
                    if st.button("Sign Up Free", key="nav_signup_btn", use_container_width=True):
                        st.session_state.landing_auth = "signup" if st.session_state.landing_auth != "signup" else None
                        st.rerun()
            else:
                if st.button("Launch Studio →", key="nav_enter_btn", type="primary", use_container_width=True):
                    st.session_state.entered_app = True
                    st.rerun()

        # ── Optional Inline Auth Drawer (Styled Card) ──
        if AUTH_AVAILABLE and st.session_state.landing_auth:
            _, auth_col, _ = st.columns([1.2, 2.6, 1.2])
            with auth_col:
                if st.session_state.landing_auth == "login":
                    with st.form("landing_login_form"):
                        st.markdown("""
<div class="auth-header">
  <div class="auth-header-title">🔑 Welcome Back</div>
  <div class="auth-header-caption">Log in to sync your conversion history and preferences.</div>
</div>
                        """, unsafe_allow_html=True)
                        l_email = st.text_input("Email Address", placeholder="name@example.com", key="l_login_email")
                        l_pw = st.text_input("Password", type="password", placeholder="••••••••", key="l_login_pw")
                        l_sub = st.form_submit_button("Sign In & Launch Studio →", use_container_width=True)
                        if l_sub:
                            ok, msg = sign_in(l_email, l_pw)
                            if ok:
                                st.session_state.entered_app = True
                                st.session_state.landing_auth = None
                                st.rerun()
                            else:
                                st.error(msg)
                elif st.session_state.landing_auth == "signup":
                    with st.form("landing_signup_form"):
                        st.markdown("""
<div class="auth-header">
  <div class="auth-header-title">✨ Create Free Account</div>
  <div class="auth-header-caption">No credit card required. Free forever with 100% local privacy.</div>
</div>
                        """, unsafe_allow_html=True)
                        s_uname = st.text_input("Choose Username", placeholder="creative_user", key="l_signup_username")
                        s_email = st.text_input("Email Address", placeholder="name@example.com", key="l_signup_email")
                        s_pw = st.text_input("Password", type="password", placeholder="••••••••", key="l_signup_pw")
                        st.markdown('<div class="violet-btn-anchor"></div>', unsafe_allow_html=True)
                        s_sub = st.form_submit_button("Create Account & Get Started →", use_container_width=True)
                        if s_sub:
                            ok, msg = sign_up(s_email, s_pw, s_uname)
                            if ok:
                                st.success(msg)
                                st.session_state.entered_app = True
                                st.session_state.landing_auth = None
                                st.rerun()
                            else:
                                st.error(msg)
                st.write("")
                st.write("")

        # ── 2. Hero Section ──
        st.markdown("""
<div class="landing-hero-box">
  <div class="hero-pill-badge">
    ⚡ 100% Local AI Image Studio &middot; Zero Cloud Uploads
  </div>
  <div class="hero-headline">
    Transform, Clean &amp; Convert<br/>Images Instantly.
  </div>
  <div class="hero-subhead">
    The privacy-first image toolkit with AI background removal, OCR text extraction, smart resizing, and watermarking — running 100% on your device.
  </div>
</div>
        """, unsafe_allow_html=True)

        # ── Two CTA buttons side by side ──
        _, cta_c1, cta_c2, _ = st.columns([1.5, 2.5, 2.5, 1.5])
        with cta_c1:
            st.markdown('<div class="hero-cta-btn-anchor"></div>', unsafe_allow_html=True)
            if st.button("🚀  Launch Studio (Instant)", key="hero_cta_primary", type="primary", use_container_width=True):
                st.session_state.entered_app = True
                st.rerun()
        with cta_c2:
            if AUTH_AVAILABLE:
                st.markdown('<div class="hero-cta-btn-anchor"></div><div class="violet-btn-anchor"></div>', unsafe_allow_html=True)
                if st.button("✨  Create Free Account", key="hero_cta_secondary", use_container_width=True):
                    st.session_state.landing_auth = "signup"
                    st.rerun()
            else:
                st.markdown('<div class="hero-cta-btn-anchor"></div>', unsafe_allow_html=True)
                if st.button("📖  Explore Features", key="hero_cta_features", type="secondary", use_container_width=True):
                    st.session_state.entered_app = True
                    st.rerun()

        # ── Trust points row below CTAs ──
        st.markdown("""
<div class="trust-row">
  <div class="trust-item">🔒 100% Private (Runs on Device)</div>
  <div class="trust-item">⚡ Instant Processing</div>
  <div class="trust-item">🆓 No Sign-up Required</div>
  <div class="trust-item">📐 7 Presets &amp; WebP</div>
</div>
        """, unsafe_allow_html=True)

    # ── 3. Feature Suite Grid (8 cards) ──
    st.markdown("""
<div id="features" class="section-head-wrap">
  <h2>Tools for Every Creative Need</h2>
  <p>Eight powerful utilities built for creators, marketers, designers, and developers.</p>
</div>
    """, unsafe_allow_html=True)

    features = [
        ("upload",    "📤", "Upload & Convert",     "Resize to social presets, compress, and switch between JPEG, PNG, and WebP."),
        ("batch",     "📦", "Batch Processing",     "Convert dozens of photos in one single run with unified quality settings."),
        ("bg_remove", "✂️",  "Background Remover",   "AI-driven transparent PNG generation powered by deep learning u2net."),
        ("ocr",       "🔤", "Text Extractor (OCR)", "Extract editable text from scanned documents, screenshots, and receipts."),
        ("watermark", "🖊️",  "Watermark Studio",     "Protect assets with customizable copyright text or brand logo overlays."),
        ("analytics", "📊", "Analytics Dashboard",  "Inspect real-time session stats, space saved, and export logs to CSV."),
        ("history",   "🕓", "Download History",     "Review previous session conversions with one-click re-download."),
        ("settings",  "⚙️",  "Settings & Themes",    "Toggle Dark/Light modes, clear session memory, and review privacy docs."),
    ]

    color_cycle = ["emerald", "violet", "sky"]

    # Row 1 (4 columns)
    f_cols1 = st.columns(4)
    for idx, (sid, icon, title, desc) in enumerate(features[:4]):
        var = color_cycle[idx % len(color_cycle)]
        with f_cols1[idx]:
            st.markdown(f"""
<div class="feat-card feat-card-{var}">
  <div>
    <div class="feat-icon feat-icon-{var}">{icon}</div>
    <div class="feat-title">{title}</div>
    <div class="feat-desc">{desc}</div>
  </div>
</div>
            """, unsafe_allow_html=True)
            if st.button(f"Open {title.split(' ')[0]} →", key=f"feat_btn_{sid}", type="primary", use_container_width=True):
                st.session_state.section = sid
                st.session_state.entered_app = True
                st.rerun()

    st.write("")

    # Row 2 (4 columns)
    f_cols2 = st.columns(4)
    for idx, (sid, icon, title, desc) in enumerate(features[4:]):
        var = color_cycle[(idx + 4) % len(color_cycle)]
        with f_cols2[idx]:
            st.markdown(f"""
<div class="feat-card feat-card-{var}">
  <div>
    <div class="feat-icon feat-icon-{var}">{icon}</div>
    <div class="feat-title">{title}</div>
    <div class="feat-desc">{desc}</div>
  </div>
</div>
            """, unsafe_allow_html=True)
            if st.button(f"Open {title.split(' ')[0]} →", key=f"feat_btn_{sid}", type="primary", use_container_width=True):
                st.session_state.section = sid
                st.session_state.entered_app = True
                st.rerun()

    # ── 4. Workflow Showcases (Starting with Workflow 1) ──
    st.markdown("""
<div id="workflows" class="section-head-wrap" style="margin-top: 4rem;">
  <h2>Powerful Workflows, Simplified</h2>
  <p>See how Image Studio Pro streamlines everyday media preparation.</p>
</div>
    """, unsafe_allow_html=True)

    # Workflow 1: AI Background Removal (Left: Description, Right: Mockup)
    w1_left, w1_right = st.columns([1.2, 1], gap="large")
    with w1_left:
        st.markdown("""
<div style="padding-top: 1rem;">
  <span class="workflow-badge workflow-badge-emerald">AI Vision Model</span>
  <div class="workflow-title">Remove backgrounds in under 2 seconds.</div>
  <div class="workflow-desc">No manual clipping or lasso tools. Built-in neural networks isolate people, products, and objects cleanly with sub-pixel edge detection.</div>
</div>
        """, unsafe_allow_html=True)
        if st.button("Try Background Remover →", key="wf_btn_bg", type="primary", use_container_width=False):
            st.session_state.section = "bg_remove"
            st.session_state.entered_app = True
            st.rerun()

    with w1_right:
        st.markdown("""
<div class="mockup-canvas">
  <div style="font-size:3rem;margin-bottom:0.5rem;">✂️</div>
  <div style="font-weight:700;font-size:1.15rem;margin-bottom:6px;">Auto Cutout Engine</div>
  <div style="font-size:0.88rem;color:#94A3B8;line-height:1.45;">Generates clean transparent RGBA PNGs locally on your hardware.</div>
  <div style="margin-top:14px;padding:6px 14px;background:rgba(16,185,129,0.12);color:#10B981;border-radius:8px;font-size:0.82rem;font-weight:700;display:inline-block;">✓ Zero Data Uploaded</div>
</div>
        """, unsafe_allow_html=True)

    st.write("")
    st.write("")

    # Workflow 2: Converter & Presets (Left: Mockup, Right: Description)
    w2_left, w2_right = st.columns([1, 1.2], gap="large")
    with w2_left:
        st.markdown("""
<div class="mockup-canvas">
  <div style="font-size:3rem;margin-bottom:0.5rem;">📐</div>
  <div style="font-weight:700;font-size:1.15rem;margin-bottom:6px;">Social Presets Matrix</div>
  <div style="font-size:0.88rem;color:#94A3B8;line-height:1.45;">Instagram, YouTube, Twitter & HD Wallpaper dimensions.</div>
  <div style="margin-top:14px;padding:6px 14px;background:rgba(124,58,237,0.12);color:#7C3AED;border-radius:8px;font-size:0.82rem;font-weight:700;display:inline-block;">⚡ Save Up to 80% Space via WebP</div>
</div>
        """, unsafe_allow_html=True)
    with w2_right:
        st.markdown("""
<div style="padding-top: 1rem;">
  <span class="workflow-badge workflow-badge-violet">Smart Compression</span>
  <div class="workflow-title">Resize, re-encode, and optimize in one step.</div>
  <div class="workflow-desc">Convert uncompressed PNGs and high-res JPEGs to modern WebP with variable quality sliders and aspect ratio locks.</div>
</div>
        """, unsafe_allow_html=True)
        if st.button("Try Image Converter →", key="wf_btn_convert", type="primary", use_container_width=False):
            st.session_state.section = "upload"
            st.session_state.entered_app = True
            st.rerun()

    st.write("")
    st.write("")

    # Workflow 3: OCR Extractor (Left: Description, Right: Mockup)
    w3_left, w3_right = st.columns([1.2, 1], gap="large")
    with w3_left:
        st.markdown("""
<div style="padding-top: 1rem;">
  <span class="workflow-badge workflow-badge-emerald">Neural OCR</span>
  <div class="workflow-title">Turn visual text into editable copy.</div>
  <div class="workflow-desc">Extract text from scanned documents, receipts, screenshots, and infographics directly into editable text areas and downloadable .txt files.</div>
</div>
        """, unsafe_allow_html=True)
        if st.button("Try Text Extractor →", key="wf_btn_ocr", type="primary", use_container_width=False):
            st.session_state.section = "ocr"
            st.session_state.entered_app = True
            st.rerun()
    with w3_right:
        st.markdown("""
<div class="mockup-canvas">
  <div style="font-size:3rem;margin-bottom:0.5rem;">🔤</div>
  <div style="font-weight:700;font-size:1.15rem;margin-bottom:6px;">EasyOCR Engine</div>
  <div style="font-size:0.88rem;color:#94A3B8;line-height:1.45;">Deep neural network for line & word boundary detection.</div>
  <div style="margin-top:14px;padding:6px 14px;background:rgba(16,185,129,0.12);color:#10B981;border-radius:8px;font-size:0.82rem;font-weight:700;display:inline-block;">📄 Export to Plain Text (.txt)</div>
</div>
        """, unsafe_allow_html=True)

    st.write("")
    st.write("")

    # Workflow 4: Watermark Studio (Left: Mockup, Right: Description)
    w4_left, w4_right = st.columns([1, 1.2], gap="large")
    with w4_left:
        st.markdown("""
<div class="mockup-canvas">
  <div style="font-size:3rem;margin-bottom:0.5rem;">🖊️</div>
  <div style="font-weight:700;font-size:1.15rem;margin-bottom:6px;">Brand Stamp Overlay</div>
  <div style="font-size:0.88rem;color:#94A3B8;line-height:1.45;">Opacity, 360° rotation, and 9-point snapping controls.</div>
  <div style="margin-top:14px;padding:6px 14px;background:rgba(124,58,237,0.12);color:#7C3AED;border-radius:8px;font-size:0.82rem;font-weight:700;display:inline-block;">🔒 Text & Logo PNG Compositing</div>
</div>
        """, unsafe_allow_html=True)
    with w4_right:
        st.markdown("""
<div style="padding-top: 1rem;">
  <span class="workflow-badge workflow-badge-violet">Asset Protection</span>
  <div class="workflow-title">Protect and watermark your creative work.</div>
  <div class="workflow-desc">Add customizable copyright signatures or transparent brand logos with fine-tuned opacity, scale, and placement controls.</div>
</div>
        """, unsafe_allow_html=True)
        if st.button("Try Watermark Studio →", key="wf_btn_wm", type="primary", use_container_width=False):
            st.session_state.section = "watermark"
            st.session_state.entered_app = True
            st.rerun()

    # ── 5. Why Image Studio Pro ──
    st.markdown("""
<div id="why-us" class="section-head-wrap" style="margin-top: 4.5rem;">
  <h2>Why Image Studio Pro?</h2>
  <p>Honest, privacy-first software engineered for zero data leaks.</p>
</div>
    """, unsafe_allow_html=True)

    why_cols = st.columns(3)
    with why_cols[0]:
        st.markdown("""
<div class="why-card">
  <div class="why-icon">🛡️</div>
  <div class="why-title">100% Local & Private</div>
  <div class="why-desc">Your photos never touch an external cloud server. Everything runs directly inside your computer's local Python runtime.</div>
</div>
        """, unsafe_allow_html=True)
    with why_cols[1]:
        st.markdown("""
<div class="why-card">
  <div class="why-icon">🧠</div>
  <div class="why-title">Real Local AI Models</div>
  <div class="why-desc">Powered by production-grade neural networks (u2net and EasyOCR) running natively on your hardware.</div>
</div>
        """, unsafe_allow_html=True)
    with why_cols[2]:
        st.markdown("""
<div class="why-card">
  <div class="why-icon">⚡</div>
  <div class="why-title">Free, No Limits</div>
  <div class="why-desc">No subscriptions, no artificial file size caps, and no forced app branding or watermarks on your exported images.</div>
</div>
        """, unsafe_allow_html=True)

    # ── 6. FAQ Accordion ──
    st.markdown("""
<div id="faq" class="section-head-wrap" style="margin-top: 4.5rem;">
  <h2>Frequently Asked Questions</h2>
  <p>Everything you need to know about Image Studio Pro.</p>
</div>
    """, unsafe_allow_html=True)

    with st.expander("❓ Are my photos uploaded to any third-party server?"):
        st.write("Never. Every single operation — from image compression to AI background removal and OCR — runs 100% inside your local Python runtime. No external image servers are ever contacted.")

    with st.expander("❓ Do I need an account to use Image Studio Pro?"):
        st.write("No! You can use every feature without creating an account. Optional Supabase login is only provided if you want to sync your download history across visits.")

    with st.expander("❓ Which file formats are supported?"):
        st.write("Image Studio Pro supports JPEG/JPG, PNG, and modern WEBP formats for both input uploads and converted downloads.")

    with st.expander("❓ Why does the first AI background removal or OCR take a moment?"):
        st.write("On the first run during a session, the neural network models (u2net and EasyOCR) load into local system memory. All subsequent operations during that session execute instantly.")

    with st.expander("❓ Can I process multiple images simultaneously?"):
        st.write("Yes! Use the **Batch Processing** section to select and convert dozens of images at once with unified format and quality presets.")

    # ── 7. Bottom Hero CTA ──
    st.markdown("""
<div class="bottom-cta-banner">
  <div class="bottom-cta-title">Ready to transform your images with total privacy?</div>
  <div class="bottom-cta-sub">Launch Image Studio Pro now — free forever with no sign-up required.</div>
</div>
    """, unsafe_allow_html=True)

    _, bcta_col, _ = st.columns([2, 3, 2])
    with bcta_col:
        if st.button("🚀  Launch Image Studio Now", key="bottom_cta_launch", type="primary", use_container_width=True):
            st.session_state.entered_app = True
            st.rerun()

    # ── 8. Footer ──
    st.markdown("""
<div class="landing-footer">
  <strong>🌿 Image Studio Pro v3.0</strong> &middot; Built with Python, Streamlit, Pillow, rembg, EasyOCR &amp; Plotly<br/>
  100% Open Source &middot; Fully Local Processing &middot; Privacy Guaranteed
</div>
    """, unsafe_allow_html=True)






# ══════════════════════════════════════════════
#  GLOBAL SCRIPT (Tilt, Nav Active & Scroll Reveal)
# ══════════════════════════════════════════════
st.markdown("""
<script>
(function(){
  /* ── Hero 3D Tilt ── */
  function initHeroTilt(){
    document.querySelectorAll('.hero-3d-wrap, .showcase-stage').forEach(function(el){
      if(el.__tiltBound) return;
      el.__tiltBound = true;
      el.addEventListener('mousemove',function(e){
        var r=el.getBoundingClientRect();
        var dx=(e.clientX-(r.left+r.width/2))/(r.width/2);
        var dy=(e.clientY-(r.top+r.height/2))/(r.height/2);
        el.style.transform='perspective(1200px) rotateY('+(dx*3)+'deg) rotateX('+(-dy*3)+'deg)';
        el.style.transition='transform 0.10s ease';
      });
      el.addEventListener('mouseleave',function(){
        el.style.transform='perspective(1200px) rotateY(0) rotateX(0)';
        el.style.transition='transform 0.45s ease';
      });
    });
  }

  /* ── Sidebar Active Nav Indicator ── */
  function markActiveNav(){
    var btns = document.querySelectorAll('[data-testid="stSidebar"] button');
    btns.forEach(function(b){
      b.classList.remove('nav-active');
      if((b.innerText||b.textContent||'').trimStart().charCodeAt(0) === 0x25B6){
        b.classList.add('nav-active');
      }
    });
  }

  /* ── Scroll Reveal via IntersectionObserver ── */
  var revealObserver = null;
  function initScrollReveal(){
    if(!window.IntersectionObserver) return;
    if(!revealObserver){
      revealObserver = new IntersectionObserver(function(entries){
        entries.forEach(function(entry){
          if(entry.isIntersecting){
            entry.target.classList.add('is-revealed');
          }
        });
      }, { threshold: 0.08 });
    }
    document.querySelectorAll('.reveal-on-scroll:not(.is-revealed)').forEach(function(el){
      revealObserver.observe(el);
    });
  }

  function handleMutations(){
    initHeroTilt();
    markActiveNav();
    initScrollReveal();
  }

  if(!window.__stAppObs){
    var _t = null;
    window.__stAppObs = new MutationObserver(function(){
      clearTimeout(_t);
      _t = setTimeout(handleMutations, 60);
    });
    window.__stAppObs.observe(document.body, {childList:true, subtree:true});
  }

  handleMutations();
})();
</script>
""", unsafe_allow_html=True)



# ══════════════════════════════════════════════
#  SECTION 1 — UPLOAD & CONVERT  (unchanged)
# ══════════════════════════════════════════════
def render_upload() -> None:
    """Render the single-image resize/convert section."""
    # ── Section Header — Modern Clean SaaS ──
    st.markdown("""
<div class="app-header-wrap">
  <div class="app-header-title">📤 Upload &amp; Convert</div>
  <div class="app-header-sub">Resize, compress, and switch between JPEG, PNG, and modern WebP with zero cloud uploads.</div>
  <div class="app-badge-row">
    <span class="app-pill-badge">🔒 100% Private</span>
    <span class="app-pill-badge">⚡ Instant Processing</span>
    <span class="app-pill-badge">📐 7 Presets</span>
    <span class="app-pill-badge">✨ WebP Ready</span>
  </div>
</div>
    """, unsafe_allow_html=True)

    # ── Upload ──
    st.markdown("### 📤 Upload Image")
    uploaded = st.file_uploader(
        "Drop your image here — JPG, PNG or WEBP",
        type=["jpg", "jpeg", "png", "webp"],
        key="main_upload",
    )

    if not uploaded:
        st.info("⬆️ Upload a JPG, PNG, or WEBP image above to get started.", icon="📸")
        return

    # ── Load image ──
    try:
        raw = uploaded.read()
        img = load_image(raw)
    except Exception as exc:
        st.error(f"Could not load image: {exc}")
        return

    orig_w, orig_h = img.size
    orig_fmt = (img.format or "JPEG").upper()

    # File info metrics
    st.markdown("#### File Info")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("📄 Name",       uploaded.name[:18] + "…" if len(uploaded.name) > 18 else uploaded.name)
    c2.metric("📐 Dimensions", f"{orig_w} × {orig_h} px")
    c3.metric("🎨 Format",     orig_fmt)
    c4.metric("💾 Size",       format_bytes(len(raw)))

    st.write("")
    col_left, col_right = st.columns([1.1, 1], gap="large")

    # ── Original preview ──
    with col_left:
        st.markdown("### 🖼️ Original Preview")
        st.image(img)

    # ── Settings form ──
    with col_right:
        st.markdown("### ⚙️ Resize & Convert Settings")
        with st.form("convert_form"):
            preset     = st.selectbox("Quick Preset", list(PRESETS.keys()), index=0)
            preset_val = PRESETS[preset]

            fc1, fc2 = st.columns(2)
            with fc1:
                w = st.number_input("Width (px)", 1, 10000,
                                    value=preset_val[0] if preset_val else orig_w)
            with fc2:
                h = st.number_input("Height (px)", 1, 10000,
                                    value=preset_val[1] if preset_val else orig_h)

            keep_aspect = st.checkbox("🔒 Maintain aspect ratio", value=True)
            out_fmt     = st.selectbox("Output Format", ["JPEG", "PNG", "WEBP"])
            quality     = st.slider("Quality (JPEG/WEBP)", 10, 100, 85,
                                    help="PNG is always lossless — quality setting ignored.")
            submitted   = st.form_submit_button("⚡  Convert Image",
                                                use_container_width=True)

    # ── Result ──
    if submitted:
        with st.spinner("Processing image…"):
            resized   = resize_image(img, int(w), int(h), keep_aspect)
            out_bytes = save_image(resized, out_fmt, quality)

        rw, rh    = resized.size
        saved_pct = compression_pct(len(raw), len(out_bytes))

        st.success("✅ Image processed successfully!", icon="🎉")

        # Stats
        st.markdown("#### 📊 Results")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("New Size",       format_bytes(len(out_bytes)))
        m2.metric("Original Size",  format_bytes(len(raw)))
        m3.metric("New Dimensions", f"{rw} × {rh}")
        m4.metric("Space Saved",    f"{saved_pct}%" if saved_pct > 0 else "—")

        st.write("")

        # Before / After comparison slider (JS required)
        st.markdown("#### 🔍 Before / After Comparison")
        b64_before = image_to_b64(img, "PNG")
        b64_after  = image_to_b64(resized, out_fmt)
        comparison_slider(b64_before, b64_after)

        st.write("")

        # Download
        ext     = FORMAT_EXT.get(out_fmt, "jpg")
        stem    = uploaded.name.rsplit(".", 1)[0]
        dl_name = f"{stem}_{rw}x{rh}.{ext}"
        st.download_button(
            f"⬇️  Download {out_fmt} — {format_bytes(len(out_bytes))}",
            data=out_bytes,
            file_name=dl_name,
            mime={"JPEG": "image/jpeg", "PNG": "image/png", "WEBP": "image/webp"}[out_fmt],
            use_container_width=True,
        )

        # ── History ──
        st.session_state.history.insert(0, {
            "name":     dl_name,
            "orig_fmt": orig_fmt,
            "out_fmt":  out_fmt,
            "orig_sz":  len(raw),
            "out_sz":   len(out_bytes),
            "dims":     f"{rw} × {rh}",
            "ts":       datetime.now().isoformat(),
        })
        st.session_state.history = st.session_state.history[:30]
        if AUTH_AVAILABLE:                                    # ── auth: persist entry for logged-in users
            save_history_entry(st.session_state.history[0])

        # ── Analytics ──
        log_operation(OP_RESIZE, len(raw), len(out_bytes), out_fmt, uploaded.name)


# ══════════════════════════════════════════════
#  SECTION 2 — BATCH PROCESSING  (unchanged + analytics)
# ══════════════════════════════════════════════
def render_batch() -> None:
    """Render the multi-file batch conversion section."""
    section_header("📦", "Batch Processing",
                   "Convert multiple images at once with the same settings.")

    st.markdown("### ⚙️ Batch Settings")
    bc1, bc2 = st.columns(2)
    with bc1:
        b_fmt = st.selectbox("Output Format", ["JPEG", "PNG", "WEBP"], key="b_fmt")
    with bc2:
        b_quality = st.slider("Quality", 10, 100, 85, key="b_quality")

    st.markdown("### 📁 Upload Images")
    files = st.file_uploader(
        "Select multiple images",
        type=["jpg", "jpeg", "png", "webp"],
        accept_multiple_files=True,
        key="batch_upload",
    )

    if not files:
        st.info("⬆️ Upload multiple images above to begin batch conversion.", icon="📦")
        return

    st.write(f"**{len(files)} image(s) selected**")

    if st.button(f"⚡  Convert All {len(files)} Images",
                 type="primary", use_container_width=True, key="batch_go"):
        results = []
        prog = st.progress(0, "Starting…")
        for i, f in enumerate(files):
            raw = f.read()
            img = load_image(raw)
            out = save_image(img, b_fmt, b_quality)
            iw, ih = img.size
            results.append({
                "name":    f.name,
                "bytes":   out,
                "fmt":     b_fmt,
                "orig_sz": len(raw),
                "out_sz":  len(out),
                "dims":    f"{iw} × {ih}",
            })
            prog.progress((i + 1) / len(files),
                          f"Processed {i + 1} / {len(files)}: {f.name}")
            # ── History ──
            st.session_state.history.insert(0, {
                "name":     f.name,
                "orig_fmt": (img.format or "JPEG").upper(),
                "out_fmt":  b_fmt,
                "orig_sz":  len(raw),
                "out_sz":   len(out),
                "dims":     f"{iw} × {ih}",
                "ts":       datetime.now().isoformat(),
            })
            if AUTH_AVAILABLE:                                # ── auth: persist entry for logged-in users
                save_history_entry(st.session_state.history[0])
            # ── Analytics ──
            log_operation(OP_BATCH, len(raw), len(out), b_fmt, f.name)

        st.session_state.batch_results = results
        st.success(f"✅ {len(results)} images converted successfully!")

    # Results table
    if st.session_state.batch_results:
        st.markdown("### ✅ Converted Images")
        st.write("Download each converted file below:")
        st.divider()
        for item in st.session_state.batch_results:
            rc1, rc2, rc3, rc4, rc5 = st.columns([3, 1, 1, 1, 1])
            rc1.write(f"**{item['name']}**")
            rc2.write(item["dims"])
            rc3.write(item["fmt"])
            rc4.write(f"**{format_bytes(item['out_sz'])}**")
            with rc5:
                ext = FORMAT_EXT.get(item["fmt"], "jpg")
                st.download_button(
                    "⬇ Download",
                    data=item["bytes"],
                    file_name=f"{item['name'].rsplit('.', 1)[0]}.{ext}",
                    mime=f"image/{ext}",
                    key=f"dl_{item['name']}",
                    use_container_width=True,
                )
            st.divider()


# ══════════════════════════════════════════════
#  SECTION 3 — BACKGROUND REMOVER  (NEW)
# ══════════════════════════════════════════════
def render_bg_remove() -> None:
    """Render the AI background removal section."""
    section_header("✂️", "Background Remover",
                   "Remove image backgrounds instantly using AI (rembg · u2net model).")

    # ── Dependency check ──
    if not REMBG_AVAILABLE:
        st.error(
            "**rembg is not installed.**  \n"
            "Run the following command and restart the app:  \n"
            "```\npip install rembg\n```",
            icon="❌",
        )
        return

    st.markdown("### 📤 Upload Image")
    uploaded = st.file_uploader(
        "Drop your image here — JPG, PNG or WEBP",
        type=["jpg", "jpeg", "png", "webp"],
        key="bg_upload",
    )

    if not uploaded:
        st.info(
            "⬆️ Upload an image above.  \n"
            "**Note:** The first run downloads the AI model (~170 MB). Subsequent runs are instant.",
            icon="✂️",
        )
        return

    raw = uploaded.read()
    orig_size_str = get_file_size(raw)

    # ── Process button ──
    if st.button("🪄  Remove Background", type="primary", use_container_width=True, key="bg_go"):
        with st.spinner("🧠 AI is removing the background… (first run may take a moment to load the model)"):
            try:
                out_bytes, elapsed = remove_background(raw)
            except Exception as exc:
                st.error(f"Background removal failed: {exc}", icon="❌")
                return

        # ── History ──
        _bg_src = Image.open(io.BytesIO(raw))
        _bg_w, _bg_h = _bg_src.size
        st.session_state.history.insert(0, {
            "name":     uploaded.name,
            "orig_fmt": uploaded.name.rsplit(".", 1)[-1].upper(),
            "out_fmt":  "PNG",
            "orig_sz":  len(raw),
            "out_sz":   len(out_bytes),
            "dims":     f"{_bg_w} × {_bg_h}",
            "ts":       datetime.now().isoformat(),
        })
        if AUTH_AVAILABLE:                                    # ── auth: persist for logged-in users
            save_history_entry(st.session_state.history[0])
        st.session_state["_bg_result"]   = out_bytes
        st.session_state["_bg_elapsed"]  = elapsed
        st.session_state["_bg_filename"] = uploaded.name
        st.success(f"✅ Background removed in **{elapsed:.2f}s**!", icon="🎉")

    # ── Display results ──
    if st.session_state.get("_bg_result") is not None:
        out_bytes = st.session_state["_bg_result"]
        elapsed   = st.session_state.get("_bg_elapsed", 0.0)
        filename  = st.session_state.get("_bg_filename", uploaded.name)

        out_size_str = get_file_size(out_bytes)

        # Metrics row
        st.markdown("#### 📊 Processing Results")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("⏱️ Processing Time", f"{elapsed:.2f}s")
        m2.metric("📦 Original Size",   orig_size_str)
        m3.metric("✅ Output Size",     out_size_str)
        m4.metric("🖼️ Output Format",   "PNG (RGBA)")

        st.write("")

        # Side-by-side preview
        st.markdown("#### 🖼️ Preview")
        prev_left, prev_right = st.columns(2)

        with prev_left:
            st.markdown("**Original**")
            st.image(raw)

        with prev_right:
            st.markdown("**Background Removed**")
            # Display result image with checkerboard implication via caption
            st.image(out_bytes)
            st.caption("✅ Transparent PNG — checkerboard pattern = transparent areas")

        st.write("")

        # Download button
        btn_params = generate_download_btn_params(out_bytes, filename)
        st.download_button(**btn_params)

        # ── Analytics ──
        log_operation(OP_BG_REMOVE, len(raw), len(out_bytes), "Transparent PNG", filename)


# ══════════════════════════════════════════════
#  SECTION 4 — TEXT EXTRACTOR (OCR)  (NEW)
# ══════════════════════════════════════════════
def render_ocr() -> None:
    """Render the EasyOCR text extraction section."""
    section_header(
        "🔤", "Text Extractor (OCR)",
        "Extract text from images, screenshots, and scanned documents with local EasyOCR.",
        badges=["🔒 100% Private", "🧠 Neural EasyOCR", "📄 Export to .TXT", "✏️ Live Editing"],
    )

    # ── Dependency check ──
    if not EASYOCR_AVAILABLE:
        st.error(
            "**easyocr is not installed.**  \n"
            "Run the following command and restart the app:  \n"
            "```\npip install easyocr\n```",
            icon="❌",
        )
        return

    st.markdown("### 📤 Upload Image")
    uploaded = st.file_uploader(
        "Drop your image here — JPG, PNG or WEBP",
        type=["jpg", "jpeg", "png", "webp"],
        key="ocr_upload",
    )

    if not uploaded:
        st.info(
            "⬆️ Upload an image containing text.  \n"
            "**Note:** The first run downloads the OCR language model (~100–200 MB). "
            "Subsequent runs are instant.",
            icon="🔤",
        )
        return

    raw = uploaded.read()

    # Show image preview
    img = load_image(raw)
    col_img, col_ctrl = st.columns([1.2, 1], gap="large")

    with col_img:
        st.markdown("### 🖼️ Image Preview")
        st.image(img)

    with col_ctrl:
        st.markdown("### ⚙️ OCR Settings")
        st.caption("Currently supports English. Multi-language support can be added via the languages list in ocr_processor.py.")
        st.write("")

        if st.button("🔍  Extract Text", use_container_width=True, type="primary", key="ocr_go"):
            with st.spinner("🧠 Running OCR… (first run may take a moment to load the model)"):
                try:
                    result = extract_text(img, languages=["en"])
                    st.session_state["ocr_result"]   = result
                    st.session_state["ocr_filename"] = uploaded.name
                    st.session_state["ocr_raw_len"]  = len(raw)
                    # ── History ──
                    _ocr_src = Image.open(io.BytesIO(raw))
                    _ocr_w, _ocr_h = _ocr_src.size
                    st.session_state.history.insert(0, {
                        "name":     uploaded.name,
                        "orig_fmt": uploaded.name.rsplit(".", 1)[-1].upper(),
                        "out_fmt":  "TXT",
                        "orig_sz":  len(raw),
                        "out_sz":   len(result["text"].encode("utf-8")),
                        "dims":     f"{_ocr_w} × {_ocr_h}",
                        "ts":       datetime.now().isoformat(),
                    })
                    if AUTH_AVAILABLE:                        # ── auth: persist for logged-in users
                        save_history_entry(st.session_state.history[0])
                    st.success(f"✅ Extracted {result['line_count']} text region(s)!", icon="🎉")
                except Exception as exc:
                    st.error(f"OCR failed: {exc}", icon="❌")
                    return

    # ── Display results ──
    result = st.session_state.get("ocr_result")
    if result is not None:
        st.divider()
        st.markdown("### 📋 OCR Results")

        # Stats row
        conf   = result["confidence"]
        conf_class = (
            "conf-high"   if conf >= 75 else
            "conf-medium" if conf >= 50 else
            "conf-low"
        )
        conf_label = (
            "High Confidence" if conf >= 75 else
            "Medium Confidence" if conf >= 50 else
            "Low Confidence"
        )

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("📝 Words Found",      result["word_count"])
        m2.metric("🔡 Characters",       result["char_count"])
        m3.metric("📄 Text Regions",     result["line_count"])
        m4.metric("✅ Avg Confidence",   f"{conf:.1f}%")

        # Confidence badge
        st.markdown(
            f'<span class="conf-badge {conf_class}">● {conf_label} — {conf:.1f}%</span>',
            unsafe_allow_html=True,
        )
        st.write("")

        # Editable text area
        st.markdown("#### 📝 Extracted Text")
        edited_text = st.text_area(
            "You can edit the text below before downloading:",
            value=result["text"],
            height=300,
            key="ocr_text_area",
        )

        # Download + action row
        dl_col, clear_col = st.columns([2, 1])
        with dl_col:
            txt_bytes = export_text_file(edited_text)
            stem = st.session_state.get("ocr_filename", "ocr_result").rsplit(".", 1)[0]
            st.download_button(
                f"⬇️  Download as TXT — {get_file_size(txt_bytes) if hasattr(get_file_size, '__module__') else f'{len(txt_bytes)} B'}",
                data=txt_bytes,
                file_name=f"{stem}_extracted.txt",
                mime="text/plain",
                use_container_width=True,
            )
        with clear_col:
            if st.button("🗑️ Clear Result", key="ocr_clear", type="secondary", use_container_width=True):
                st.session_state["ocr_result"] = None
                st.rerun()

        # ── Analytics ──
        raw_len = st.session_state.get("ocr_raw_len", 0)
        filename = st.session_state.get("ocr_filename", uploaded.name)
        log_operation(OP_OCR, raw_len, len(txt_bytes), "TXT", filename)


# ══════════════════════════════════════════════
#  SECTION 5 — WATERMARK STUDIO  (NEW)
# ══════════════════════════════════════════════
def render_watermark() -> None:
    """Render the watermark (text + logo) section."""
    section_header(
        "🖊️", "Watermark Studio",
        "Add text or logo watermarks to your images with fine-tuned opacity, scale, and placement controls.",
        badges=["🔒 100% Private", "🔤 Text & Logo Stamping", "🔄 360° Rotation", "📍 9-Point Snapping"],
    )

    st.markdown("### 📤 Upload Base Image")
    uploaded = st.file_uploader(
        "Drop your image here — JPG, PNG or WEBP",
        type=["jpg", "jpeg", "png", "webp"],
        key="wm_upload",
    )

    if not uploaded:
        st.info("⬆️ Upload an image to watermark.", icon="🖊️")
        return

    raw = uploaded.read()
    try:
        base_img = load_image(raw)
    except Exception as exc:
        st.error(f"Could not load image: {exc}", icon="❌")
        return

    # ── Watermark tabs ──
    st.markdown("### ⚙️ Watermark Settings")
    tab_text, tab_logo = st.tabs(["🔤  Text Watermark", "🖼️  Logo Watermark"])

    wm_result: Image.Image | None = None
    applied_type = ""

    # ── TEXT WATERMARK TAB ──
    with tab_text:
        wt_col, wp_col = st.columns([1, 1.2], gap="large")

        with wt_col:
            st.markdown("**Text Settings**")
            wm_text   = st.text_input("Watermark Text", value="© Image Studio Pro", key="wm_text")
            wm_fsize  = st.slider("Font Size", 12, 200, 36, key="wm_fsize")
            wm_opac   = st.slider("Opacity", 0.05, 1.0, 0.50, 0.05, key="wm_opac",
                                  help="1.0 = fully opaque, 0.0 = invisible")
            wm_angle  = st.slider("Rotation (°)", -180, 180, 0, key="wm_angle")
            wm_pos    = st.selectbox("Position", POSITIONS, index=4, key="wm_pos")

            wm_col_hex = st.color_picker("Text Colour", "#ffffff", key="wm_col")
            # Parse hex → RGB
            h = wm_col_hex.lstrip("#")
            wm_rgb = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

            if st.button("✅  Apply Text Watermark", use_container_width=True, type="primary", key="wm_text_apply"):
                with st.spinner("Applying watermark…"):
                    try:
                        wm_result = add_text_watermark(
                            base_img,
                            text=wm_text or "Watermark",
                            font_size=wm_fsize,
                            opacity=wm_opac,
                            angle=float(wm_angle),
                            position=wm_pos,
                            color=wm_rgb,
                        )
                        applied_type = "Text Watermark"
                        st.session_state["_wm_result"] = wm_result
                        st.session_state["_wm_type"]   = applied_type
                        # ── History ──
                        _wmt_w, _wmt_h = wm_result.size
                        _wmt_out = save_image(wm_result, "PNG", quality=92)
                        st.session_state.history.insert(0, {
                            "name":     uploaded.name,
                            "orig_fmt": uploaded.name.rsplit(".", 1)[-1].upper(),
                            "out_fmt":  "PNG",
                            "orig_sz":  len(raw),
                            "out_sz":   len(_wmt_out),
                            "dims":     f"{_wmt_w} × {_wmt_h}",
                            "ts":       datetime.now().isoformat(),
                        })
                        if AUTH_AVAILABLE:                    # ── auth: persist for logged-in users
                            save_history_entry(st.session_state.history[0])
                        st.success("✅ Text watermark applied!", icon="🎉")
                    except Exception as exc:
                        st.error(f"Failed to apply watermark: {exc}", icon="❌")

        with wp_col:
            st.markdown("**Preview**")
            display_img = st.session_state.get("_wm_result", base_img)
            st.image(display_img)

    # ── LOGO WATERMARK TAB ──
    with tab_logo:
        wl_col, wlp_col = st.columns([1, 1.2], gap="large")

        with wl_col:
            st.markdown("**Logo Settings**")
            logo_file = st.file_uploader(
                "Upload logo (PNG with transparency recommended)",
                type=["jpg", "jpeg", "png", "webp"],
                key="wm_logo_file",
            )
            wl_scale = st.slider("Logo Size (% of image width)", 5, 80, 20, key="wl_scale",
                                 help="Logo width as a percentage of the base image width.")
            wl_opac  = st.slider("Opacity", 0.05, 1.0, 0.80, 0.05, key="wl_opac")
            wl_pos   = st.selectbox("Position", POSITIONS, index=4, key="wl_pos")

            if logo_file and st.button("✅  Apply Logo Watermark", use_container_width=True, type="primary", key="wm_logo_apply"):
                try:
                    logo_bytes = logo_file.read()
                    logo_img   = load_image(logo_bytes)
                    with st.spinner("Compositing logo…"):
                        wm_result = add_logo_watermark(
                            base_img,
                            logo=logo_img,
                            scale=wl_scale / 100.0,
                            opacity=wl_opac,
                            position=wl_pos,
                        )
                    applied_type = "Logo Watermark"
                    st.session_state["_wm_result"] = wm_result
                    st.session_state["_wm_type"]   = applied_type
                    # ── History ──
                    _wml_w, _wml_h = wm_result.size
                    _wml_out = save_image(wm_result, "PNG", quality=92)
                    st.session_state.history.insert(0, {
                        "name":     uploaded.name,
                        "orig_fmt": uploaded.name.rsplit(".", 1)[-1].upper(),
                        "out_fmt":  "PNG",
                        "orig_sz":  len(raw),
                        "out_sz":   len(_wml_out),
                        "dims":     f"{_wml_w} × {_wml_h}",
                        "ts":       datetime.now().isoformat(),
                    })
                    if AUTH_AVAILABLE:                        # ── auth: persist for logged-in users
                        save_history_entry(st.session_state.history[0])
                    st.success("✅ Logo watermark applied!", icon="🎉")
                except Exception as exc:
                    st.error(f"Failed to apply logo: {exc}", icon="❌")
            elif not logo_file:
                st.info("⬆️ Upload a logo image above.", icon="🖼️")

        with wlp_col:
            st.markdown("**Preview**")
            display_img = st.session_state.get("_wm_result", base_img)
            st.image(display_img)

    # ── Download section ──
    final_img = st.session_state.get("_wm_result")
    if final_img is not None:
        st.divider()
        st.markdown("### ⬇️ Download Watermarked Image")

        dl_col1, dl_col2, dl_col3 = st.columns(3)
        stem = uploaded.name.rsplit(".", 1)[0]

        for col, fmt, mime_type, ext in [
            (dl_col1, "PNG",  "image/png",  "png"),
            (dl_col2, "JPEG", "image/jpeg", "jpg"),
            (dl_col3, "WEBP", "image/webp", "webp"),
        ]:
            out_bytes = save_image(final_img, fmt, quality=92)
            col.download_button(
                f"⬇️  {fmt}  ({format_bytes(len(out_bytes))})",
                data=out_bytes,
                file_name=f"{stem}_watermarked.{ext}",
                mime=mime_type,
                use_container_width=True,
                key=f"wm_dl_{fmt}",
            )

            # ── Analytics (log once per download attempt; use PNG as canonical) ──
            if fmt == "PNG":
                log_operation(
                    OP_WATERMARK,
                    len(raw),
                    len(out_bytes),
                    fmt,
                    uploaded.name,
                )

        # Clear button
        if st.button("🗑️ Clear Watermark", key="wm_clear", type="secondary", use_container_width=False):
            st.session_state.pop("_wm_result", None)
            st.session_state.pop("_wm_type", None)
            st.rerun()


# ══════════════════════════════════════════════
#  SECTION 6 — ANALYTICS DASHBOARD  (NEW)
# ══════════════════════════════════════════════
def render_analytics() -> None:
    """Render the session analytics dashboard."""
    section_header(
        "📊", "Analytics Dashboard",
        "Track image operations, storage space saved, and format distribution across your session.",
        badges=["🔒 100% Private", "📈 Interactive Plotly Charts", "💾 Storage Savings", "📄 CSV Export"],
    )

    analytics_data = st.session_state.get("analytics", [])

    if not analytics_data:
        st.info(
            "No data yet.  \n"
            "Process at least one image using any feature to see analytics here.",
            icon="📊",
        )
        return

    df = pd.DataFrame(analytics_data)

    # ── Action buttons ──
    btn1, btn2, _ = st.columns([1, 1, 3])
    with btn1:
        csv_bytes = export_csv(df)
        st.download_button(
            "⬇️  Export CSV",
            data=csv_bytes,
            file_name="image_studio_analytics.csv",
            mime="text/csv",
            use_container_width=True,
        )
    with btn2:
        if st.button("🗑️ Clear Analytics", key="clear_analytics", type="secondary", use_container_width=True):
            st.session_state.analytics = []
            st.rerun()

    st.divider()

    # ── KPI metric cards ──
    metrics = generate_metrics(df)
    st.markdown("### 📈 Session Summary")
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("🖼️ Images Processed",  metrics["total_images"])
    k2.metric("💾 Total Space Saved",  metrics["total_saved"])
    k3.metric("📄 Most Used Format",   metrics["top_format"])
    k4.metric("⚡ Most Used Operation", metrics["top_operation"])

    st.divider()

    # ── Charts ──
    st.markdown("### 📊 Charts")
    charts = create_charts(df, dark=dark)

    chart_row1_left, chart_row1_right = st.columns(2, gap="large")

    with chart_row1_left:
        if charts.get("operations_pie"):
            st.plotly_chart(charts["operations_pie"], use_container_width=True)
        else:
            st.info("Not enough data for Operations Distribution chart.")

    with chart_row1_right:
        if charts.get("format_bar"):
            st.plotly_chart(charts["format_bar"], use_container_width=True)
        else:
            st.info("Not enough data for Format Usage chart.")

    chart_row2_left, chart_row2_right = st.columns(2, gap="large")

    with chart_row2_left:
        if charts.get("daily_line"):
            st.plotly_chart(charts["daily_line"], use_container_width=True)
        else:
            st.info("Not enough data for Daily Activity chart.")

    with chart_row2_right:
        if charts.get("space_saved_bar"):
            st.plotly_chart(charts["space_saved_bar"], use_container_width=True)
        else:
            st.info("Not enough data for Space Saved chart.")

    st.divider()

    # ── Raw data table ──
    st.markdown("### 📋 Raw Session Log")
    # Drop raw bytes column if present, show only human-readable columns
    display_cols = [c for c in df.columns if c not in ("Original (B)", "Output (B)", "Saved (B)")]
    display_df = df[display_cols] if display_cols else df
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
    )


# ══════════════════════════════════════════════
#  SECTION 7 — DOWNLOAD HISTORY  (unchanged)
# ══════════════════════════════════════════════
def render_history() -> None:
    """Render the session download history table."""
    h = st.session_state.history
    section_header(
        "🕒", "Download History",
        f"Review and manage {len(h)} processed file{'s' if len(h) != 1 else ''} from this session.",
        badges=["🔒 100% Private", "⚡ Session Persistent", "📊 Detailed Stats"],
    )

    if not h:
        st.info("No history yet. Convert an image to see it here.", icon="ℹ️")
        return

    col_btn, _ = st.columns([1, 4])
    with col_btn:
        if st.button("🗑️ Clear History", key="clear_hist", type="secondary"):
            st.session_state.history = []
            st.rerun()

    rows = [{
        "File":       item["name"],
        "Conversion": f"{item['orig_fmt']} → {item['out_fmt']}",
        "Original":   format_bytes(item["orig_sz"]),
        "Output":     format_bytes(item["out_sz"]),
        "Saved":      f"-{compression_pct(item['orig_sz'], item['out_sz'])}%"
                      if compression_pct(item["orig_sz"], item["out_sz"]) > 0 else "—",
        "Dimensions": item["dims"],
        "Time":       time_ago(item["ts"]),
    } for item in h]

    df = pd.DataFrame(rows)
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "File":       st.column_config.TextColumn("📄 File",       width="large"),
            "Conversion": st.column_config.TextColumn("🔄 Conversion"),
            "Original":   st.column_config.TextColumn("📦 Original"),
            "Output":     st.column_config.TextColumn("✅ Output"),
            "Saved":      st.column_config.TextColumn("💚 Saved"),
            "Dimensions": st.column_config.TextColumn("📐 Dimensions"),
            "Time":       st.column_config.TextColumn("🕓 Time"),
        },
    )


# ══════════════════════════════════════════════
#  SECTION 8 — SETTINGS  (updated version info)
# ══════════════════════════════════════════════
def render_settings() -> None:
    """Render the application settings and information page."""
    section_header(
        "⚙️", "Settings & Themes",
        "Configure visual theme preferences, reset session data, and review offline privacy documentation.",
        badges=["🔒 100% Private", "🌓 Light / Dark Modes", "⚡ Session Controls", "🌿 Image Studio Pro v3.0"],
    )

    # ── Preferences ──
    st.markdown("### 🎨 Preferences")
    st.write(f"**Current theme:** {'🌙 Dark mode' if dark else '☀️ Light mode'}")

    sc1, sc2 = st.columns(2)
    with sc1:
        if st.button("🌓 Toggle Theme", key="settings_theme", type="primary", use_container_width=True):
            st.session_state.dark = not dark
            st.rerun()
    with sc2:
        if st.button("🗑️ Clear All Data", key="settings_clear", type="secondary", use_container_width=True):
            st.session_state.history       = []
            st.session_state.batch_results = []
            st.session_state.analytics     = []
            st.session_state.pop("_bg_result",  None)
            st.session_state.pop("ocr_result",  None)
            st.session_state.pop("_wm_result",  None)
            st.success("All session data cleared.")

    st.divider()

    # ── Privacy ──
    st.markdown("### 🔒 Privacy")
    st.success(
        "**100% Local Processing**  \n"
        "All image operations run on your machine using Python + Pillow / rembg / EasyOCR.  \n"
        "No images are sent to any server. Your files stay completely private.",
        icon="✅",
    )

    st.divider()

    # ── Supported formats ──
    st.markdown("### 🖼️ Supported Formats")
    fc1, fc2, fc3 = st.columns(3)
    with fc1:
        st.info("**🟡 JPEG**\n\nBest for photos. Smaller file sizes with lossy compression.", icon="📷")
    with fc2:
        st.info("**🔵 PNG**\n\nLossless quality. Supports transparency. Larger files.", icon="🖼️")
    with fc3:
        st.info("**🟢 WEBP**\n\nModern format. Best compression with excellent quality.", icon="⚡")

    st.divider()

    # ── Features overview ──
    st.markdown("### 🚀 Features")
    feat_data = [
        ("📤 Upload & Convert",     "Resize, compress, and convert single images."),
        ("📦 Batch Processing",     "Convert multiple images simultaneously."),
        ("✂️ Background Remover",  "AI-powered background removal (rembg)."),
        ("🔤 Text Extractor (OCR)", "Extract text from images (EasyOCR)."),
        ("🖊️ Watermark Studio",     "Add text or logo watermarks."),
        ("📊 Analytics Dashboard",  "Session-scoped processing analytics."),
        ("🕓 Download History",     "Track all conversions in the current session."),
    ]
    for feat, desc in feat_data:
        fa, fb = st.columns([1, 3])
        fa.markdown(f"**{feat}**")
        fb.markdown(desc)

    st.divider()

    # ── About ──
    st.markdown("### ℹ️ About")
    st.markdown(
        "**Image Studio Pro v3.0**  \n"
        "Built with Python · Streamlit · Pillow · rembg · EasyOCR · Plotly  \n"
        "🌐 **Live App:** [imageconverterpro.streamlit.app](https://imageconverterpro.streamlit.app/)  \n"
        "Open source · No sign-up · No upload limits"
    )


# ══════════════════════════════════════════════
#  ROUTING
# ══════════════════════════════════════════════
_route = {
    "upload":    render_upload,
    "batch":     render_batch,
    "bg_remove": render_bg_remove,
    "ocr":       render_ocr,
    "watermark": render_watermark,
    "analytics": render_analytics,
    "history":   render_history,
    "settings":  render_settings,
}

if not st.session_state.entered_app:
    render_landing_page()
else:
    render_app_top_nav()
    _route.get(st.session_state.section, render_upload)()

