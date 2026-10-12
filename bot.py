import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, Update


TOKEN = os.getenv("BOT_TOKEN", "8461181717:AAH3zf9IBJS04kiXDPi6ocO1f9A5f8AbK7k")
bot = Bot(token=TOKEN)
dp = Dispatcher()

MY_TEXT = "Great. Now take the parameters from the previous image, multi"

@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(MY_TEXT)

@dp.message(F.text)
async def any_text(message: Message):
    await message.answer(MY_TEXT)


async def handler(request):
    if request.method == "POST":
        try:
            # Читаем JSON от серверов Telegram
            json_data = await request.json()
            update = Update.model_validate(json_data, context={"bot": bot})
            await dp.feed_update(bot, update)
            return {"status": "ok"}
        except Exception as e:
            print(f"Error: {e}")
            return {"status": "error"}, 500
    return {"status": "Method Not Allowed"}, 405