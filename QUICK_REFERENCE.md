# ⚡ Quick Reference Card - Cloud Setup

## 🔑 Credentials Needed

### MongoDB Atlas
```
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/...
MONGODB_DB_NAME=exam_paper_ai
```
Get from: https://cloud.mongodb.com → Connect → Connection String

### Cloudinary
```
CLOUDINARY_CLOUD_NAME=dxxxxxx
CLOUDINARY_API_KEY=123456789012345
CLOUDINARY_API_SECRET=abcdefghijklmnopqrstuvwxyz
```
Get from: https://cloudinary.com/console → Dashboard

### Gemini AI
```
GEMINI_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```
Get from: https://makersuite.google.com/app/apikey

---

## 🚀 Quick Start Commands

```bash
# 1. Install dependencies
cd backend
install_cloud_deps.bat

# 2. Configure environment
cp .env.example .env
# Edit .env with your credentials

# 3. Start backend
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

# 4. Start frontend (new terminal)
cd frontend
npm run dev
```

---

## 📊 Key Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/teacher/upload-resource` | Upload file to Cloudinary |
| GET | `/teacher/resources` | List uploaded resources |
| DELETE | `/teacher/resources/{id}` | Delete resource |
| POST | `/teacher/generate-paper` | Generate exam paper |
| GET | `/teacher/papers` | List generated papers |

---

## 🔍 Success Indicators

### Backend Startup
```
✅ Connected to MongoDB Atlas: exam_paper_ai
✅ Database indexes created
```

### File Upload
```
📤 Upload request from teacher xxx
✅ PDF validated: 5 pages
✅ Extracted 1234 characters, 5 topics
☁️ Uploading to Cloudinary...
✅ Cloudinary upload successful
✅ Resource saved to MongoDB
```

### File Delete
```
🗑️ Deleting resource: filename.pdf
✅ Deleted file from Cloudinary
✅ Deleted 5 embeddings from RAG
✅ Deleted resource metadata
```

---

## 🐛 Common Errors & Fixes

| Error | Fix |
|-------|-----|
| "Failed to connect to MongoDB" | Check URI, password, IP whitelist |
| "Cloudinary upload failed" | Verify credentials, check quota |
| "Module 'cloudinary' not found" | `pip install cloudinary` |
| "DNS resolution failed" | `pip install dnspython` |

---

## 📁 File Locations

| File | Purpose |
|------|---------|
| `backend/.env` | Your credentials (DO NOT COMMIT) |
| `backend/.env.example` | Template with instructions |
| `backend/app/core/config.py` | Configuration loader |
| `backend/app/services/cloudinary_service.py` | Cloudinary integration |
| `backend/app/routes/teacher.py` | Upload/delete endpoints |

---

## 🔗 Important Links

- **MongoDB Atlas**: https://cloud.mongodb.com
- **Cloudinary Dashboard**: https://cloudinary.com/console
- **Gemini API Keys**: https://makersuite.google.com/app/apikey
- **API Docs**: http://127.0.0.1:8000/docs
- **Frontend**: http://localhost:5173

---

## 📦 Dependencies

```bash
pip install cloudinary==1.36.0
pip install motor==3.3.2
pip install pymongo[srv]==4.6.1
pip install dnspython==2.4.2
pip install python-dotenv==1.0.0
```

---

## ✅ Testing Checklist

- [ ] Backend starts without errors
- [ ] MongoDB Atlas connection successful
- [ ] Upload PDF file
- [ ] File appears in Cloudinary dashboard
- [ ] File appears in resources list
- [ ] Cloud icon (☁️) opens file
- [ ] Delete removes file from Cloudinary
- [ ] Delete removes file from MongoDB

---

## 🎯 Quick Troubleshooting

1. **Check logs** in backend terminal
2. **Verify credentials** in `.env`
3. **Test connection** to MongoDB Atlas
4. **Check quota** in Cloudinary dashboard
5. **Review** `CLOUD_MIGRATION_GUIDE.md`

---

**Need detailed help?** See `CLOUD_MIGRATION_GUIDE.md`

**Ready to deploy?** See `README_CLOUD.md`
