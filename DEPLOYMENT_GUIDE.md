# 🚀 Deployment Guide: Exam Paper Generator on Render

## 📋 Prerequisites

### **1. Render Account**
- Create account at [render.com](https://render.com)
- Connect your GitHub repository
- Have a credit card for the free tier

### **2. Environment Variables**
Prepare these secrets in Render dashboard:

```bash
# Database (Render will provide this)
DATABASE_URL=mongodb+srv://...

# AI API Keys (Get from respective providers)
GEMINI_API_KEY=AIzaSy...

# Security (Generate random strings)
SECRET_KEY=your-super-secret-key-here

# Application Settings
MONGODB_URL=mongodb+srv://...
CORS_ORIGINS=https://your-frontend-app.onrender.com

# Email (Optional - for notifications)
SMTP_TLS=True
SMTP_PORT=587
SMTP_HOST=smtp.gmail.com
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

---

## 🛠️ Step-by-Step Deployment

### **Step 1: Deploy MongoDB (Free Tier)**
1. **Go to Render Dashboard**
2. **Click "New+" → "PostgreSQL"** (Wait, MongoDB!)
3. **Actually:** Use MongoDB Atlas (free tier) or Render's PostgreSQL for now
4. **For MongoDB Atlas:**
   - Create cluster at [mongodb.com/atlas](https://mongodb.com/atlas)
   - Get connection string
   - Use it as `DATABASE_URL` in Render

### **Step 2: Deploy Backend**
1. **In Render Dashboard:**
   - Click "New+" → "Web Service"
   - Connect your GitHub repo
   - **Name:** `exam-generator-backend`
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

2. **Environment Variables:**
   ```bash
   DATABASE_URL=mongodb+srv://username:password@cluster.mongodb.net/exam_generator
   GEMINI_API_KEY=your_gemini_api_key
   SECRET_KEY=your_secret_key
   MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/exam_generator
   CORS_ORIGINS=https://exam-generator-frontend.onrender.com
   ```

3. **Deploy:**
   - Click "Create Web Service"
   - Wait for deployment (2-3 minutes)

### **Step 3: Deploy Frontend**
1. **In Render Dashboard:**
   - Click "New+" → "Static Site"
   - Connect your GitHub repo
   - **Name:** `exam-generator-frontend`
   - **Build Command:** `npm install && npm run build`
   - **Publish Directory:** `dist`

2. **Environment Variables:**
   ```bash
   # No special env vars needed for frontend
   ```

3. **Deploy:**
   - Click "Create Static Site"
   - Wait for deployment (1-2 minutes)

### **Step 4: Update CORS Origins**
1. **Go to Backend Service** in Render
2. **Environment Variables**
3. **Update `CORS_ORIGINS`:**
   ```bash
   CORS_ORIGINS=https://exam-generator-frontend.onrender.com
   ```

4. **Redeploy Backend:**
   - Click "Manual Deploy" → "Deploy latest commit"

---

## 🔧 Configuration Files

### **render.yaml** (Already Created)
```yaml
services:
  - type: web
    name: exam-generator-frontend
    runtime: node
    buildCommand: cd frontend && npm install && npm run build
    startCommand: cd frontend && npm start
    envVars:
      - key: NODE_ENV
        value: production

  - type: web
    name: exam-generator-backend
    runtime: python
    buildCommand: cd backend && pip install -r requirements.txt
    startCommand: cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: DATABASE_URL
        fromService:
          type: pserv
          name: mongodb
          property: connectionString
      - key: GEMINI_API_KEY
        generateValue: true
      - key: SECRET_KEY
        generateValue: true
      - key: MONGODB_URL
        fromService:
          type: pserv
          name: mongodb
          property: connectionString
      - key: CORS_ORIGINS
        value: "https://exam-generator-frontend.onrender.com"

  - type: pserv
    name: mongodb
    ipAllowList: []
```

### **Frontend package.json** (Updated)
```json
{
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "start": "vite preview --host 0.0.0.0 --port $PORT"
  }
}
```

---

## 🌐 Accessing Your Application

### **After Deployment:**

1. **Frontend URL:** `https://exam-generator-frontend.onrender.com`
2. **Backend URL:** `https://exam-generator-backend.onrender.com`
3. **API Base:** `https://exam-generator-backend.onrender.com/api`

### **Test Deployment:**
```bash
# Health check
curl https://exam-generator-backend.onrender.com/health

# Should return: {"status": "healthy", "database": "connected", "api": "operational"}
```

---

## 🔐 Required API Keys

### **1. Gemini API Key**
1. **Go to:** https://makersuite.google.com/app/apikey
2. **Create API Key**
3. **Add to Render:** `GEMINI_API_KEY=AIzaSy...`

