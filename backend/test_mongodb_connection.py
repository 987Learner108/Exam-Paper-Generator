"""
Test MongoDB Atlas connection
"""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

async def test_mongodb_connection():
    print("\n" + "="*60)
    print("  MONGODB ATLAS CONNECTION TEST")
    print("="*60 + "\n")
    
    print(f"📊 Connecting to MongoDB Atlas...")
    print(f"   Database: {settings.MONGODB_DB_NAME}")
    print(f"   URI: {settings.MONGODB_URI[:30]}...{settings.MONGODB_URI[-20:]}\n")
    
    try:
        # Create client
        client = AsyncIOMotorClient(
            settings.MONGODB_URI,
            serverSelectionTimeoutMS=5000
        )
        
        # Test connection with ping
        await client.admin.command('ping')
        
        print("✅ Successfully connected to MongoDB Atlas!")
        
        # Get database
        db = client[settings.MONGODB_DB_NAME]
        
        # List collections
        collections = await db.list_collection_names()
        print(f"\n📁 Collections in '{settings.MONGODB_DB_NAME}':")
        if collections:
            for col in collections:
                count = await db[col].count_documents({})
                print(f"   • {col}: {count} documents")
        else:
            print("   (No collections yet - will be created on first use)")
        
        # Close connection
        client.close()
        
        print("\n" + "="*60)
        print("  CONNECTION TEST PASSED ✅")
        print("="*60 + "\n")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Connection failed!")
        print(f"   Error: {str(e)}\n")
        
        print("🔧 Troubleshooting:")
        print("   1. Check your MONGODB_URI in .env file")
        print("   2. Verify password is correct (no special characters issues)")
        print("   3. Ensure IP is whitelisted in MongoDB Atlas")
        print("   4. Check network/firewall settings\n")
        
        print("="*60)
        print("  CONNECTION TEST FAILED ❌")
        print("="*60 + "\n")
        
        return False

if __name__ == "__main__":
    asyncio.run(test_mongodb_connection())
