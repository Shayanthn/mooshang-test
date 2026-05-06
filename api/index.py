import os
import json
from flask import Flask, request, jsonify
from openai import OpenAI

app = Flask(__name__)

# تنظیمات مدل‌های رایگان با قابلیت جایگزینی خودکار (Fallback)

# --- Primary AI (Gemini) ---
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
GEMINI_MODEL = "gemini-1.5-flash-latest"

gemini_client = OpenAI(api_key=GEMINI_API_KEY, base_url=GEMINI_BASE_URL)

# --- Fallback AI (OpenRouter) ---
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
OPENROUTER_MODEL = "openai/gpt-oss-20b:free"

openrouter_client = OpenAI(api_key=OPENROUTER_API_KEY, base_url=OPENROUTER_BASE_URL)

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
        try:
            # اول تلاش میکنیم از Gemini جواب بگیریم
            response = gemini_client.chat.completions.create(
                model=GEMINI_MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT.replace("{CLINIC_PROTOCOLS}", CLINIC_PROTOCOLS)},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.3,
                max_tokens=300
            )
            ai_reply = response.choices[0].message.content
        except Exception as gemini_err:
            print(f"Gemini failed: {gemini_err}. Switching to OpenRouter...")
            # اگر Gemini ارور داد یا تحریم بود، خودکار سوییچ میکند روی OpenRouter
            response = openrouter_client.chat.completions.create(
                model=OPENROUTER_MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT.replace("{CLINIC_PROTOCOLS}", CLINIC_PROTOCOLS)},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.3,
                max_tokens=300
            )
            ai_reply = response.choices[0].message.content
            
        return jsonify({"reply": ai_reply})
        
    except Exception as e:
        print(f"AI Error (Both models failed): {e}")
        return jsonify({"reply": "متاسفانه دستیار هوشمند در حال حاضر قطع است، پیام شما به پزشک ارجاع داده شد 🌸"}), 500

if __name__ == '__main__':
    print("🚀 AI Clinic Agent is running on http://localhost:5001")
    app.run(host='0.0.0.0', port=5001)
