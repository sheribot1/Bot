import os
from flask import Flask, request
from google import genai
import telegram

app = Flask(__name__)

# اطلاعات توکن و دسترسی شما
TELEGRAM_BOT_TOKEN = "9185983238:AAErsGdtwOkcjBMKJ056VGsglmFMfbq6IgY"
ALLOWED_USER_ID = 1338799561  # فقط شما اجازه دسترسی دارید

# کلید جمینای از محیط هاست خوانده می‌شود
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)
bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)


@app.route(f"/{TELEGRAM_BOT_TOKEN}", methods=["POST"])
def webhook():
  json_update = request.get_json(force=True)
  update = telegram.Update.de_json(json_update, bot)

  if update.message and update.message.text:
    user_id = update.message.from_user.id
    chat_id = update.message.chat_id
    user_message = update.message.text

    # امنیت: بررسی اینکه پیام از طرف خودِ شما ارسال شده باشد
    if user_id != ALLOWED_USER_ID:
      bot.send_message(
          chat_id=chat_id,
          text="متأسفم، این ربات اختصاصی است و شما اجازه استفاده از آن را ندارید.",
      )
      return "OK", 200

    try:
      response = client.models.generate_content(
          model="gemini-2.5-flash", contents=user_message
      )
      bot.send_message(chat_id=chat_id, text=response.text)
    except Exception as e:
      bot.send_message(
          chat_id=chat_id, text="متأسفانه در پردازش درخواست خطایی رخ داد."
      )

  return "OK", 200


@app.route("/")
def home():
  return "Bot is alive and running!"


if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host="0.0.0.0", port=port)
