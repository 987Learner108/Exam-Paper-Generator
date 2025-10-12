@echo off
echo ============================================================
echo  Starting Intelligent Exam Paper Generator Backend
echo ============================================================
echo.

echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo.
echo Starting Uvicorn server...
echo Backend will be available at: http://localhost:8000
echo API docs at: http://localhost:8000/docs
echo.

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

pause
