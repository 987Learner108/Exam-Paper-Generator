"""
List available Gemini models for your API key
"""

import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.config import settings

print("="*70)
print("🔍 Checking Available Gemini Models")
print("="*70)

print(f"\n🔑 Using API Key: {settings.GEMINI_API_KEY[:10]}...{settings.GEMINI_API_KEY[-4:]}")

try:
    import google.generativeai as genai
    
    # Configure with API key
    genai.configure(api_key=settings.GEMINI_API_KEY)
    
    print("\n📋 Available Models:")
    print("-" * 70)
    
    models = genai.list_models()
    
    generative_models = []
    for model in models:
        # Check if it supports generateContent
        if 'generateContent' in model.supported_generation_methods:
            generative_models.append(model.name)
            print(f"✅ {model.name}")
            print(f"   Description: {model.display_name}")
            print(f"   Methods: {', '.join(model.supported_generation_methods)}")
            print()
    
    if not generative_models:
        print("❌ No models found that support generateContent")
    else:
        print("="*70)
        print("\n💡 Recommended model to use:")
        
        # Find the best model
        if any('gemini-1.5-flash' in m for m in generative_models):
            recommended = [m for m in generative_models if 'gemini-1.5-flash' in m][0]
        elif any('gemini-1.5-pro' in m for m in generative_models):
            recommended = [m for m in generative_models if 'gemini-1.5-pro' in m][0]
        elif any('gemini-pro' in m for m in generative_models):
            recommended = [m for m in generative_models if 'gemini-pro' in m][0]
        else:
            recommended = generative_models[0]
        
        # Extract just the model name (remove 'models/' prefix)
        model_name = recommended.replace('models/', '')
        
        print(f"   Model: {model_name}")
        print(f"\n📝 Update your code to use:")
        print(f'   model="{model_name}"')
        
        print("\n🔧 File to update:")
        print("   backend/app/services/langgraph_flow.py (line 59)")
        
except ImportError:
    print("\n❌ google-generativeai package not installed")
    print("💡 Install it with:")
    print("   pip install google-generativeai")
    
except Exception as e:
    print(f"\n❌ Error listing models: {str(e)}")
    print("\n💡 Troubleshooting:")
    print("   1. Check your API key is valid")
    print("   2. Visit: https://makersuite.google.com/app/apikey")
    print("   3. Make sure the key has proper permissions")

print("\n" + "="*70)
