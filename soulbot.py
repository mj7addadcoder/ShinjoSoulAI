import logging
import os
import requests
from telegram import Update, ForceReply
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "openrouter/gpt-3.5-turbo"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_html(
        f"مرحباً {user.first_name}! 💜\n\nأنا شينچو سول – النسخة المجانية، جاهز أسمعك وأرد عليك. اكتب لي أي شيء الآن 🕊️",
        reply_markup=ForceReply(selective=True),
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text

    try:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": MODEL,
            "messages": [
                {"role": "system", "content": "كن رفيقًا ذكيًا يستمع بلطف ويدعم المشاعر الإنسانية."},
                {"role": "user", "content": user_message}
            ]
        }
        response = requests.post(OPENROUTER_ENDPOINT, headers=headers, json=payload)
        data = response.json()
        reply = data['choices'][0]['message']['content']
        await update.message.reply_text(reply)

    except Exception as e:
        await update.message.reply_text("⚠️ حدث خطأ أثناء الاتصال بـ OpenRouter. تأكد من التوكن أو حاول لاحقًا.")
        print("❌ ERROR:", e)

def main():
    if not TELEGRAM_TOKEN or not OPENROUTER_API_KEY:
        raise ValueError("❌ تأكد من وجود TELEGRAM_BOT_TOKEN و OPENROUTER_API_KEY في متغيرات البيئة.")
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ FATAL ERROR: {e}")
        logger.exception("❌ FATAL ERROR:")
