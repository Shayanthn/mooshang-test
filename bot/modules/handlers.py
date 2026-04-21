from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from telegram.ext import ContextTypes
from modules.user_manager import user_manager
from config import WELCOME_MESSAGE, MORE_INFO_MESSAGE, SUCCESS_MESSAGE, MAIN_KEYBOARD, WEB_APP_URL

import json

class Handlers:
    """تمام Handlers تلگرام"""
    
    @staticmethod
    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """کماند /start"""
        user = update.effective_user
        chat_id = update.effective_chat.id
        
        # بررسی اینکه آیا کاربر قبلاً ثبت‌نام کرده است
        if user_manager.is_user_registered(chat_id):
            user_id = user_manager.get_user_id(chat_id)
            message = WELCOME_MESSAGE.format(user_id=user_id)
        else:
            # ایجاد کاربر جدید
            user_id = user_manager.create_new_user(chat_id, user.first_name, user.last_name or '')
            message = WELCOME_MESSAGE.format(user_id=user_id)
        
        # صفحه‌کلید
        reply_markup = ReplyKeyboardMarkup(
            MAIN_KEYBOARD,
            resize_keyboard=True,
            input_field_placeholder="یک گزینه انتخاب کنید..."
        )
        
        await update.message.reply_html(message, reply_markup=reply_markup)
        print(f'✅ User started: Chat ID {chat_id}, User ID: {user_id}')
    
    @staticmethod
    async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """کماند /help"""
        help_text = '''
<b>🆘 راهنمای دستورات</b>

/start - شروع کردن با ربات
/help - نمایش این پیام
/myinfo - نمایش اطلاعات من
/contact - تماس با ما

<b>دکمه‌های زیر هم موجود است:</b>
🔘 📝 ثبت اطلاعات
🔘 ✅ اطلاعاتو ثبت کردم
🔘 ❓ اطلاعات بیشتر
🔘 📊 اطلاعات من
        '''
        await update.message.reply_html(help_text)
    
    @staticmethod
    async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """هندل پیام‌های متنی و مینی‌اپ"""
        chat_id = update.effective_chat.id
        
        # اگر اطلاعات از سمت WebApp بازگشته باشد
        if update.message.web_app_data:
            data = json.loads(update.message.web_app_data.data)
            if data.get("action") == "form_submitted":
                success_msg = f'''
🎉 <b>اطلاعات شما با موفقیت ثبت شد!</b>

👤 <b>نام:</b> {data.get("firstName")} {data.get("lastName")}
📱 <b>شماره تماس:</b> {data.get("phone")}

همکاران ما در اولین فرصت با شما تماس می‌گیرند.
'''
                await update.message.reply_html(success_msg, reply_markup=ReplyKeyboardMarkup(MAIN_KEYBOARD, resize_keyboard=True))
            return
            
        message_text = update.message.text
        
        # بررسی کاربر
        if not user_manager.is_user_registered(chat_id):
            await update.message.reply_text('❌ لطفاً ابتدا /start را فشار دهید.')
            return
        
        user_id = user_manager.get_user_id(chat_id)
        
        # دکمه‌ها
        if message_text == '📝 ثبت اطلاعات':
            await Handlers.show_form_instructions(update, context, user_id)
        
        elif message_text == '✅ اطلاعاتو ثبت کردم':
            await update.message.reply_html(
                SUCCESS_MESSAGE.format(user_id=user_id),
                reply_markup=ReplyKeyboardMarkup(MAIN_KEYBOARD, resize_keyboard=True)
            )
        
        elif message_text == '❓ اطلاعات بیشتر':
            await update.message.reply_html(
                MORE_INFO_MESSAGE,
                reply_markup=ReplyKeyboardMarkup(MAIN_KEYBOARD, resize_keyboard=True)
            )
        
        elif message_text == '📊 اطلاعات من':
            await Handlers.show_user_info(update, context, user_id)
        
        else:
            # پیام عمومی
            await update.message.reply_text(
                '❓ متاسفانه نمی‌تونم این متن را بفهمم.\n\n'
                'لطفاً از دکمه‌های زیر استفاده کنید:',
                reply_markup=ReplyKeyboardMarkup(MAIN_KEYBOARD, resize_keyboard=True)
            )
    
    @staticmethod
    async def show_form_instructions(update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: str) -> None:
        """نمایش دستورالعمل‌های فرم و باز کردن WebApp"""
        message = f'''
<b>📝 ثبت اطلاعات</b>

برای ثبت اطلاعات کامل خود، لطفاً روی دکمه زیر کلیک کنید:

🆔 <b>شناسه کاربری شما:</b> <code>{user_id}</code>

<b>لطفاً این شناسه را یادداشت کنید!</b> این شناسه برای شناسایی اطلاعات شما استفاده می‌شود.
        '''
        
        # ساخت دکمه URL 
        form_url = f"{WEB_APP_URL}/?user_id={user_id}"
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("📝 باز کردن فرم ثبت‌نام", web_app=WebAppInfo(url=form_url))]
        ])
        
        await update.message.reply_html(message, reply_markup=keyboard)
    
    @staticmethod
    async def send_welcome_back_message(chat_id: int, user_id: str, context: ContextTypes.DEFAULT_TYPE) -> None:
        """ارسال پیام خوش‌آمد بازگشت"""
        message = f'''
<b>✅ اطلاعات شما دریافت شد!</b>

شناسه شما: <code>{user_id}</code>

<b>📋 اطلاعات ثبت‌شده:</b>
درحال پردازش اطلاعات...

مشاوران ما به‌زودی با شما تماس خواهند گرفت.

دوباره می‌توانید دکمه‌های زیر را استفاده کنید:
        '''
        
        reply_markup = ReplyKeyboardMarkup(MAIN_KEYBOARD, resize_keyboard=True)
        
        try:
            await context.bot.send_message(
                chat_id=chat_id,
                text=message,
                parse_mode='HTML',
                reply_markup=reply_markup
            )
        except Exception as e:
            print(f'Error sending message: {e}')
    
    @staticmethod
    async def handle_callback_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """هندل callback queries"""
        query = update.callback_query
        await query.answer()
        
        chat_id = query.message.chat_id
        user_id = user_manager.get_user_id(chat_id)
        
        if query.data == 'data_registered':
            await query.edit_message_text(
                text='✅ متشکریم! اطلاعات شما با موفقیت ثبت شد.',
                parse_mode='HTML'
            )
            await Handlers.send_welcome_back_message(chat_id, user_id, context)
    
    @staticmethod
    async def show_user_info(update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: str) -> None:
        """نمایش اطلاعات کاربر"""
        user_data = user_manager.get_user_info(user_id)
        
        if not user_data:
            await update.message.reply_text('❌ اطلاعات کاربر یافت نشد.')
            return
            
        first_name = user_data.get('extra_info', {}).get('firstName', user_data.get('first_name', ''))
        last_name = user_data.get('extra_info', {}).get('lastName', user_data.get('last_name', ''))
        phone = user_data.get('phone', 'ثبت نشده') or 'ثبت نشده'
        smoker = user_data.get('smoker', 'ثبت نشده') or 'ثبت نشده'
        diabetes = user_data.get('diabetes', 'ثبت نشده') or 'ثبت نشده'
        
        # ترجمه به فارسی
        smoker_text = 'بله' if smoker == 'yes' else 'خیر' if smoker == 'no' else 'ثبت نشده'
        diabetes_text = 'بله' if diabetes == 'yes' else 'خیر' if diabetes == 'no' else 'ثبت نشده'
        
        info_text = f'''
<b>📊 اطلاعات پروفایل شما</b>

🆔 <b>شناسه کاربری:</b> <code>{user_data['user_id']}</code>
👤 <b>نام:</b> {first_name} {last_name}
☎️ <b>شماره تماس:</b> {phone}

<b>اطلاعات پزشکی:</b>
🚬 <b>سیگاری:</b> {smoker_text}
🍎 <b>دیابت:</b> {diabetes_text}
        '''
        
        await update.message.reply_html(info_text)
    
    @staticmethod
    async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """هندل کننده خطاها"""
        print(f'❌ Error: {context.error}')
