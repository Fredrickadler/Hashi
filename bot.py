
from aiogram import Bot, Dispatcher, executor, types

TOKEN = "7992131826:AAESzqUPUYmXQMPi81rDZlekIRBiQRUuLJA"
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

ADMIN_USERNAME = "@FRBKX"
ENERGY_CAP = 8000
users = {}

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    user_id = message.from_user.id
    if user_id not in users:
        users[user_id] = {"energy": ENERGY_CAP, "referrals": 0}
    await message.reply(f"Welcome to Tiny Hash!\nYour current energy: {users[user_id]['energy']}")

@dp.message_handler(commands=["task"])
async def add_task(message: types.Message):
    if message.from_user.username == ADMIN_USERNAME.strip("@"):
        await message.reply("Send the task details in this format:\nTitle: [Task Title]\nDescription: [Details]\nReward: [Energy Amount]\nLink: [URL]")
    else:
        await message.reply("You are not authorized to use this command.")

@dp.message_handler(lambda message: message.text and message.text.startswith("Title:"))
async def save_task(message: types.Message):
    if message.from_user.username == ADMIN_USERNAME.strip("@"):
        # Placeholder for saving tasks
        await message.reply("Task saved successfully!")
    else:
        await message.reply("You are not authorized to add tasks.")

@dp.message_handler(commands=["energy"])
async def check_energy(message: types.Message):
    user_id = message.from_user.id
    energy = users.get(user_id, {}).get("energy", 0)
    await message.reply(f"Your current energy: {energy}")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
