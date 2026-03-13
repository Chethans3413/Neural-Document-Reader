#!/usr/bin/env python
import subprocess
import sys
import os

os.chdir(r"D:\ai project")

# Run streamlit and capture output
try:
    result = subprocess.run(
        [sys.executable, "-m", "streamlit", "run", "app.py"],
        capture_output=True,
        text=True,
        timeout=10
    )
    print("STDOUT:")
    print(result.stdout[:2000] if result.stdout else "(empty)")
    print("\nSTDERR:")
    print(result.stderr[:2000] if result.stderr else "(empty)")
    print(f"\nReturn code: {result.returncode}")
except subprocess.TimeoutExpired:
    print("Streamlit is still running (good sign!)")
except Exception as e:
    print(f"Error: {e}")