### **2. MongoDB Atlas**
1. **Go to:** https://mongodb.com/atlas
2. **Create Free Cluster** (M0 - 512MB)
3. **Get Connection String**
4. **Add to Render:** `DATABASE_URL=mongodb+srv://...`

### **3. Secret Key**
- **Generate:** `openssl rand -hex 32`
- **Add to Render:** `SECRET_KEY=your_generated_key`

---

## 📊 Render Pricing (Free Tier)

### **What's Free:**
- ✅ **512MB MongoDB Atlas** cluster
- ✅ **750 hours/month** for web services
- ✅ **100GB/month** bandwidth
- ✅ **Custom domains** with limitations

### **Limitations:**
- ⏰ **Services sleep** after 15 minutes of inactivity
- ⏰ **Cold start** takes 20-30 seconds
- 💾 **512MB database** storage limit
- 🌐 **Basic bandwidth** (100GB/month)

---

## 🚨 Troubleshooting

### **Issue 1: Database Connection Failed**
```bash
# Check MongoDB Atlas
1. Verify cluster is running
2. Check IP whitelist (add 0.0.0.0/0 for all)
3. Verify connection string format
```

### **Issue 2: Gemini API Key Invalid**
```bash
# Verify API key
1. Test with curl:
curl -H "Content-Type: application/json" \
     -d '{"contents":[{"parts":[{"text":"Hello"}]}]}' \
     "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=YOUR_KEY"

2. Should return valid response
```

### **Issue 3: CORS Errors**
```bash
# Update CORS_ORIGINS in Render:
CORS_ORIGINS=https://your-frontend-domain.onrender.com
```

### **Issue 4: Services Not Starting**
```bash
# Check Render logs:
1. Go to service dashboard
2. Click "Logs" tab
3. Look for error messages
```

---

## 🎯 Production Checklist

### **Before Going Live:**
- [ ] **Test all features** on staging
- [ ] **Verify database connections**
- [ ] **Test file uploads** (PDFs, docs)
- [ ] **Check AI generation** works
- [ ] **Verify email notifications** (optional)
- [ ] **Test user registration/login**
- [ ] **Check PDF generation**
- [ ] **Verify CORS** settings
- [ ] **Test on mobile devices**
- [ ] **Check performance** with multiple users

### **Security Checklist:**
- [ ] **Strong SECRET_KEY** (32+ characters)
- [ ] **Database credentials** secured
- [ ] **API keys** not exposed in client
- [ ] **HTTPS enabled** (Render provides this)
- [ ] **Input validation** working
- [ ] **File upload restrictions** enforced

---

## 📈 Scaling Considerations

### **Current Limitations (Free Tier):**
- ⏰ **15-minute inactivity timeout**
- 💾 **512MB database storage**
- 🌐 **100GB/month bandwidth**

### **When to Upgrade:**
- **High traffic:** Upgrade to paid Render plans
- **More storage:** Upgrade MongoDB Atlas cluster
- **Always-on:** Use paid Render services

### **Cost Estimates:**
- **Render Paid:** $7-25/month per service
- **MongoDB Atlas:** $9/month for 2GB cluster
- **Total:** $20-60/month for basic production

---

## 🔄 Updates and Maintenance

### **Deploying Updates:**
1. **Push to GitHub** main branch
2. **Render auto-deploys** (if enabled)
3. **Or manually deploy** from Render dashboard

### **Monitoring:**
- **Render Dashboard:** Service health, logs, metrics
- **MongoDB Atlas:** Database performance, storage
- **Application Logs:** Check for errors

### **Backups:**
- **MongoDB Atlas:** Automatic daily backups
- **Code:** GitHub repository
- **Environment:** Render secrets management

---

## 🎉 Success!

### **Your Application is Live!**

**Frontend:** `https://your-app-name.onrender.com`
**Backend:** `https://your-backend-name.onrender.com`

### **Features Available:**
- ✅ **User registration/login**
- ✅ **Resource upload** (PDFs, docs)
- ✅ **AI-powered paper generation**
- ✅ **Question verification**
- ✅ **PDF generation**
- ✅ **Email notifications**
- ✅ **Responsive design**
- ✅ **Multi-user support**

---

## 📞 Support

### **Issues:**
1. **Check Render logs** first
2. **Verify environment variables**
3. **Test database connection**
4. **Check API keys validity**

### **Common Fixes:**
- **Regenerate API keys** if expired
- **Update CORS origins** for frontend changes
- **Restart services** if stuck
- **Check MongoDB Atlas** cluster status

---

**🎊 Congratulations! Your AI-powered exam paper generator is now deployed and accessible worldwide!** 🌍✨
