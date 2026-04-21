import json
import uuid
from pathlib import Path
from datetime import datetime
from config import DATABASE_FILE
from filelock import FileLock

class Database:
    """پایگاه داده JSON برای مدیریت کاربران"""
    
    def __init__(self):
        self.db_file = DATABASE_FILE
        self.lock_file = self.db_file.with_suffix('.json.lock')
        self.lock = FileLock(self.lock_file)
        self._ensure_db_exists()
    
    def _ensure_db_exists(self):
        """اطمینان از وجود فایل دیتابیس"""
        with self.lock:
            if not self.db_file.exists():
                self._save_data({})
                print(f'✅ Database created at {self.db_file}')
    
    def _load_data(self):
        """بارگذاری داده‌ها از فایل"""
        try:
            with open(self.db_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
        except FileNotFoundError:
            return {}
    
    def _save_data(self, data):
        """ذخیره داده‌ها به فایل - فقط در Context Manager."""
        with open(self.db_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
    def add_user(self, chat_id, first_name, last_name):
        """اضافه کردن کاربر جدید"""
        user_id = str(uuid.uuid4())[:8]  # شناسه یکتای 8 کاراکتری
        with self.lock:
            data = self._load_data()
            
            data[user_id] = {
                'chat_id': chat_id,
                'user_id': user_id,
                'first_name': first_name,
                'last_name': last_name,
                'created_at': datetime.now().isoformat(),
                'phone': None,
                'smoker': None,
                'diabetes': None,
                'extra_info': {}
            }
            
            self._save_data(data)
        print(f'✅ User added: {user_id} (Chat ID: {chat_id})')
        return user_id
    
    def get_user_by_chat_id(self, chat_id):
        """پیدا کردن کاربر توسط Chat ID"""
        with self.lock:
            data = self._load_data()
        for user_id, user_data in data.items():
            if user_data['chat_id'] == chat_id:
                return user_id, user_data
        return None, None
    
    def get_user_by_id(self, user_id):
        with self.lock:
            data = self._load_data()
        return data.get(user_id)
    
    def update_user(self, user_id, **kwargs):
        """به‌روزرسانی اطلاعات کاربر"""
        with self.lock:
            data = self._load_data()
            if user_id in data:
                data[user_id].update(kwargs)
                data[user_id]['updated_at'] = datetime.now().isoformat()
                self._save_data(data)
                print(f'✅ User updated: {user_id}')
                return True
        return False
    
    def add_form_data(self, user_id, form_data):
        """افزودن داده‌های فرم وب‌سایت"""
        with self.lock:
            data = self._load_data()
            if user_id in data:
                data[user_id].update(form_data)
                data[user_id]['form_updated_at'] = datetime.now().isoformat()
                self._save_data(data)
                print(f'✅ Form data added for user: {user_id}')
                return True
        return False
    
    def get_all_users(self):
        """دریافت تمام کاربران"""
        with self.lock:
            return self._load_data()
    
    def user_exists(self, chat_id):
        """بررسی وجود کاربر"""
        _, user_data = self.get_user_by_chat_id(chat_id)
        return user_data is not None

# ایجاد instance
db = Database()
