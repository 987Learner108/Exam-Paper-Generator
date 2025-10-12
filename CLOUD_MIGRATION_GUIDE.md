# ☁️ Cloud Migration Guide - MongoDB Atlas & Cloudinary

This guide explains how to migrate the Intelligent Exam Paper Generator from local storage to cloud services.

---

## 📋 Table of Contents
1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [MongoDB Atlas Setup](#mongodb-atlas-setup)
4. [Cloudinary Setup](#cloudinary-setup)
5. [Environment Configuration](#environment-configuration)
6. [Installation](#installation)
7. [Testing](#testing)
8. [Deployment](#deployment)

---

## 🎯 Overview

### What Changed?
- **Database**: Local MongoDB Compass → **MongoDB Atlas** (Cloud)
- **File Storage**: Local filesystem/GridFS → **Cloudinary** (Cloud CDN)

### Benefits
✅ Scalable cloud infrastructure  
✅ No local storage dependencies  
✅ Fast CDN delivery for files  
✅ Ready for production deployment  
✅ Automatic backups (MongoDB Atlas)  
✅ Global file distribution (Cloudinary)

---

## 📦 Prerequisites

### Required Accounts
1. **MongoDB Atlas** (Free tier available)
   - Sign up: https://www.mongodb.com/cloud/atlas/register

2. **Cloudinary** (Free tier: 25GB storage, 25GB bandwidth/month)
   - Sign up: https://cloudinary.com/users/register/free

3. **Google AI Studio** (For Gemini API)
   - Get API key: https://makersuite.google.com/app/apikey

### Required Software
- Python 3.8+
- Node.js 16+
- pip (Python package manager)
- npm (Node package manager)

---

## 🗄️ MongoDB Atlas Setup

### Step 1: Create a Cluster
1. Go to https://cloud.mongodb.com
2. Click "Build a Database"
3. Choose **FREE** tier (M0 Sandbox)
4. Select your preferred cloud provider and region
5. Name your cluster (e.g., `exam-paper-cluster`)
6. Click "Create"

### Step 2: Create Database User
1. Go to **Database Access** (left sidebar)
2. Click "Add New Database User"
3. Choose **Password** authentication
4. Username: `exam_admin` (or your choice)
5. Password: Generate a strong password (save it!)
6. Database User Privileges: **Read and write to any database**
7. Click "Add User"

### Step 3: Configure Network Access
1. Go to **Network Access** (left sidebar)
2. Click "Add IP Address"
3. For development: Click "Allow Access from Anywhere" (0.0.0.0/0)
4. For production: Add your server's specific IP
5. Click "Confirm"

### Step 4: Get Connection String
1. Go to **Database** → Click "Connect" on your cluster
2. Choose "Connect your application"
3. Driver: **Python**, Version: **3.12 or later**
4. Copy the connection string:
   ```
   mongodb+srv://exam_admin:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```
5. Replace `<password>` with your actual password
6. Save this for your `.env` file

### Step 5: Create Database & Collections
The application will automatically create these collections:
- `users` - User accounts
- `resources` - Uploaded files metadata
- `papers` - Generated exam papers
- `prompts_history` - Generation history

---

## ☁️ Cloudinary Setup

### Step 1: Create Account
1. Go to https://cloudinary.com/users/register/free
2. Sign up with email or Google
3. Verify your email

### Step 2: Get Credentials
1. Go to **Dashboard**: https://cloudinary.com/console
2. You'll see your credentials:
   - **Cloud name**: `dxxxxxx`
   - **API Key**: `123456789012345`
   - **API Secret**: `abcdefghijklmnopqrstuvwxyz`
3. Copy these values for your `.env` file

### Step 3: Configure Upload Presets (Optional)
1. Go to **Settings** → **Upload**
2. Scroll to **Upload presets**
3. Edit the default preset or create new one
4. Set folder: `exam_resources`
5. Save

---

## ⚙️ Environment Configuration

### Step 1: Copy Example File
```bash
cd backend
cp .env.example .env
```

### Step 2: Edit `.env` File
Open `backend/.env` and fill in your credentials:

```env
# MongoDB Atlas
MONGODB_URI=mongodb+srv://exam_admin:YOUR_PASSWORD@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
MONGODB_DB_NAME=exam_paper_ai

# Cloudinary
CLOUDINARY_CLOUD_NAME=dxxxxxx
CLOUDINARY_API_KEY=123456789012345
CLOUDINARY_API_SECRET=abcdefghijklmnopqrstuvwxyz

# Gemini AI
GEMINI_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

# JWT (Generate secure key)
JWT_SECRET=your_super_secret_jwt_key_change_this
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Email (Gmail)
EMAIL_USER=your_email@gmail.com
EMAIL_PASS=your_app_specific_password
EMAIL_FROM=your_email@gmail.com

# URLs
BACKEND_URL=http://127.0.0.1:8000
FRONTEND_URL=http://localhost:5173
```

### Step 3: Generate JWT Secret
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```
Copy the output and use it as `JWT_SECRET`

---

## 📥 Installation

### Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install cloud packages
pip install cloudinary motor pymongo[srv] python-dotenv

# Start backend server
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

---

## 🧪 Testing

### Test 1: MongoDB Atlas Connection
```bash
# Backend should show:
✅ Connected to MongoDB Atlas: exam_paper_ai
✅ Database indexes created
```

### Test 2: Upload File to Cloudinary
1. Login to the application
2. Go to "Upload Resources"
3. Upload a PDF file
4. Check backend logs:
   ```
   📤 Upload request from teacher xxx
   ✅ PDF validated: 5 pages
   ✅ Extracted 1234 characters, 5 topics
   ☁️ Uploading to Cloudinary...
   ✅ Cloudinary upload successful: exam_resources/xxx/filename
   ✅ Resource saved to MongoDB: xxx
   ```
5. Verify in Cloudinary Dashboard: https://cloudinary.com/console/media_library

### Test 3: List Resources
1. Go to Teacher Dashboard
2. Check "Uploaded Resources" section
3. Should show files with Cloudinary URLs

### Test 4: Delete Resource
1. Click delete icon on a resource
2. Check backend logs:
   ```
   🗑️ Deleting resource: filename.pdf
   ✅ Deleted file from Cloudinary
   ✅ Deleted 5 embeddings from RAG
   ✅ Deleted resource metadata
   ```
3. Verify file is removed from Cloudinary

---

## 🚀 Deployment

### Environment Variables for Production

```env
# Production MongoDB Atlas
MONGODB_URI=mongodb+srv://prod_user:STRONG_PASSWORD@prod-cluster.xxxxx.mongodb.net/?retryWrites=true&w=majority

# Production URLs
BACKEND_URL=https://api.yourapp.com
FRONTEND_URL=https://yourapp.com

# Secure JWT
JWT_SECRET=VERY_LONG_RANDOM_STRING_FOR_PRODUCTION
```

### Deployment Platforms

#### Option 1: Railway (Recommended)
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Deploy backend
cd backend
railway up

# Deploy frontend
cd frontend
railway up
```

#### Option 2: Render
1. Connect your GitHub repository
2. Create new Web Service for backend
3. Create new Static Site for frontend
4. Add environment variables in dashboard

#### Option 3: Vercel (Frontend) + Railway (Backend)
```bash
# Deploy frontend to Vercel
cd frontend
vercel

# Deploy backend to Railway
cd backend
railway up
```

---

## 📊 Monitoring

### MongoDB Atlas
- Dashboard: https://cloud.mongodb.com
- View metrics: Database → Metrics
- Check logs: Database → Logs

### Cloudinary
- Dashboard: https://cloudinary.com/console
- View usage: Dashboard → Usage
- Media library: Media Library

---

## 🔒 Security Best Practices

### 1. Environment Variables
- ✅ Never commit `.env` to Git
- ✅ Use different credentials for dev/prod
- ✅ Rotate secrets regularly

### 2. MongoDB Atlas
- ✅ Use strong passwords
- ✅ Restrict IP access in production
- ✅ Enable database encryption
- ✅ Set up automated backups

### 3. Cloudinary
- ✅ Use signed uploads for sensitive files
- ✅ Set upload limits
- ✅ Enable moderation if needed

---

## 🐛 Troubleshooting

### Issue: "Failed to connect to MongoDB Atlas"
**Solution:**
1. Check your connection string is correct
2. Verify password doesn't contain special characters (URL encode if needed)
3. Ensure IP is whitelisted (0.0.0.0/0 for development)
4. Check network/firewall settings

### Issue: "Cloudinary upload failed"
**Solution:**
1. Verify credentials in `.env`
2. Check file size (max 10MB by default)
3. Ensure file type is allowed
4. Check Cloudinary quota (free tier limits)

### Issue: "Module not found: cloudinary"
**Solution:**
```bash
pip install cloudinary
```

### Issue: "Database indexes creation failed"
**Solution:**
- This is usually a warning, not critical
- Indexes will be created on first use
- Check MongoDB Atlas user has write permissions

---

## 📚 Additional Resources

- [MongoDB Atlas Documentation](https://docs.atlas.mongodb.com/)
- [Cloudinary Python SDK](https://cloudinary.com/documentation/python_integration)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [React Deployment](https://create-react-app.dev/docs/deployment/)

---

## ✅ Migration Checklist

- [ ] MongoDB Atlas cluster created
- [ ] Database user created with read/write access
- [ ] Network access configured (IP whitelisted)
- [ ] Connection string obtained
- [ ] Cloudinary account created
- [ ] Cloudinary credentials obtained
- [ ] `.env` file configured with all credentials
- [ ] Backend dependencies installed (`cloudinary`, `motor`)
- [ ] Backend starts successfully
- [ ] MongoDB Atlas connection confirmed
- [ ] File upload to Cloudinary tested
- [ ] File listing works
- [ ] File deletion works
- [ ] Ready for deployment! 🚀

---

**Need help?** Check the logs in your backend terminal for detailed error messages.

**Success!** Your application is now running on cloud infrastructure! 🎉
