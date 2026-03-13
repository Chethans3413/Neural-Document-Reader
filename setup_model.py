#!/usr/bin/env python3
"""
Download the neural-chat model for Ollama
Run this once: python setup_model.py
"""
import requests
import json

def download_model(model_name="neural-chat"):
    """Download model from Ollama"""
    print(f"⏳ Downloading {model_name} model...")
    print("This may take a few minutes on first run...\n")
    
    url = "http://localhost:11434/api/pull"
    data = {"name": model_name}
    
    try:
        response = requests.post(url, json=data, stream=True)
        
        for line in response.iter_lines():
            if line:
                parsed = json.loads(line)
                status = parsed.get('status', '')
                digest = parsed.get('digest', '')
                
                if 'pulling' in status.lower():
                    print(f"Pulling: {status}")
                elif 'downloading' in status.lower():
                    print(f"⬇️  Downloading...")
                elif 'verifying' in status.lower():
                    print(f"✓ Verifying...")
                elif 'success' in status.lower() or digest:
                    print(f"✅ {status}")
        
        print(f"\n✅ {model_name} model downloaded successfully!")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print(f"Make sure Ollama is running: ollama serve")

if __name__ == "__main__":
    download_model("neural-chat")
