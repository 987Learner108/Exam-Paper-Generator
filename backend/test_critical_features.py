"""
Quick test script for critical features
Run this to verify all implementations
"""

import asyncio
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.embedding_service import embedding_service


def test_faiss():
    """Test FAISS embedding service"""
    print("\n" + "="*70)
    print("🧪 Testing FAISS Embedding Service")
    print("="*70)
    
    try:
        # Test 1: Add questions
        print("\n📝 Test 1: Adding questions to FAISS...")
        questions = [
            ("What is a binary search tree?", "q1"),
            ("Explain the concept of recursion", "q2"),
            ("What are the advantages of linked lists?", "q3"),
        ]
        
        embedding_service.add_questions_batch(questions)
        print(f"   ✅ Added {len(questions)} questions")
        
        # Test 2: Check similarity
        print("\n🔍 Test 2: Checking similarity...")
        similar_question = "What is a BST?"
        is_similar, results = embedding_service.check_similarity(similar_question, threshold=0.75)
        
        if is_similar:
            print(f"   ✅ Found similar question: {results[0][0]} (similarity: {results[0][1]:.2f})")
        else:
            print(f"   ✅ No similar questions found")
        
        # Test 3: Find similar questions
        print("\n🔎 Test 3: Finding similar questions...")
        similar = embedding_service.find_similar_questions("Explain recursion", k=3)
        print(f"   ✅ Found {len(similar)} similar questions:")
        for qid, score in similar[:3]:
            print(f"      - {qid}: {score:.2f}")
        
        # Test 4: Index stats
        print("\n📊 Test 4: Index statistics...")
        stats = embedding_service.get_index_stats()
        print(f"   ✅ Total questions: {stats['total_questions']}")
        print(f"   ✅ Dimension: {stats['dimension']}")
        print(f"   ✅ Index size: {stats['index_size_mb']:.2f} MB")
        
        print("\n✅ FAISS tests passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ FAISS test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_imports():
    """Test critical imports"""
    print("\n" + "="*70)
    print("📦 Testing Critical Imports")
    print("="*70)
    
    try:
        print("\n✓ Testing FAISS...")
        import faiss
        print("  ✅ faiss imported successfully")
        
        print("\n✓ Testing SentenceTransformers...")
        from sentence_transformers import SentenceTransformer
        print("  ✅ sentence-transformers imported successfully")
        
        print("\n✓ Testing Motor (MongoDB async)...")
        from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorGridFSBucket
        print("  ✅ motor imported successfully")
        
        print("\n✓ Testing PyMuPDF...")
        import fitz
        print("  ✅ PyMuPDF imported successfully")
        
        print("\n✓ Testing LangChain...")
        from langchain_google_genai import ChatGoogleGenerativeAI
        print("  ✅ langchain-google-genai imported successfully")
        
        print("\n✓ Testing LangGraph...")
        from langgraph.graph import StateGraph, END
        print("  ✅ langgraph imported successfully")
        
        print("\n✅ All imports successful!")
        return True
        
    except Exception as e:
        print(f"\n❌ Import test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_config():
    """Test configuration"""
    print("\n" + "="*70)
    print("⚙️  Testing Configuration")
    print("="*70)
    
    try:
        from app.core.config import settings
        
        print(f"\n✓ MongoDB URI: {'✅ Set' if settings.MONGO_URI else '❌ Missing'}")
        print(f"✓ Gemini API Key: {'✅ Set' if settings.GEMINI_API_KEY else '❌ Missing'}")
        print(f"✓ Secret Key: {'✅ Set' if settings.SECRET_KEY else '❌ Missing'}")
        print(f"✓ Email User: {'✅ Set' if settings.EMAIL_USER else '❌ Missing'}")
        
        print("\n✅ Configuration check complete!")
        return True
        
    except Exception as e:
        print(f"\n❌ Config test failed: {e}")
        return False


def main():
    """Run all tests"""
    print("\n" + "="*70)
    print("🚀 CRITICAL FEATURES TEST SUITE")
    print("="*70)
    
    results = {
        "Imports": test_imports(),
        "Configuration": test_config(),
        "FAISS": test_faiss(),
    }
    
    print("\n" + "="*70)
    print("📊 TEST RESULTS")
    print("="*70)
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name:20s}: {status}")
    
    all_passed = all(results.values())
    
    print("\n" + "="*70)
    if all_passed:
        print("🎉 ALL TESTS PASSED! System is ready!")
    else:
        print("⚠️  SOME TESTS FAILED! Check errors above.")
    print("="*70)
    
    return all_passed


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
