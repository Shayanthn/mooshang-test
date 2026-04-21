# 🧪 راهنمای تست محلی پروژه

**تاریخ:** 1403/01/26  
**وضعیت:** 🚀 آماده برای تست

---

## 📋 محتویات پروژه

```
clinic automation/
├── index.html              # صفحه وب اصلی (فرم ثبت اطلاعات)
├── script.js               # JavaScript (تست + API)
├── styles.css              # استایل‌ها
├── data.json               # داده‌های JSON (اختیاری)
└── bot/
    ├── main.py             # ربات تلگرام
    ├── api.py              # سرور API Flask
    ├── config.py           # تنظیمات
    ├── requirements.txt    # وابستگی‌های Python
    ├── modules/
    │   ├── database.py     # مدیریت DB
    │   ├── user_manager.py # مدیریت کاربران
    │   └── handlers.py     # Handlers
    ├── database/
    │   └── users.json      # DATABASE (خودکار ساخته می‌شود)
    └── logs/
        └── bot.log         # لاگ‌ها
```

---

## 🚀 گام‌های اجرا

### **گام 1️⃣: نصب وابستگی‌های Python**

```powershell
cd bot
pip install -r requirements.txt
```

✅ **منتظر:** نصب `python-telegram-bot`, `flask`, `requests`

---

### **گام 2️⃣: سرور API را شروع کنید** (Terminal 1)

```powershell
cd bot
python api.py
```

**انتظار ببرید:**
```
╔════════════════════════════════════════════╗
║  🔌  API Server                            ║
║  Flask REST API - Form Handler             ║
╚════════════════════════════════════════════╝

 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
```

✅ **تنظیم:** سرور روی `http://localhost:5000` اجرا می‌شود

---

### **گام 3️⃣: ربات تلگرام را شروع کنید** (Terminal 2)

```powershell
cd bot
python main.py
```

**انتظار ببرید:**
```
╔════════════════════════════════════════════╗
║  🤖  ربات تلگرام کاشت موی                ║
║  Hair Transplant Clinic Bot                ║
║  Python - Telegram Bot API                 ║
╚════════════════════════════════════════════╝

🚀 Starting bot...

✅ Bot started successfully!
```

✅ **تنظیم:** ربات روی Telegram فعال است

---

### **گام 4️⃣: وب‌سایت را باز کنید** (مرورگر)

```
http://localhost:8000/index.html
```

یا اگر Python Server دارید:
```powershell
python -m http.server 8000
```

---

## 🧪 تست مرحله به مرحله

### **صفحه وب:**

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃  💗 درخواست اطلاعات بیمار   ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃                             ┃
┃ 👤 اطلاعات شخصی            ┃
┃ ┌────────────────────────┐ ┃
┃ │ نام: [              ] │ ┃
┃ │ نام خانوادگی: [     ] │ ┃
┃ │ شماره تماس: [      ] │ ┃
┃ └────────────────────────┘ ┃
┃                             ┃
┃ 🏥 اطلاعات پزشکی           ┃
┃ ┌────────────────────────┐ ┃
┃ │ سیگاری: [انتخاب کنید] │ ┃
┃ │ دیابت: [انتخاب کنید] │ ┃
┃ └────────────────────────┘ ┃
┃                             ┃
┃ 🔗 تماس بیشتر              ┃
┃ ┌────────────────────────┐ ┃
┃ │ شناسه تلگرام: [....] │ ┃
┃ └────────────────────────┘ ┃
┃                             ┃
┃     [ثبت اطلاعات]         ┃
┃                             ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃ 🧪 پنل تست توسعه‌دهندگان     ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃ شناسه تست: test_user_001      ┃
┃                             ┃
┃ [🚀 شروع تست محلی]        ┃
┃ [🔄 حذف داده‌های تست]     ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

---

## 📱 تست عملی (مثال واقعی)

### **مرحله 1: دکمه "🚀 شروع تست محلی" را کلیک کنید**

```
🧪 Starting test mode with user: test_user_001
📤 Sending test data...
```

✅ **فرم خودکار پر می‌شود:**
```
نام: محمد
نام خانوادگی: رضایی
شماره تماس: 09151234567
سیگاری: خیر
دیابت: خیر
شناسه: test_user_001
```

### **مرحله 2: دکمه "ثبت اطلاعات" را کلیک کنید**

```
✅ اطلاعات شما با موفقیت ثبت شد
```

### **مرحله 3: بررسی Database**

**باز کنید:** `bot/database/users.json`

```json
{
  "test_user_001": {
    "chat_id": null,
    "user_id": "test_user_001",
    "first_name": "unknown",
    "last_name": "user",
    "phone": "09151234567",
    "smoker": "no",
    "diabetes": "no",
    "firstName": "محمد",
    "lastName": "رضایی",
    "created_at": "2026-04-15T14:30:00",
    "form_updated_at": "2026-04-15T14:35:00"
  }
}
```

