def get_css(dark: bool = False) -> str:
    """Return the full <style> block. Tokens switch between light and dark modes."""

    # ── Colour tokens ──────────────────────────────────────────────────────
    bg           = "#1a1d27"                      if dark else "linear-gradient(135deg,#f0fdf4 0%,#dcfce7 40%,#f9fffe 100%)"
    card         = "rgba(30,40,55,0.90)"          if dark else "rgba(255,255,255,0.92)"
    card_border  = "rgba(74,222,128,0.25)"        if dark else "#a7f3d0"
    text1        = "#f0faf0"                      if dark else "#0f3d1a"     # boosted contrast
    text2        = "#c4e8c4"                      if dark else "#1a5c29"     # was too faint
    input_bg     = "rgba(15,25,40,0.95)"          if dark else "#ffffff"
    input_border = "rgba(74,222,128,0.50)"        if dark else "#4ade80"
    input_text   = "#f0faf0"                      if dark else "#0f3d1a"
    border       = "#4a5568"                      if dark else "#a7f3d0"
    shadow_card  = "0.30"                         if dark else "0.10"
    shadow_hover = "0.40"                         if dark else "0.18"
    blob_opacity = "0.04"                         if dark else "0.18"
    blob1_col    = "#22c55e"                      if dark else "#bbf7d0"
    blob2_col    = "#16a34a"                      if dark else "#d1fae5"
    menu_bg      = "#1e2837"                      if dark else "#ffffff"
    menu_text    = "#f0faf0"                      if dark else "#0f3d1a"
    stat_bg      = "rgba(255,255,255,0.08)"       if dark else "rgba(255,255,255,0.95)"
    stat_border  = "rgba(74,222,128,0.30)"        if dark else "#86efac"
    stat_val     = "#4ade80"                      if dark else "#14532d"
    stat_lbl     = "#c4e8c4"                      if dark else "#1a5c29"
    chip_bg      = "rgba(22,163,74,0.20)"         if dark else "rgba(220,252,231,0.95)"
    chip_border  = "rgba(74,222,128,0.50)"        if dark else "#4ade80"
    chip_color   = "#86efac"                      if dark else "#14532d"
    panel_title  = "#4ade80"                      if dark else "#14532d"
    panel_border = "rgba(74,222,128,0.30)"        if dark else "#bbf7d0"
    uploader_bg  = "rgba(22,163,74,0.10)"         if dark else "rgba(240,253,244,0.95)"
    uploader_bdr = "rgba(74,222,128,0.60)"        if dark else "#4ade80"
    uploader_txt = "#86efac"                      if dark else "#14532d"
    uploader_btn = "rgba(22,163,74,0.25)"         if dark else "#bbf7d0"
    success_bg   = "rgba(22,163,74,0.18)"         if dark else "#dcfce7"
    success_bdr  = "rgba(74,222,128,0.50)"        if dark else "#4ade80"
    success_txt  = "#86efac"                      if dark else "#14532d"
    tbl_hover    = "rgba(255,255,255,0.06)"       if dark else "rgba(220,252,231,0.50)"
    divider_col  = "rgba(74,222,128,0.20)"        if dark else "#bbf7d0"
    label_col    = "#c4e8c4"                      if dark else "#1a5c29"     # widget labels

    # ── 3D Hero Color Palette matching Target Image ──
    if dark:
        hero_bg             = "linear-gradient(135deg,rgba(4,8,18,0.97) 0%,rgba(8,24,16,0.96) 60%,rgba(4,8,22,0.97) 100%)"
        hero_border         = "rgba(74,222,128,0.28)"
        hero_shadow         = "0 48px 100px rgba(0,0,0,0.65), 0 20px 40px rgba(0,0,0,0.40), inset 0 1px 0 rgba(255,255,255,0.10), 0 0 0 1px rgba(74,222,128,0.08)"
        hero_title_color    = "#ffffff"
        hero_title_bg       = "none"
        hero_title_clip     = "initial"
        hero_title_fill     = "initial"
        hero_title_shadow   = "0 2px 4px rgba(0,0,0,0.80), 0 8px 32px rgba(0,0,0,0.60), 0 0 60px rgba(74,222,128,0.25)"
        hero_overlay_bg     = "rgba(0,0,0,0.35)"
        hero_overlay_bdr    = "rgba(255,255,255,0.07)"
        hero_overlay_shd    = "0 8px 32px rgba(0,0,0,0.40), inset 0 1px 0 rgba(255,255,255,0.06)"
        hero_float_bg       = "rgba(5,12,24,0.72)"
        hero_float_color    = "#ffffff"
        hero_float_bdr      = "rgba(255,255,255,0.18)"
        hero_float_shadow   = "0 12px 40px rgba(0,0,0,0.55), inset 0 1px 0 rgba(255,255,255,0.14), 0 0 0 1px rgba(74,222,128,0.10)"
        hero_float_span     = "#6ee7b7"
        
        hero_sub_color      = "rgba(220,252,231,0.92)"
        hero_sub_shadow     = "0 1px 4px rgba(0,0,0,0.50)"
        hero_sub_span_color = "rgba(187,247,208,0.70)"
        
        badge_bg            = "rgba(22,163,74,0.30)"
        badge_bdr           = "rgba(74,222,128,0.70)"
        badge_txt           = "#a7f3d0"
        badge_shadow        = "0 0 18px rgba(74,222,128,0.28), inset 0 1px 0 rgba(255,255,255,0.10)"
        badge_text_shadow   = "0 1px 3px rgba(0,0,0,0.50)"
        
        badge_cyan_bg       = "rgba(0,200,240,0.22)"
        badge_cyan_bdr      = "rgba(0,229,255,0.60)"
        badge_cyan_txt      = "#a5f3fc"
        badge_cyan_shd      = "0 0 18px rgba(0,229,255,0.25), inset 0 1px 0 rgba(255,255,255,0.10)"
        
        badge_purple_bg     = "rgba(139,92,246,0.25)"
        badge_purple_bdr    = "rgba(167,139,250,0.60)"
        badge_purple_txt    = "#ddd6fe"
        badge_purple_shd    = "0 0 18px rgba(139,92,246,0.28), inset 0 1px 0 rgba(255,255,255,0.10)"
        
        badge_white_bg      = "rgba(255,255,255,0.14)"
        badge_white_bdr     = "rgba(255,255,255,0.35)"
        badge_white_txt     = "#f0f0f0"
        badge_white_shd     = "0 0 12px rgba(255,255,255,0.10), inset 0 1px 0 rgba(255,255,255,0.15)"
    else:
        hero_bg             = "rgba(255, 255, 255, 0.82)"
        hero_border         = "rgba(74, 222, 128, 0.35)"
        hero_shadow         = "0 30px 70px rgba(74, 222, 128, 0.12), 0 4px 20px rgba(0, 0, 0, 0.02), inset 0 1px 0 rgba(255,255,255,0.95)"
        hero_title_color    = "transparent"
        hero_title_bg       = "linear-gradient(90deg, #113f1e 0%, #1c7c34 50%, #4caf50 100%)"
        hero_title_clip     = "text"
        hero_title_fill     = "transparent"
        hero_title_shadow   = "none"
        hero_overlay_bg     = "transparent"
        hero_overlay_bdr    = "transparent"
        hero_overlay_shd    = "none"
        hero_float_bg       = "#ffffff"
        hero_float_color    = "#14532d"
        hero_float_bdr      = "rgba(74, 222, 128, 0.35)"
        hero_float_shadow   = "0 8px 30px rgba(74, 222, 128, 0.10), 0 2px 10px rgba(0, 0, 0, 0.04)"
        hero_float_span     = "#16a34a"
        
        hero_sub_color      = "#15803d"
        hero_sub_shadow     = "none"
        hero_sub_span_color = "#4b5563"
        
        badge_bg            = "#ffffff"
        badge_bdr           = "rgba(74, 222, 128, 0.35)"
        badge_txt           = "#14532d"
        badge_shadow        = "0 4px 15px rgba(74, 222, 128, 0.08)"
        badge_text_shadow   = "none"
        
        badge_cyan_bg       = "#ffffff"
        badge_cyan_bdr      = "rgba(74, 222, 128, 0.35)"
        badge_cyan_txt      = "#14532d"
        badge_cyan_shd      = "0 4px 15px rgba(74, 222, 128, 0.08)"
        
        badge_purple_bg     = "#ffffff"
        badge_purple_bdr    = "rgba(74, 222, 128, 0.35)"
        badge_purple_txt    = "#14532d"
        badge_purple_shd    = "0 4px 15px rgba(74, 222, 128, 0.08)"
        
        badge_white_bg      = "#ffffff"
        badge_white_bdr     = "rgba(74, 222, 128, 0.35)"
        badge_white_txt     = "#14532d"
        badge_white_shd     = "0 4px 15px rgba(74, 222, 128, 0.08)"

    return f"""
<style>
/* ══════════════════════════════════════════════
   FONTS
══════════════════════════════════════════════ */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@500;600;700;800;900&display=swap');
*,*::before,*::after {{ box-sizing: border-box; }}
html, body, [class*="css"] {{ font-family: 'Inter', sans-serif; }}

/* ══════════════════════════════════════════════
   GREEN HEADER / TOOLBAR
══════════════════════════════════════════════ */
header[data-testid="stHeader"] {{
    background: linear-gradient(90deg,#14532d 0%,#15803d 50%,#16a34a 100%) !important;
    border-bottom: 2px solid rgba(74,222,128,0.40) !important;
    box-shadow: 0 2px 16px rgba(22,163,74,0.30) !important;
    height: 3.2rem !important;
}}
header[data-testid="stHeader"] *,
[data-testid="stToolbar"],
[data-testid="stToolbar"] * {{
    color: #d1fae5 !important;
    fill: #d1fae5 !important;
    stroke: #d1fae5 !important;
}}
[data-testid="stDecoration"] {{
    background: linear-gradient(90deg,#4ade80,#16a34a,#15803d) !important;
    height: 3px !important;
}}
#MainMenu, footer {{ display: none !important; }}

/* ══════════════════════════════════════════════
   APP BACKGROUND
══════════════════════════════════════════════ */
.stApp {{
    background: {bg} !important;
    min-height: 100vh;
}}
.block-container {{
    padding: 1.5rem 2rem 3rem !important;
    max-width: 1000px;
}}

/* ══════════════════════════════════════════════
   SIDEBAR
══════════════════════════════════════════════ */
[data-testid="stSidebar"] {{
    background: linear-gradient(170deg,#0f3d1a 0%,#14532d 50%,#166534 100%) !important;
    border-right: 1px solid rgba(74,222,128,0.20) !important;
    box-shadow: 4px 0 32px rgba(20,83,45,0.35) !important;
}}
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] div,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] div,
[data-testid="stSidebar"] li,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stMarkdown p,
[data-testid="stSidebar"] .stMarkdown span {{ color: #ffffff !important; }}
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {{ color: #ffffff !important; font-weight: 700 !important; }}
[data-testid="stSidebar"] strong {{ color: #ffffff !important; font-weight: 700 !important; }}
[data-testid="stSidebar"] hr {{ border-color: rgba(255,255,255,0.25) !important; }}
/* Sidebar captions */
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p,
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] span {{
    color: #d1fae5 !important;
    font-size: 0.80rem !important;
}}
/* Inline code in sidebar (preset dimensions) */
[data-testid="stSidebar"] code {{
    color: #4ade80 !important;
    background: rgba(74,222,128,0.15) !important;
    border-radius: 4px !important;
    padding: 0.1rem 0.4rem !important;
    font-size: 0.78rem !important;
}}

/* ══════════════════════════════════════════════
   GLOBAL TEXT — high contrast
══════════════════════════════════════════════ */
body, p, div, li, span,
.stMarkdown, .stMarkdown p {{ color: {text1} !important; }}
h1,h2,h3,h4,h5,h6 {{ color: {text1} !important; font-weight: 700 !important; }}
strong {{ color: {text1} !important; }}

/* Caption text — must stay readable */
[data-testid="stCaptionContainer"] p {{
    color: {text2} !important;
    font-size: 0.85rem !important;
}}

/* Widget labels — boosted visibility */
label,
[data-testid="stWidgetLabel"],
[data-testid="stWidgetLabel"] p,
.stCheckbox label,
.stSelectbox label,
.stNumberInput label,
.stSlider label {{
    color: {label_col} !important;
    font-weight: 700 !important;
    font-size: 0.84rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
}}

/* ══════════════════════════════════════════════
   STREAMLIT INTERNAL — strip stray backgrounds
══════════════════════════════════════════════ */
[data-testid="stForm"] {{
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
}}
[data-testid="stVerticalBlock"],
[data-testid="stVerticalBlockBorderWrapper"],
[data-testid="stHorizontalBlock"],
[data-testid="column"],
div[data-testid="stElementContainer"],
div.stMarkdown,
div.element-container,
[data-testid="stFormSubmitButton"] {{
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}}

/* ══════════════════════════════════════════════
   INPUTS
══════════════════════════════════════════════ */
.stNumberInput input,
input[type="number"] {{
    color: {input_text} !important;
    background: {input_bg} !important;
    border: 2px solid {input_border} !important;
    border-radius: 10px !important;
    font-size: 0.95rem !important;
    font-weight: 700 !important;
}}
.stNumberInput input:focus {{
    border-color: #16a34a !important;
    box-shadow: 0 0 0 3px rgba(22,163,74,0.25) !important;
}}

/* Selectbox */
.stSelectbox div[data-baseweb="select"] > div,
[data-baseweb="select"] > div {{
    color: {input_text} !important;
    background: {input_bg} !important;
    border: 2px solid {input_border} !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    font-size: 0.92rem !important;
    box-shadow: none !important;
}}
/* ── Dropdown / Popover — full override for light mode ── */
[data-baseweb="popover"],
[data-baseweb="popover"] *,
[data-baseweb="menu"],
[data-baseweb="menu"] *,
[role="listbox"],
[role="listbox"] * {{
    background: {menu_bg} !important;
    color: {menu_text} !important;
}}
/* Popover container itself */
[data-baseweb="popover"] {{
    background: {menu_bg} !important;
    border: 2px solid {input_border} !important;
    border-radius: 14px !important;
    box-shadow: 0 16px 48px rgba(0,0,0,0.18) !important;
    overflow: hidden !important;
}}
/* Individual items */
[data-baseweb="menu"] ul,
[role="listbox"] {{
    background: {menu_bg} !important;
    padding: 6px !important;
}}
[data-baseweb="menu"] li,
[role="option"] {{
    background: {menu_bg} !important;
    color: {menu_text} !important;
    font-weight: 600 !important;
    font-size: 0.92rem !important;
    border-radius: 8px !important;
    margin: 2px 0 !important;
    padding: 8px 12px !important;
}}
/* Hover state */
[data-baseweb="menu"] li:hover,
[role="option"]:hover {{
    background: rgba(22,163,74,0.18) !important;
    color: #15803d !important;
}}
/* Selected / active item */
[aria-selected="true"],
[aria-selected="true"] * {{
    background: rgba(22,163,74,0.22) !important;
    color: #14532d !important;
    font-weight: 700 !important;
}}
/* Overide any dark surfaces Streamlit injects into the popover */
[data-baseweb="popover"] [class*="surface"],
[data-baseweb="popover"] [class*="bg"] {{
    background: {menu_bg} !important;
}}

/* Slider */
input[type="range"] {{ accent-color: #16a34a; }}
[data-testid="stSlider"] [data-testid="stMarkdownContainer"] p {{
    color: {text1} !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
}}

/* Checkbox */
.stCheckbox span {{
    color: {text2} !important;
    font-weight: 600 !important;
    font-size: 0.92rem !important;
}}

/* ══════════════════════════════════════════════
   FILE UPLOADER
══════════════════════════════════════════════ */
@keyframes glowPulse {{
    0%, 100% {{ box-shadow: 0 0  0  0 rgba(74,222,128,0.00); border-color: {uploader_bdr}; }}
    50%       {{ box-shadow: 0 0 22px 6px rgba(74,222,128,0.22); border-color: #4ade80; }}
}}
[data-testid="stFileUploaderDropzone"],
[data-testid="stFileUploaderDropzone"] > div {{
    background: {uploader_bg} !important;
    border: 2px dashed {uploader_bdr} !important;
    border-radius: 18px !important;
    transition: transform 0.25s ease, background 0.25s ease !important;
}}
[data-testid="stFileUploaderDropzone"]:hover,
[data-testid="stFileUploaderDropzone"]:focus-within {{
    animation: glowPulse 1.8s ease-in-out infinite !important;
    transform: scale(1.012) !important;
    background: rgba(22,163,74,0.14) !important;
}}
[data-testid="stFileUploaderDropzone"] span,
[data-testid="stFileUploaderDropzone"] p,
[data-testid="stFileUploaderDropzoneInstructions"] span {{
    color: {uploader_txt} !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
}}
[data-testid="stFileUploaderDropzone"] button {{
    background: {uploader_btn} !important;
    color: {uploader_txt} !important;
    border: 2px solid {uploader_bdr} !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
}}
/* Uploaded file name */
[data-testid="stFileUploaderFile"] span {{
    color: {text1} !important;
    font-weight: 600 !important;
}}

/* ══════════════════════════════════════════════
   BUTTONS
══════════════════════════════════════════════ */
.stButton button,
[data-testid="stFormSubmitButton"] button {{
    background: linear-gradient(135deg,#15803d 0%,#16a34a 100%) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.65rem 1.8rem !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    box-shadow: 0 4px 16px rgba(22,163,74,0.40) !important;
    transition: all 0.25s !important;
    font-family: 'Inter', sans-serif !important;
}}
.stButton button:hover,
[data-testid="stFormSubmitButton"] button:hover {{
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(22,163,74,0.50) !important;
    background: linear-gradient(135deg,#166534 0%,#15803d 100%) !important;
}}
.stButton button p,
.stButton button span,
[data-testid="stFormSubmitButton"] button p,
[data-testid="stFormSubmitButton"] button span {{
    color: #ffffff !important;
    font-weight: 700 !important;
}}

.stDownloadButton button {{
    background: linear-gradient(135deg,#0d9488,#0f766e) !important;
    box-shadow: 0 4px 16px rgba(13,148,136,0.40) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.65rem 1.8rem !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    transition: all 0.25s !important;
}}
.stDownloadButton button:hover {{
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(13,148,136,0.50) !important;
}}
.stDownloadButton button p,
.stDownloadButton button span {{ color: #ffffff !important; font-weight: 700 !important; }}

/* ══════════════════════════════════════════════
   ALERTS
══════════════════════════════════════════════ */
[data-testid="stSuccess"] {{
    background: {success_bg} !important;
    border: 2px solid {success_bdr} !important;
    border-radius: 14px !important;
}}
[data-testid="stSuccess"] p {{ color: {success_txt} !important; font-weight: 600 !important; }}
[data-testid="stInfo"] {{
    background: rgba(22,163,74,0.10) !important;
    border: 2px solid rgba(74,222,128,0.35) !important;
    border-radius: 14px !important;
}}
[data-testid="stInfo"] p {{ color: {text1} !important; font-weight: 500 !important; }}
[data-testid="stError"] {{ border-radius: 14px !important; }}

/* ══════════════════════════════════════════════
   PROGRESS BAR
══════════════════════════════════════════════ */
[data-testid="stProgressBar"] > div {{
    background: rgba(22,163,74,0.18) !important;
    border-radius: 99px !important;
}}
[data-testid="stProgressBar"] > div > div {{
    background: linear-gradient(90deg,#16a34a,#4ade80) !important;
    border-radius: 99px !important;
}}

/* ══════════════════════════════════════════════
   METRIC CARDS — clearly visible values
══════════════════════════════════════════════ */
@keyframes metricFadeUp {{
    from {{ opacity: 0; transform: translateY(10px); }}
    to   {{ opacity: 1; transform: translateY(0);    }}
}}
[data-testid="stMetric"] {{
    background: {stat_bg};
    backdrop-filter: blur(20px) saturate(160%);
    -webkit-backdrop-filter: blur(20px) saturate(160%);
    border-radius: 18px;
    padding: 1.2rem 1.4rem;
    border: 2px solid {stat_border};
    box-shadow:
        0 4px 20px rgba(22,163,74,0.12),
        inset 0 1px 0 rgba(255,255,255,0.10);
    text-align: center;
    transition: box-shadow 0.28s ease, transform 0.28s ease;
    animation: metricFadeUp 0.45s ease both;
}}
[data-testid="stMetric"]:hover {{
    box-shadow:
        0 12px 36px rgba(22,163,74,0.22),
        inset 0 1px 0 rgba(255,255,255,0.15),
        0 0 0 1.5px rgba(74,222,128,0.40);
    transform: translateY(-3px);
}}
[data-testid="stMetricValue"] {{
    font-family: 'Poppins', sans-serif !important;
    font-size: 1.30rem !important;
    font-weight: 900 !important;
    color: {stat_val} !important;
    letter-spacing: -0.01em !important;
}}
[data-testid="stMetricLabel"] {{
    font-size: 0.74rem !important;
    font-weight: 700 !important;
    color: {stat_lbl} !important;
    text-transform: uppercase !important;
    letter-spacing: 0.07em !important;
}}
[data-testid="stMetricDelta"] {{ display: none !important; }}

/* ══════════════════════════════════════════════
   DATAFRAME — history table
══════════════════════════════════════════════ */
[data-testid="stDataFrame"] {{
    border-radius: 16px !important;
    overflow: hidden !important;
    border: 2px solid {stat_border} !important;
}}
.stDataFrame th {{
    background: rgba(22,163,74,0.20) !important;
    color: {text1} !important;
    font-weight: 700 !important;
    font-size: 0.80rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.06em !important;
}}
.stDataFrame td {{
    color: {text1} !important;
    font-weight: 500 !important;
    font-size: 0.88rem !important;
}}

/* ══════════════════════════════════════════════
   DIVIDER
══════════════════════════════════════════════ */
hr {{ border-color: {divider_col} !important; margin: 0.8rem 0 !important; }}

/* ══════════════════════════════════════════════
   FLOATING BLOBS (ambient decoration)
══════════════════════════════════════════════ */
.blob {{
    position: fixed;
    border-radius: 50%;
    filter: blur(120px);
    opacity: {blob_opacity};
    pointer-events: none;
    z-index: 0;
    will-change: transform;
    animation: blobFloat 22s ease-in-out infinite alternate;
}}
.blob1 {{
    width: 850px; height: 850px;
    background: radial-gradient(circle at 40% 40%, {blob1_col}, {blob2_col});
    top: -350px; left: -350px;
    animation-duration: 24s;
}}
.blob2 {{
    width: 700px; height: 700px;
    background: radial-gradient(circle at 60% 60%, {blob2_col}, {blob1_col});
    bottom: -300px; right: -300px;
    animation-delay: 6s; animation-duration: 20s;
}}
.blob3 {{
    width: 480px; height: 480px;
    background: radial-gradient(circle, rgba(74,222,128,0.55), transparent 70%);
    top: 38%; left: 55%;
    filter: blur(100px);
    animation-delay: 3s; animation-duration: 17s;
}}
@keyframes blobFloat {{
    0%   {{ transform: translate(0,   0)   scale(1.00) rotate(0deg);  }}
    30%  {{ transform: translate(45px, -35px) scale(1.06) rotate(4deg);  }}
    65%  {{ transform: translate(-25px, 45px) scale(0.94) rotate(-3deg); }}
    100% {{ transform: translate(30px, 20px) scale(1.04) rotate(2deg);  }}
}}

/* ══════════════════════════════════════════════
   CARD / PANEL TITLE helpers
══════════════════════════════════════════════ */
.s-card {{
    background: {card};
    backdrop-filter: blur(24px) saturate(180%);
    -webkit-backdrop-filter: blur(24px) saturate(180%);
    border-radius: 20px;
    padding: 1.6rem 1.8rem;
    border: 1.5px solid {card_border};
    box-shadow:
        0 8px 32px rgba(0,0,0,{shadow_card}),
        inset 0 1px 0 rgba(255,255,255,0.12),
        0 0 0 0 rgba(74,222,128,0);
    margin-bottom: 1.2rem;
    transition: box-shadow 0.30s ease, transform 0.30s ease;
}}
.s-card:hover {{
    box-shadow:
        0 18px 48px rgba(0,0,0,{shadow_hover}),
        inset 0 1px 0 rgba(255,255,255,0.18),
        0 0 0 1.5px rgba(74,222,128,0.35);
    transform: translateY(-4px);
}}

.s-panel-title {{
    font-family: 'Poppins', sans-serif;
    font-size: 1rem;
    font-weight: 700;
    color: {panel_title};
    border-bottom: 2px solid {panel_border};
    padding-bottom: 0.6rem;
    margin-bottom: 1rem;
}}

/* Hero banners */
.s-hero {{
    background: linear-gradient(135deg,#f0fdf4 0%,#dcfce7 55%,#fafff8 100%);
    border-radius: 24px;
    padding: 2rem 2.4rem 1.6rem;
    border: 1.5px solid #86efac;
    margin-bottom: 1.5rem;
    box-shadow: 0 8px 32px rgba(22,163,74,0.12);
}}
.s-hero-dark {{
    background: linear-gradient(135deg,#0f3d1a 0%,#14532d 55%,#15803d 100%);
    border-radius: 24px;
    padding: 2rem 2.4rem 1.6rem;
    border: 1.5px solid rgba(74,222,128,0.35);
    margin-bottom: 1.5rem;
    box-shadow: 0 8px 32px rgba(0,0,0,0.35);
}}

/* Chips */
.s-chip {{
    display: inline-flex;
    align-items: center;
    padding: 0.30rem 0.85rem;
    border-radius: 8px;
    background: {chip_bg};
    border: 1.5px solid {chip_border};
    color: {chip_color};
    font-size: 0.80rem;
    font-weight: 700;
    margin-right: 0.4rem;
    margin-bottom: 0.4rem;
}}

/* Empty state */
.s-empty {{ text-align: center; padding: 3rem 2rem; }}
.s-empty-icon {{ font-size: 3.5rem; margin-bottom: 1rem; }}

/* Format pills */
.fmt-pill {{ display:inline-block; padding:0.18rem 0.6rem; border-radius:6px;
            font-size:0.72rem; font-weight:800; letter-spacing:0.05em; }}
.fmt-jpeg {{ background:rgba(251,191,36,0.20); color:#b45309;
            border:1.5px solid rgba(251,191,36,0.50); }}
.fmt-png  {{ background:rgba(59,130,246,0.18); color:#1d4ed8;
            border:1.5px solid rgba(59,130,246,0.45); }}
.fmt-webp {{ background:rgba(16,185,129,0.18); color:#047857;
            border:1.5px solid rgba(16,185,129,0.45); }}

/* ══════════════════════════════════════════════
   STREAMLIT TABS (new feature sections)
══════════════════════════════════════════════ */
[data-testid="stTabs"] [data-baseweb="tab-list"] {{
    background: transparent !important;
    border-bottom: 2px solid {divider_col} !important;
    gap: 0.25rem !important;
}}
[data-testid="stTabs"] [data-baseweb="tab"] {{
    background: transparent !important;
    color: {text2} !important;
    font-weight: 600 !important;
    font-size: 0.90rem !important;
    border-radius: 10px 10px 0 0 !important;
    padding: 0.5rem 1.2rem !important;
    border: none !important;
    transition: all 0.2s !important;
}}
[data-testid="stTabs"] [aria-selected="true"] {{
    background: rgba(22,163,74,0.18) !important;
    color: {panel_title} !important;
    border-bottom: 3px solid #16a34a !important;
    font-weight: 800 !important;
}}
[data-testid="stTabs"] [data-baseweb="tab"]:hover {{
    background: rgba(22,163,74,0.10) !important;
    color: {panel_title} !important;
}}

/* ══════════════════════════════════════════════
   OCR — text area
══════════════════════════════════════════════ */
.stTextArea textarea {{
    background: {input_bg} !important;
    color: {input_text} !important;
    border: 2px solid {input_border} !important;
    border-radius: 12px !important;
    font-family: 'Inter', monospace !important;
    font-size: 0.92rem !important;
    line-height: 1.6 !important;
    resize: vertical !important;
}}
.stTextArea textarea:focus {{
    border-color: #16a34a !important;
    box-shadow: 0 0 0 3px rgba(22,163,74,0.20) !important;
}}

/* ══════════════════════════════════════════════
   ANALYTICS — chart containers
══════════════════════════════════════════════ */
.analytics-card {{
    background: {stat_bg};
    backdrop-filter: blur(20px) saturate(160%);
    -webkit-backdrop-filter: blur(20px) saturate(160%);
    border: 2px solid {stat_border};
    border-radius: 20px;
    padding: 1.3rem 1.6rem;
    text-align: center;
    box-shadow: 0 4px 20px rgba(22,163,74,0.10), inset 0 1px 0 rgba(255,255,255,0.10);
    transition: box-shadow 0.30s ease, transform 0.30s ease;
    animation: metricFadeUp 0.5s ease both;
}}
.analytics-card:hover {{
    box-shadow:
        0 16px 44px rgba(22,163,74,0.22),
        inset 0 1px 0 rgba(255,255,255,0.15),
        0 0 0 1.5px rgba(74,222,128,0.38);
    transform: translateY(-5px);
}}
.analytics-val {{
    font-family: 'Poppins', sans-serif;
    font-size: 1.7rem;
    font-weight: 900;
    color: {stat_val};
    letter-spacing: -0.02em;
}}
.analytics-lbl {{
    font-size: 0.72rem;
    font-weight: 700;
    color: {stat_lbl};
    text-transform: uppercase;
    letter-spacing: 0.07em;
    margin-top: 0.30rem;
}}

/* Plotly chart background blending */
.js-plotly-plot, .plotly, .plot-container {{
    border-radius: 16px !important;
    overflow: hidden !important;
}}

/* ══════════════════════════════════════════════
   CONFIDENCE BADGE (OCR)
══════════════════════════════════════════════ */
.conf-badge {{
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.28rem 0.9rem;
    border-radius: 99px;
    font-size: 0.82rem;
    font-weight: 800;
    letter-spacing: 0.04em;
}}
.conf-high   {{ background:rgba(22,163,74,0.18); color:#15803d; border:1.5px solid rgba(22,163,74,0.40); }}
.conf-medium {{ background:rgba(251,191,36,0.18); color:#b45309; border:1.5px solid rgba(251,191,36,0.50); }}
.conf-low    {{ background:rgba(239,68,68,0.18);  color:#b91c1c; border:1.5px solid rgba(239,68,68,0.45); }}

/* ══════════════════════════════════════════════
   PROCESSING TIME BADGE
══════════════════════════════════════════════ */
.proc-time {{
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    padding: 0.25rem 0.80rem;
    border-radius: 99px;
    background: rgba(22,163,74,0.14);
    border: 1.5px solid rgba(22,163,74,0.35);
    color: {panel_title};
    font-size: 0.78rem;
    font-weight: 700;
}}

/* ══════════════════════════════════════════════
   MICRO-ANIMATION KEYFRAMES
══════════════════════════════════════════════ */
@keyframes fadeInScale {{
    from {{ opacity:0; transform:scale(0.94) translateY(18px); }}
    to   {{ opacity:1; transform:scale(1)    translateY(0);    }}
}}
@keyframes floatY {{
    0%,100% {{ transform:translateY(0px);  }}
    50%     {{ transform:translateY(-9px); }}
}}
@keyframes shimmer {{
    0%   {{ background-position:-200% center; }}
    100% {{ background-position: 200% center; }}
}}
@keyframes pulseGlow {{
    0%,100% {{ box-shadow:0 0 10px rgba(74,222,128,0.20); }}
    50%     {{ box-shadow:0 0 32px rgba(74,222,128,0.55),0 0 64px rgba(22,163,74,0.20); }}
}}
@keyframes badgePop {{
    from {{ opacity:0; transform:scale(0.65) translateY(10px); }}
    to   {{ opacity:1; transform:scale(1)    translateY(0);    }}
}}
@keyframes floatCard {{
    0%,100% {{ transform:translateY(0px)   rotateX(2deg)  rotateY(-3deg); }}
    50%     {{ transform:translateY(-12px) rotateX(-2deg) rotateY(3deg);  }}
}}
@keyframes orbDrift {{
    0%   {{ transform:translate(0,0)       scale(1.00); }}
    33%  {{ transform:translate(55px,-40px) scale(1.14); }}
    66%  {{ transform:translate(-30px,55px) scale(0.90); }}
    100% {{ transform:translate(40px,25px)  scale(1.07); }}
}}
@keyframes ringPulse {{
    0%,100% {{ opacity:0.35; transform:scale(1);    }}
    50%     {{ opacity:0.65; transform:scale(1.05); }}
}}
@keyframes borderSweep {{
    from {{ transform:rotate(0deg);   }}
    to   {{ transform:rotate(360deg); }}
}}
@keyframes uploadPulse {{
    0%,100% {{ transform:translateY(0)   scale(1);    }}
    50%     {{ transform:translateY(-7px) scale(1.05); }}
}}

/* ══════════════════════════════════════════════
   AMBIENT 3D ORBS & GLASS RINGS
══════════════════════════════════════════════ */
.orb {{
    position:fixed;
    border-radius:50%;
    pointer-events:none;
    z-index:0;
    will-change:transform;
    animation:orbDrift 26s ease-in-out infinite alternate;
}}
.orb-cyan {{
    background:radial-gradient(circle at 35% 35%,rgba(0,229,255,0.28),rgba(0,229,255,0) 65%);
    filter:blur(90px);
    animation-duration:28s;
}}
.orb-purple {{
    background:radial-gradient(circle at 60% 40%,rgba(157,78,255,0.22),rgba(157,78,255,0) 65%);
    filter:blur(100px);
    animation-duration:32s;
    animation-direction:alternate-reverse;
    animation-delay:-8s;
}}
.orb-emerald {{
    background:radial-gradient(circle at 50% 50%,rgba(0,255,157,0.18),rgba(0,255,157,0) 65%);
    filter:blur(110px);
    animation-duration:22s;
    animation-delay:-4s;
}}
.glass-ring {{
    position:fixed;
    border-radius:50%;
    border:1.5px solid rgba(255,255,255,0.07);
    pointer-events:none;
    z-index:0;
    animation:ringPulse 9s ease-in-out infinite;
    backdrop-filter:blur(1px);
}}

/* ══════════════════════════════════════════════
   3D TILT CARDS (JS-driven via .tilt-3d class)
══════════════════════════════════════════════ */
.tilt-3d {{
    transition:transform 0.18s ease, box-shadow 0.30s ease;
    transform-style:preserve-3d;
    will-change:transform;
    cursor:default;
}}
.tilt-3d:hover {{
    box-shadow:
        0 28px 70px rgba(0,0,0,0.38),
        0 0 50px rgba(74,222,128,0.18),
        inset 0 1px 0 rgba(255,255,255,0.14);
}}

/* ══════════════════════════════════════════════
   3D HERO SECTION
══════════════════════════════════════════════ */
.hero-3d-wrap {{
    position:relative;
    border-radius:32px;
    padding:2.8rem 3rem 2.2rem;
    background:{hero_bg};
    border:1.5px solid {hero_border};
    backdrop-filter:blur(40px) saturate(200%);
    -webkit-backdrop-filter:blur(40px) saturate(200%);
    box-shadow:{hero_shadow};
    overflow:hidden;
    margin-top:1.2rem;
    margin-bottom:2.4rem;
    transform-style:preserve-3d;
}}
/* Rotating neon border conic sweep — dimmed so content reads clearly */
.hero-3d-wrap::before {{
    content:'';
    position:absolute;
    inset:-2px;
    border-radius:33px;
    background:conic-gradient(
        from 0deg,
        transparent 0deg,
        rgba(74,222,128,0.30) 60deg,
        rgba(0,229,255,0.18) 120deg,
        transparent 180deg,
        rgba(157,78,255,0.18) 240deg,
        transparent 360deg
    );
    animation:borderSweep 8s linear infinite;
    z-index:-1;
    opacity:0.40;
}}
/* Ultra-subtle inner mesh grid — 5% opacity */
.hero-3d-wrap::after {{
    content:'';
    position:absolute;
    inset:0;
    background-image:
        linear-gradient(rgba(255,255,255,0.025) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,0.025) 1px, transparent 1px);
    background-size:48px 48px;
    pointer-events:none;
    z-index:0;
}}

/* Hero title — pure white or gradient, dominant, maximum readability */
.hero-gradient-title {{
    font-family:'Poppins',sans-serif;
    font-size:2.75rem;
    font-weight:900;
    line-height:1.08;
    letter-spacing:-0.03em;
    color:{hero_title_color};
    background:{hero_title_bg};
    -webkit-background-clip:{hero_title_clip};
    -webkit-text-fill-color:{hero_title_fill};
    background-clip:{hero_title_clip};
    text-shadow:{hero_title_shadow};
    margin-bottom:0.7rem;
    position:relative;
    z-index:4;
}}

/* Content elevation overlay — dark glass layer behind text */
.hero-content-overlay {{
    position:relative;
    z-index:4;
    background:{hero_overlay_bg};
    backdrop-filter:blur(8px);
    -webkit-backdrop-filter:blur(8px);
    border-radius:20px;
    padding:1.6rem 2rem;
    border:1px solid {hero_overlay_bdr};
    box-shadow:{hero_overlay_shd};
}}
/* Floating 3D decorative cards inside hero — stronger glass */
.hero-float-card {{
    position:absolute;
    background:{hero_float_bg};
    backdrop-filter:blur(20px) saturate(180%);
    -webkit-backdrop-filter:blur(20px) saturate(180%);
    border:1px solid {hero_float_bdr};
    border-radius:14px;
    padding:0.65rem 1rem;
    font-size:0.75rem;
    font-weight:700;
    color:{hero_float_color};
    pointer-events:none;
    z-index:5;
    box-shadow:{hero_float_shadow};
    animation:floatCard 6s ease-in-out infinite;
}}
.hero-float-card span {{
    color:{hero_float_span} !important;
}}
.hero-float-card:nth-of-type(1) {{ animation-delay:0s; }}
.hero-float-card:nth-of-type(2) {{ animation-delay:-2s; }}
.hero-float-card:nth-of-type(3) {{ animation-delay:-4s; }}

/* Subtitle and sub-text */
.hero-subtitle {{
    font-size: 1.05rem !important;
    color: {hero_sub_color} !important;
    line-height: 1.75 !important;
    margin-bottom: 1.4rem !important;
    font-weight: 700 !important;
    max-width: 540px !important;
    text-shadow: {hero_sub_shadow} !important;
}}
.hero-subtitle-sub {{
    font-size: 0.84rem !important;
    color: {hero_sub_span_color} !important;
    font-weight: 400 !important;
    display: block;
    margin-top: 0.35rem;
}}

/* ══════════════════════════════════════════════
   ANIMATED NEON BADGES — high contrast
══════════════════════════════════════════════ */
.badge-3d {{
    display:inline-flex;
    align-items:center;
    gap:0.38rem;
    padding:0.32rem 0.95rem;
    border-radius:99px;
    font-size:0.74rem;
    font-weight:800;
    letter-spacing:0.05em;
    text-transform:uppercase;
    border:1.5px solid;
    animation:badgePop 0.5s cubic-bezier(0.34,1.56,0.64,1) both;
    transition:transform 0.2s ease, box-shadow 0.2s ease, background 0.2s ease;
    cursor:default;
    margin-right:0.45rem;
    margin-bottom:0.5rem;
    position:relative;
    z-index:4;
    text-shadow:{badge_text_shadow};
}}
.badge-3d:hover {{ transform:translateY(-3px) scale(1.08); }}
/* Emerald — brighter, solid-feeling */
.badge-emerald {{
    background:{badge_bg};
    border-color:{badge_bdr};
    color:{badge_txt};
    box-shadow:{badge_shadow};
}}
/* Cyan — increased contrast */
.badge-cyan {{
    background:{badge_cyan_bg};
    border-color:{badge_cyan_bdr};
    color:{badge_cyan_txt};
    box-shadow:{badge_cyan_shd};
    animation-delay:0.1s;
}}
/* Purple — increased contrast */
.badge-purple {{
    background:{badge_purple_bg};
    border-color:{badge_purple_bdr};
    color:{badge_purple_txt};
    box-shadow:{badge_purple_shd};
    animation-delay:0.2s;
}}
/* White — clearly visible */
.badge-white {{
    background:{badge_white_bg};
    border-color:{badge_white_bdr};
    color:{badge_white_txt};
    box-shadow:{badge_white_shd};
    animation-delay:0.3s;
}}

/* ══════════════════════════════════════════════
   NEON GLOW UTILITIES
══════════════════════════════════════════════ */
.glow-emerald {{ box-shadow:0 0 20px rgba(74,222,128,0.42),0 0 60px rgba(22,163,74,0.22); }}
.glow-cyan    {{ box-shadow:0 0 20px rgba(0,229,255,0.42), 0 0 60px rgba(0,229,255,0.16); }}
.glow-purple  {{ box-shadow:0 0 20px rgba(157,78,255,0.42),0 0 60px rgba(157,78,255,0.16); }}
.text-glow-emerald {{ text-shadow:0 0 22px rgba(74,222,128,0.65); }}
.text-glow-cyan    {{ text-shadow:0 0 22px rgba(0,229,255,0.65);  }}

/* ══════════════════════════════════════════════
   3D METRIC CARDS — depth overlay
══════════════════════════════════════════════ */
[data-testid="stMetric"] {{
    transform-style:preserve-3d;
    position:relative;
}}
[data-testid="stMetric"]::after {{
    content:'';
    position:absolute;
    inset:0;
    border-radius:18px;
    background:linear-gradient(135deg,rgba(74,222,128,0.09) 0%,rgba(0,229,255,0.04) 50%,transparent 100%);
    pointer-events:none;
}}

/* ══════════════════════════════════════════════
   PREMIUM UPLOAD ZONE — floating icon + glow
══════════════════════════════════════════════ */
[data-testid="stFileUploaderDropzoneInstructions"] svg,
[data-testid="stFileUploaderDropzone"] svg {{
    animation:uploadPulse 3s ease-in-out infinite;
    filter:drop-shadow(0 0 8px rgba(74,222,128,0.55));
}}

/* ══════════════════════════════════════════════
   FLOATING GLASS NAV DOCK
══════════════════════════════════════════════ */
.glass-dock {{
    position:fixed;
    bottom:24px;
    left:50%;
    transform:translateX(-50%);
    display:flex;
    gap:0.35rem;
    background:rgba(8,18,28,0.80);
    backdrop-filter:blur(28px) saturate(200%);
    -webkit-backdrop-filter:blur(28px) saturate(200%);
    border:1px solid rgba(74,222,128,0.18);
    border-radius:99px;
    padding:0.45rem 0.7rem;
    box-shadow:
        0 20px 60px rgba(0,0,0,0.45),
        inset 0 1px 0 rgba(255,255,255,0.08),
        0 0 0 1px rgba(74,222,128,0.05),
        0 0 40px rgba(74,222,128,0.08);
    z-index:9999;
}}
.dock-item {{
    display:flex;
    flex-direction:column;
    align-items:center;
    justify-content:center;
    width:42px;
    height:42px;
    border-radius:12px;
    font-size:1.15rem;
    cursor:pointer;
    transition:transform 0.22s cubic-bezier(0.34,1.56,0.64,1),background 0.2s ease,box-shadow 0.2s ease;
    position:relative;
    text-decoration:none;
}}
.dock-item:hover {{
    transform:scale(1.38) translateY(-7px);
    background:rgba(74,222,128,0.16);
    box-shadow:0 8px 24px rgba(74,222,128,0.25);
}}
.dock-item .dock-label {{
    position:absolute;
    bottom:calc(100% + 10px);
    left:50%;
    transform:translateX(-50%) translateY(6px);
    background:rgba(5,12,20,0.90);
    backdrop-filter:blur(8px);
    color:#e2fce8;
    font-family:'Inter',sans-serif;
    font-size:0.62rem;
    font-weight:700;
    padding:0.18rem 0.55rem;
    border-radius:6px;
    white-space:nowrap;
    opacity:0;
    pointer-events:none;
    transition:opacity 0.18s ease,transform 0.18s ease;
    border:1px solid rgba(74,222,128,0.20);
}}
.dock-item:hover .dock-label {{
    opacity:1;
    transform:translateX(-50%) translateY(0);
}}

/* ══════════════════════════════════════════════
   COMPARISON SLIDER — glass handle
══════════════════════════════════════════════ */
.cmp-handle-glass {{
    width:40px;
    height:40px;
    background:rgba(22,163,74,0.28);
    backdrop-filter:blur(12px);
    -webkit-backdrop-filter:blur(12px);
    border-radius:50%;
    border:2px solid rgba(74,222,128,0.75);
    box-shadow:
        0 0 0 5px rgba(74,222,128,0.14),
        0 10px 28px rgba(0,0,0,0.32),
        inset 0 1px 0 rgba(255,255,255,0.22);
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:13px;
    color:#fff;
    transition:box-shadow 0.25s,transform 0.25s;
    cursor:col-resize;
}}
.cmp-handle-glass:hover,
#cmpHandle:hover .cmp-handle-glass {{
    box-shadow:
        0 0 0 9px rgba(74,222,128,0.20),
        0 0 35px rgba(74,222,128,0.55),
        0 10px 28px rgba(0,0,0,0.32);
    transform:scale(1.14);
}}
</style>"""
