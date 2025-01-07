from flask import Flask, render_template, request
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import sqlite3

# --- Configurations ---
BOT_TOKEN = "7992131826:AAESzqUPUYmXQMPi81rDZlekIRBiQRUuLJA"
ADMIN_USERNAME = "@FRBKX"
TOTAL_BLOCKS = 1000000
TOTAL_SUPPLY = 1000000000
ENERGY_CAP = 8000
INITIAL_ENERGY = 8000

# Flask App
app = Flask(__name__)

# --- Database Setup ---
def init_db():
    conn = sqlite3.connect("tinyhash.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            energy INTEGER DEFAULT ?,
            referrals INTEGER DEFAULT 0
        )
        """,
        (INITIAL_ENERGY,),
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT,
            reward INTEGER
        )
        """
    )
    conn.commit()
    conn.close()

# Add user to the database
def add_user(username):
    conn = sqlite3.connect("tinyhash.db")
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, energy) VALUES (?, ?)", (username, INITIAL_ENERGY)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        pass
    conn.close()

# Update user energy
def update_energy(username, amount):
    conn = sqlite3.connect("tinyhash.db")
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET energy = energy + ? WHERE username = ?", (amount, username)
    )
    conn.commit()
    conn.close()

# Fetch user data
def get_user(username):
    conn = sqlite3.connect("tinyhash.db")
    cursor = conn.cursor()
    cursor.execute("SELECT energy, referrals FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user

# Add task
def add_task(description, reward):
    conn = sqlite3.connect("tinyhash.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tasks (description, reward) VALUES (?, ?)", (description, reward)
    )
    conn.commit()
    conn.close()

# Fetch all tasks
def get_tasks():
    conn = sqlite3.connect("tinyhash.db")
    cursor = conn.cursor()
    cursor.execute("SELECT description, reward FROM tasks")
    tasks = cursor.fetchall()
    conn.close()
    return tasks

# --- Telegram Bot ---
bot = Bot(BOT_TOKEN)

def start(update, context):
    username = update.effective_user.username
    add_user(username)
    update.message.reply_text(
        f"Welcome to Tiny Hash, @{username}!\nYou have {INITIAL_ENERGY} energy to start mining!"
    )

def mine(update, context):
    username = update.effective_user.username
    user = get_user(username)
    if not user:
        update.message.reply_text("You need to register first. Use /start.")
        return

    energy = user[0]
    if energy < 10:
        update.message.reply_text("You don't have enough energy to mine. Complete tasks to refill!")
    else:
        update_energy(username, -10)
        update.message.reply_text(f"Mining successful! 10 energy consumed. Remaining energy: {energy - 10}")

def tasks(update, context):
    username = update.effective_user.username
    user = get_user(username)
    if not user:
        update.message.reply_text("You need to register first. Use /start.")
        return

    tasks = get_tasks()
    if not tasks:
        update.message.reply_text("No tasks available right now.")
        return

    message = "Available Tasks:\n"
    for task in tasks:
        message += f"- {task[0]}: {task[1]} energy\n"
    update.message.reply_text(message)

def add_task_command(update, context):
    if update.effective_user.username != ADMIN_USERNAME:
        update.message.reply_text("You are not authorized to add tasks.")
        return

    try:
        description = context.args[0]
        reward = int(context.args[1])
        add_task(description, reward)
        update.message.reply_text(f"Task '{description}' with reward {reward} energy added.")
    except (IndexError, ValueError):
        update.message.reply_text("Usage: /task <description> <reward>")

# --- Telegram Bot Setup ---
updater = Updater(BOT_TOKEN, use_context=True)
dp = updater.dispatcher

dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("mine", mine))
dp.add_handler(CommandHandler("tasks", tasks))
dp.add_handler(CommandHandler("task", add_task_command))

# --- Flask Route ---
@app.route("/")
def dashboard():
    return render_template("dashboard.html")

# --- Main ---
if __name__ == "__main__":
    init_db()
    updater.start_polling()
    app.run(debug=True)