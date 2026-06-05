"""
Image Studio Pro — Streamlit App
Logic: Python + Pillow  |  UI: Streamlit API
HTML kept only for: CSS injection · comparison slider (JS) · ambient blobs
"""
import io
import base64
from datetime import datetime

import pandas as pd
import streamlit as st
from PIL import Image

from utils.image_processor import (
    load_image, resize_image, save_image,
    image_to_b64, format_bytes, compression_pct, PRESETS, FORMAT_EXT,
)
from utils.styles import get_css

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
#  SESSION STATE
# ══════════════════════════════════════════════
_defaults = {"section": "upload", "dark": False, "history": [], "batch_results": []}
for k, v in _defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

dark = st.session_state.dark

# ══════════════════════════════════════════════
#  CSS + DECORATIONS
# ══════════════════════════════════════════════
st.markdown(get_css(dark), unsafe_allow_html=True)
# Ambient blobs are position:fixed CSS decorations — no Streamlit native equivalent
st.markdown('<div class="blob blob1"></div><div class="blob blob2"></div>',
            unsafe_allow_html=True)


# ══════════════════════════════════════════════
#  PURE-PYTHON HELPERS
# ══════════════════════════════════════════════
def time_ago(iso: str) -> str:
    diff = (datetime.now() - datetime.fromisoformat(iso)).total_seconds()
    if diff < 60:    return "Just now"
    if diff < 3600:  return f"{int(diff / 60)}m ago"
    if diff < 86400: return f"{int(diff / 3600)}h ago"
    return f"{int(diff / 86400)}d ago"


def section_header(icon: str, title: str, subtitle: str = "") -> None:
    """Render a consistent section header using native Streamlit."""
    st.markdown(f"## {icon} {title}")
    if subtitle:
        st.caption(subtitle)
    st.divider()


def card(title: str = "", icon: str = "") -> None:
    """Render a labelled card title using native Streamlit subheader."""
    if title:
        st.markdown(f"**{icon} {title}**" if icon else f"**{title}**")


