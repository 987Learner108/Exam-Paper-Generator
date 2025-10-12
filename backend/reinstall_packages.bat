@echo off
echo ============================================================
echo  Clean Reinstall of AI Packages
echo ============================================================
echo.

echo [1/5] Uninstalling conflicting packages...
pip uninstall -y langchain langchain-core langchain-google-genai langchain-community langgraph langsmith

echo.
echo [2/5] Clearing pip cache...
pip cache purge

echo.
echo [3/5] Installing compatible versions...
pip install langchain==0.3.0
pip install langchain-core==0.3.0
pip install langchain-community==0.3.0
pip install langsmith==0.2.0
pip install langgraph==0.2.0
pip install langchain-google-genai==2.0.0
pip install google-generativeai==0.8.3

echo.
echo [4/5] Installing MongoDB driver with srv support (for MongoDB Atlas)...
pip install "pymongo[srv]>=4.0,<5.0"
pip install motor>=3.0,<4.0
pip install dnspython>=2.0

echo.
echo [5/5] Installing Cloudinary for file storage...
pip install cloudinary==1.36.0
pip install python-dotenv==1.0.0

echo.
echo ============================================================
echo  Verifying installation...
echo ============================================================
pip show langchain
pip show langchain-google-genai
pip show langgraph
pip show pymongo
pip show motor
pip show cloudinary

echo.
echo ============================================================
echo  Installation Complete!
echo ============================================================
echo.
echo Next steps:
echo 1. Configure .env file with MongoDB Atlas URI and Cloudinary credentials
echo 2. Test: python test_gemini_direct.py
echo 3. Start backend: uvicorn app.main:app --reload
echo.
pause
