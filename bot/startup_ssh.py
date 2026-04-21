import subprocess
import time
import threading
import os
import re
import sys

def start_api_server():
    print("🔌 شروع API سرور...")
    return subprocess.Popen([sys.executable, "bot/api.py"], cwd=".")

def start_bot(webapp_url):
    print("🤖 شروع ربات تلگرام...")
    env = os.environ.copy()
    env["WEB_APP_URL"] = webapp_url
    return subprocess.Popen([sys.executable, "bot/main.py"], cwd=".", env=env)

def start_web_server():
    # دیگر نیازی به http.server نیست چون Flask خودش فایل‌ها رو میده
    pass

def setup_ssh_tunnel():
    print("⏳ در حال ساخت لینک امن (HTTPS) با سرویس رایگان جایگزین Ngrok...")
    try:
        # اجرای SSH به صورت مخفی (تصحیح localhost به 127.0.0.1 برای جلوگیری از باگ IPv6 ویندوز)
        tunnel_proc = subprocess.Popen(
            ["ssh", "-o", "StrictHostKeyChecking=no", "-R", "80:127.0.0.1:5000", "nokey@localhost.run"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding='utf-8'
        )
        
        url = None
        # خواندن خروجی برای پیدا کردن لینک
        for line in iter(tunnel_proc.stdout.readline, ''):
            if "https://" in line and ".lhr.life" in line:
                match = re.search(r'(https://[a-zA-Z0-9-]+\.lhr\.life)', line)
                if match:
                    url = match.group(1)
                    break
            elif "Permission denied" in line or "port forwarding is disabled" in line:
                print("❌ ارور سرور:", line.strip())
                break
                
        if not url:
            print("❌ نتوانستم لینک HTTPS بگیرم. ممکن است مشکل اینترنت داشته باشید.")
            return None, tunnel_proc
            
        print(f"\n✅ تونل HTTPS ساخته شد: {url}\n")
        
        # رشته‌ای برای خالی کردن خروجی تونل تا مسدود/قطع نشود
        def consume_output(pipe):
            for _ in iter(pipe.readline, ''):
                pass
        threading.Thread(target=consume_output, args=(tunnel_proc.stdout,), daemon=True).start()
        
        return url, tunnel_proc
    except Exception as e:
        print(f"❌ خطا در تونل: {e}")
        return None, None

def main():
    print("""
    ╔═══════════════════════════════════════════╗
    ║  🚀 راه‌اندازی سریع ربات و وب‌سایت کلینیک ║
    ║  ✅ بدون نیاز به فیلترشکن و Ngrok         ║
    ╚═══════════════════════════════════════════╝
    """)
    
    # 1. گرفتن لینک معتبر و آزاد
    public_url, tunnel_proc = setup_ssh_tunnel()
    
    if public_url:
        print("-" * 50)
        print(f"🔗 لینک اختصاصی شما برای تلگرام:\n{public_url}")
        print("-" * 50)
        
        # 2. شروع سرویس‌ها در پس‌زمینه
        proc_api = start_api_server()
        time.sleep(1) # تا سرور api بالا بیاد
        
        proc_bot = start_bot(public_url)
        
        print("\n🎉 سیستم کامنت کامل بالا آمد! حالا موبایل خود یا تلگرام ویندوز را باز کنید.")
        print("🤖 با ارسال /start به ربات، دکمه شیشه‌ای فرم را باز کرده و ثبت نام کنید.\n")
        
        # 3. باز نگه داشتن کنسول
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\n⛔ درخواست توقف... در حال بستن سرویس‌ها...")
            proc_api.terminate()
            proc_bot.terminate()
            if tunnel_proc:
                tunnel_proc.terminate()
            print("👋 با موفقیت خارج شد.")
            
    else:
        print("❌ استارتاپ متوقف شد. لطفاً دوباره امتحان کنید.")

if __name__ == "__main__":
    main()