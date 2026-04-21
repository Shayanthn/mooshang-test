"""
🤖 ربات تلگرام کاشت موی - سیستم مادر
Python Telegram Bot - Modular Architecture
"""

import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from config import BOT_TOKEN, LOG_FILE
from modules.handlers import Handlers

# تنظیم لاگ‌گیری پیشرفته
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
# جلوگیری از لاگ‌های اضافی کتابخانه‌های داخلی
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

async def post_init(application):
    """اجرای پس از راه‌اندازی"""
    print('✅ Bot started successfully!')

def main():
    """تابع اصلی"""
    print('''
    ╔════════════════════════════════════════════╗
    ║  🤖  ربات تلگرام کاشت موی                ║
    ║  Hair Transplant Clinic Bot                ║
    ║  Python - Telegram Bot API                 ║
    ╚════════════════════════════════════════════╝
    ''')
    
    # ایجاد Application
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Handlers
    app.add_handler(CommandHandler('start', Handlers.start))
    app.add_handler(CommandHandler('help', Handlers.help_command))
    app.add_handler(MessageHandler(filters.TEXT | filters.StatusUpdate.WEB_APP_DATA, Handlers.handle_message))
    
    # Error handler
    app.add_error_handler(Handlers.error_handler)
    
    # Post-init
    app.post_init = post_init
    
    # شروع ربات
    print('🚀 Starting bot...\n')
    app.run_polling(allowed_updates=['message', 'edited_message'])

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\n\n⛔ Bot stopped by user')
    except Exception as e:
        print(f'\n\n❌ Error: {e}')
