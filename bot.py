from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# اطلاعات ربات و تنظیمات
BOT_TOKEN = "7992131826:AAESzqUPUYmXQMPi81rDZlekIRBiQRUuLJA"
ADMIN_USERNAME = "@FRBKX"
INITIAL_ENERGY = 8000
ENERGY_CAP = 8000
tasks = [{"task": "Follow Twitter", "reward": 50}, {"task": "Join Telegram Channel", "reward": 30}]
users_data = {}

# دستور /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in users_data:
        users_data[user_id] = {"energy": INITIAL_ENERGY, "tasks_done": [], "referrals": 0}
    await update.message.reply_text(
        f"Welcome to Tiny Hash! You have {INITIAL_ENERGY} energy.\n"
        "Use /dashboard to view your status."
    )

# دستور /dashboard
async def dashboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_data = users_data.get(user_id, {})
    energy = user_data.get("energy", 0)
    referrals = user_data.get("referrals", 0)
    await update.message.reply_text(
        f"Dashboard:\n"
        f"Energy: {energy}/{ENERGY_CAP}\n"
        f"Referrals: {referrals}\n"
        "Complete tasks to earn more energy."
    )

# دستور /tasks
async def tasks_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    task_text = "Available Tasks:\n"
    for idx, task in enumerate(tasks, 1):
        task_text += f"{idx}. {task['task']} - Reward: {task['reward']} energy\n"
    await update.message.reply_text(task_text)

# دستور /referral
async def referral(update: Update, context: ContextTypes.DEFAULT_TYPE):
    referral_link = f"https://t.me/TinyHashBot?start={update.effective_user.id}"
    await update.message.reply_text(
        f"Share this link to invite others:\n{referral_link}\n"
        "Earn rewards for each successful referral!"
    )

# دستور /task (برای ادمین)
async def add_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.username != ADMIN_USERNAME.strip("@"):
        await update.message.reply_text("You are not authorized to add tasks.")
        return

    args = context.args
    if len(args) < 2:
        await update.message.reply_text("Usage: /task <task_name> <reward>")
        return

    task_name = " ".join(args[:-1])
    try:
        reward = int(args[-1])
        tasks.append({"task": task_name, "reward": reward})
        await update.message.reply_text(f"Task '{task_name}' added with reward {reward} energy.")
    except ValueError:
        await update.message.reply_text("Invalid reward. It must be a number.")

# راه‌اندازی اپلیکیشن
def main():
    application = Application.builder().token(BOT_TOKEN).build()

    # افزودن هندلرها
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("dashboard", dashboard))
    application.add_handler(CommandHandler("tasks", tasks_list))
    application.add_handler(CommandHandler("referral", referral))
    application.add_handler(CommandHandler("task", add_task))

    # اجرای ربات
    application.run_polling()

if __name__ == "__main__":
    main()