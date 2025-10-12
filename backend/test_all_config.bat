@echo off
echo ============================================================
echo  TESTING ALL ENVIRONMENT CONFIGURATIONS
echo ============================================================
echo.

echo [1/3] Testing Environment Variables...
python test_env_config.py

echo.
echo [2/3] Testing MongoDB Atlas Connection...
python test_mongodb_connection.py

echo.
echo [3/3] Testing Cloudinary Connection...
python test_cloudinary_connection.py

echo.
echo ============================================================
echo  ALL TESTS COMPLETE
echo ============================================================
echo.
pause
