"""
Test script to verify .env configuration
"""

from app.core.config import settings

print("\n" + "="*60)
print("  ENVIRONMENT CONFIGURATION TEST")
print("="*60 + "\n")

# MongoDB Atlas
print("📊 MongoDB Atlas Configuration:")
print(f"   URI: {settings.MONGODB_URI[:30]}...{settings.MONGODB_URI[-20:]}")
print(f"   Database: {settings.MONGODB_DB_NAME}")
print(f"   Status: {'✅ Configured' if settings.MONGODB_URI else '❌ Missing'}\n")

# Cloudinary
print("☁️  Cloudinary Configuration:")
print(f"   Cloud Name: {settings.CLOUDINARY_CLOUD_NAME}")
print(f"   API Key: {settings.CLOUDINARY_API_KEY}")
print(f"   API Secret: {'*' * (len(settings.CLOUDINARY_API_SECRET) - 4) + settings.CLOUDINARY_API_SECRET[-4:]}")
print(f"   Status: {'✅ Configured' if settings.CLOUDINARY_CLOUD_NAME else '❌ Missing'}\n")

# Gemini AI
print("🤖 Gemini AI Configuration:")
print(f"   API Key: {settings.GEMINI_API_KEY[:10]}...{settings.GEMINI_API_KEY[-10:]}")
print(f"   Status: {'✅ Configured' if settings.GEMINI_API_KEY else '❌ Missing'}\n")

# JWT
print("🔐 JWT Configuration:")
print(f"   Secret: {'*' * 20}")
print(f"   Algorithm: {settings.JWT_ALGORITHM}")
print(f"   Expiry: {settings.ACCESS_TOKEN_EXPIRE_MINUTES} minutes")
print(f"   Status: {'✅ Configured' if settings.JWT_SECRET else '❌ Missing'}\n")

# Email
print("📧 Email Configuration:")
print(f"   User: {settings.EMAIL_USER}")
print(f"   From: {settings.EMAIL_FROM}")
print(f"   Status: {'✅ Configured' if settings.EMAIL_USER else '❌ Missing'}\n")

# Application URLs
print("🌐 Application URLs:")
print(f"   Backend: {settings.BACKEND_URL}")
print(f"   Frontend: {settings.FRONTEND_URL}\n")

print("="*60)
print("  TEST COMPLETE")
print("="*60 + "\n")

# Check if all critical configs are present
critical_configs = [
    settings.MONGODB_URI,
    settings.CLOUDINARY_CLOUD_NAME,
    settings.CLOUDINARY_API_KEY,
    settings.CLOUDINARY_API_SECRET,
    settings.GEMINI_API_KEY,
    settings.JWT_SECRET,
    settings.EMAIL_USER
]

if all(critical_configs):
    print("✅ All critical configurations are present!")
    print("✅ You can start the backend server now.\n")
else:
    print("❌ Some configurations are missing!")
    print("❌ Please check your .env file.\n")
