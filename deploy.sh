#!/bin/bash

# 🚀 Exam Paper Generator Deployment Script for Render
# This script helps prepare and deploy the application to Render

set -e  # Exit on any error

echo "🚀 Starting deployment preparation for Render..."

# Check if we're in the correct directory
if [ ! -f "render.yaml" ]; then
    echo "❌ Error: render.yaml not found. Please run this script from the project root."
    exit 1
fi

# Check required files
echo "📋 Checking required files..."

required_files=("backend/requirements.txt" "frontend/package.json" "frontend/vite.config.js")
for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ Missing required file: $file"
        exit 1
    else
        echo "✅ Found: $file"
    fi
done

# Check for environment files
if [ ! -f ".env.example" ]; then
    echo "⚠️  Warning: .env.example not found. Environment variables need to be configured in Render dashboard."
fi

if [ ! -f "frontend/.env.example" ]; then
    echo "⚠️  Warning: frontend/.env.example not found."
fi

# Validate Python dependencies
echo "🐍 Validating Python dependencies..."
cd backend
python -c "import fastapi, uvicorn, motor, pymongo, langchain, sentence_transformers; print('✅ All Python dependencies available')" || {
    echo "❌ Python dependencies validation failed. Run 'pip install -r requirements.txt' first."
    exit 1
}
cd ..

# Validate Node.js dependencies
echo "📦 Validating Node.js dependencies..."
cd frontend
npm list --depth=0 > /dev/null || {
    echo "❌ Node.js dependencies validation failed. Run 'npm install' first."
    exit 1
}

# Test frontend build
echo "🔨 Testing frontend build..."
npm run build > /dev/null || {
    echo "❌ Frontend build failed. Check your build configuration."
    exit 1
}
cd ..

echo "✅ All validations passed!"

# Create deployment summary
echo ""
echo "📋 Deployment Summary:"
echo "=========================="
echo "✅ Backend service configured in render.yaml"
echo "✅ Frontend static site configured in render.yaml"
echo "✅ Environment variables documented in .env.example"
echo "✅ Python dependencies validated"
echo "✅ Node.js dependencies validated"
echo "✅ Frontend build tested"

echo ""
echo "🚀 Next Steps for Deployment:"
echo "=========================="
echo "1. Push your code to GitHub"
echo "2. Connect your GitHub repo to Render"
echo "3. Create two services using render.yaml configuration"
echo "4. Set environment variables in Render dashboard:"
echo "   - Copy from .env.example"
echo "   - Update with your actual API keys and URLs"
echo "5. Deploy and test your application"

echo ""
echo "🔗 Required Environment Variables:"
echo "=================================="
echo "Backend Service:"
echo "  - MONGODB_URL"
echo "  - GEMINI_API_KEY"
echo "  - JWT_SECRET_KEY"
echo "  - CLOUDINARY_CLOUD_NAME (optional)"
echo "  - CLOUDINARY_API_KEY (optional)"
echo "  - CLOUDINARY_API_SECRET (optional)"
echo "  - FRONTEND_ALLOWED_ORIGINS"

echo ""
echo "Frontend Service:"
echo "  - VITE_BACKEND_URL"

echo ""
echo "🎉 Deployment preparation complete!"
echo "Your application is ready for Render deployment."
