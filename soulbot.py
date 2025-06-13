import logging
import os
import openai
from telegram import Update, ForceReply
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# تسجيل تفصيلي يظهر في Railway logs
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# مفاتيح البيئة
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_KEY

# تصنيف نوع الرسالة
def get_prompt_type(text: str) -> str:
    text = text.lower()
    if "فضفضة" in text or "أبوح" in text:
        return "أنت رفيق عاطفي يستمع دون أن يحكم. كن حنونًا ومتفهمًا."
    elif "استشارة" in text or "رأيك" in text:
        return "كن تحليليًا وعقلانيًا، اعطِ رأيك كخبير محترم."
    elif "تحفيز" in text or "يأس" in text:
        return "كن مشجعًا وداعمًا كأفضل صديق."
    else:
        return "كن رفيقًا ذكيًا، استمع ورد بلطف دون أحكام."

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info("✅ استقبل أمر /start")
    await update.message.reply_text("مرحبًا بك، أنا Shinjo Soul GPT – رفيقك العاطفي. أرسل لي أي شيء 💜")

# الرد على الرسائل
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_text = update.message.text
    logger.info(f"📥 Received: {user_text}")
    print(f"📥 User message: {user_text}")

    system_prompt = get_prompt_type(user_text)
    logger.info(f"🧠 Prompt type: {system_prompt}")

    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_text}
            ],
            temperature=0.7
        )
        reply = completion.choices[0].message.content
        logger.info(f"📤 GPT reply: {reply}")
        print(f"📤 GPT: {reply}")
        await update.message.reply_text(reply)

    except Exception as e:
        logger.exception("🚨 GPT Error:")
        await update.message.reply_text("⚠️ عذرًا، حدث خلل لحظي. حاول لاحقًا.")

# تشغيل البوت
def main():
    if not TELEGRAM_TOKEN or not OPENAI_KEY:
        raise ValueError("❌ لم يتم العثور على TELEGRAM_BOT_TOKEN أو OPENAI_API_KEY")

    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ ShinjoSoulGPT_V2 is running and ready to receive messages.")
    logger.info("🚀 ShinjoSoulGPT_V2 launched.")
    app.run_polling()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ FATAL ERROR: {e}")
        logger.exception("❌ FATAL ERROR:")
