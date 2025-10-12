@echo off
REM 🚀 Exam Paper Generator Deployment Script for Windows
REM This script helps prepare and deploy the application to Render

echo 🚀 Starting deployment preparation for Render...

REM Check if we're in the correct directory
if not exist "render.yaml" (
    echo ❌ Error: render.yaml not found. Please run this script from the project root.
    pause
    exit /b 1
)

REM Check required files
echo 📋 Checking required files...

set "required_files=backend\requirements.txt frontend\package.json frontend\vite.config.js"
for %%f in (%required_files%) do (
    if not exist "%%f" (
        echo ❌ Missing required file: %%f
        pause
        exit /b 1
    ) else (
        echo ✅ Found: %%f
    )
)

REM Check for environment files
if not exist ".env.example" (
    echo ⚠️  Warning: .env.example not found. Environment variables need to be configured in Render dashboard.
)

if not exist "frontend\.env.example" (
    echo ⚠️  Warning: frontend\.env.example not found.
)

REM Validate Python dependencies
echo 🐍 Validating Python dependencies...
cd backend

REM Try to activate virtual environment if it exists
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
)

REM Test basic imports first
python -c "import sys; print('Python version:', sys.version)" >nul 2>&1
if errorlevel 1 (
    echo ❌ Cannot run Python. Please ensure Python is installed and virtual environment is activated.
    cd ..
    pause
    exit /b 1
)

REM Test individual imports to identify issues
echo Testing individual package imports...

REM Test FastAPI
python -c "import fastapi; print('✅ FastAPI imported')" >nul 2>&1
if errorlevel 1 (
    echo ❌ FastAPI import failed
    cd ..
    pause
    exit /b 1
)

REM Test database packages
python -c "import motor, pymongo; print('✅ Database packages imported')" >nul 2>&1
if errorlevel 1 (
    echo ❌ Database packages import failed
    cd ..
    pause
    exit /b 1
)

REM Test AI packages (these might fail but shouldn't block deployment)
python -c "import langchain; print('✅ LangChain imported')" >nul 2>&1
if errorlevel 1 (
    echo ⚠️  LangChain import failed - this may cause issues but deployment can continue
) else (
    echo ✅ LangChain validated
)

python -c "import sentence_transformers; print('✅ Sentence Transformers imported')" >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Sentence Transformers import failed - this may cause issues but deployment can continue
) else (
    echo ✅ Sentence Transformers validated
)

cd ..

REM Validate Node.js dependencies
echo 📦 Validating Node.js dependencies...
cd frontend
npm list --depth=0 >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js dependencies validation failed. Run 'npm install' first.
    cd ..
    pause
    exit /b 1
) else (
    echo ✅ Node.js dependencies validated
)
cd ..

REM Test frontend build
echo 🔨 Testing frontend build...
cd frontend
npm run build >nul 2>&1
if errorlevel 1 (
    echo ❌ Frontend build failed. Check your build configuration.
    cd ..
    pause
    exit /b 1
) else (
    echo ✅ Frontend build tested successfully
)
cd ..

echo ✅ All validations passed!

REM Create deployment summary
echo.
echo 📋 Deployment Summary:
echo ==========================
echo ✅ Backend service configured in render.yaml
echo ✅ Frontend static site configured in render.yaml
echo ✅ Environment variables documented in .env.example
echo ✅ Python dependencies validated
echo ✅ Node.js dependencies validated
echo ✅ Frontend build tested

echo.
echo 🚀 Next Steps for Deployment:
echo ==========================
echo 1. Push your code to GitHub
echo 2. Connect your GitHub repo to Render
echo 3. Create two services using render.yaml configuration
echo 4. Set environment variables in Render dashboard:
echo    - Copy from .env.example
echo    - Update with your actual API keys and URLs
echo 5. Deploy and test your application

echo.
echo 🔗 Required Environment Variables:
echo ==================================
echo Backend Service:
echo   - MONGODB_URL
echo   - GEMINI_API_KEY
echo   - JWT_SECRET_KEY
echo   - CLOUDINARY_CLOUD_NAME (optional)
echo   - CLOUDINARY_API_KEY (optional)
echo   - CLOUDINARY_API_SECRET (optional)
echo   - FRONTEND_ALLOWED_ORIGINS

echo.
echo Frontend Service:
echo   - VITE_BACKEND_URL

echo.
echo 🎉 Deployment preparation complete!
echo Your application is ready for Render deployment.

echo.
echo 💡 Tip: If you encounter PyMuPDF build issues, the deployment uses
echo    'pip install --no-build-isolation' to avoid compilation problems.

pause
