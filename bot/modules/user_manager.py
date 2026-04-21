from modules.database import db

class UserManager:
    """مدیریت کاربران و شناسه‌های یکتا"""
    
    @staticmethod
    def create_new_user(chat_id, first_name='Unknown', last_name='User'):
        """ایجاد کاربر جدید و دریافت شناسه یکتا"""
        user_id = db.add_user(chat_id, first_name, last_name)
        return user_id
    
    @staticmethod
    def get_user_id(chat_id):
        """دریافت شناسه کاربر توسط Chat ID"""
        user_id, _ = db.get_user_by_chat_id(chat_id)
        return user_id
    
    @staticmethod
    def get_user_info(user_id):
        """دریافت اطلاعات کاربر"""
        return db.get_user_by_id(user_id)
    
    @staticmethod
    def is_user_registered(chat_id):
        """بررسی ثبت‌نام کاربر"""
        return db.user_exists(chat_id)
    
    @staticmethod
    def save_user_info(chat_id, phone=None, smoker=None, diabetes=None):
        """ذخیره اطلاعات کاربر از تلگرام"""
        user_id, _ = db.get_user_by_chat_id(chat_id)
        if user_id:
            update_dict = {}
            if phone:
                update_dict['phone'] = phone
            if smoker is not None:
                update_dict['smoker'] = smoker
            if diabetes is not None:
                update_dict['diabetes'] = diabetes
            
            db.update_user(user_id, **update_dict)
            return user_id
        return None
    
    @staticmethod
    def save_web_form_data(user_id, form_data):
        """ذخیره داده‌های فرم وب‌سایت"""
        return db.add_form_data(user_id, form_data)

user_manager = UserManager()