✅ **همه‌چیز ذخیره شده است!**

---

## 🔍 Console Logs (DevTools)

**F12 را فشار دهید** و **Console** را باز کنید:

```javascript
// وقتی صفحه لود می‌شود:
✅ Form ready for input
🔗 Telegram Web App: false

// وقتی "شروع تست محلی" را کلیک می‌کنید:
🧪 Starting test mode with user: test_user_001
📤 Sending test data...
✅ Test data saved successfully!
📊 Response: {status: 'success', message: '...', user_id: 'test_user_001'}

// وقتی "ثبت اطلاعات" را کلیک می‌کنید:
✅ Data submitted: {
  firstName: "محمد",
  lastName: "رضایی",
  phone: "09151234567",
  smoker: "no",
  diabetes: "no",
  timestamp: "2026-04-15T14:35:00",
  source: "telegram_web_app"
}
```

---

## 📊 API Endpoints (برای تست)

### **1. ثبت داده‌های فرم**
```
POST http://localhost:5000/api/form/submit

Body:
{
  "user_id": "test_user_001",
  "firstName": "محمد",
  "lastName": "رضایی",
  "phone": "09151234567",
  "smoker": "no",
  "diabetes": "no"
}

Response:
{
  "status": "success",
  "message": "اطلاعات با موفقیت ذخیره شد",
  "user_id": "test_user_001"
}
```

### **2. تایید کاربر**
```
GET http://localhost:5000/api/validate-user/test_user_001

Response:
{
  "status": "success",
  "exists": true,
  "user": {
    "user_id": "test_user_001",
    "name": "محمد رضایی"
  }
}
```

### **3. دریافت اطلاعات کاربر**
```
GET http://localhost:5000/api/user/test_user_001

Response:
{
  "status": "success",
  "user": { ... }
}
```

### **4. دریافت تمام کاربران**
```
GET http://localhost:5000/api/all-users

Response:
{
  "status": "success",
  "total": 1,
  "users": { ... }
}
```

---

## 📝 مثال cURL برای تست

```bash
# ثبت داده‌های فرم
curl -X POST http://localhost:5000/api/form/submit \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test_user_001",
    "firstName": "محمد",
    "lastName": "رضایی",
    "phone": "09151234567",
    "smoker": "no",
    "diabetes": "no"
  }'

# تایید کاربر
curl http://localhost:5000/api/validate-user/test_user_001

# دریافت اطلاعات
curl http://localhost:5000/api/user/test_user_001

# دریافت تمام کاربران
curl http://localhost:5000/api/all-users
```

---

## 🐛 عیب‌یابی

### **❌ Error: Connection refused**
```
❓ مشکل: سرور API راه‌نیافته
✅ راه‌حل: 
   1. Terminal اول را بررسی کنید (python api.py)
   2. Port 5000 را Check کنید
   3. api.py را دوباره شروع کنید
```

### **❌ Error: Module not found**
```
❓ مشکل: وابستگی‌های Python نصب نشده
✅ راه‌حل:
   cd bot
   pip install -r requirements.txt
```

### **❌ فرم داده پذیرفت**
```
❓ مشکل: شناسه صحیح نیست
✅ راه‌حل:
   1. Console را بررسی کنید
   2. شناسه را تغییر دهید
   3. "حذف داده‌های تست" را کلیک کنید
```

---

## ✅ نتیجه انتظار شده

```
✅ 3 Terminal باز است ✅
   Terminal 1: API Server (port 5000)
   Terminal 2: Telegram Bot
   
✅ وب‌سایت در http://localhost:8000 ✅

✅ دکمه "🚀 شروع تست محلی" ✅
   - داده‌های تست ارسال می‌شود
   - فرم خودکار پر می‌شود
   - Database تحدیث می‌شود

✅ دکمه "ثبت اطلاعات" ✅
   - داده‌ها به API پیام می‌شود
   - پیام تایید نشان داده می‌شود
   - Database ذخیره می‌شود

✅ فایل Database ✅
   bot/database/users.json
   - تمام اطلاعات ذخیره‌شده
```

---

## 🎯 خلاصه

| مرحله | عمل | نتیجه |
|------|------|--------|
| 1 | pip install wابستگی‌ها | ✅ libraries نصب |
| 2 | python api.py | ✅ API روی :5000 |
| 3 | python main.py | ✅ Telegram فعال |
| 4 | localhost:8000 | ✅ وب‌سایت باز |
| 5 | 🚀 شروع تست | ✅ فرم پر می‌شود |
| 6 | ✅ ثبت | ✅ داده‌های ذخیره |
| 7 | users.json | ✅ Database تحدیث |

---

**حالا تست را شروع کنید!** 🚀
