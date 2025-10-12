"""
Direct test of Gemini API without LangChain
"""

import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.config import settings

print("="*70)
print("🧪 Testing Gemini API Directly")
print("="*70)

api_key = settings.GEMINI_API_KEY
print(f"\n🔑 API Key: {api_key[:10]}...{api_key[-4:]}")

try:
    import google.generativeai as genai
    
    # Configure
    genai.configure(api_key=api_key)
    
    print("\n📋 Step 1: Listing available models...")
    models = list(genai.list_models())
    
    print(f"   Found {len(models)} models")
    
    # Find models that support generateContent
    content_models = [
        m for m in models 
        if 'generateContent' in m.supported_generation_methods
    ]
    
    print(f"\n✅ Models supporting generateContent: {len(content_models)}")
    for model in content_models:
        model_name = model.name.replace('models/', '')
        print(f"   • {model_name}")
    
    if not content_models:
        print("\n❌ No models found!")
        print("💡 Your API key might not have access to Gemini models")
        print("   Visit: https://makersuite.google.com/app/apikey")
        exit(1)
    
    # Test with the first available model
    test_model = content_models[0].name
    print(f"\n🧪 Step 2: Testing with {test_model}...")
    
    model = genai.GenerativeModel(test_model)
    response = model.generate_content("Say hello in one word")
    
    print(f"   ✅ Success!")
    print(f"   Response: {response.text}")
    
    # Recommend model for LangChain
    print("\n" + "="*70)
    print("💡 RECOMMENDED MODEL FOR YOUR CODE:")
    print("="*70)
    
    # Find best model
    model_name = test_model.replace('models/', '')
    
    print(f"\nUse this in langgraph_flow.py:")
    print(f'   model="{model_name}"')
    
    print("\n📝 Update line 68 in backend/app/services/langgraph_flow.py:")
    print(f'   model_to_use = "{model_name}"')
    
except ImportError:
    print("\n❌ google-generativeai not installed")
    print("💡 Install with: pip install google-generativeai")
    
except Exception as e:
    print(f"\n❌ Error: {str(e)}")
    print("\n💡 Troubleshooting:")
    print("   1. Check API key is valid")
    print("   2. Try generating new key at: https://makersuite.google.com/app/apikey")
    print("   3. Make sure you're using the latest google-generativeai package")
    print("      pip install --upgrade google-generativeai")

print("\n" + "="*70)
