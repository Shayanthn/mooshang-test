# Configuration File
import os
from pathlib import Path

# Bot Token
BOT_TOKEN = '422332102:AAETZYxSSXkjMP-sIBXc41hYq4DzrUOLJNk'

# API URLs
API_BASE_URL = 'http://localhost:5000'

# 🌐 برای محیط محلی: 'http://localhost:8000'
# 🔒 برای WebApp (نیاز به HTTPS): استفاده از ngrok
# ngrok http 8000 را اجرا کن و URL را اینجا قرار بده
WEB_APP_URL = os.getenv('WEB_APP_URL', 'http://localhost:8000')  # Set via ngrok or env var

# Database Settings
BASE_DIR = Path(__file__).parent.parent
DATABASE_DIR = BASE_DIR / 'database'
DATABASE_DIR.mkdir(exist_ok=True)
DATABASE_FILE = DATABASE_DIR / 'users.json'

# Logging
LOG_DIR = BASE_DIR / 'logs'
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / 'bot.log'

# UI Strings
WELCOME_MESSAGE = '''
سلام! 👋 خوش‌آمدید به <b>مرکز کاشت مو تخصصی</b> 

من <b>دستیار هوشمند</b> شما هستم. آماده‌ام تا در <b>فرایند کاشت</b> موتان راهنمایی کنم.

🆔 <b>شناسه شما:</b> <code>{user_id}</code>

📋 <b>درباره خدمات ما:</b>
✓ <b>کاشت موی طبیعی</b> با بالاترین کیفیت
✓ <b>مشاوره رایگان</b> بدون تعهد
✓ <b>تضمین نتایج</b> تا 100%
✓ <b>تجربه بالغ بر 15 سال</b>

🚀 <b>برای شروع:</b> روی دکمه <b>"📝 ثبت اطلاعات"</b> کلیک کنید و فرم را پر کنید.
مشاوران ما به‌زودی با شما تماس خواهند گرفت.

برای سوالات بیشتر می‌توانید از من پرسش کنید! 💬
'''

MORE_INFO_MESSAGE = '''
<b>📚 معلومات بیشتر درباره کاشت موی</b>

<b>🔹 فواید کاشت موی:</b>
• بازیافت اعتماد به نفس
• نتایج طبیعی و دائمی
• بدون ترومای جراحی شدید
• بازگشت سریع به فعالیت‌های روزمره

<b>🔹 مراحل فرآیند:</b>
1️⃣ مشاوره رایگان و آنلاین
2️⃣ ثبت‌نام و تجزیه و تحلیل
3️⃣ برنامه‌ریزی فردی
4️⃣ اجرای پروتکل کاشت
5️⃣ پیگیری و نتایج

<b>🔹 سوالات متداول:</b>
Q: آیا درد دارد؟ A: خیر، تحت بیهوشی موضعی انجام می‌شود
Q: چند جلسه لازم است؟ A: معمولاً 1-3 جلسه
Q: نتیجه چه زمانی مشهود است؟ A: 3-6 ماه

برای اطلاعات بیشتر با ما تماس بگیرید! 📞
'''

SUCCESS_MESSAGE = '''
<b>🎉 تبریک می‌گویم!</b>

اطلاعات شما در سیستم ما ثبت شد. ✅
مشاوران تخصصی ما در کوتاه‌ترین زمان با شما تماس خواهند گرفت.

📞 زمان‌های تماس: شنبه تا پنج‌شنبه، 09:00 تا 18:00
☎️ شماره تماس: 021-XXXX-XXXX

منتظر شنیدن از شما هستیم! 😊

🆔 شناسه کاربری: <code>{user_id}</code>
'''

# Reply Keyboard Setup
MAIN_KEYBOARD = [
    ['📝 ثبت اطلاعات'],
    ['✅ اطلاعاتو ثبت کردم', '❓ اطلاعات بیشتر'],
    ['📊 من‌اطلاعات']
]

print('✅ Configuration loaded')
