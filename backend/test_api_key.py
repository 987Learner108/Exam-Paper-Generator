"""
Test script to verify Gemini API key is loaded correctly
"""

import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.config import settings

print("="*60)
print("🔍 Checking Environment Configuration")
print("="*60)

print(f"\n📁 Current directory: {os.getcwd()}")
print(f"📄 .env file exists: {os.path.exists('.env')}")

if os.path.exists('.env'):
    print("\n📝 .env file contents (first 5 lines):")
    with open('.env', 'r') as f:
        for i, line in enumerate(f):
            if i < 5:
                # Mask sensitive data
                if 'API_KEY' in line and '=' in line:
                    key, value = line.split('=', 1)
                    if len(value.strip()) > 10:
                        masked = value.strip()[:10] + "..." + value.strip()[-4:]
                    else:
                        masked = value.strip()
                    print(f"   {key}={masked}")
                elif 'MONGO_URI' in line:
                    print(f"   {line.strip()}")
                else:
                    print(f"   {line.strip()}")

print("\n🔑 Loaded Configuration:")
print(f"   GEMINI_API_KEY: {settings.GEMINI_API_KEY[:10]}...{settings.GEMINI_API_KEY[-4:] if len(settings.GEMINI_API_KEY) > 14 else '[TOO SHORT]'}")
print(f"   MONGO_URI: {settings.MONGO_URI}")
print(f"   API Key Length: {len(settings.GEMINI_API_KEY)} characters")

# Validate API key format
if settings.GEMINI_API_KEY.startswith('AIza'):
    print("   ✅ API key format looks correct (starts with AIza)")
elif settings.GEMINI_API_KEY == 'your_gemini_api_key_here':
    print("   ❌ API key is still the placeholder!")
    print("\n💡 Action Required:")
    print("   1. Get API key from: https://makersuite.google.com/app/apikey")
    print("   2. Update GEMINI_API_KEY in backend/.env")
    print("   3. Restart the backend server")
else:
    print("   ⚠️  API key format unusual (should start with 'AIza')")

# Test API key with Gemini
print("\n🧪 Testing Gemini API connection...")
try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",  # Updated model name
        google_api_key=settings.GEMINI_API_KEY,
        convert_system_message_to_human=True
    )
    
    # Simple test
    response = llm.invoke("Say 'Hello' in one word")
    print(f"   ✅ API key is valid!")
    print(f"   Response: {response.content}")
    
except Exception as e:
    print(f"   ❌ API key test failed!")
    print(f"   Error: {str(e)}")
    print("\n💡 Troubleshooting:")
    print("   1. Verify your API key at: https://makersuite.google.com/app/apikey")
    print("   2. Make sure the key is active and not expired")
    print("   3. Check if you have API quota remaining")

print("\n" + "="*60)
