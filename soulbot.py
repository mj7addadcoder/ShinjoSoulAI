
import os
import json
import requests
from dotenv import load_dotenv

# تحميل المتغيرات من .env
load_dotenv()
INSTANCE_ID = os.getenv("INSTANCE_ID")
TOKEN = os.getenv("TOKEN")
API_URL = f"https://api.ultramsg.com/{INSTANCE_ID}/messages/chat"

# تحميل الردود
with open("responses.json", "r", encoding="utf-8") as f:
    responses = json.load(f)

# دالة الإرسال
def send_message(to, message):
    payload = {
        "to": to,
        "message": message
    }
    headers = {
        "Content-Type": "application/json",
        "token": TOKEN
    }
    response = requests.post(API_URL, json=payload, headers=headers)
    return response.text

# مثال تجربة
if __name__ == "__main__":
    user_input = input("🧠 اكتب مشاعرك أو كلمتك المفتاحية: ").strip()
    message = responses.get(user_input, "أنا هنا معك دائمًا… فقط تحدث إلي ❤️")
    to_number = input("📱 أدخل رقمك بصيغة دولية (مثل +966...): ").strip()
    result = send_message(to_number, message)
    print("📤 تم الإرسال:", result)
