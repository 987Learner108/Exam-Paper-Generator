@echo off
echo ============================================================
echo  Fixing MongoDB Packages (Version Compatibility)
echo ============================================================
echo.

echo [1/3] Uninstalling incompatible versions...
pip uninstall -y pymongo motor

echo.
echo [2/3] Installing compatible versions...
pip install "pymongo[srv]>=4.0,<5.0"
pip install motor>=3.0,<4.0
pip install dnspython>=2.0

echo.
echo [3/3] Verifying installation...
pip show pymongo
pip show motor

echo.
echo ============================================================
echo  Fix Complete!
echo ============================================================
echo.
echo Now test: python test_mongodb_connection.py
echo.
pause
