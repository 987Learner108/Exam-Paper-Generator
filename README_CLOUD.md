# ☁️ Intelligent Exam Paper Generator - Cloud Edition

## 🚀 Quick Start (Cloud Setup)

### Prerequisites
- Python 3.8+
- Node.js 16+
- MongoDB Atlas account (free tier)
- Cloudinary account (free tier)
- Gemini API key

### 1. Clone & Install

```bash
# Clone repository
git clone <your-repo>
cd projectZero

# Backend setup
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

# Install cloud dependencies
install_cloud_deps.bat  # Windows
# Or manually:
pip install cloudinary motor pymongo[srv] dnspython python-dotenv

# Frontend setup
cd ../frontend
npm install
```

### 2. Configure Environment

```bash
cd backend
cp .env.example .env
# Edit .env with your credentials
```

**Required credentials:**
- MongoDB Atlas URI
- Cloudinary credentials (cloud_name, api_key, api_secret)
- Gemini API key
- JWT secret

### 3. Start Application

```bash
# Terminal 1: Backend
cd backend
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

# Terminal 2: Frontend
cd frontend
npm run dev
```

### 4. Access Application
- Frontend: http://localhost:5173
- Backend API: http://127.0.0.1:8000
- API Docs: http://127.0.0.1:8000/docs

---

## 📁 Project Structure

```
projectZero/
├── backend/
│   ├── app/
│   │   ├── core/
│   │   │   ├── config.py          # ✅ Updated with cloud config
│   │   │   ├── database.py        # ✅ Updated for MongoDB Atlas
│   │   │   └── auth.py
│   │   ├── services/
│   │   │   ├── cloudinary_service.py  # ✅ NEW - Cloudinary integration
│   │   │   ├── langgraph_flow.py
│   │   │   ├── file_parser.py
│   │   │   └── ...
│   │   ├── routes/
│   │   │   ├── teacher.py         # ✅ Updated for cloud storage
│   │   │   └── ...
│   │   └── main.py
│   ├── .env.example               # ✅ NEW - Environment template
│   ├── requirements_cloud.txt     # ✅ NEW - Cloud dependencies
│   └── install_cloud_deps.bat     # ✅ NEW - Quick install script
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── TeacherDashboard.jsx  # ✅ Updated to show Cloudinary URLs
│   │   │   └── ...
│   │   └── ...
│   └── package.json
├── CLOUD_MIGRATION_GUIDE.md       # ✅ NEW - Detailed setup guide
├── CLOUD_MIGRATION_SUMMARY.md     # ✅ NEW - Complete changes overview
└── README_CLOUD.md                # ✅ THIS FILE
```

---

## 🌐 Cloud Services

### MongoDB Atlas (Database)
- **Purpose**: Store all application data
- **Collections**: users, resources, papers, prompts_history
- **Features**: Automatic backups, scaling, 99.9% uptime
- **Free Tier**: 512MB storage

### Cloudinary (File Storage)
- **Purpose**: Store uploaded files (PDF, DOCX, PPTX, images)
- **Features**: CDN delivery, automatic optimization, transformations
- **Free Tier**: 25GB storage, 25GB bandwidth/month

---

## 🔧 Key Features

### File Upload Flow
1. User uploads file (PDF/DOCX/PPTX/Image)
2. Backend validates file type and size
3. File is parsed to extract text and topics
4. File is uploaded to Cloudinary
5. Cloudinary URL and metadata saved to MongoDB Atlas
6. User can view/delete files

### Data Flow
```
User Upload → FastAPI → Cloudinary → MongoDB Atlas
                ↓
         File Parser (Extract text)
                ↓
         Gemini AI (Generate questions)
                ↓
         MongoDB Atlas (Save paper)
```

---

## 📊 API Endpoints

### Upload Resource
```http
POST /teacher/upload-resource
Content-Type: multipart/form-data

file: <file>
subject: "Data Structures"
department: "Computer Science"
```

**Response:**
```json
{
  "id": "67890abcdef",
  "filename": "DS_Syllabus.pdf",
  "cloudinary_url": "https://res.cloudinary.com/xxx/...",
  "topics": ["Arrays", "Linked Lists"],
  "file_size": 1048576,
  "message": "Resource uploaded successfully to Cloudinary"
}
```

### List Resources
```http
GET /teacher/resources
Authorization: Bearer <token>
```

**Response:**
```json
[
  {
    "id": "67890abcdef",
    "filename": "DS_Syllabus.pdf",
    "file_type": "pdf",
    "file_size": 1048576,
    "cloudinary_url": "https://res.cloudinary.com/xxx/...",
    "topics": ["Arrays", "Linked Lists"],
    "subject": "Data Structures",
    "department": "Computer Science",
    "uploaded_by": "John Doe",
    "uploaded_at": "2025-01-12T10:00:00Z"
  }
]
```

### Delete Resource
```http
DELETE /teacher/resources/{resource_id}
Authorization: Bearer <token>
```

**Response:**
```json
{
  "message": "Resource deleted successfully",
  "filename": "DS_Syllabus.pdf"
}
```

