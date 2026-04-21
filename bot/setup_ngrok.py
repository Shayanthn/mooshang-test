#!/usr/bin/env python3
"""
Setup ngrok tunnel for HTTPS proxy
"""
import os
import sys
from pyngrok import ngrok

def setup_ngrok():
    """Setup ngrok tunnel"""
    try:
        # از پورت 8000 برای web app استفاده کن
        public_url = ngrok.connect(8000, "http")
        print(f"\n✅ ngrok tunnel created!")
        print(f"🔗 Public URL: {public_url}")
        print(f"💾 Update config.py with: WEB_APP_URL = '{public_url}'\n")
        
        # Keep tunnel alive
        print("🔄 ngrok tunnel is running...")
        print("Press Ctrl+C to stop\n")
        
        ngrok_process = ngrok.get_ngrok_process()
        ngrok_process.proc.wait()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    setup_ngrok()
