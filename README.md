# 🌿 Image Studio Pro

**Image Studio Pro** is a modern, responsive, and 100% private web application built with **Streamlit** and **Pillow**. It provides a sleek user interface for resizing, converting, and processing images locally on your machine.

---

## ✨ Features

- **Upload & Convert**: Easily drag and drop **JPG, PNG, or WEBP** images.
- **Resize Images**: Scale images freely by width and height, or lock the aspect ratio to prevent distortion.
- **Social Media Presets**: One-click resizing for standard formats (Instagram Post/Story, YouTube Thumbnail, Twitter Header, WhatsApp DP, HD Wallpaper, Facebook Cover).
- **Format Conversion & Compression**: Convert between JPEG, PNG, and WEBP. Adjust quality levels to compress JPEG/WEBP images and save storage space.
- **📦 Batch Processing**: Upload multiple images and convert/resize them all at once using the same settings.
- **Interactive UI & Dark Mode**: Beautiful and modern UI with interactive before/after sliders, responsive cards, and a built-in Dark/Light mode toggle.
- **Download History**: View a detailed dashboard of your current session's conversions, tracking original size vs. new size, space saved, and dimensions.
- **🔒 100% Private**: All processing happens entirely on your local machine using Python. No images are ever uploaded to an external server.

---

## 🛠️ Installation

To run this project locally, ensure you have Python installed, then follow these steps:

1. **Clone this repository:**
   ```bash
   git clone https://github.com/2326praveen/Image-Resizer-and-Converter-Tool-.git
   ```

2. **Navigate to the project directory:**
   ```bash
   cd Image-Resizer-and-Converter-Tool-
   ```

3. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## 🚀 Usage

1. Start the Streamlit application:
   ```bash
   streamlit run app.py
   ```
   *(Alternatively, you can just double-click the `run.bat` file if you are on Windows).*

2. Open the URL provided in your terminal (usually `http://localhost:8501`) in your web browser.

---

## ☁️ Deployment

This application is fully compatible with **Streamlit Community Cloud** for free hosting.
1. Log in to [Streamlit Community Cloud](https://share.streamlit.io/).
2. Create a new app and link this repository (`2326praveen/Image-Resizer-and-Converter-Tool-`).
3. Set the main file path to `app.py` and click **Deploy!**