---

## 🔒 Security

### Environment Variables
- Never commit `.env` to Git
- Use different credentials for dev/prod
- Rotate secrets regularly

### MongoDB Atlas
- IP whitelist enabled
- Strong passwords
- Encryption at rest
- Automated backups

### Cloudinary
- Signed uploads
- Upload limits enforced
- Quota monitoring

---

## 🧪 Testing

### Manual Testing
1. **Upload Test**
   - Upload a PDF file
   - Check Cloudinary dashboard
   - Verify file appears in resources list

2. **View Test**
   - Click cloud icon (☁️) next to file
   - File should open in new tab from Cloudinary

3. **Delete Test**
   - Delete a resource
   - Verify removed from Cloudinary
   - Verify removed from MongoDB

### Backend Logs
Watch for these success messages:
```
✅ Connected to MongoDB Atlas: exam_paper_ai
✅ Database indexes created
📤 Upload request from teacher 123
✅ Cloudinary upload successful
✅ Resource saved to MongoDB
```

---

## 🚀 Deployment

### Option 1: Railway
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Deploy
railway up
```

### Option 2: Render
1. Connect GitHub repository
2. Create Web Service (backend)
3. Create Static Site (frontend)
4. Add environment variables

### Option 3: Vercel + Railway
```bash
# Frontend to Vercel
cd frontend
vercel

# Backend to Railway
cd backend
railway up
```

### Environment Variables for Production
```env
MONGODB_URI=mongodb+srv://prod_user:STRONG_PASS@prod-cluster.mongodb.net/...
CLOUDINARY_CLOUD_NAME=your_cloud
CLOUDINARY_API_KEY=your_key
CLOUDINARY_API_SECRET=your_secret
GEMINI_API_KEY=your_key
JWT_SECRET=VERY_LONG_RANDOM_STRING
BACKEND_URL=https://api.yourapp.com
FRONTEND_URL=https://yourapp.com
```

---

## 📈 Monitoring

### MongoDB Atlas
- Dashboard: https://cloud.mongodb.com
- View metrics, logs, and performance
- Set up alerts

### Cloudinary
- Dashboard: https://cloudinary.com/console
- Monitor usage and bandwidth
- View uploaded files

---

## 🐛 Troubleshooting

### "Failed to connect to MongoDB Atlas"
1. Check connection string
2. Verify password (URL encode special chars)
3. Whitelist IP (0.0.0.0/0 for dev)
4. Test connection: `ping cluster0.xxxxx.mongodb.net`

### "Cloudinary upload failed"
1. Verify credentials in `.env`
2. Check file size (max 10MB)
3. Check file type is allowed
4. Verify Cloudinary quota

### "Module not found: cloudinary"
```bash
pip install cloudinary
```

### "DNS resolution failed"
```bash
pip install dnspython
```

---

## 📚 Documentation

- **Setup Guide**: `CLOUD_MIGRATION_GUIDE.md`
- **Changes Summary**: `CLOUD_MIGRATION_SUMMARY.md`
- **API Docs**: http://127.0.0.1:8000/docs (when running)

---

## 🎯 Features

### For Teachers
- ✅ Upload resources (PDF, DOCX, PPTX, images)
- ✅ Generate exam papers with AI
- ✅ Customize Bloom's taxonomy distribution
- ✅ Approve and download papers
- ✅ Manage approved papers repository
- ✅ View generation history

### For Admin
- ✅ Manage users
- ✅ View analytics
- ✅ System monitoring

---

## 🔄 Migration from Local

If you have existing local data:

1. **Export from local MongoDB**
```bash
mongodump --db exam_generator --out ./backup
```

2. **Import to MongoDB Atlas**
```bash
mongorestore --uri "mongodb+srv://..." --db exam_paper_ai ./backup/exam_generator
```

3. **Migrate files to Cloudinary**
   - Use Cloudinary's bulk upload API
   - Or re-upload through the application

---

## ✅ Production Checklist

- [ ] MongoDB Atlas cluster created
- [ ] Database user with strong password
- [ ] IP whitelist configured
- [ ] Cloudinary account set up
- [ ] All credentials in `.env`
- [ ] Backend tested locally
- [ ] Frontend tested locally
- [ ] File upload/delete working
- [ ] JWT secret is strong and unique
- [ ] Email configured
- [ ] Deployed to hosting platform
- [ ] Production URLs updated
- [ ] SSL/HTTPS enabled
- [ ] Monitoring set up

---

## 📞 Support

For issues or questions:
1. Check `CLOUD_MIGRATION_GUIDE.md`
2. Review backend logs
3. Check MongoDB Atlas logs
4. Check Cloudinary dashboard

---

## 🎉 Success!

Your application is now running on cloud infrastructure with:
- ✅ Scalable database (MongoDB Atlas)
- ✅ Global file delivery (Cloudinary CDN)
- ✅ Production-ready architecture
- ✅ No local dependencies
- ✅ Easy deployment

**Happy coding!** 🚀
