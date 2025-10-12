"""
Seed script to populate the database with initial data
"""

import asyncio
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings
from passlib.context import CryptContext

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def seed_database():
    print("\n" + "="*60)
    print("  DATABASE SEEDING")
    print("="*60 + "\n")
    
    # Connect to MongoDB Atlas
    print("📊 Connecting to MongoDB Atlas...")
    client = AsyncIOMotorClient(settings.MONGODB_URI)
    db = client[settings.MONGODB_DB_NAME]
    
    try:
        # Test connection
        await client.admin.command('ping')
        print("✅ Connected successfully!\n")
        
        # ============================================
        # 1. SEED USERS
        # ============================================
        print("👥 Seeding Users...")
        
        # Check if admin already exists
        existing_admin = await db.users.find_one({"email": "admin@examgen.com"})
        
        if existing_admin:
            print("   ⚠️  Admin user already exists, skipping...")
        else:
            # Create admin user
            admin_user = {
                "email": "admin@examgen.com",
                "password": pwd_context.hash("admin123"),  # Change this in production!
                "full_name": "System Administrator",
                "role": "admin",
                "department": "Administration",
                "created_at": datetime.utcnow(),
                "is_active": True
            }
            
            result = await db.users.insert_one(admin_user)
            print(f"   ✅ Created admin user: admin@examgen.com")
            print(f"      Password: admin123 (Change this!)")
            print(f"      ID: {result.inserted_id}")
        
        # Check if teacher already exists
        existing_teacher = await db.users.find_one({"email": "teacher@examgen.com"})
        
        if existing_teacher:
            print("   ⚠️  Teacher user already exists, skipping...")
        else:
            # Create sample teacher user
            teacher_user = {
                "email": "teacher@examgen.com",
                "password": pwd_context.hash("teacher123"),  # Change this in production!
                "full_name": "John Doe",
                "role": "teacher",
                "department": "Computer Science",
                "created_at": datetime.utcnow(),
                "is_active": True
            }
            
            result = await db.users.insert_one(teacher_user)
            print(f"   ✅ Created teacher user: teacher@examgen.com")
            print(f"      Password: teacher123 (Change this!)")
            print(f"      ID: {result.inserted_id}")
        
        print()
        
        # ============================================
        # 2. SEED SUBJECTS
        # ============================================
        print("📚 Seeding Subjects...")
        
        subjects = [
            {
                "name": "Data Structures and Algorithms",
                "code": "CS201",
                "department": "Computer Science",
                "year": 2,
                "credits": 4,
                "created_at": datetime.utcnow()
            },
            {
                "name": "Database Management Systems",
                "code": "CS301",
                "department": "Computer Science",
                "year": 3,
                "credits": 4,
                "created_at": datetime.utcnow()
            },
            {
                "name": "Operating Systems",
                "code": "CS302",
                "department": "Computer Science",
                "year": 3,
                "credits": 4,
                "created_at": datetime.utcnow()
            },
            {
                "name": "Computer Networks",
                "code": "CS303",
                "department": "Computer Science",
                "year": 3,
                "credits": 3,
                "created_at": datetime.utcnow()
            },
            {
                "name": "Machine Learning",
                "code": "CS401",
                "department": "Computer Science",
                "year": 4,
                "credits": 4,
                "created_at": datetime.utcnow()
            }
        ]
        
        # Check if subjects already exist
        existing_subjects = await db.subjects.count_documents({})
        
        if existing_subjects > 0:
            print(f"   ⚠️  {existing_subjects} subjects already exist, skipping...")
        else:
            result = await db.subjects.insert_many(subjects)
            print(f"   ✅ Created {len(result.inserted_ids)} subjects")
            for subject in subjects:
                print(f"      • {subject['code']}: {subject['name']}")
        
        print()
        
        # ============================================
        # 3. CREATE INDEXES
        # ============================================
        print("🔍 Creating Database Indexes...")
        
        # Users indexes
        await db.users.create_index("email", unique=True)
        await db.users.create_index("role")
        print("   ✅ Users indexes created")
        
        # Resources indexes
        await db.resources.create_index("teacher_id")
        await db.resources.create_index("subject")
        await db.resources.create_index([("subject", 1), ("teacher_id", 1)])
        print("   ✅ Resources indexes created")
        
        # Papers indexes
        await db.papers.create_index("teacher_id")
        await db.papers.create_index("status")
        await db.papers.create_index([("teacher_id", 1), ("status", 1)])
        await db.papers.create_index([("subject", 1), ("status", 1)])
        print("   ✅ Papers indexes created")
        
        # History indexes
        await db.prompts_history.create_index("teacher_id")
        await db.prompts_history.create_index("created_at")
        print("   ✅ History indexes created")
        
        # Subjects indexes
        await db.subjects.create_index("code", unique=True)
        await db.subjects.create_index("department")
        print("   ✅ Subjects indexes created")
        
        print()
        
        # ============================================
        # 4. SUMMARY
        # ============================================
        print("="*60)
        print("  SEEDING COMPLETE!")
        print("="*60 + "\n")
        
        # Count documents
        users_count = await db.users.count_documents({})
        subjects_count = await db.subjects.count_documents({})
        resources_count = await db.resources.count_documents({})
        papers_count = await db.papers.count_documents({})
        
        print("📊 Database Summary:")
        print(f"   • Users: {users_count}")
        print(f"   • Subjects: {subjects_count}")
        print(f"   • Resources: {resources_count}")
        print(f"   • Papers: {papers_count}")
        
        print("\n🔐 Login Credentials:")
        print("   Admin:")
        print("      Email: admin@examgen.com")
        print("      Password: admin123")
        print()
        print("   Teacher:")
        print("      Email: teacher@examgen.com")
        print("      Password: teacher123")
        
        print("\n⚠️  IMPORTANT: Change these passwords in production!")
        print()
        
    except Exception as e:
        print(f"\n❌ Error during seeding: {str(e)}")
        raise
    
    finally:
        client.close()
        print("✅ Database connection closed\n")


if __name__ == "__main__":
    asyncio.run(seed_database())
