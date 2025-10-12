@echo off
echo ============================================================
echo  Updating Gemini AI Packages
echo ============================================================
echo.

echo [1/3] Upgrading langchain-google-genai...
pip install --upgrade langchain-google-genai

echo.
echo [2/3] Upgrading google-generativeai...
pip install --upgrade google-generativeai

echo.
echo [3/3] Verifying installation...
pip show langchain-google-genai
pip show google-generativeai

echo.
echo ============================================================
echo  Update Complete!
echo ============================================================
echo.
echo Next steps:
echo 1. Run: python list_models.py
echo 2. Restart backend: uvicorn app.main:app --reload
echo.
pause
