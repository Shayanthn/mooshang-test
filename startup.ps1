# ==========================================
# 🚀 Clinic Automation - Complete Startup
# ==========================================

Write-Host "
╔════════════════════════════════════════╗
║  🏥 کاشت موی - Startup                ║
║  Clinic Automation System              ║
╚════════════════════════════════════════╝
" -ForegroundColor Cyan

# 1️⃣ پیمایش به پوشه‌ها
$botDir = "c:\Users\Cyber System\Desktop\clinic aotumation\bot"
$appDir = "c:\Users\Cyber System\Desktop\clinic aotumation"

Write-Host "`n📂 پوشه‌ها:" -ForegroundColor Green
Write-Host "   Bot:  $botDir"
Write-Host "   App:  $appDir"

# 2️⃣ اختیار: ngrok HTTPS
Write-Host "`n🔒 آیا می‌خواهی ngrok را استفاده کنی؟ (برای WebApp HTTPS)" -ForegroundColor Yellow
Write-Host "    (اگر بله، قبلاً 'ngrok.exe' را دانلود کن)"
Write-Host "`n    دستور: ngrok http 8000"
Write-Host "    سپس HTTPS URL را اینجا کپی کن (متل: https://xxxx-xxx.ngrok.io) "
$ngrokUrl = Read-Host "`n🌐 ngrok HTTPS URL (یا Enter برای بدون ngrok)"

# 3️⃣ هر سرویس را در یک PowerShell جدید شروع کن
Write-Host "`n🚀 سرویس‌ها را شروع می‌کنم..." -ForegroundColor Green

# API Server
Write-Host "`n📍 [1/3] API Server (Port 5000)..." -ForegroundColor Cyan
$apiProcess = Start-Process powershell -ArgumentList "-Command cd '$botDir'; python api.py" -PassThru -NoNewWindow
Write-Host "    ✅ شروع شد (PID: $($apiProcess.Id))" -ForegroundColor Green

# Telegram Bot
Write-Host "`n📍 [2/3] Telegram Bot..." -ForegroundColor Cyan
if ($ngrokUrl) {
    $botProcess = Start-Process powershell -ArgumentList "-Command `$env:WEB_APP_URL='$ngrokUrl'; cd '$botDir'; python main.py" -PassThru -NoNewWindow
    Write-Host "    ✅ شروع شد (ngrok: $ngrokUrl) - PID: $($botProcess.Id)" -ForegroundColor Green
} else {
    $botProcess = Start-Process powershell -ArgumentList "-Command cd '$botDir'; python main.py" -PassThru -NoNewWindow
    Write-Host "    ✅ شروع شد (PID: $($botProcess.Id)) - بدون ngrok" -ForegroundColor Green
}

# Web Server
Write-Host "`n📍 [3/3] Web Server (Port 8000)..." -ForegroundColor Cyan
$webProcess = Start-Process powershell -ArgumentList "-Command cd '$appDir'; python -m http.server 8000" -PassThru -NoNewWindow
Write-Host "    ✅ شروع شد (PID: $($webProcess.Id))" -ForegroundColor Green

# ✅ خلاصه
Write-Host "`
╔════════════════════════════════════════╗
║  ✅ تمام سرویس‌ها شروع شدند!         ║
╚════════════════════════════════════════╝

📊 وضعیت:
   🔌 API Server:    http://localhost:5000
   🤖 Telegram Bot:  Running...
   🌐 Web Server:    http://localhost:8000
" -ForegroundColor Green

if ($ngrokUrl) {
    Write-Host "   🔒 ngrok HTTPS:   $ngrokUrl" -ForegroundColor Cyan
}

Write-Host "
🎯 نحوه استفاده:
   1. تلگرام → /start
   2. دکمه '📝 ثبت اطلاعات' را کلیک کن
   3. فرم را پر کن ✍️
   4. 'بازگشت به ربات' را کلیک کن
   5. اطلاعات شما ذخیره شد! ✅

⚠️  برای بسته کردن: هر پنجره را بسته
" -ForegroundColor Yellow
