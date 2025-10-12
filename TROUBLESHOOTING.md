# 🔧 Troubleshooting Guide

## 🚨 Common Errors & Solutions

### **1. Upload Timeout Error**

**Error:**
```
Failed to upload to Cloudinary: TimeoutError('The write operation timed out')
```

**Causes:**
- File is too large (>5MB)
- Slow internet connection
- Cloudinary server issues

**Solutions:**

#### **A. Compress Your File**

**For PDFs:**
- Use: https://www.ilovepdf.com/compress_pdf
- Or: https://smallpdf.com/compress-pdf
- Target: Under 5MB

**For PPTX:**
1. Open PowerPoint
2. File → Compress Pictures
3. Select "Email (96 ppi)"
4. Save As → Save

**For DOCX:**
1. Open Word
2. File → Compress Pictures
3. Remove unused media
4. Save As → Save

#### **B. Check Internet Speed**
```bash
# Test your upload speed
speedtest-cli
```

**Minimum recommended:**
- Upload speed: 5 Mbps
- Ping: < 100ms

#### **C. Split Large Files**
If file is >10MB:
- Split into multiple smaller files
- Upload separately
- Combine content later

---

### **2. Authentication Error (403 Forbidden)**

**Error:**
```
INFO: 127.0.0.1:64566 - "GET /auth/me HTTP/1.1" 403 Forbidden
```

**Causes:**
- JWT token expired
- Backend restarted (tokens invalidated)
- Invalid credentials

**Solutions:**

#### **A. Logout and Login Again**
1. Click "Logout" in the app
2. Login with your credentials
3. Try uploading again

#### **B. Clear Browser Cache**
```
Chrome: Ctrl + Shift + Delete
Firefox: Ctrl + Shift + Delete
Edge: Ctrl + Shift + Delete
```

#### **C. Check Backend is Running**
```bash
# Backend should be running on port 8000
curl http://127.0.0.1:8000/docs
```

---

### **3. Connection Refused Error**

**Error:**
```
Failed to load resource: net::ERR_CONNECTION_REFUSED
```

**Causes:**
- Backend server not running
- Wrong port
- Firewall blocking

**Solutions:**

#### **A. Start Backend Server**
```bash
cd backend
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

#### **B. Check Port**
```bash
# Windows
netstat -ano | findstr :8000

# Mac/Linux
lsof -i :8000
```

#### **C. Check Firewall**
- Allow port 8000 in Windows Firewall
- Disable antivirus temporarily to test

---

### **4. File Size Limit Error**

**Error:**
```
File size exceeds 10MB limit
```

**Solution:**
- Compress file to under 10MB
- Use recommended compression tools above
- Or split into multiple files

---

### **5. Invalid File Type Error**

**Error:**
```
Invalid file type. Allowed: PDF, DOCX, PPTX, Images
```

**Allowed formats:**
- ✅ PDF (.pdf)
- ✅ Word (.docx)
- ✅ PowerPoint (.pptx)
- ✅ Images (.jpg, .jpeg, .png, .webp)

**Not allowed:**
- ❌ .doc (old Word format)
- ❌ .ppt (old PowerPoint format)
- ❌ .txt, .rtf, .odt

**Solution:**
Convert to supported format:
- .doc → .docx (Save As in Word)
- .ppt → .pptx (Save As in PowerPoint)

---

### **6. MongoDB Connection Error**

**Error:**
```
Failed to connect to MongoDB Atlas
```

**Solutions:**

#### **A. Check Connection String**
```bash
# Test connection
python test_mongodb_connection.py
```

#### **B. Verify Credentials**
1. Go to https://cloud.mongodb.com
2. Check password is correct
3. Ensure IP is whitelisted (0.0.0.0/0 for dev)

#### **C. Check Network**
```bash
# Ping MongoDB Atlas
ping cluster01.bbt2q2h.mongodb.net
```

---

### **7. Cloudinary Authentication Error**

**Error:**
```
Cloudinary authentication failed
```

**Solutions:**

#### **A. Verify Credentials**
```bash
# Test Cloudinary connection
python test_cloudinary_connection.py
```

#### **B. Check .env File**
```env
CLOUDINARY_CLOUD_NAME=drc6mpyvc
CLOUDINARY_API_KEY=918664534129623
CLOUDINARY_API_SECRET=GYLwku-lG56skArUFkfSmobAgJs
```

#### **C. Regenerate API Key**
1. Go to https://cloudinary.com/console
2. Settings → Security
3. Regenerate API Secret
4. Update .env file

---

## 🔍 Debugging Steps

### **Step 1: Check Backend Logs**

Look for errors in terminal where backend is running:

```bash
# Good logs
✅ Connected to MongoDB Atlas
✅ Cloudinary upload successful

# Bad logs
❌ Failed to connect
❌ Upload timeout
```

### **Step 2: Check Frontend Console**

Open browser DevTools (F12):
- Console tab: Look for errors
- Network tab: Check failed requests

### **Step 3: Test Components**

```bash
# Test environment config
python test_env_config.py

# Test MongoDB
python test_mongodb_connection.py

# Test Cloudinary
python test_cloudinary_connection.py
```

### **Step 4: Check File Details**

Before uploading:
- File size: < 5MB recommended
- File format: PDF, DOCX, PPTX, or image
- File name: No special characters

---

## 📊 Performance Tips

### **For Faster Uploads:**

1. **Optimize File Size**
   - Compress before uploading
   - Remove unnecessary images
   - Use PDF instead of PPTX when possible

2. **Network Connection**
   - Use wired connection (not WiFi)
   - Close other downloads
   - Upload during off-peak hours

3. **File Format**
   - **Fastest**: PDF (2-5 seconds)
   - **Medium**: DOCX (5-10 seconds)
   - **Slower**: PPTX (10-20 seconds)

---

## 🆘 Still Having Issues?

### **Collect Debug Information:**

1. **Backend logs** (last 50 lines)
2. **Frontend console errors** (screenshot)
3. **File details** (size, format)
4. **Network speed** (upload/download)

### **Check System Requirements:**

- Python 3.8+
- Node.js 16+
- Internet: 5+ Mbps upload
- RAM: 4GB+ available

### **Restart Everything:**

```bash
# 1. Stop backend (Ctrl+C)
# 2. Stop frontend (Ctrl+C)

# 3. Restart backend
cd backend
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

# 4. Restart frontend
cd frontend
npm run dev

# 5. Clear browser cache
# 6. Logout and login again
```

---

## ✅ Quick Checklist

Before reporting an issue, verify:

- [ ] Backend is running (http://127.0.0.1:8000/docs works)
- [ ] Frontend is running (http://localhost:5173 works)
- [ ] Logged in successfully
- [ ] File is under 10MB
- [ ] File format is supported
- [ ] Internet connection is stable
- [ ] MongoDB Atlas connection works
- [ ] Cloudinary connection works
- [ ] No firewall blocking
- [ ] Browser cache cleared

---

## 📞 Support Resources

- **MongoDB Atlas**: https://cloud.mongodb.com
- **Cloudinary Dashboard**: https://cloudinary.com/console
- **API Documentation**: http://127.0.0.1:8000/docs

---

**Most issues can be resolved by:**
1. Compressing the file
2. Logging out and back in
3. Restarting backend/frontend
4. Checking internet connection
