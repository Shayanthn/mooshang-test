"""
API برای ارتباط وب‌سایت با دیتابیس
Flask REST API - Web Form Handler
"""

from flask import Flask, request, jsonify, send_from_directory
from modules.database import db
from modules.user_manager import user_manager
import logging
import os
from config import LOG_FILE

# تعیین پوشه استاتیک (روت پروژه)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

app = Flask(__name__, static_folder=BASE_DIR, static_url_path='')

# تنظیم لاگ‌گیری پیشرفته
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# CORS Header
@app.after_request
def add_cors_headers(response):
    """اضافه کردن CORS Headers"""
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

@app.route('/')
def index():
    """نمایش صفحه اصلی فرم"""
    return send_from_directory(BASE_DIR, 'index.html')

@app.route('/admin')
def admin_page():
    """نمایش پنل مدیریت"""
    return send_from_directory(BASE_DIR, 'admin.html')

@app.route('/styles.css')
def serve_css():
    """نمایش استایل‌ها"""
    return send_from_directory(BASE_DIR, 'styles.css')

@app.route('/admin.css')
def serve_admin_css():
    """نمایش استایل‌های پنل مدیریت"""
    return send_from_directory(BASE_DIR, 'admin.css')

@app.route('/script.js')
def serve_js():
    """نمایش اسکریپت"""
    return send_from_directory(BASE_DIR, 'script.js')

@app.route('/admin.js')
def serve_admin_js():
    """نمایش اسکریپت‌های پنل مدیریت"""
    return send_from_directory(BASE_DIR, 'admin.js')

@app.route('/api/health', methods=['GET'])
def health_check():
    """بررسی وضعیت سرور"""
    return jsonify({'status': 'ok', 'message': 'API is running'}), 200

# ==========================================
# 📊 ADMIN API ENDPOINTS
# ==========================================

@app.route('/api/admin/users', methods=['GET'])
def get_all_users():
    """دریافت لیست تمام کاربران برای پنل مدیریت"""
    try:
        users = db.get_all_users()
        return jsonify({
            'status': 'success',
            'data': users
        }), 200
    except Exception as e:
        logger.error(f'Error getting users: {e}')
        return jsonify({'status': 'error', 'message': 'خطا در دریافت اطلاعات'}), 500

@app.route('/api/admin/stats', methods=['GET'])
def get_admin_stats():
    """دریافت آمارهای داشبورد مدیریت"""
    try:
        users = db.get_all_users()
        total_users = len(users)
        
        # تعداد فرم‌های تکمیل شده
        completed_forms = sum(1 for u in users.values() if u.get('first_name') or u.get('form_updated_at'))
        
        # تعداد موارد خاص (سیگاری/دیابتی)
        smokers = sum(1 for u in users.values() if str(u.get('smoker')).lower() == 'yes')
        diabetics = sum(1 for u in users.values() if str(u.get('diabetes')).lower() == 'yes')
        
        return jsonify({
            'status': 'success',
            'data': {
                'totalUsers': total_users,
                'completedForms': completed_forms,
                'smokers': smokers,
                'diabetics': diabetics
            }
        }), 200
    except Exception as e:
        logger.error(f'Error getting stats: {e}')
        return jsonify({'status': 'error', 'message': 'خطا در دریافت آمار'}), 500

@app.route('/api/admin/users', methods=['POST'])
def add_user_manually():
    """ثبت دستی بیمار توسط منشی"""
    try:
        data = request.get_json()
        
        # تولید یک آیدی تصادفی برای بیمارانی که تلگرام ندارند
        import uuid
        user_id = 'manual_' + str(uuid.uuid4())[:8]
        
        form_data = {
            'chat_id': None,
            'user_id': user_id,
            'first_name': data.get('firstName'),
            'last_name': data.get('lastName'),
            'phone': data.get('phone'),
            'smoker': data.get('smoker'),
            'diabetes': data.get('diabetes'),
            'created_at': __import__('datetime').datetime.now().isoformat(),
            'is_manual': True
        }
        
        # به دیتابیس لوکال مستقیم وصل میشیم چون متد add_form_data نیازمند ساخت قبلی هست
        # پس با استفاده از lock خودمون هندل میکنیم
        with db.lock:
            db_data = db._load_data()
            db_data[user_id] = form_data
            db._save_data(db_data)
            
        return jsonify({
            'status': 'success',
            'message': 'ثبت دستی با موفقیت انجام شد',
            'user_id': user_id
        }), 200
    except Exception as e:
        logger.error(f'Error manually adding user: {e}')
        return jsonify({'status': 'error', 'message': 'خطا در ثبت کاربر'}), 500

