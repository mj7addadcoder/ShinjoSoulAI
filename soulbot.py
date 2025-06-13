import os
import logging
import requests
from telegram import Update, ForceReply
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# === إعدادات عامة ===
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "ضع_التوكن_هنا")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "ضع_مفتاح_openrouter_هنا")

# إعداد السجلات
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# دالة الاتصال بـ OpenRouter
def chat_with_openrouter(api_key, messages, model="openrouter/gpt-3.5-turbo"):
    endpoint = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "messages": messages
    }

    try:
        response = requests.post(endpoint, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        return data['choices'][0]['message']['content']
    except Exception as e:
        logger.error(f"⚠️ خطأ OpenRouter: {e}")
        return "حدث خلل في الاتصال بالخدمة… حاول مرة أخرى لاحقًا."

# دالة تحليل نوع الرسالة وتحديد البرومبت المناسب
def get_prompt_type(text: str) -> str:
    text = text.lower()
    if any(word in text for word in ["فضفضة", "أبوح", "تعبان", "قلق", "وحداني", "ضيق"]):
        return "أنت رفيق عاطفي يستمع باهتمام دون حكم. كن حنونًا، داعمًا، ومستوعبًا للمشاعر."
    elif any(word in text for word in ["استشارة", "رأيك", "مشورة", "أشير", "هل أبدأ", "تنصحني"]):
        return "أنت مستشار حكيم تحلل الموقف بهدوء ووضوح، وتركز على تقديم نصيحة عقلانية."
    elif any(word in text for word in ["تحفيز", "يأس", "فشل", "أحبط", "فقدت الأمل"]):
        return "كن صديقًا مشجعًا يلهم الأمل، ويذكره بقيمته وقوته."
    else:
        return "كن مساعدًا ذكيًا رقيقًا، يتحدث بلغة إنسانية حنونة دون إصدار أحكام."

# أمر /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    welcome_text = f"مرحباً {user.first_name}! 👋\n\nأنا شينچو سول – مساعدك الذكي والداعم النفسي.\n\nاكتب لي ما تشعر به وسأكون هنا لأجلك دائمًا 💜"
    await update.message.reply_html(welcome_text, reply_markup=ForceReply(selective=True))

# استقبال الرسائل والرد عليها
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_text = update.message.text
    prompt = get_prompt_type(user_text)

    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": user_text}
    ]

    reply = chat_with_openrouter(OPENROUTER_API_KEY, messages)
    await update.message.reply_text(reply)

# تشغيل البوت
def main() -> None:
    if TELEGRAM_BOT_TOKEN.startswith("ضع_") or OPENROUTER_API_KEY.startswith("ضع_"):
        raise ValueError("❌ تأكد من تعيين متغيرات البيئة TELEGRAM_BOT_TOKEN و OPENROUTER_API_KEY")

    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.run_polling()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ FATAL ERROR: {e}")
        logger.exception("❌ FATAL ERROR:")
