@echo off
REM ═════════════════════════════════════════════════════════════════
REM  🚀 شروع خودکار پروژه کلینیک تلگرام
REM  Clinic Automation Bot - Auto Start Script
REM ═════════════════════════════════════════════════════════════════

echo.
echo ╔══════════════════════════════════════════════════════════────╗
echo ║  🚀 شروع پروژه کلینیک - Clinic Automation Bot              ║
echo ║  فاز تست - Test Phase                                      ║
echo ╚══════════════════════════════════════════════════════════────╝
echo.

REM بررسی Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python نصب نشده است!
    echo 📥 لطفاً Python را از https://www.python.org نصب کنید
    pause
    exit /b 1
)
echo ✅ Python پیدا شد

REM بررسی Bot Folder
if not exist "bot" (
    echo ❌ پوشه 'bot' یافت نشد!
    cd bot
) else (
    cd bot
)

REM نصب وابستگی‌ها
echo.
echo 📦 نصب وابستگی‌های Python...
pip install -r requirements.txt >nul 2>&1
if errorlevel 1 (
    echo ❌ خطا در نصب وابستگی‌ها
    pause
    exit /b 1
)
echo ✅ وابستگی‌ها نصب شدند

REM باز کردن Terminal‌های جدید
echo.
echo 🚀 شروع سرویس‌ها...
echo.

REM Terminal 1: API Server
start "API Server (Port 5000)" cmd /k "python api.py"
echo ✅ API Server شروع شد (port 5000)
timeout /t 2 >nul

REM Terminal 2: Telegram Bot
start "Telegram Bot" cmd /k "python main.py"
echo ✅ Telegram Bot شروع شد

REM Terminal 3: Web Server
echo ✅ وب‌سایت آماده است: http://localhost:8000
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║  ✅ تمام سرویس‌ها فعال است!                              ║
echo ║                                                             ║
echo ║  📱 Telegram Bot: آماده                                   ║
echo ║  🔌 API Server: http://localhost:5000                     ║
echo ║  🌐 Web App: http://localhost:8000                        ║
echo ║                                                             ║
echo ║  🧪 برای شروع تست:                                       ║
echo ║  1. چند Terminal باز شد - آن‌ها را بسته نکنید             ║
echo ║  2. مرورگر را باز کنید                                   ║
echo ║  3. http://localhost:8000/index.html را باز کنید         ║
echo ║  4. دکمه "🚀 شروع تست محلی" را کلیک کنید                 ║
echo ║                                                             ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

REM باقی مانده
cmd /k "python -m http.server 8000"
