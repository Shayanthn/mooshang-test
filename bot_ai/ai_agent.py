import os
import json
from flask import Flask, request, jsonify
from openai import OpenAI

app = Flask(__name__)

# شما می‌توانید کلید API خود را اینجا وارد کنید یا در فایل .env بگذارید
# اگر از سایت‌های ایرانی (روبین، جی‌پی‌تی-ای‌پی‌آی و...) که تحریم نیستند استفاده می‌کنید، Bsae URL را تغییر دهید.
API_KEY = os.environ.get("OPENAI_API_KEY", "your-openai-api-key-here")
BASE_URL = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1") 

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

# خواندن پروتکل‌های کلینیک (پایگاه دانش - RAG Context)
def load_knowledge_base():
    kb_path = os.path.join(os.path.dirname(__file__), "clinic_knowledge_base.txt")
    if os.path.exists(kb_path):
        with open(kb_path, "r", encoding="utf-8") as f:
            return f.read()
    return "پایگاه دانش کلینیک خالی است."

CLINIC_PROTOCOLS = load_knowledge_base()

SYSTEM_PROMPT = f"""
شما دستیار هوشمند و دلسوز «کلینیک پزشکی/زیبایی» هستید. وظیفه شما پاسخگویی سریع، علمی و آرام‌بخش به بیماران است که ممکن است دچار استرس قبل یا بعد از عمل باشند.

پروتکل‌های پزشکی و دستورالعمل‌های کلینیک ما در زیر آمده است:
------------------
{{CLINIC_PROTOCOLS}}
------------------

قوانین پاسخگویی شما:
۱. فقط بر اساس پروتکل بالا جواب بدهید، اطلاعات پزشکی از خودتان اضافه نکنید.
۲. با لحنی کاملاً مهربان، محترمانه و آرام‌بخش پاسخ دهید.
۳. در صورتی که بیمار علائم خطرناکی (مثل خونریزی شدید، تب بالا، عفونت وسیع، درد غیرقابل تحمل) داشت، علاوه بر راهنمایی، حتماً به او بگویید: "نگران نباشید، این مورد به پزشک ارجاع داده شد و با شما تماس می‌گیریم."
۴. اگر سوال بیمار در پروتکل‌ها وجود نداشت، معذرت‌خواهی کنید و بگویید سوال به پشتیبان انسانی ارجاع داده شد.
۵. پاسخ باید کوتاه (حداکثر ۳-۴ خط) و خوانا و با ایموجی‌های مناسب باشد.
"""

@app.route('/ask-ai', methods=['POST'])
def ask_ai():
    data = request.json
    user_message = data.get("message", "")
    user_id = data.get("user_id", "unknown")

    if not user_message:
        return jsonify({"reply": "متامی دریافت نشد."}), 400

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini", # مدل پیشنهادی برای سرعت و قیمت مناسب
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT.replace("{CLINIC_PROTOCOLS}", CLINIC_PROTOCOLS)},
                {"role": "user", "content": user_message}
            ],
            temperature=0.3, # برای اینکه دقت علمی حفظ شود و هذیان نگوید
            max_tokens=300
        )
        
        ai_reply = response.choices[0].message.content
        return jsonify({"reply": ai_reply})
        
    except Exception as e:
        print(f"AI Error: {e}")
        return jsonify({"reply": "متاسفانه دستیار هوشمند در حال حاضر قطع است، پیام شما به پزشک ارجاع داده شد 🌸"}), 500

if __name__ == '__main__':
    print("🚀 AI Clinic Agent is running on http://localhost:5001")
    app.run(host='0.0.0.0', port=5001)
