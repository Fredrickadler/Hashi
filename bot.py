from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, CallbackContext
import os

# توکن ربات
BOT_TOKEN = "7992131826:AAESzqUPUYmXQMPi81rDZlekIRBiQRUuLJA"

# تنظیمات وب‌سرور Flask
app = Flask(__name__)

# نمونه‌سازی ربات
bot = Bot(token=BOT_TOKEN)

# تنظیم Webhook
WEBHOOK_URL = "https://your-domain.com/your-webhook-path"  # آدرس سرور و مسیر دلخواه را وارد کنید
bot.set_webhook(url=WEBHOOK_URL)

# تنظیم Dispatcher برای مدیریت دستورات
dispatcher = Dispatcher(bot, None, workers=4)

# تعریف دستورات ربات
def start(update: Update, context: CallbackContext):
    update.message.reply_text("سلام! به ربات TinyHash خوش آمدید.")

def task(update: Update, context: CallbackContext):
    if update.message.from_user.username == "FRBKX":  # فقط ادمین اجازه اضافه کردن تسک را دارد
        update.message.reply_text("تسک با موفقیت اضافه شد.")
    else:
        update.message.reply_text("شما اجازه استفاده از این دستور را ندارید.")

# ثبت دستورات در Dispatcher
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("task", task))

# پردازش پیام‌های Webhook
@app.route(f"/your-webhook-path", methods=["POST"])
def webhook():
    if request.method == "POST":
        update = Update.de_json(request.get_json(force=True), bot)
        dispatcher.process_update(update)
        return "OK", 200

# اجرای برنامه
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))