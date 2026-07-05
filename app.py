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
    "section":       "upload",
    "dark":          False,
    "history":       [],
    "batch_results": [],
    "analytics":     [],          # NEW: per-session analytics log
    "ocr_result":    None,        # NEW: cache last OCR result
    "wm_preview":    None,        # NEW: cache watermark preview bytes
}
for k, v in _defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

dark = st.session_state.dark

# ══════════════════════════════════════════════
#  CSS + DECORATIONS
# ══════════════════════════════════════════════
st.markdown(get_css(dark), unsafe_allow_html=True)
# Ambient blobs — position:fixed decorations
st.markdown(
    '<div class="blob blob1"></div><div class="blob blob2"></div><div class="blob blob3"></div>',
    unsafe_allow_html=True,
)
# 3D neon orbs + glass rings
st.markdown("""
<div class="orb orb-cyan"  style="width:420px;height:420px;top:-180px;right:5%;"></div>
<div class="orb orb-purple" style="width:380px;height:380px;bottom:-160px;left:8%;"></div>
<div class="orb orb-emerald" style="width:300px;height:300px;top:45%;right:25%;"></div>
<div class="glass-ring" style="width:500px;height:500px;top:-200px;left:-200px;"></div>
<div class="glass-ring" style="width:360px;height:360px;bottom:-150px;right:-120px;animation-delay:-3s;"></div>
""", unsafe_allow_html=True)
# JS: mouse-tracking 3D tilt for .tilt-3d elements
st.markdown("""
<script>
(function(){
  function initTilt(){
    document.querySelectorAll('.tilt-3d').forEach(function(el){
      el.addEventListener('mousemove',function(e){
        var r=el.getBoundingClientRect();
        var dx=(e.clientX-(r.left+r.width/2))/(r.width/2);
        var dy=(e.clientY-(r.top+r.height/2))/(r.height/2);
        el.style.transform='perspective(900px) rotateY('+(dx*9)+'deg) rotateX('+(-dy*9)+'deg) translateZ(14px)';
        el.style.transition='transform 0.08s ease';
      });
      el.addEventListener('mouseleave',function(){
        el.style.transform='perspective(900px) rotateY(0) rotateX(0) translateZ(0)';
        el.style.transition='transform 0.55s ease';
      });
    });
  }
  var obs=new MutationObserver(initTilt);
  obs.observe(document.body,{childList:true,subtree:true});
  initTilt();
})();
</script>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════
#  PURE-PYTHON HELPERS
# ══════════════════════════════════════════════
def time_ago(iso: str) -> str:
    """Return a human-readable 'time ago' string from an ISO timestamp."""
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
SECTIONS = [
    ("upload",    "📤", "Upload & Convert"),
    ("batch",     "📦", "Batch Processing"),
    ("bg_remove", "✂️",  "Background Remover"),
    ("ocr",       "🔤", "Text Extractor (OCR)"),
    ("watermark", "🖊️",  "Watermark Studio"),
    ("analytics", "📊", "Analytics Dashboard"),
    ("history",   "🕓", "Download History"),
    ("settings",  "⚙️",  "Settings"),
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
        "Image Studio Pro v3.0  \n"
        "Built with Python · Streamlit · Pillow  \n"
        "🌐 [Live App](https://imageconverterpro.streamlit.app/)  \n"
        "🔒 No uploads · No sign-up · Fully local"
    )

# Floating Docker for quick access
st.markdown("""
<div style="position:fixed;bottom:20px;right:20px;z-index:9999;
            background:rgba(15,23,42,0.8);backdrop-filter:blur(12px);
            padding:10px 16px;border-radius:12px;border:1px solid rgba(255,255,255,0.1);
            display:flex;gap:12px;box-shadow:0 10px 25px rgba(0,0,0,0.3);">
  <span style="font-size:16px;">✨</span>
  <span style="font-size:12px;color:#cbd5e1;font-weight:600;">Image Studio Pro</span>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════
#  SECTION 1 — UPLOAD & CONVERT  (unchanged)
# ══════════════════════════════════════════════
def render_upload() -> None:
    """Render the single-image resize/convert section."""
    # ── Hero Banner — 3D Glassmorphism ──
    st.markdown("""\
<div class="hero-3d-wrap tilt-3d">
  <div class="hero-float-card" style="top:16px;right:20px;">
    🖼️&nbsp; PNG &rarr; WEBP &nbsp;<span style="color:#6ee7b7;">-62%</span>
  </div>
  <div class="hero-float-card" style="top:80px;right:12px;">
    ✓&nbsp; <span style="color:#67e8f9;">Background Removed</span>
  </div>
  <div class="hero-float-card" style="bottom:20px;right:16px;">
    🤖&nbsp; OCR&nbsp;<span style="color:#c4b5fd;">98.4%</span>
  </div>
  <div class="hero-content-overlay">
    <div style="margin-bottom:0.85rem;">
      <span class="badge-3d badge-emerald">🌿 Image Studio Pro</span>
      <span class="badge-3d badge-cyan">🔒 100% Private</span>
    </div>
    <div class="hero-gradient-title">Image Resizer &amp; Converter</div>
    <div class="hero-subtitle">
      Upload &middot; Resize &middot; Convert &middot; Remove BG &middot; Extract Text &middot; Watermark
      <span class="hero-subtitle-sub">All processing runs locally — your images never leave your device.</span>
    </div>
    <div style="display:flex;flex-wrap:wrap;gap:0.15rem;">
      <span class="badge-3d badge-emerald" style="animation-delay:0.05s;">⚡ Instant</span>
      <span class="badge-3d badge-cyan" style="animation-delay:0.12s;">📦 Batch Mode</span>
      <span class="badge-3d badge-purple" style="animation-delay:0.20s;">✂️ AI BG Removal</span>
      <span class="badge-3d badge-white" style="animation-delay:0.28s;">🔤 OCR Extractor</span>
      <span class="badge-3d badge-emerald" style="animation-delay:0.36s;">📐 7 Presets</span>
      <span class="badge-3d badge-cyan" style="animation-delay:0.44s;">🌓 Dark Mode</span>
    </div>
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
    if st.button("🪄  Remove Background", use_container_width=True, key="bg_go"):
        with st.spinner("🧠 AI is removing the background… (first run may take a moment to load the model)"):
            try:
                out_bytes, elapsed = remove_background(raw)
            except Exception as exc:
                st.error(f"Background removal failed: {exc}", icon="❌")
                return

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
    section_header("🔤", "Text Extractor (OCR)",
                   "Extract text from images, screenshots, and scanned documents.")

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

        if st.button("🔍  Extract Text", use_container_width=True, key="ocr_go"):
            with st.spinner("🧠 Running OCR… (first run may take a moment to load the model)"):
                try:
                    result = extract_text(img, languages=["en"])
                    st.session_state["ocr_result"]   = result
                    st.session_state["ocr_filename"] = uploaded.name
                    st.session_state["ocr_raw_len"]  = len(raw)
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
            if st.button("🗑️ Clear Result", key="ocr_clear", use_container_width=True):
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
    section_header("🖊️", "Watermark Studio",
                   "Add text or logo watermarks to your images with full control.")

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

            if st.button("✅  Apply Text Watermark", use_container_width=True, key="wm_text_apply"):
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

            if logo_file and st.button("✅  Apply Logo Watermark", use_container_width=True, key="wm_logo_apply"):
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
        if st.button("🗑️ Clear Watermark", key="wm_clear", use_container_width=False):
            st.session_state.pop("_wm_result", None)
            st.session_state.pop("_wm_type", None)
            st.rerun()


# ══════════════════════════════════════════════
#  SECTION 6 — ANALYTICS DASHBOARD  (NEW)
# ══════════════════════════════════════════════
def render_analytics() -> None:
    """Render the session analytics dashboard."""
    section_header("📊", "Analytics Dashboard",
                   "Track all image processing operations during this session.")

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
        if st.button("🗑️ Clear Analytics", key="clear_analytics", use_container_width=True):
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
        if st.button("🗑️ Clear All Data", key="settings_clear", use_container_width=True):
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
_route.get(st.session_state.section, render_upload)()
