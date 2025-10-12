"""
Test Cloudinary connection and configuration
"""

import cloudinary
import cloudinary.api
from app.core.config import settings

print("\n" + "="*60)
print("  CLOUDINARY CONNECTION TEST")
print("="*60 + "\n")

print("☁️  Cloudinary Configuration:")
print(f"   Cloud Name: {settings.CLOUDINARY_CLOUD_NAME}")
print(f"   API Key: {settings.CLOUDINARY_API_KEY}")
print(f"   API Secret: {'*' * (len(settings.CLOUDINARY_API_SECRET) - 4) + settings.CLOUDINARY_API_SECRET[-4:]}\n")

# Configure Cloudinary
cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET,
    secure=True
)

print("🔍 Testing connection...\n")

try:
    # Test by getting account usage info
    result = cloudinary.api.usage()
    
    print("✅ Successfully connected to Cloudinary!")
    print(f"\n📊 Account Information:")
    print(f"   Plan: {result.get('plan', 'N/A')}")
    print(f"   Credits: {result.get('credits', {}).get('usage', 0):,}")
    print(f"   Storage Used: {result.get('storage', {}).get('usage', 0) / 1024 / 1024:.2f} MB")
    print(f"   Bandwidth Used: {result.get('bandwidth', {}).get('usage', 0) / 1024 / 1024:.2f} MB")
    
    # Get resource count
    resources = cloudinary.api.resources(max_results=1)
    total_resources = resources.get('total_count', 0)
    print(f"   Total Resources: {total_resources}")
    
    print("\n" + "="*60)
    print("  CONNECTION TEST PASSED ✅")
    print("="*60 + "\n")
    
except cloudinary.exceptions.AuthorizationRequired as e:
    print("❌ Authentication failed!")
    print(f"   Error: Invalid credentials\n")
    
    print("🔧 Troubleshooting:")
    print("   1. Check CLOUDINARY_CLOUD_NAME in .env")
    print("   2. Check CLOUDINARY_API_KEY in .env")
    print("   3. Check CLOUDINARY_API_SECRET in .env")
    print("   4. Verify credentials at: https://cloudinary.com/console\n")
    
    print("="*60)
    print("  CONNECTION TEST FAILED ❌")
    print("="*60 + "\n")
    
except Exception as e:
    print(f"❌ Connection failed!")
    print(f"   Error: {str(e)}\n")
    
    print("🔧 Troubleshooting:")
    print("   1. Verify Cloudinary credentials")
    print("   2. Check internet connection")
    print("   3. Check firewall settings\n")
    
    print("="*60)
    print("  CONNECTION TEST FAILED ❌")
    print("="*60 + "\n")
