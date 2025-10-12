"""
Environment Setup Helper
Run this to check and configure your .env file
"""

import os
import secrets
from pathlib import Path


def generate_secret_key():
    """Generate a secure secret key"""
    return secrets.token_urlsafe(32)


def check_env_file():
    """Check if .env file exists and has all required variables"""
    env_path = Path(".env")
    env_example_path = Path(".env.example")
    
    print("="*70)
    print("🔧 Environment Configuration Check")
    print("="*70)
    
    # Check if .env exists
    if not env_path.exists():
        print("\n❌ .env file not found!")
        print("\n📝 Creating .env from .env.example...")
        
        if env_example_path.exists():
            # Copy .env.example to .env
            with open(env_example_path, 'r') as f:
                content = f.read()
            
            # Generate a random JWT secret
            jwt_secret = generate_secret_key()
            content = content.replace('your_super_secret_jwt_key_here_min_32_chars', jwt_secret)
            
            with open(env_path, 'w') as f:
                f.write(content)
            
            print("✅ Created .env file with generated JWT_SECRET")
            print(f"   JWT_SECRET: {jwt_secret[:20]}...")
        else:
            print("❌ .env.example not found!")
            return False
    
    # Load and check .env
    print("\n📋 Checking environment variables...")
    
    required_vars = {
        'GEMINI_API_KEY': 'Gemini API key from Google AI Studio',
        'MONGO_URI': 'MongoDB connection string',
        'JWT_SECRET': 'Secret key for JWT tokens',
        'EMAIL_USER': 'Gmail address for sending emails',
        'EMAIL_PASS': 'Gmail app password',
        'EMAIL_FROM': 'Email from address',
    }
    
    optional_vars = {
        'JWT_ALGORITHM': 'HS256',
        'ACCESS_TOKEN_EXPIRE_MINUTES': '1440',
        'BACKEND_URL': 'http://localhost:8000',
        'FRONTEND_URL': 'http://localhost:5173',
        'MAX_FILE_SIZE': '10485760',
        'UPLOAD_DIR': 'uploads',
    }
    
    # Read .env file
    env_vars = {}
    with open(env_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                env_vars[key.strip()] = value.strip()
    
    # Check required variables
    missing = []
    placeholder = []
    
    print("\n✅ Required Variables:")
    for var, description in required_vars.items():
        if var not in env_vars:
            missing.append(var)
            print(f"   ❌ {var:30s} - MISSING")
        elif 'your_' in env_vars[var] or env_vars[var] == '':
            placeholder.append(var)
            print(f"   ⚠️  {var:30s} - PLACEHOLDER (needs configuration)")
        else:
            # Mask sensitive values
            value = env_vars[var]
            if len(value) > 20:
                display = value[:10] + '...' + value[-5:]
            else:
                display = value[:5] + '...'
            print(f"   ✅ {var:30s} - {display}")
    
    print("\n📝 Optional Variables:")
    for var, default in optional_vars.items():
        value = env_vars.get(var, default)
        print(f"   ✓ {var:30s} - {value}")
    
    # Summary
    print("\n" + "="*70)
    if missing:
        print("❌ Missing variables:", ', '.join(missing))
        return False
    elif placeholder:
        print("⚠️  Variables need configuration:", ', '.join(placeholder))
        print("\n📝 Next steps:")
        print("   1. Get Gemini API key: https://makersuite.google.com/app/apikey")
        print("   2. Set up MongoDB Atlas: https://www.mongodb.com/cloud/atlas")
        print("   3. Create Gmail app password: https://myaccount.google.com/apppasswords")
        print("   4. Update .env file with your credentials")
        return False
    else:
        print("✅ All environment variables configured!")
        return True


def test_imports():
    """Test if all required packages are installed"""
    print("\n" + "="*70)
    print("📦 Checking Python Packages")
    print("="*70)
    
    packages = {
        'fastapi': 'FastAPI',
        'uvicorn': 'Uvicorn',
        'motor': 'Motor (MongoDB async)',
        'pydantic': 'Pydantic',
        'pydantic_settings': 'Pydantic Settings',
        'langchain': 'LangChain',
        'langchain_google_genai': 'LangChain Google GenAI',
        'langgraph': 'LangGraph',
        'faiss': 'FAISS',
        'sentence_transformers': 'Sentence Transformers',
        'fitz': 'PyMuPDF',
        'docx': 'python-docx',
        'pptx': 'python-pptx',
        'PIL': 'Pillow',
        'pytesseract': 'pytesseract',
        'reportlab': 'ReportLab',
        'fastapi_mail': 'FastAPI Mail',
        'passlib': 'Passlib',
        'python_jose': 'Python JOSE',
    }
    
    missing = []
    
    for module, name in packages.items():
        try:
            __import__(module)
            print(f"   ✅ {name:30s}")
        except ImportError:
            print(f"   ❌ {name:30s} - NOT INSTALLED")
            missing.append(name)
    
    if missing:
        print(f"\n❌ Missing packages: {', '.join(missing)}")
        print("\n📝 Install with:")
        print("   pip install -r requirements.txt")
        return False
    else:
        print("\n✅ All packages installed!")
        return True


def main():
    """Main setup function"""
    print("\n" + "="*70)
    print("🚀 Intelligent Exam Paper Generator - Setup")
    print("="*70)
    
    # Check environment
    env_ok = check_env_file()
    
    # Check packages
    packages_ok = test_imports()
    
    # Final summary
    print("\n" + "="*70)
    print("📊 Setup Summary")
    print("="*70)
    
    print(f"Environment: {'✅ Ready' if env_ok else '❌ Needs configuration'}")
    print(f"Packages:    {'✅ Ready' if packages_ok else '❌ Needs installation'}")
    
    if env_ok and packages_ok:
        print("\n🎉 System is ready to run!")
        print("\n📝 Next steps:")
        print("   1. Start backend:  uvicorn app.main:app --reload")
        print("   2. Start frontend: cd ../frontend && npm run dev")
        print("   3. Open browser:   http://localhost:5173")
    else:
        print("\n⚠️  System needs configuration. Follow the steps above.")
    
    print("="*70)


if __name__ == "__main__":
    main()
