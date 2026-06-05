@echo off
echo Starting Image Resizer & Converter...
call "%~dp0.venv\Scripts\activate.bat"
streamlit run "%~dp0app.py"
