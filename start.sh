#!/bin/bash
# رفتن به پوشه ربات
cd bot

# اجرای ربات در بک‌گراند
python main.py &

# اجرای سرور Flask با Gunicorn برای محیط پروداکشن
gunicorn api:app -b 0.0.0.0:$PORT
