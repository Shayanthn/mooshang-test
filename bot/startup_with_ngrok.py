"""
🚀 Startup Script - تمام سرویس‌ها با ngrok HTTPS Tunnel
"""

import subprocess
import time
import threading
from pyngrok import ngrok
import requests

# تنظیم ngrok
NGROK_AUTH_TOKEN = '3CcUTuQtAltPhuU3KwEIhcvj9PE_5MfbSe51pNaXsFJrWwi2h'  # اگر اکتیویشن دارید، قرار دهید

def setup_ngrok():
    """نصب ngrok tunnel"""
    try:
        if NGROK_AUTH_TOKEN:
            ngrok.set_auth_token(NGROK_AUTH_TOKEN)
        
        # ایجاد HTTP tunnel برای درگاه ۸۰۰۰
        public_url = ngrok.connect(8000, "http")
        print(f"\n✅ ngrok tunnel ایجاد شد: {public_url}\n")
        return str(public_url)
    except Exception as e:
        print(f"❌ خطا در ngrok: {e}")
        return None

def start_api_server():
    """شروع Flask API سرور"""
    print("\n🔌 شروع API سرور...")
    subprocess.Popen(["python", "bot/api.py"], cwd=".")

def start_bot():
    """شروع Telegram Bot"""
    print("\n🤖 شروع ربات تلگرام...")
    subprocess.Popen(["python", "bot/main.py"], cwd=".")

def start_web_server():
    """شروع وب سرور"""
    print("\n🌐 شروع وب سرور...")
    subprocess.Popen(["python", "-m", "http.server", "8000"], cwd=".")

def main():
    print("""
    ╔═══════════════════════════════════════════╗
    ║  🚀 سیستم کلینیک - Startup Script         ║
    ║  تمام سرویس‌ها + ngrok HTTPS tunnel       ║
    ╚═══════════════════════════════════════════╝
    """)
    
    # تنظیم ngrok
    public_url = setup_ngrok()
    
    # شروع سرویس‌ها (در ترد‌های متوازی)
    threads = []
    
    t1 = threading.Thread(target=start_api_server, daemon=True)
    t2 = threading.Thread(target=start_bot, daemon=True)
    t3 = threading.Thread(target=start_web_server, daemon=True)
    
    threads = [t1, t2, t3]
    
    for t in threads:
        t.start()
    
    print("\n✅ تمام سرویس‌ها شروع شدند!")
    print(f"\n📱 وب‌سایت: {public_url}")
    print(f"🔌 API: {public_url}/api/")
    print(f"🤖 ربات: در حال اجرا...\n")
    
    # حفظ اجرا
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n⛔ تمام سرویس‌ها بسته شدند")
        ngrok.kill()

if __name__ == "__main__":
    main()
