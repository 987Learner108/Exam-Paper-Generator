#!/bin/bash

echo "🚀 Starting deployment process..."

# Install frontend dependencies and build
echo "📦 Building frontend..."
cd frontend
npm install
npm run build
cd ..

# Install backend dependencies
echo "🐍 Installing backend dependencies..."
cd backend
pip install -r requirements.txt
cd ..

echo "✅ Build completed successfully!"
echo ""
echo "📋 Next steps for Render deployment:"
echo "1. Go to https://render.com"
echo "2. Connect your GitHub repository"
echo "3. Create three services:"
echo "   - MongoDB Atlas (external)"
echo "   - Backend web service"
echo "   - Frontend static site"
echo ""
echo "📖 See DEPLOYMENT_GUIDE.md for detailed instructions"
