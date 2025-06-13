import logging
import os
import openai
from telegram import Update, ForceReply
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# تفعيل سجل التشغيل
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# إعداد مفاتيح API
TELEGRAM_TOKEN = os.getenv("8091089486:AAFVTzoOkTHBh9vUKHraUQ9LCOF9il799Ok")
OPENAI_KEY = os.getenv("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")
openai.api_key = OPENAI_KEY

# موجهات (Prompts) مخصصة حسب نوع الرسالة
def get_prompt_type(text: str) -> str:
    text = text.lower()
    if "فضفضة" in text or "أبوح" in text or "تعبان" in text:
        return "أنت رفيق عاطفي يستمع دون أن يحكم. كن حنونًا، اصغِ جيدًا، ولا تعطي حلولًا مباشرة."
    elif "استشارة" in text or "رأيك" in text or "مشورة" in text:
        return "كن عقلانيًا وتحليليًا، اجعل ردك مرتبًا وواضحًا كخبير."
    elif "تحفيز" in text or "حفزني" in text or "يأس" in text:
        return "كن داعمًا ومشجعًا كصديق وفي يشعل الأمل."
    else:
        return "كن رفيقًا ذكيًا، استمع ورد بلطف دون أحكام."

# أمر /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    welcome_text = f"مرحباً {user.first_name}! 💜\n\nأنا شينچو سول – GPT، رفيقك الذكي والداعم النفسي. فضفضلي، استشرني، أو فقط اطلب كلمة تحفيزية… وسأكون هنا لأجلك.\n\nاكتب لي أي شيء الآن 💌"
    await update.message.reply_html(welcome_text, reply_markup=ForceReply(selective=True))

# الرد على الرسائل
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_text = update.message.text
    system_prompt = get_prompt_type(user_text)

    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_text}
            ],
            temperature=0.85
        )
        reply = completion.choices[0].message.content
        await update.message.reply_text(reply)

    except Exception as e:
        await update.message.reply_text("عذرًا… حدث خلل مؤقت في الاتصال بالذكاء الاصطناعي. حاول مرة أخرى لاحقًا.")
        logger.error(f"خطأ في GPT: {e}")

# تشغيل البوت
def main() -> None:
    if not TELEGRAM_TOKEN or not OPENAI_KEY:
        raise ValueError("❌ تأكد من وجود TELEGRAM_BOT_TOKEN و OPENAI_API_KEY في متغيرات البيئة.")
    
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.run_polling()

if __name__ == "__main__":
    main()

    user_input = input("🧠 اكتب مشاعرك أو كلمتك المفتاحية: ").strip()
    message = responses.get(user_input, "أنا هنا معك دائمًا… فقط تحدث إلي ❤️")
    to_number = input("📱 أدخل رقمك بصيغة دولية (مثل +966...): ").strip()
    result = send_message(to_number, message)
    print("📤 تم الإرسال:", result)