@app.route('/api/admin/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """حذف بیمار از پنل مدیریت"""
    try:
        with db.lock:
            db_data = db._load_data()
            if user_id in db_data:
                del db_data[user_id]
                db._save_data(db_data)
                return jsonify({'status': 'success', 'message': 'کاربر حذف شد'}), 200
            else:
                return jsonify({'status': 'error', 'message': 'کاربر یافت نشد'}), 404
    except Exception as e:
        logger.error(f'Error deleting user: {e}')
        return jsonify({'status': 'error', 'message': 'خطا در حذف کاربر'}), 500

# ==========================================
# 📊 BOT & APP ENDPOINTS
# ==========================================

@app.route('/api/user/<user_id>', methods=['GET'])
def get_user(user_id):
    """دریافت اطلاعات کاربر"""
    user_data = db.get_user_by_id(user_id)
    if not user_data:
        return jsonify({'status': 'error', 'message': 'کاربر یافت نشد'}), 404
    
    return jsonify({
        'status': 'success',
        'user': user_data
    }), 200

@app.route('/api/form/submit', methods=['POST'])
def submit_form():
    """دریافت داده‌های فرم از وب‌سایت"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        
        if not user_id:
            return jsonify({
                'status': 'error',
                'message': 'شناسه کاربری الزامی است'
            }), 400
        
        # بررسی وجود کاربر
        user_data = db.get_user_by_id(user_id)
        if not user_data:
            return jsonify({
                'status': 'error',
                'message': 'کاربر یافت نشد'
            }), 404
        
        # آماده‌کردن داده‌های فرم
        form_data = {
            'first_name': data.get('firstName'),
            'last_name': data.get('lastName'),
            'phone': data.get('phone'),
            'smoker': data.get('smoker'),
            'diabetes': data.get('diabetes'),
            'extra_info': {
                'firstName': data.get('firstName'),
                'lastName': data.get('lastName'),
            }
        }
        
        # ذخیره داده‌ها
        user_manager.save_web_form_data(user_id, form_data)
        
        return jsonify({
            'status': 'success',
            'message': 'اطلاعات با موفقیت ذخیره شد',
            'user_id': user_id
        }), 200
    
    except Exception as e:
        logger.error(f'Error in submit_form: {e}')
        return jsonify({
            'status': 'error',
            'message': 'خطا در پردازش داده‌ها'
        }), 500

@app.route('/api/notify-telegram/<user_id>', methods=['POST'])
def notify_telegram(user_id):
    """اطلاع رسانی به کاربر در تلگرام"""
    try:
        user_data = db.get_user_by_id(user_id)
        if not user_data:
            return jsonify({
                'status': 'error',
                'message': 'کاربر یافت نشد'
            }), 404
        
        # بازگرداندن اطلاعات برای اطلاع رسانی
        return jsonify({
            'status': 'success',
            'message': 'اطلاعات شما دریافت شد',
            'user': user_data
        }), 200
    
    except Exception as e:
        logger.error(f'Error in notify_telegram: {e}')
        return jsonify({
            'status': 'error',
            'message': 'خطا در اطلاع رسانی'
        }), 500

@app.route('/api/validate-user/<user_id>', methods=['GET'])
def validate_user(user_id):
    """تایید وجود کاربر"""
    user_data = db.get_user_by_id(user_id)
    return jsonify({
        'status': 'success',
        'exists': user_data is not None,
        'user': {
            'user_id': user_data['user_id'],
            'name': f"{user_data['first_name']} {user_data['last_name']}"
        } if user_data else None
    }), 200

@app.route('/api/all-users', methods=['GET'])
def get_all_users():
    """دریافت تمام کاربران (فقط برای مدیریت)"""
    users = db.get_all_users()
    return jsonify({
        'status': 'success',
        'total': len(users),
        'users': users
    }), 200

@app.errorhandler(404)
def not_found(e):
    """هندل صفحات یافت نشده"""
    return jsonify({
        'status': 'error',
        'message': 'صفحه یافت نشد'
    }), 404

@app.errorhandler(500)
def internal_error(e):
    """هندل خطاهای داخلی"""
    return jsonify({
        'status': 'error',
        'message': 'خطای داخلی سرور'
    }), 500

if __name__ == '__main__':
    print('''
    ╔════════════════════════════════════════════╗
    ║  🔌  API Server                            ║
    ║  Flask REST API - Form Handler             ║
    ╚════════════════════════════════════════════╝
    ''')
    app.run(debug=True, host='0.0.0.0', port=5000)
