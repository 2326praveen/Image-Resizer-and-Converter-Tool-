# 🌿 Image Studio Pro

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://imageconverterpro.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Privacy First](https://img.shields.io/badge/Privacy-100%25%20Local-10B981)](https://imageconverterpro.streamlit.app/)

**Image Studio Pro** is an open-source, privacy-first image editing and media utility suite built with **Streamlit**, **Pillow**, **u2net**, and **EasyOCR**. It provides 8 creative and conversion tools with an **Emerald & Violet design system**, dark/light mode theming, and an optional **Supabase cloud sync** layer.

🔗 **Live Deployment**: [imageconverterpro.streamlit.app](https://imageconverterpro.streamlit.app/)  
📁 **GitHub Repository**: [2326praveen/Image-Resizer-and-Converter-Tool-](https://github.com/2326praveen/Image-Resizer-and-Converter-Tool-)

---

## 🌟 Core Highlights

- 🔒 **100% Local & Private**: All image processing, compression, AI background removal, and OCR run directly inside your local Python runtime. No external image servers are ever contacted.
- ⚡ **Production-Grade Local AI**: Powered by `u2net` for sub-pixel background isolation and `EasyOCR` for multi-language text detection without third-party API costs or data sharing.
- 🎨 **Modern Design System**: Light canvas (`#FBFBFA`) with Emerald (`#10B981`) primary actions, Violet (`#7C3AED`) secondary treatments, ambient corner glows, and a one-click Dark/Light mode toggle.
- 🔑 **Guest-First with Optional Cloud Sync**: Every single tool is accessible instantly with zero sign-up required. Users can optionally create a free account to sync their download history and analytics across devices.

---

## 🛠️ The 8 Creative Modules

### 1. 📤 Upload & Convert
- **Format Transcoding**: Convert seamlessly between **JPEG**, **PNG**, and modern **WEBP**.
- **Social Media Presets**: One-click dimensions for Instagram (Post/Story), YouTube Thumbnails, Twitter Headers, WhatsApp DP, HD Wallpapers, and Facebook Covers.
- **Smart Compression**: Adjustable quality sliders with live space-saving calculations (save up to 80% with WebP).
- **Interactive Before/After Slider**: Real-time interactive split-pane comparison to inspect visual quality before downloading.

### 2. 📦 Batch Processing
- **Bulk Media Conversion**: Upload dozens of images simultaneously.
- **Unified Presets**: Apply global dimension constraints, output formats, and compression quality across the entire batch in one pass.
- **Progress Tracking & Instant Downloads**: Real-time progress bar with per-file download buttons.

### 3. ✂️ AI Background Remover
- **Neural Auto-Cutout**: Powered by the deep learning `rembg` (`u2net`) model.
- **Clean Transparent PNGs**: Isolates subjects, products, and portraits with sub-pixel edge detection.
- **Cached Memory Engine**: Loads the neural network once per session for sub-2-second subsequent runs.

### 4. 🔤 Text Extractor (OCR)
- **Deep Neural OCR**: Powered by `EasyOCR` to detect line and word boundaries in scanned documents, receipts, screenshots, and infographics.
- **Weighted Confidence Scoring**: Computes text detection accuracy and provides word/line counts.
- **Plain Text Export**: In-app editable text area with one-click `.txt` UTF-8 download.

### 5. 🖊️ Watermark Studio
- **Dual Watermarking Modes**: Apply customizable copyright text signatures or transparent brand logo PNGs.
- **Fine-Tuned Controls**: 9-point anchor snapping (Top-Left to Bottom-Right), 0–100% opacity, 360° rotation, and dynamic font/logo scaling.
- **Live Canvas Preview**: Real-time visual feedback before applying the stamp.

### 6. 📊 Analytics Dashboard
- **Session Intelligence**: Track cumulative bandwidth saved, total conversions, and format distribution.
- **Interactive Charts**: Responsive Plotly visualizations breakdown file size reductions and operation frequencies.
- **CSV Data Export**: Export session audit logs to a clean `.csv` file.

### 7. 🕒 Download History
- **Conversion Audit Log**: Detailed ledger displaying source format, target format, original file size, output size, compression percentage, dimensions, and relative timestamp.
- **Instant Re-Downloads**: Quickly access and re-download assets processed during the current session.

### 8. ⚙️ Settings & Themes
- **Dark / Light Mode Toggle**: Seamlessly switch between the clean light theme and the sleek dark slate (`#0F172A` / `#1E293B`) theme.
- **Session Memory Purge**: One-click wipe of active memory and session cache.
- **Privacy & Security Center**: Offline architecture documentation and licensing information.

---

## 🔑 Optional User Authentication & Cloud Sync

Image Studio Pro is engineered with a **Guest-First** philosophy:

```
┌────────────────────────────────────────────────────────┐
│                   IMAGE STUDIO PRO                     │
│                                                        │
│   ┌──────────────────────┐   ┌──────────────────────┐  │
│   │     GUEST MODE       │   │    LOGGED-IN USER    │  │
│   │  (No Setup Needed)   │   │  (Optional Supabase) │  │
│   │                      │   │                      │  │
│   │ • 100% Tool Access   │   │ • 100% Tool Access   │  │
│   │ • In-Memory History  │   │ • Persistent History │  │
│   │ • Zero Sign-Up       │   │ • Cloud Analytics    │  │
│   │ • Total Local Priv.  │   │ • Multi-Device Sync  │  │
│   └──────────────────────┘   └──────────────────────┘  │
└────────────────────────────────────────────────────────┘
```

- **Zero Friction**: If no database secrets are configured, the app runs in 100% Guest Mode with zero prompts or popups.
- **Purely Additive**: Connecting **Supabase** unlocks cross-session download history persistence and cross-device sync.

### Enabling Cloud Sync (Optional)

1. Create a free project at [supabase.com](https://supabase.com).
2. Execute the database schema provided in [`SETUP_AUTH.md`](./SETUP_AUTH.md) in your Supabase SQL Editor.
3. Configure your credentials:
   - **Locally**: Add to `.streamlit/secrets.toml`:
     ```toml
     SUPABASE_URL = "https://your-project-id.supabase.co"
     SUPABASE_ANON_KEY = "your-supabase-anon-key"
     ```
   - **Streamlit Community Cloud**: Paste the same keys into **App Settings $\rightarrow$ Secrets**.

---

## 🚀 Quick Start & Local Setup

### Prerequisites
- **Python 3.9+** (Python 3.10–3.12 recommended)
- **Git**

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/2326praveen/Image-Resizer-and-Converter-Tool-.git
   cd Image-Resizer-and-Converter-Tool-
   ```

2. **Create and activate a virtual environment**:
   ```bash
   # Windows (PowerShell)
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1

   # macOS / Linux
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Launch the application**:
   ```bash
   streamlit run app.py
   ```
   Open your browser at `http://localhost:8501`.

---

## ☁️ Deployment Guide

### Deploying to Streamlit Community Cloud

1. Fork or push this repository to your GitHub account.
2. Sign in to [share.streamlit.io](https://share.streamlit.io/).
3. Click **New app**, select your repository, branch (`main`), and set the main file path to `app.py`.
4. *(Optional)* If using Supabase authentication, expand **Advanced settings $\rightarrow$ Secrets** and paste your `SUPABASE_URL` and `SUPABASE_ANON_KEY`.
5. Click **Deploy!**

---

## 📁 Repository Structure

```text
├── app.py                      # Main Streamlit application & routing
├── requirements.txt            # Python dependencies (Streamlit, Pillow, EasyOCR, Rembg, etc.)
├── SETUP_AUTH.md               # Supabase database schema & setup guide
├── .streamlit/
│   ├── config.toml             # Streamlit theme & performance configuration
│   └── secrets.toml            # (Local only, ignored by Git) Supabase API credentials
├── utils/
│   ├── auth.py                 # Supabase authentication & SSL handlers
│   ├── background_remover.py   # AI background removal utilities (rembg)
│   ├── ocr_processor.py        # Neural text extraction utilities (EasyOCR)
│   ├── persistence.py          # Database read/write sync for history and analytics
│   ├── styles.py               # Complete CSS design system & dynamic theme engine
│   └── watermark_processor.py  # Text and logo compositing & placement engine
└── README.md                   # Project documentation
```

---

## 🛡️ Privacy & Security

- **No Remote Processing**: Image bytes stay in memory (`io.BytesIO`) during your active browser tab session and are cleared upon reload.
- **No Analytics Tracking**: Zero third-party trackers, telemetry, or cookies.
- **Encrypted Auth**: If Supabase is enabled, authentication tokens and sessions use industry-standard HTTPS and Supabase Row Level Security (RLS).

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.
