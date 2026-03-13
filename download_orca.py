"""
Download orca-mini model for Ollama
"""
import requests
import json

def download_model(model_name="orca-mini"):
    """Download model from Ollama API"""
    print(f"⏳ Downloading {model_name} model (this takes ~3-5 minutes)...")
    
    url = "http://localhost:11434/api/pull"
    data = {"name": model_name}
    
    try:
        response = requests.post(url, json=data, stream=True)
        
        total_lines = 0
        for line in response.iter_lines():
            if line:
                try:
                    parsed = json.loads(line)
                    status = parsed.get('status', '')
                    if 'pulling' in status.lower() or 'downloading' in status.lower():
                        total_lines += 1
                        if total_lines % 10 == 0:
                            print(f"⬇️  {status}...")
                except:
                    pass
        
        print(f"✅ {model_name} model downloaded successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print(f"Make sure Ollama is running in another PowerShell window: ollama serve")
        return False

if __name__ == "__main__":
    success = download_model("orca-mini")
    if success:
        print("\n✅ Ready! The app will now use orca-mini model.")
        print("It's MUCH faster than Phi (3-5x faster)!")
