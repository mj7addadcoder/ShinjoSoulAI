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
    user_text = update.message.text
    system_prompt = get_prompt_type(user_text)

    logger.info(f"📥 Received message: {user_text}")
    logger.info(f"🧠 Using system prompt: {system_prompt}")

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
        logger.info(f"📤 GPT Reply: {reply}")
        await update.message.reply_text(reply)

    except Exception as e:
        error_message = f"🚨 GPT Error: {e}"
        logger.error(error_message)
        await update.message.reply_text("عذرًا… حصل خطأ أثناء توليد الرد من الذكاء الاصطناعي.")
