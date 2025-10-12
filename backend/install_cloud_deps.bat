@echo off
echo ============================================================
echo  Installing Cloud Services Dependencies
echo ============================================================
echo.

echo [1/2] Installing Cloudinary...
pip install cloudinary==1.36.0

echo.
echo [2/2] Installing MongoDB Atlas support...
pip install motor==3.3.2 pymongo[srv]==4.6.1 dnspython==2.4.2 python-dotenv==1.0.0

echo.
echo ============================================================
echo  Installation Complete!
echo ============================================================
echo.
echo Next steps:
echo 1. Copy .env.example to .env
echo 2. Fill in your MongoDB Atlas and Cloudinary credentials
echo 3. Start the server: uvicorn app.main:app --reload
echo.
pause
