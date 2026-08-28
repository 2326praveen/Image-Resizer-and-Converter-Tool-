def get_css(dark: bool = False, is_landing: bool = False) -> str:
    """Return the full <style> block. Tokens switch between light and dark modes."""

    # ── Colour tokens — Bold, Modern SaaS palette ──────────────────────────────
    bg           = "#0B0D10"                       if dark else "#F8FAFC"
    card         = "#14171D"                       if dark else "#FFFFFF"
    card_border  = "rgba(255,255,255,0.08)"        if dark else "rgba(0,0,0,0.07)"
    card_shadow  = "0 4px 16px rgba(0,0,0,0.35)"   if dark else "0 2px 8px rgba(0,0,0,0.06)"
    card_shadow_hover = "0 8px 24px rgba(0,0,0,0.50)" if dark else "0 8px 24px rgba(0,0,0,0.10)"
    text1        = "#F8FAFC"                       if dark else "#0F172A"
    text2        = "#94A3B8"                       if dark else "#475569"
    input_bg     = "#1A1D24"                       if dark else "#FFFFFF"
    input_border = "rgba(255,255,255,0.14)"        if dark else "rgba(0,0,0,0.14)"
    input_text   = "#F8FAFC"                       if dark else "#0F172A"
    divider_col  = "rgba(255,255,255,0.08)"        if dark else "rgba(0,0,0,0.08)"
    label_col    = "#94A3B8"                       if dark else "#64748B"
    accent       = "#10B981"                       if dark else "#059669"
    accent_hover = "#34D399"                       if dark else "#047857"
    accent_bg    = "rgba(16,185,129,0.14)"         if dark else "rgba(5,150,105,0.08)"
    sidebar_bg   = "#0E1015"                       if dark else "#F8FAFC"
    nav_hover    = "rgba(255,255,255,0.06)"        if dark else "rgba(0,0,0,0.05)"
    nav_act_bg   = "rgba(16,185,129,0.16)"         if dark else "rgba(5,150,105,0.10)"
    nav_act_bdr  = "#10B981"                       if dark else "#059669"

    uploader_bg  = "rgba(16,185,129,0.05)"         if dark else "rgba(5,150,105,0.03)"
    uploader_bdr = "rgba(16,185,129,0.32)"         if dark else "rgba(5,150,105,0.25)"
    uploader_txt = "#94A3B8"                       if dark else "#475569"
    uploader_btn = "#1A1D24"                       if dark else "#FFFFFF"

    landing_sidebar_css = "[data-testid=\"stSidebar\"] { display: none !important; }"
    landing_max_width = "1200px"

    return f"""
<style>
/* ══════════════════════════════════════════════
   CSS CUSTOM PROPERTIES
══════════════════════════════════════════════ */
:root {{
    --bg:           {bg};
    --card:         {card};
    --text1:        {text1};
    --text2:        {text2};
    --accent:       {accent};
    --accent-hover: {accent_hover};
    --accent-bg:    {accent_bg};
    --border:       {card_border};
    --radius:       12px;
}}

/* ══════════════════════════════════════════════
   FONTS & RESET
══════════════════════════════════════════════ */
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');
*,*::before,*::after {{ box-sizing: border-box; }}
html, body, [class*="css"] {{
    font-family: 'Plus Jakarta Sans', 'Inter', -apple-system, sans-serif;
}}

/* ══════════════════════════════════════════════
   HEADER — hidden
══════════════════════════════════════════════ */
header[data-testid="stHeader"] {{
    height: 0 !important;
    overflow: hidden !important;
    border: none !important;
    padding: 0 !important;
    margin: 0 !important;
}}
[data-testid="stDecoration"] {{ display: none !important; }}
#MainMenu, footer {{ display: none !important; }}

/* ══════════════════════════════════════════════
   APP CONTAINER & GLOBAL AMBIENT GLOW
══════════════════════════════════════════════ */
.stApp {{
    background: {bg} !important;
    background-image: 
        radial-gradient(circle at 0% 0%, rgba(16, 185, 129, 0.08) 0%, transparent 38%),
        radial-gradient(circle at 100% 100%, rgba(124, 58, 237, 0.09) 0%, transparent 40%) !important;
    background-attachment: fixed !important;
    min-height: 100vh;
}}
.block-container {{
    padding: 1.2rem 2rem 3.5rem !important;
    max-width: {landing_max_width} !important;
}}

{landing_sidebar_css}

/* ══════════════════════════════════════════════
   GLOBAL TEXT & LABELS
══════════════════════════════════════════════ */
body, p, div, li, span,
.stMarkdown, .stMarkdown p {{ color: {text1} !important; }}
h1,h2,h3,h4,h5,h6 {{ color: {text1} !important; font-weight: 700 !important; letter-spacing: -0.02em; }}
strong {{ color: {text1} !important; }}
[data-testid="stCaptionContainer"] p {{ color: {text2} !important; font-size: 0.85rem !important; }}

label,
[data-testid="stWidgetLabel"],
[data-testid="stWidgetLabel"] p,
.stCheckbox label,
.stSelectbox label,
.stNumberInput label,
.stSlider label {{
    color: {label_col} !important;
    font-weight: 600 !important;
    font-size: 0.84rem !important;
}}

/* ── Unified Buttons Across ALL Modules ── */
.stButton button[kind="primary"],
.stDownloadButton button,
[data-testid="stFormSubmitButton"] button {{
    background: linear-gradient(135deg, #10B981 0%, #0D9488 100%) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.55rem 1.25rem !important;
    font-weight: 700 !important;
    font-size: 0.88rem !important;
    box-shadow: 0 4px 14px rgba(16,185,129,0.30) !important;
    transition: all 0.20s cubic-bezier(0.16, 1, 0.3, 1) !important;
}}
.stButton button[kind="primary"]:hover,
.stDownloadButton button:hover,
[data-testid="stFormSubmitButton"] button:hover {{
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(16,185,129,0.42) !important;
    background: linear-gradient(135deg, #34D399 0%, #0D9488 100%) !important;
}}
.stButton button[kind="primary"]:active,
.stDownloadButton button:active,
[data-testid="stFormSubmitButton"] button:active {{
    transform: translateY(0) !important;
    box-shadow: 0 2px 6px rgba(16,185,129,0.25) !important;
    background: linear-gradient(135deg, #059669 0%, #0F766E 100%) !important;
}}
.stButton button[kind="primary"] p, .stButton button[kind="primary"] span,
.stDownloadButton button p, .stDownloadButton button span,
[data-testid="stFormSubmitButton"] button p,
[data-testid="stFormSubmitButton"] button span {{
    color: #FFFFFF !important;
    font-weight: 700 !important;
}}

.stButton button[kind="secondary"],
.stButton button:not([kind="primary"]) {{
    background: #FFFFFF !important;
    color: #475569 !important;
    border: 1px solid rgba(0, 0, 0, 0.12) !important;
    border-radius: 10px !important;
    padding: 0.52rem 0.95rem !important;
    font-weight: 600 !important;
    font-size: 0.86rem !important;
    box-shadow: 0 2px 6px rgba(0,0,0,0.04) !important;
    transition: all 0.18s cubic-bezier(0.16, 1, 0.3, 1) !important;
}}
.stButton button[kind="secondary"]:hover,
.stButton button:not([kind="primary"]):hover {{
    background: #F8FAFC !important;
    border-color: rgba(16,185,129,0.35) !important;
    color: #0F172A !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.07) !important;
}}
.stButton button[kind="secondary"] p, .stButton button[kind="secondary"] span,
.stButton button:not([kind="primary"]) p, .stButton button:not([kind="primary"]) span {{
    color: #475569 !important;
    font-weight: 600 !important;
}}
.stButton button[kind="secondary"]:hover p, .stButton button[kind="secondary"]:hover span,
.stButton button:not([kind="primary"]):hover p, .stButton button:not([kind="primary"]):hover span {{
    color: #0F172A !important;
}}

/* Top Navigation Responsive Pill Grid */
@media (max-width: 1100px) {{
    div[data-testid="stHorizontalBlock"] {{
        flex-wrap: wrap !important;
        gap: 0.5rem !important;
    }}
    div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {{
        min-width: 140px !important;
        width: auto !important;
        flex: 1 1 calc(25% - 0.5rem) !important;
    }}
}}
@media (max-width: 600px) {{
    div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {{
        min-width: 100% !important;
        width: 100% !important;
        flex: 1 1 100% !important;
    }}
}}

.stDownloadButton button {{
    background: {card} !important;
    color: {accent} !important;
    border: 1.5px solid {accent_bg} !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08) !important;
    border-radius: 10px !important;
    padding: 0.55rem 1.35rem !important;
    font-weight: 600 !important;
    font-size: 0.90rem !important;
    transition: all 0.20s ease !important;
}}
.stDownloadButton button:hover {{
    background: {accent_bg} !important;
    border-color: {accent} !important;
    transform: translateY(-2px) scale(1.015) !important;
    box-shadow: 0 6px 18px rgba(16,185,129,0.18) !important;
}}
.stDownloadButton button p, .stDownloadButton button span {{
    color: {accent} !important; font-weight: 600 !important;
}}

/* ── Form Inputs ── */
.stNumberInput input, .stTextInput input, input[type="number"], input[type="text"], input[type="password"] {{
    color: {input_text} !important;
    background: {input_bg} !important;
    border: 1.5px solid {input_border} !important;
    border-radius: 10px !important;
    font-size: 0.92rem !important;
    padding: 0.55rem 0.85rem !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}}
.stNumberInput input:focus, .stTextInput input:focus {{
    border-color: {accent} !important;
    box-shadow: 0 0 0 3px {accent_bg} !important;
    outline: none !important;
}}

/* ══════════════════════════════════════════════
   FILE UPLOADER
══════════════════════════════════════════════ */
[data-testid="stFileUploaderDropzone"] {{
    background: transparent !important;
    border: 1.5px dashed {uploader_bdr} !important;
    border-radius: 12px !important;
    padding: 1.5rem !important;
    transition: border-color 0.2s ease, background 0.2s ease !important;
}}
[data-testid="stFileUploaderDropzone"]:hover,
[data-testid="stFileUploaderDropzone"]:focus-within {{
    border-color: {accent} !important;
    background: {accent_bg} !important;
}}
[data-testid="stFileUploaderDropzone"] span,
[data-testid="stFileUploaderDropzone"] p,
[data-testid="stFileUploaderDropzoneInstructions"] span,
[data-testid="stFileUploaderDropzoneInstructions"] div {{
    color: {text2} !important;
    font-weight: 500 !important;
}}
[data-testid="stFileUploaderDropzone"] button {{
    background: {card} !important;
    color: {text1} !important;
    border: 1px solid {card_border} !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05) !important;
}}
[data-testid="stFileUploaderDropzone"] button:hover {{
    background: {accent_bg} !important;
    border-color: {accent} !important;
    color: {accent} !important;
}}

/* ══════════════════════════════════════════════
   SIDEBAR (App Mode)
══════════════════════════════════════════════ */
[data-testid="stSidebar"] {{
    background: {sidebar_bg} !important;
    border-right: 1px solid {card_border} !important;
}}
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] div,
[data-testid="stSidebar"] li,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stMarkdown p,
[data-testid="stSidebar"] .stMarkdown span {{ color: {text1} !important; }}
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {{ color: {text1} !important; font-weight: 700 !important; }}
[data-testid="stSidebar"] strong {{ color: {text1} !important; font-weight: 600 !important; }}
[data-testid="stSidebar"] hr {{ border-color: {divider_col} !important; }}
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {{
    color: {text2} !important; font-size: 0.80rem !important;
}}
[data-testid="stSidebar"] .stButton button {{
    background: {card} !important;
    color: {text1} !important;
    border: 1px solid {card_border} !important;
    border-radius: 10px !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.03) !important;
    font-weight: 600 !important;
    text-align: left !important;
    transition: all 0.18s cubic-bezier(0.16, 1, 0.3, 1) !important;
    padding: 0.52rem 0.85rem !important;
    margin-bottom: 0.25rem !important;
}}
[data-testid="stSidebar"] .stButton button:hover {{
    background: {accent_bg} !important;
    border-color: rgba(16,185,129,0.3) !important;
    transform: translateX(3px) !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.06) !important;
}}
[data-testid="stSidebar"] .stButton button p,
[data-testid="stSidebar"] .stButton button span {{
    color: {text1} !important;
    font-weight: 600 !important;
}}
[data-testid="stSidebar"] button.nav-active {{
    background: {nav_act_bg} !important;
    border-color: {accent} !important;
    box-shadow: 0 2px 10px rgba(16,185,129,0.15) !important;
}}
[data-testid="stSidebar"] button.nav-active p,
[data-testid="stSidebar"] button.nav-active span {{
    color: {accent} !important;
    font-weight: 700 !important;
}}

/* ══════════════════════════════════════════════
   APP TOP NAVIGATION BAR & PILLS
══════════════════════════════════════════════ */
.nav-pill-active button {{
    background: linear-gradient(135deg, #10B981 0%, #0D9488 100%) !important;
    color: #FFFFFF !important;
    border: 1px solid rgba(255,255,255,0.18) !important;
    border-radius: 10px !important;
    box-shadow: 0 4px 16px rgba(16,185,129,0.38) !important;
    padding: 0.50rem 0.65rem !important;
    font-weight: 700 !important;
    font-size: 0.84rem !important;
    transition: all 0.20s cubic-bezier(0.16, 1, 0.3, 1) !important;
}}
.nav-pill-active button p, .nav-pill-active button span {{
    color: #FFFFFF !important;
    font-weight: 700 !important;
    font-size: 0.84rem !important;
}}
.nav-pill-inactive button {{
    background: {card} !important;
    color: {text2} !important;
    border: 1px solid {card_border} !important;
    border-radius: 10px !important;
    box-shadow: {card_shadow} !important;
    padding: 0.50rem 0.65rem !important;
    font-weight: 600 !important;
    font-size: 0.84rem !important;
    transition: all 0.18s cubic-bezier(0.16, 1, 0.3, 1) !important;
}}
.nav-pill-inactive button:hover {{
    background: {nav_hover} !important;
    color: {text1} !important;
    border-color: rgba(16,185,129,0.25) !important;
    transform: translateY(-2px) !important;
    box-shadow: {card_shadow_hover} !important;
}}
.nav-pill-inactive button p, .nav-pill-inactive button span {{
    color: {text2} !important;
    font-weight: 600 !important;
    font-size: 0.84rem !important;
}}
.nav-pill-inactive button:hover p, .nav-pill-inactive button:hover span {{
    color: {text1} !important;
}}

.logout-btn-wrap button {{
    background: {card} !important;
    color: {text2} !important;
    border: 1px solid {card_border} !important;
    border-radius: 8px !important;
    box-shadow: none !important;
    font-weight: 600 !important;
    font-size: 0.82rem !important;
    padding: 0.35rem 0.75rem !important;
}}
.logout-btn-wrap button:hover {{
    background: {nav_hover} !important;
    color: #EF4444 !important;
    border-color: rgba(239, 68, 68, 0.3) !important;
}}
.logout-btn-wrap button p, .logout-btn-wrap button span {{
    color: {text2} !important;
    font-size: 0.82rem !important;
}}
.logout-btn-wrap button:hover p, .logout-btn-wrap button:hover span {{
    color: #EF4444 !important;
}}

/* ══════════════════════════════════════════════
   LIGHT HERO BANNER (Landing Page only)
══════════════════════════════════════════════ */
div[data-testid="stVerticalBlock"]:has(.hero-banner-anchor):not(:has(#features)),
div[data-testid="stVerticalBlockBorderWrapper"]:has(.hero-banner-anchor):not(:has(#features)) {{
    position: relative !important;
    background: #FBFBFA !important;
    background-image: 
        radial-gradient(circle at 0% 0%, rgba(16, 185, 129, 0.18) 0%, transparent 36%),
        radial-gradient(circle at 100% 100%, rgba(124, 58, 237, 0.22) 0%, transparent 38%),
        radial-gradient(circle at 50% 100%, rgba(16, 185, 129, 0.08) 0%, transparent 22%) !important;
    border-radius: 24px !important;
    padding: 1.5rem 2rem 2.2rem !important;
    margin-bottom: 3.5rem !important;
    border: 1px solid {card_border} !important;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04) !important;
    overflow: hidden !important;
}}

div[data-testid="stVerticalBlock"]:has(.hero-banner-anchor):not(:has(#features)) .hero-headline {{
    color: #0F172A !important;
    font-weight: 800 !important;
    text-shadow: none !important;
}}
div[data-testid="stVerticalBlock"]:has(.hero-banner-anchor):not(:has(#features)) .hero-subhead {{
    color: #64748B !important;
    font-weight: 400 !important;
    text-shadow: none !important;
}}
div[data-testid="stVerticalBlock"]:has(.hero-banner-anchor):not(:has(#features)) .hero-pill-badge {{
    background: rgba(16, 185, 129, 0.10) !important;
    border: 1px solid rgba(16, 185, 129, 0.25) !important;
    color: #10B981 !important;
    box-shadow: none !important;
}}
div[data-testid="stVerticalBlock"]:has(.hero-banner-anchor):not(:has(#features)) .trust-row,
div[data-testid="stVerticalBlock"]:has(.hero-banner-anchor):not(:has(#features)) .trust-item {{
    color: #64748B !important;
    font-weight: 600 !important;
}}
div[data-testid="stVerticalBlock"]:has(.hero-banner-anchor):not(:has(#features)) .nav-link-item {{
    color: #64748B !important;
}}
div[data-testid="stVerticalBlock"]:has(.hero-banner-anchor):not(:has(#features)) .nav-link-item:hover {{
    color: #10B981 !important;
}}
div[data-testid="stVerticalBlock"]:has(.hero-banner-anchor):not(:has(#features)) .hero-brand-title {{
    color: #0F172A !important;
}}


/* ── Zero-Height Anchor Containers ── */
.nav-login-btn-anchor,
.violet-outline-btn-anchor,
.hero-cta-btn-anchor,
.violet-btn-anchor {{
    position: absolute;
    width: 0;
    height: 0;
    opacity: 0;
    pointer-events: none;
}}
div[data-testid="stElementContainer"]:has(.nav-login-btn-anchor),
div[data-testid="stElementContainer"]:has(.violet-outline-btn-anchor),
div[data-testid="stElementContainer"]:has(.hero-cta-btn-anchor),
div[data-testid="stElementContainer"]:has(.violet-btn-anchor) {{
    height: 0 !important;
    min-height: 0 !important;
    margin: 0 !important;
    padding: 0 !important;
    line-height: 0 !important;
    overflow: hidden !important;
}}

/* ── Top Navbar Button Alignment (Log In & Sign Up Free) ── */
div[data-testid="column"]:has(.nav-login-btn-anchor) button,
div[data-testid="column"]:has(.violet-outline-btn-anchor) button {{
    height: 38px !important;
    min-height: 38px !important;
    max-height: 38px !important;
    padding: 0 16px !important;
    font-size: 0.88rem !important;
    font-weight: 700 !important;
    border-radius: 10px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    margin-top: 1px !important;
    margin-bottom: 0 !important;
    box-sizing: border-box !important;
    line-height: 1 !important;
}}

/* Log In Button (Clean White Card with Subtle Border) */
div[data-testid="column"]:has(.nav-login-btn-anchor) button {{
    background: #FFFFFF !important;
    color: #475569 !important;
    border: 1px solid rgba(0, 0, 0, 0.12) !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04) !important;
}}
div[data-testid="column"]:has(.nav-login-btn-anchor) button:hover {{
    background: #F8FAFC !important;
    color: #0F172A !important;
    border-color: rgba(16, 185, 129, 0.40) !important;
    box-shadow: 0 3px 8px rgba(0,0,0,0.06) !important;
    transform: translateY(-1px) !important;
}}
div[data-testid="column"]:has(.nav-login-btn-anchor) button p,
div[data-testid="column"]:has(.nav-login-btn-anchor) button span {{
    color: #475569 !important;
    font-weight: 600 !important;
}}
div[data-testid="column"]:has(.nav-login-btn-anchor) button:hover p,
div[data-testid="column"]:has(.nav-login-btn-anchor) button:hover span {{
    color: #0F172A !important;
}}

/* Sign Up Free Button (Outlined Violet) */
div[data-testid="column"]:has(.violet-outline-btn-anchor) button,
div[data-testid="column"]:has(.violet-outline-btn-anchor) [kind="secondary"],
div[data-testid="column"]:has(.violet-outline-btn-anchor) button[type="button"],
div[data-testid="stElementContainer"]:has(.violet-outline-btn-anchor) + div[data-testid="stElementContainer"] button,
div[data-testid="stElementContainer"]:has(.violet-outline-btn-anchor) + div[data-testid="stElementContainer"] [kind="secondary"] {{
    background: #FFFFFF !important;
    color: #7C3AED !important;
    border: 1.5px solid #7C3AED !important;
    box-shadow: 0 1px 4px rgba(124, 58, 237, 0.12) !important;
}}
div[data-testid="column"]:has(.violet-outline-btn-anchor) button:hover,
div[data-testid="column"]:has(.violet-outline-btn-anchor) [kind="secondary"]:hover,
div[data-testid="column"]:has(.violet-outline-btn-anchor) button[type="button"]:hover,
div[data-testid="stElementContainer"]:has(.violet-outline-btn-anchor) + div[data-testid="stElementContainer"] button:hover,
div[data-testid="stElementContainer"]:has(.violet-outline-btn-anchor) + div[data-testid="stElementContainer"] [kind="secondary"]:hover {{
    background: rgba(124, 58, 237, 0.08) !important;
    color: #6D28D9 !important;
    border-color: #6D28D9 !important;
    box-shadow: 0 4px 12px rgba(124, 58, 237, 0.20) !important;
    transform: translateY(-1px) !important;
}}
div[data-testid="column"]:has(.violet-outline-btn-anchor) button p,
div[data-testid="column"]:has(.violet-outline-btn-anchor) button span,
div[data-testid="column"]:has(.violet-outline-btn-anchor) [kind="secondary"] p,
div[data-testid="column"]:has(.violet-outline-btn-anchor) [kind="secondary"] span,
div[data-testid="stElementContainer"]:has(.violet-outline-btn-anchor) + div[data-testid="stElementContainer"] button p,
div[data-testid="stElementContainer"]:has(.violet-outline-btn-anchor) + div[data-testid="stElementContainer"] button span,
div[data-testid="stElementContainer"]:has(.violet-outline-btn-anchor) + div[data-testid="stElementContainer"] [kind="secondary"] p,
div[data-testid="stElementContainer"]:has(.violet-outline-btn-anchor) + div[data-testid="stElementContainer"] [kind="secondary"] span {{
    color: #7C3AED !important;
    font-weight: 700 !important;
}}
div[data-testid="column"]:has(.violet-outline-btn-anchor) button:hover p,
div[data-testid="column"]:has(.violet-outline-btn-anchor) button:hover span,
div[data-testid="column"]:has(.violet-outline-btn-anchor) [kind="secondary"]:hover p,
div[data-testid="column"]:has(.violet-outline-btn-anchor) [kind="secondary"]:hover span,
div[data-testid="stElementContainer"]:has(.violet-outline-btn-anchor) + div[data-testid="stElementContainer"] button:hover p,
div[data-testid="stElementContainer"]:has(.violet-outline-btn-anchor) + div[data-testid="stElementContainer"] button:hover span,
div[data-testid="stElementContainer"]:has(.violet-outline-btn-anchor) + div[data-testid="stElementContainer"] [kind="secondary"]:hover p,
div[data-testid="stElementContainer"]:has(.violet-outline-btn-anchor) + div[data-testid="stElementContainer"] [kind="secondary"]:hover span {{
    color: #6D28D9 !important;
}}

/* Hero CTA Button Pair Equal Width (260px) & Alignment */
div[data-testid="column"]:has(.hero-cta-btn-anchor) button,
div[data-testid="stElementContainer"]:has(.hero-cta-btn-anchor) button,
div[data-testid="stElementContainer"]:has(.hero-cta-btn-anchor) + div[data-testid="stElementContainer"] button {{
    width: 100% !important;
    min-width: 250px !important;
    height: 48px !important;
    font-size: 0.95rem !important;
    font-weight: 700 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    margin: 0 auto !important;
}}

/* Violet Secondary Action Buttons (Hero CTA, Submit Signup) */
div[data-testid="column"]:has(.violet-btn-anchor) button,
div[data-testid="stElementContainer"]:has(.violet-btn-anchor) button,
div[data-testid="stElementContainer"]:has(.violet-btn-anchor) + div[data-testid="stElementContainer"] button,
div[data-testid="stForm"]:has(.violet-btn-anchor) [data-testid="stFormSubmitButton"] button,
div[data-testid="stForm"]:has(.violet-btn-anchor) button[type="submit"] {{
    background: linear-gradient(135deg, #7C3AED 0%, #6D28D9 100%) !important;
    color: #FFFFFF !important;
    border: 1px solid rgba(124, 58, 237, 0.50) !important;
    box-shadow: 0 4px 14px rgba(124, 58, 237, 0.28) !important;
}}
div[data-testid="column"]:has(.violet-btn-anchor) button:hover,
div[data-testid="stElementContainer"]:has(.violet-btn-anchor) button:hover,
div[data-testid="stElementContainer"]:has(.violet-btn-anchor) + div[data-testid="stElementContainer"] button:hover,
div[data-testid="stForm"]:has(.violet-btn-anchor) [data-testid="stFormSubmitButton"] button:hover,
div[data-testid="stForm"]:has(.violet-btn-anchor) button[type="submit"]:hover {{
    background: linear-gradient(135deg, #8B5CF6 0%, #6D28D9 100%) !important;
    color: #FFFFFF !important;
    border-color: rgba(124, 58, 237, 0.70) !important;
    box-shadow: 0 6px 18px rgba(124, 58, 237, 0.40) !important;
    transform: translateY(-2px) !important;
}}
div[data-testid="column"]:has(.violet-btn-anchor) button p,
div[data-testid="column"]:has(.violet-btn-anchor) button span,
div[data-testid="stElementContainer"]:has(.violet-btn-anchor) button p,
div[data-testid="stElementContainer"]:has(.violet-btn-anchor) button span,
div[data-testid="stElementContainer"]:has(.violet-btn-anchor) + div[data-testid="stElementContainer"] button p,
div[data-testid="stElementContainer"]:has(.violet-btn-anchor) + div[data-testid="stElementContainer"] button span,
div[data-testid="stForm"]:has(.violet-btn-anchor) [data-testid="stFormSubmitButton"] button p,
div[data-testid="stForm"]:has(.violet-btn-anchor) [data-testid="stFormSubmitButton"] button span,
div[data-testid="stForm"]:has(.violet-btn-anchor) button[type="submit"] p,
div[data-testid="stForm"]:has(.violet-btn-anchor) button[type="submit"] span {{
    color: #FFFFFF !important;
    font-weight: 700 !important;
}}

/* ══════════════════════════════════════════════
   LANDING PAGE HERO & NAVBAR STYLES
══════════════════════════════════════════════ */
.landing-nav-box {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.8rem 1.4rem;
    border-radius: 14px;
    background: {card};
    border: 1px solid {card_border};
    box-shadow: 0 4px 20px rgba(0,0,0,0.06);
    margin-bottom: 2rem;
}}
.nav-link-item {{
    color: {text2} !important;
    font-weight: 600;
    font-size: 0.92rem;
    text-decoration: none;
    transition: color 0.2s ease;
}}
.nav-link-item:hover {{
    color: {accent} !important;
}}

@media (max-width: 768px) {{
    .nav-links-center {{
        display: none !important;
    }}
}}

.landing-hero-box {{
    text-align: center;
    padding: 2.5rem 1rem 2rem;
}}
.hero-pill-badge {{
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.35rem 1rem;
    border-radius: 99px;
    background: {accent_bg};
    border: 1px solid rgba(16,185,129,0.25);
    color: {accent};
    font-size: 0.82rem;
    font-weight: 700;
    margin-bottom: 1.2rem;
}}
.hero-headline {{
    font-size: 3.2rem;
    font-weight: 800;
    line-height: 1.12;
    letter-spacing: -0.035em;
    margin-bottom: 1.1rem;
    color: {text1};
}}
@media (max-width: 768px) {{
    .hero-headline {{ font-size: 2.1rem; }}
}}
.hero-subhead {{
    font-size: 1.15rem;
    color: {text2};
    max-width: 680px;
    margin: 0 auto 1.8rem;
    line-height: 1.6;
    font-weight: 400;
}}
.trust-row {{
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 1.5rem;
    color: {text2};
    font-size: 0.88rem;
    font-weight: 600;
    margin-top: 1.2rem;
    margin-bottom: 1.5rem;
}}
.trust-item {{
    display: flex;
    align-items: center;
    gap: 0.4rem;
}}

/* ══════════════════════════════════════════════
   FEATURE GRID STYLES
══════════════════════════════════════════════ */
.section-head-wrap {{
    text-align: center;
    margin-bottom: 2.2rem;
    padding-top: 1rem;
}}
.section-head-wrap h2 {{
    font-size: 2.1rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    margin-bottom: 0.5rem;
    color: {text1};
}}
.section-head-wrap p {{
    font-size: 1.05rem;
    color: {text2};
    max-width: 600px;
    margin: 0 auto;
}}

.feat-card {{
    background: {card};
    border: 1px solid {card_border};
    border-radius: 14px;
    padding: 1.35rem 1.25rem 1rem;
    box-shadow: 0 4px 18px rgba(0,0,0,0.04);
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    transition: transform 0.22s ease, box-shadow 0.22s ease, border-color 0.22s ease;
}}
.feat-card:hover {{
    transform: translateY(-4px);
    box-shadow: 0 10px 28px rgba(0,0,0,0.08);
}}
.feat-card-emerald:hover {{
    border-color: rgba(16, 185, 129, 0.40) !important;
}}
.feat-card-violet:hover {{
    border-color: rgba(124, 58, 237, 0.40) !important;
}}
.feat-card-sky:hover {{
    border-color: rgba(14, 165, 233, 0.40) !important;
}}

.feat-icon {{
    width: 44px;
    height: 44px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.35rem;
    margin-bottom: 0.9rem;
}}
.feat-icon-emerald {{
    background: rgba(16, 185, 129, 0.12);
    border: 1px solid rgba(16, 185, 129, 0.22);
}}
.feat-icon-violet {{
    background: rgba(124, 58, 237, 0.12);
    border: 1px solid rgba(124, 58, 237, 0.22);
}}
.feat-icon-sky {{
    background: rgba(14, 165, 233, 0.12);
    border: 1px solid rgba(14, 165, 233, 0.22);
}}

/* Violet Secondary Action Button */
div[data-testid="stElementContainer"]:has(.violet-btn-anchor) + div[data-testid="stElementContainer"] button,
div[data-testid="stElementContainer"]:has(.violet-btn-anchor) button,
div:has(> .violet-btn-anchor) + div button,
div:has(> .violet-btn-anchor) button {{
    background: linear-gradient(135deg, #7C3AED 0%, #6D28D9 100%) !important;
    color: #FFFFFF !important;
    border: 1px solid rgba(124, 58, 237, 0.40) !important;
    box-shadow: 0 4px 14px rgba(124, 58, 237, 0.30) !important;
}}
div[data-testid="stElementContainer"]:has(.violet-btn-anchor) + div[data-testid="stElementContainer"] button:hover,
div[data-testid="stElementContainer"]:has(.violet-btn-anchor) button:hover,
div:has(> .violet-btn-anchor) + div button:hover,
div:has(> .violet-btn-anchor) button:hover {{
    background: linear-gradient(135deg, #8B5CF6 0%, #6D28D9 100%) !important;
    color: #FFFFFF !important;
    border-color: rgba(124, 58, 237, 0.60) !important;
    box-shadow: 0 6px 18px rgba(124, 58, 237, 0.45) !important;
    transform: translateY(-2px) !important;
}}
div[data-testid="stElementContainer"]:has(.violet-btn-anchor) + div[data-testid="stElementContainer"] button p,
div[data-testid="stElementContainer"]:has(.violet-btn-anchor) + div[data-testid="stElementContainer"] button span,
div[data-testid="stElementContainer"]:has(.violet-btn-anchor) button p,
div[data-testid="stElementContainer"]:has(.violet-btn-anchor) button span,
div:has(> .violet-btn-anchor) + div button p,
div:has(> .violet-btn-anchor) + div button span,
div:has(> .violet-btn-anchor) button p,
div:has(> .violet-btn-anchor) button span {{
    color: #FFFFFF !important;
}}

.feat-title {{
    font-size: 1.02rem;
    font-weight: 700;
    color: {text1};
    margin-bottom: 0.4rem;
    letter-spacing: -0.01em;
}}
.feat-desc {{
    font-size: 0.86rem;
    color: {text2};
    line-height: 1.45;
    margin-bottom: 1rem;
}}

/* ══════════════════════════════════════════════
   WORKFLOW SHOWCASE STYLES
══════════════════════════════════════════════ */
.workflow-badge {{
    display: inline-block;
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    padding: 0.28rem 0.85rem;
    border-radius: 99px;
    margin-bottom: 0.8rem;
}}
.workflow-badge-emerald {{
    background: rgba(16, 185, 129, 0.10);
    color: #10B981;
    border: 1px solid rgba(16, 185, 129, 0.25);
}}
.workflow-badge-violet {{
    background: rgba(124, 58, 237, 0.10);
    color: #7C3AED;
    border: 1px solid rgba(124, 58, 237, 0.25);
}}
.workflow-title {{
    font-size: 1.75rem;
    font-weight: 800;
    letter-spacing: -0.025em;
    line-height: 1.25;
    color: {text1};
    margin-bottom: 0.8rem;
}}
.workflow-desc {{
    font-size: 1rem;
    color: {text2};
    line-height: 1.6;
    margin-bottom: 1.3rem;
}}
.mockup-canvas {{
    background: {card};
    border: 1px solid {card_border};
    border-radius: 16px;
    padding: 2.2rem 1.8rem;
    text-align: center;
    box-shadow: 0 4px 20px rgba(0,0,0,0.04);
    border-top: 3px solid #10B981;
    transition: transform 0.20s ease, box-shadow 0.20s ease;
}}
.mockup-canvas:hover {{
    transform: translateY(-2px);
    box-shadow: 0 8px 26px rgba(0,0,0,0.08);
}}

/* ══════════════════════════════════════════════
   WHY US, CTA BANNER & FOOTER
══════════════════════════════════════════════ */
.why-card {{
    background: {card};
    border: 1px solid {card_border};
    border-radius: 14px;
    padding: 1.8rem 1.4rem;
    box-shadow: 0 4px 20px rgba(0,0,0,0.04);
    height: 100%;
    transition: transform 0.2s ease;
}}
.why-card:hover {{
    transform: translateY(-3px);
}}
.why-icon {{
    font-size: 2.2rem;
    margin-bottom: 0.8rem;
}}
.why-title {{
    font-size: 1.15rem;
    font-weight: 700;
    color: {text1};
    margin-bottom: 0.5rem;
    letter-spacing: -0.01em;
}}
.why-desc {{
    font-size: 0.90rem;
    color: {text2};
    line-height: 1.5;
}}

.bottom-cta-banner {{
    text-align: center;
    background: {card};
    border: 1px solid {card_border};
    border-radius: 18px;
    padding: 3rem 2rem;
    margin-top: 4rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 8px 32px rgba(0,0,0,0.06);
    border-top: 3px solid {accent};
}}
.bottom-cta-title {{
    font-size: 2rem;
    font-weight: 800;
    color: {text1};
    letter-spacing: -0.025em;
    margin-bottom: 0.6rem;
}}
.bottom-cta-sub {{
    font-size: 1.05rem;
    color: {text2};
    margin-bottom: 1.5rem;
}}

.landing-footer {{
    text-align: center;
    padding: 2.5rem 1rem 1rem;
    border-top: 1px solid {card_border};
    margin-top: 4rem;
    color: {text2};
    font-size: 0.86rem;
    line-height: 1.6;
}}

/* ══════════════════════════════════════════════
   AUTH DRAWER / FORM CARD STYLES
══════════════════════════════════════════════ */
[data-testid="stForm"] {{
    background: {card} !important;
    border: 1px solid {card_border} !important;
    border-radius: 18px !important;
    padding: 2.2rem 2.4rem !important;
    box-shadow: 0 12px 40px rgba(0,0,0,0.08) !important;
    border-top: 3px solid {accent} !important;
}}
.auth-header {{
    text-align: center;
    margin-bottom: 1.5rem;
}}
.auth-header-title {{
    font-size: 1.4rem;
    font-weight: 800;
    color: {text1};
    margin-bottom: 0.35rem;
    letter-spacing: -0.02em;
}}
.auth-header-caption {{
    font-size: 0.88rem;
    color: {text2};
    line-height: 1.4;
}}

/* ══════════════════════════════════════════════
   APP MODE HELPERS
══════════════════════════════════════════════ */
.app-header-wrap {{
    position: relative;
    background: {card};
    border: 1px solid {card_border};
    border-radius: 18px;
    padding: 1.6rem 2rem 1.4rem;
    margin-bottom: 1.8rem;
    box-shadow: 0 4px 18px rgba(0, 0, 0, 0.03);
    background-image: 
        radial-gradient(circle at 100% 0%, rgba(124, 58, 237, 0.06) 0%, transparent 40%),
        radial-gradient(circle at 0% 100%, rgba(16, 185, 129, 0.06) 0%, transparent 40%);
}}
.app-header-title {{
    font-size: 1.85rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    color: {text1};
    margin-bottom: 0.35rem;
}}
.app-header-sub {{
    font-size: 0.95rem;
    color: {text2};
    margin-bottom: 0.9rem;
    line-height: 1.5;
}}
.app-badge-row {{
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
}}
.app-pill-badge {{
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    padding: 0.25rem 0.75rem;
    border-radius: 99px;
    background: {accent_bg};
    border: 1px solid rgba(16,185,129,0.25);
    color: {accent};
    font-size: 0.78rem;
    font-weight: 700;
}}

.s-card {{
    background: {card};
    border-radius: 16px;
    padding: 1.6rem 1.8rem;
    border: 1px solid {card_border};
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    margin-bottom: 1.4rem;
    transition: transform 0.20s ease, box-shadow 0.20s ease, border-color 0.20s ease;
}}
.s-card:hover {{
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(0,0,0,0.08);
    border-color: rgba(16, 185, 129, 0.30);
}}
.s-card-title {{
    font-size: 1.15rem;
    font-weight: 700;
    color: {text1};
    margin-bottom: 1rem;
    letter-spacing: -0.01em;
}}

[data-testid="stMetric"] {{
    background: {card};
    border-radius: 14px;
    padding: 1.1rem 1.3rem;
    border: 1px solid {card_border};
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    text-align: center;
    transition: transform 0.20s ease, box-shadow 0.20s ease, border-color 0.20s ease;
}}
[data-testid="stMetric"]:hover {{
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(0,0,0,0.07);
    border-color: rgba(16, 185, 129, 0.30);
}}
[data-testid="stMetricValue"] {{
    font-size: 1.35rem !important;
    font-weight: 800 !important;
    color: {accent} !important;
}}
[data-testid="stMetricLabel"] {{
    font-size: 0.80rem !important;
    font-weight: 600 !important;
    color: {text2} !important;
}}
[data-testid="stMetricDelta"] {{ display: none !important; }}

[data-testid="stTabs"] [data-baseweb="tab-list"] {{
    background: transparent !important;
    border-bottom: 1px solid {divider_col} !important;
}}
[data-testid="stTabs"] [aria-selected="true"] {{
    background: transparent !important;
    color: {accent} !important;
    border-bottom: 2px solid {accent} !important;
    font-weight: 700 !important;
}}
</style>"""