# Only unavoidable HTML: JavaScript-driven before/after slider
def comparison_slider(b64_before: str, b64_after: str) -> None:
    st.markdown(f"""
    <div style="position:relative;width:100%;border-radius:16px;overflow:hidden;
                user-select:none;touch-action:none;margin-top:0.5rem;" id="cmp">
      <img src="{b64_before}"
           style="display:block;width:100%;height:auto;max-height:320px;
                  object-fit:contain;background:#f0fdf4;" />
      <div id="cmpAfter"
           style="position:absolute;top:0;left:0;width:50%;height:100%;
                  overflow:hidden;border-right:3px solid #16a34a;">
        <img src="{b64_after}"
             style="display:block;width:100%;height:auto;max-height:320px;
                    object-fit:contain;background:#ffffff;position:absolute;
                    top:0;left:0;" id="cmpAfterImg"/>
      </div>
      <div id="cmpHandle"
           style="position:absolute;top:0;bottom:0;left:50%;width:3px;
                  background:#16a34a;cursor:col-resize;display:flex;
                  align-items:center;justify-content:center;">
        <div style="width:32px;height:32px;background:#16a34a;border-radius:50%;
                    border:3px solid white;box-shadow:0 2px 8px rgba(0,0,0,0.3);
                    display:flex;align-items:center;justify-content:center;
                    font-size:12px;color:white;">⟺</div>
      </div>
      <span style="position:absolute;top:8px;left:8px;background:rgba(0,0,0,0.60);
                   color:#fff;font-size:11px;font-weight:800;padding:3px 10px;
                   border-radius:99px;">BEFORE</span>
      <span style="position:absolute;top:8px;right:8px;background:rgba(22,163,74,0.85);
                   color:#fff;font-size:11px;font-weight:800;padding:3px 10px;
                   border-radius:99px;">AFTER</span>
    </div>
    <input type="range" min="0" max="100" value="50" id="cmpSlider"
      style="width:100%;margin-top:0.5rem;accent-color:#16a34a;"
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
SECTIONS = [
    ("upload",   "📤", "Upload & Convert"),
    ("batch",    "📦", "Batch Processing"),
    ("history",  "🕓", "Download History"),
    ("settings", "⚙️",  "Settings"),
]

with st.sidebar:
    # ── Branding ──
    st.markdown("# 🌿 Image Studio Pro")
    st.caption("Resize · Convert · Export — 100% Private")
    st.divider()

    # ── Navigation ──
    st.markdown("**NAVIGATION**")
    for sid, icon, label in SECTIONS:
        active = st.session_state.section == sid
        btn_label = f"{'▶ ' if active else ''}{icon}  {label}"
        if st.button(btn_label, key=f"nav_{sid}", use_container_width=True):
            st.session_state.section = sid
            st.rerun()

    st.divider()

    # ── How to Use ──
    st.markdown("**📖 HOW TO USE**")
    st.markdown(
        "**1️⃣ Upload** — Drop a JPG, PNG or WEBP  \n"
        "**2️⃣ Preset** — Pick a size preset or enter custom  \n"
        "**3️⃣ Format** — Choose output format  \n"
        "**4️⃣ Quality** — Set compression (JPEG/WEBP)  \n"
        "**5️⃣ Convert** — Click ⚡ Convert Image  \n"
        "**6️⃣ Download** — Save your result"
    )

    st.divider()

    # ── Format Guide ──
    st.markdown("**🎨 FORMAT GUIDE**")
    st.markdown(
        "🟡 **JPEG** — Best for photos. Small file sizes. "
        "Slight quality loss (lossy).  \n"
        "🔵 **PNG** — Lossless quality. Supports transparency. "
        "Larger files.  \n"
        "🟢 **WEBP** — Modern format. Best compression + quality. "
        "Widely supported."
    )

    st.divider()

    # ── Preset Sizes ──
    st.markdown("**📐 PRESET DIMENSIONS**")
    preset_info = [
        ("Instagram Post",    "1080 × 1080"),
        ("Instagram Story",   "1080 × 1920"),
        ("YouTube Thumbnail", "1280 × 720"),
        ("WhatsApp DP",       "512 × 512"),
        ("HD Wallpaper",      "1920 × 1080"),
        ("Twitter Header",    "1500 × 500"),
        ("Facebook Cover",    "820 × 312"),
    ]
    for name, size in preset_info:
        col_n, col_s = st.columns([3, 2])
        col_n.caption(name)
        col_s.caption(f"`{size}`")

    st.divider()

    # ── Tips ──
    st.markdown("**💡 TIPS**")
    st.markdown(
        "• Use **WEBP** for web images — smallest file size  \n"
        "• Use **PNG** when you need a transparent background  \n"
        "• **Quality 80–90** is ideal for JPEG — good balance  \n"
        "• Enable **aspect ratio lock** to avoid distortion  \n"
        "• Batch mode converts **multiple files at once**"
    )

    st.divider()

    # ── Theme toggle ──
    col1, col2 = st.columns(2)
    with col1:
        st.caption("🌙 Dark" if dark else "☀️ Light")
    with col2:
        if st.button("Switch", key="theme_toggle", use_container_width=True):
            st.session_state.dark = not dark
            st.rerun()

    st.divider()

    # ── About ──
    st.markdown("**ℹ️ ABOUT**")
    st.caption(
        "Image Studio Pro v2.0  \n"
        "Built with Python · Streamlit · Pillow  \n"
        "🔒 No uploads · No sign-up · Fully local"
    )


# ══════════════════════════════════════════════
#  UPLOAD & CONVERT
# ══════════════════════════════════════════════
def render_upload() -> None:
    # ── Hero Banner ──
    title_grad = "linear-gradient(90deg,#14532d,#16a34a,#4ade80)" if not dark else "linear-gradient(90deg,#4ade80,#86efac,#ffffff)"
    hero_bg    = ("linear-gradient(135deg,#0f3d1a 0%,#14532d 40%,#1a5c29 70%,#166534 100%)"
                  if dark else
                  "linear-gradient(135deg,#f0fdf4 0%,#dcfce7 35%,#bbf7d0 65%,#f0fdf4 100%)")
    border_col = "rgba(74,222,128,0.40)" if dark else "rgba(22,163,74,0.30)"
    sub_col    = "#a7f3d0"               if dark else "#166534"
    chip_dark  = "rgba(255,255,255,0.12)" if dark else "rgba(255,255,255,0.70)"
    chip_bdr   = "rgba(255,255,255,0.25)" if dark else "rgba(22,163,74,0.35)"
    chip_txt   = "#d1fae5"               if dark else "#14532d"

    st.markdown(f"""
    <div style="
        background: {hero_bg};
        border-radius: 28px;
        padding: 2.4rem 2.8rem 2rem;
        border: 1.5px solid {border_col};
        box-shadow: 0 12px 48px rgba(22,163,74,0.15), 0 2px 8px rgba(0,0,0,0.06);
        margin-top: 1.2rem;
        margin-bottom: 2.4rem;
        position: relative;
        overflow: hidden;
    ">
      <!-- decorative circles -->
      <div style="position:absolute;top:-60px;right:-60px;width:220px;height:220px;
                  border-radius:50%;background:rgba(74,222,128,0.12);pointer-events:none;"></div>
      <div style="position:absolute;bottom:-40px;left:30%;width:160px;height:160px;
                  border-radius:50%;background:rgba(22,163,74,0.08);pointer-events:none;"></div>
      <div style="position:absolute;top:20px;right:140px;width:80px;height:80px;
                  border-radius:50%;background:rgba(74,222,128,0.10);pointer-events:none;"></div>

      <!-- badge: gap between emoji and text via margin -->
      <div style="display:inline-flex;align-items:center;
                  padding:0.32rem 1.1rem;border-radius:99px;
                  background:rgba(22,163,74,0.18);
                  border:1.5px solid rgba(22,163,74,0.40);
                  margin-bottom:1.2rem;">
        <span style="font-size:1rem;">🌿</span>
        <span style="display:inline-block;width:0.55rem;"></span>
        <span style="font-size:0.74rem;font-weight:800;letter-spacing:0.12em;
                     color:#15803d;text-transform:uppercase;">Image Studio Pro</span>
      </div>

      <!-- title: solid accent color on Resizer (gradient-clip broken in Streamlit iframes) -->
      <div style="font-family:'Poppins',sans-serif;font-size:2.6rem;font-weight:900;
                  line-height:1.10;margin-bottom:0.65rem;letter-spacing:-0.02em;">
        <span style="color:{'#f0fdf4' if dark else '#14532d'};">Image&#8202;</span>
        <span style="color:{'#4ade80' if dark else '#16a34a'};">Resizer</span>
        <span style="color:{'#f0fdf4' if dark else '#14532d'};"> &amp; Converter</span>
      </div>

      <!-- subtitle -->
      <div style="font-size:1.05rem;color:{sub_col};line-height:1.7;margin-bottom:1.4rem;font-weight:500;">
        Upload any image · Resize to any dimension · Convert between formats · Download instantly
      </div>

      <!-- feature chips -->
      <div style="display:flex;flex-wrap:wrap;gap:0.5rem;">
        {''.join(f'<span style="display:inline-flex;align-items:center;gap:0.35rem;padding:0.32rem 0.9rem;border-radius:99px;background:{chip_dark};border:1.5px solid {chip_bdr};color:{chip_txt};font-size:0.78rem;font-weight:700;">{chip}</span>'
        for chip in ["🔒 100% Private","⚡ Instant","📦 Batch Mode","🖼️ JPEG · PNG · WEBP","📐 7 Size Presets","🌓 Dark Mode"])}
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

    # File info — native metrics
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
        st.image(img, use_container_width=True)

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
        m1.metric("New Size",      format_bytes(len(out_bytes)))
        m2.metric("Original Size", format_bytes(len(raw)))
        m3.metric("New Dimensions", f"{rw} × {rh}")
        m4.metric("Space Saved",   f"{saved_pct}%" if saved_pct > 0 else "—")

        st.write("")

        # Before / After (HTML slider — JS required, no Streamlit equivalent)
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

        # Save to history
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


# ══════════════════════════════════════════════
#  BATCH PROCESSING
# ══════════════════════════════════════════════
def render_batch() -> None:
    section_header("📦", "Batch Processing",
                   "Convert multiple images at once with the same settings.")

    # Settings
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
                 use_container_width=True, key="batch_go"):
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
            st.session_state.history.insert(0, {
                "name":     f.name,
                "orig_fmt": (img.format or "JPEG").upper(),
                "out_fmt":  b_fmt,
                "orig_sz":  len(raw),
                "out_sz":   len(out),
                "dims":     f"{iw} × {ih}",
                "ts":       datetime.now().isoformat(),
            })
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
#  DOWNLOAD HISTORY
# ══════════════════════════════════════════════
def render_history() -> None:
    h = st.session_state.history
    section_header("🕓", "Download History",
                   f"{len(h)} conversion{'s' if len(h) != 1 else ''} this session.")

    if not h:
        st.info("No history yet. Convert an image to see it here.", icon="ℹ️")
        return

    col_btn, _ = st.columns([1, 4])
    with col_btn:
        if st.button("🗑️ Clear History", key="clear_hist"):
            st.session_state.history = []
            st.rerun()

    # Build DataFrame — 100% Python, no HTML table
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
#  SETTINGS
# ══════════════════════════════════════════════
def render_settings() -> None:
    section_header("⚙️", "Settings", "App preferences and information.")

    # ── Preferences ──
    st.markdown("### 🎨 Preferences")
    st.write(f"**Current theme:** {'🌙 Dark mode' if dark else '☀️ Light mode'}")

    sc1, sc2 = st.columns(2)
    with sc1:
        if st.button("🌓 Toggle Theme", key="settings_theme", use_container_width=True):
            st.session_state.dark = not dark
            st.rerun()
    with sc2:
        if st.button("🗑️ Clear All History", key="settings_clear", use_container_width=True):
            st.session_state.history = []
            st.session_state.batch_results = []
            st.success("All history cleared.")

    st.divider()

    # ── Privacy ──
    st.markdown("### 🔒 Privacy")
    st.success(
        "**100% Local Processing**  \n"
        "All image operations run on your machine using Python + Pillow.  \n"
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

    # ── About ──
    st.markdown("### ℹ️ About")
    st.markdown(
        "**Image Studio Pro v2.0**  \n"
        "Built with Python · Streamlit · Pillow  \n"
        "Open source · No sign-up · No upload limits"
    )


# ══════════════════════════════════════════════
#  ROUTING
# ══════════════════════════════════════════════
_route = {
    "upload":   render_upload,
    "batch":    render_batch,
    "history":  render_history,
    "settings": render_settings,
}
_route.get(st.session_state.section, render_upload)()
