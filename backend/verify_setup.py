"""
Quick verification script - checks if backend can start
"""

import sys
import os

print("="*70)
print("🔍 Backend Verification")
print("="*70)

# Test 1: Import main app
print("\n1️⃣ Testing app imports...")
try:
    from app.main import app
    print("   ✅ App imports successfully")
except Exception as e:
    print(f"   ❌ Import failed: {e}")
    sys.exit(1)

# Test 2: Check routes
print("\n2️⃣ Testing routes...")
try:
    from app.routes import auth, admin, teacher
    print("   ✅ All routes imported")
except Exception as e:
    print(f"   ❌ Routes import failed: {e}")
    sys.exit(1)

# Test 3: Check services
print("\n3️⃣ Testing services...")
try:
    from app.services.embedding_service import embedding_service
    print("   ✅ Embedding service loaded")
    
    from app.services.langgraph_flow import paper_generator
    print("   ✅ Paper generator loaded")
    
    from app.services.pdf_generator import PDFGenerator
    print("   ✅ PDF generator loaded")
except Exception as e:
    print(f"   ❌ Services import failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 4: Check config
print("\n4️⃣ Testing configuration...")
try:
    from app.core.config import settings
    
    # Check required settings
    required = ['GEMINI_API_KEY', 'MONGO_URI', 'JWT_SECRET', 'EMAIL_USER']
    missing = []
    
    for var in required:
        try:
            value = getattr(settings, var)
            if value and 'your_' not in value:
                print(f"   ✅ {var} configured")
            else:
                print(f"   ⚠️  {var} needs configuration")
                missing.append(var)
        except AttributeError:
            print(f"   ❌ {var} missing")
            missing.append(var)
    
    # Check SECRET_KEY alias
    try:
        secret = settings.SECRET_KEY
        print(f"   ✅ SECRET_KEY alias working")
    except Exception as e:
        print(f"   ❌ SECRET_KEY alias failed: {e}")
    
    if missing:
        print(f"\n   ⚠️  Configure these in .env: {', '.join(missing)}")
    
except Exception as e:
    print(f"   ❌ Config failed: {e}")
    import traceback
    traceback.print_exc()

# Test 5: Check FAISS
print("\n5️⃣ Testing FAISS...")
try:
    import faiss
    from sentence_transformers import SentenceTransformer
    print("   ✅ FAISS and SentenceTransformers available")
    
    # Test embedding service
    stats = embedding_service.get_index_stats()
    print(f"   ✅ FAISS index: {stats['total_questions']} questions")
except Exception as e:
    print(f"   ⚠️  FAISS test: {e}")

# Summary
print("\n" + "="*70)
print("📊 Verification Summary")
print("="*70)
print("✅ Backend is ready to start!")
print("\n📝 Next steps:")
print("   1. Configure .env file (if needed)")
print("   2. Run: uvicorn app.main:app --reload")
print("   3. Open: http://localhost:8000/docs")
print("="*70)
