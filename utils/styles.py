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
    blob_opacity = "0.07"                         if dark else "0.40"
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
[data-testid="stFileUploaderDropzone"],
[data-testid="stFileUploaderDropzone"] > div {{
    background: {uploader_bg} !important;
    border: 2px dashed {uploader_bdr} !important;
    border-radius: 16px !important;
    transition: all 0.3s !important;
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
[data-testid="stMetric"] {{
    background: {stat_bg};
    backdrop-filter: blur(10px);
    border-radius: 16px;
    padding: 1.1rem 1.3rem;
    border: 2px solid {stat_border};
    box-shadow: 0 4px 16px rgba(22,163,74,0.10);
    text-align: center;
}}
[data-testid="stMetricValue"] {{
    font-family: 'Poppins', sans-serif !important;
    font-size: 1.25rem !important;
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
    filter: blur(90px);
    opacity: {blob_opacity};
    pointer-events: none;
    z-index: 0;
    animation: blobDrift 18s ease-in-out infinite alternate;
}}
.blob1 {{ width:700px; height:700px; background:{blob1_col}; top:-250px; left:-250px; }}
.blob2 {{ width:600px; height:600px; background:{blob2_col}; bottom:-250px; right:-250px; animation-delay: 4s; }}
@keyframes blobDrift {{
    from {{ transform: translate(0, 0) scale(1); }}
    to   {{ transform: translate(30px, 20px) scale(1.05); }}
}}

/* ══════════════════════════════════════════════
   CARD / PANEL TITLE helpers
══════════════════════════════════════════════ */
.s-card {{
    background: {card};
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    border-radius: 20px;
    padding: 1.6rem 1.8rem;
    border: 1.5px solid {card_border};
    box-shadow: 0 8px 32px rgba(0,0,0,{shadow_card});
    margin-bottom: 1.2rem;
    transition: box-shadow 0.25s;
}}
.s-card:hover {{ box-shadow: 0 12px 40px rgba(0,0,0,{shadow_hover}); }}

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
</style>"""
