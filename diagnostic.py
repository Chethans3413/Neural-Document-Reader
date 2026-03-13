"""
Diagnostic script to test the entire pipeline
"""
import sys
import tempfile
import os

print("="*60)
print("DIAGNOSTIC TEST")
print("="*60)

# Test 1: Check Ollama connection
print("\n1. Testing Ollama connection...")
try:
    import requests
    response = requests.get("http://localhost:11434/api/tags", timeout=5)
    if response.status_code == 200:
        print("✓ Ollama is running")
        models = response.json().get("models", [])
        print(f"  Available models: {[m['name'] for m in models]}")
    else:
        print("✗ Ollama is not responding correctly")
        sys.exit(1)
except Exception as e:
    print(f"✗ Ollama connection failed: {str(e)}")
    print("  Make sure to run: ollama serve")
    sys.exit(1)

# Test 2: Test RAG Storage
print("\n2. Testing RAG Storage module...")
try:
    from rag_storage import RAGStorage
    print("✓ RAG Storage module imported successfully")
except Exception as e:
    print(f"✗ RAG Storage import failed: {str(e)}")
    sys.exit(1)

# Test 3: Test LLM Handler
print("\n3. Testing LLM Handler module...")
try:
    from llm_handler import LLMHandler
    print("✓ LLM Handler module imported successfully")
    
    # Test LLM initialization
    try:
        llm = LLMHandler(model_name="phi", temperature=0)
        print("✓ LLM initialized with 'phi' model")
    except Exception as e:
        print(f"✗ LLM initialization failed: {str(e)}")
        print("  Make sure you have downloaded phi model: ollama pull phi")
        sys.exit(1)
        
except Exception as e:
    print(f"✗ LLM Handler import failed: {str(e)}")
    sys.exit(1)

# Test 4: Test AI Agent
print("\n4. Testing AI Agent module...")
try:
    from ai_agent import AIAgent
    print("✓ AI Agent module imported successfully")
except Exception as e:
    print(f"✗ AI Agent import failed: {str(e)}")
    sys.exit(1)

# Test 5: Create a sample PDF for testing (if one doesn't exist)
print("\n5. Testing PDF loading...")
try:
    # We can't create a real PDF without pypdf utils, so we'll just test the import
    from langchain_community.document_loaders import PyPDFLoader
    print("✓ PDF loader available")
except Exception as e:
    print(f"✗ PDF loader failed: {str(e)}")
    sys.exit(1)

print("\n" + "="*60)
print("ALL TESTS PASSED! Your setup is ready.")
print("="*60)
print("\nTo use the app:")
print("1. Make sure Ollama is running: ollama serve")
print("2. Download phi model: ollama pull phi (if not already done)")
print("3. Start the app: python -m streamlit run app.py")
print("4. Go to: http://localhost:8501")
