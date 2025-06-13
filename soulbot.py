import logging
import os
import openai
from telegram import Update, ForceReply
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# إعداد السجل
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# جلب المفاتيح من البيئة
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_KEY

# تصنيف البرومبت
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

# أمر البدء
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    welcome_text = f"مرحباً {user.first_name}! 💜\n\nأنا شينچو سول – GPT، رفيقك الذكي والداعم النفسي. فضفضلي، استشرني، أو فقط اطلب كلمة تحفيزية… وسأكون هنا لأجلك.\n\nاكتب لي أي شيء الآن 💌"
    await update.message.reply_html(welcome_text, reply_markup=ForceReply(selective=True))

# الردود التفاعلية
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        user_text = update.message.text
        logger.info(f"📥 Received message: {user_text}")
        system_prompt = get_prompt_type(user_text)

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_text}
            ],
            temperature=0.85
        )
        reply = completion.choices[0].message.content
        logger.info(f"📤 GPT reply: {reply}")
        await update.message.reply_text(reply)
    except Exception as e:
        logger.exception("🚨 Unhandled error in handle_message:")
        await update.message.reply_text("🚧 عذرًا، حصل خلل أثناء الرد. حاول مجددًا بعد قليل.")

# التشغيل
def main() -> None:
    if not TELEGRAM_TOKEN or not OPENAI_KEY:
        raise ValueError("❌ تأكد من وجود TELEGRAM_BOT_TOKEN و OPENAI_API_KEY في متغيرات البيئة.")

    application = Application.builder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Shinjo Soul Bot is running and listening for messages...")
    application.run_polling()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"🚨 Fatal error: {e}")
