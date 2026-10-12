import asyncio
import json
import os
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, Update

# Инициализируем бота
TOKEN = os.getenv("BOT_TOKEN", "8807378632:AAHHbPcfAjtjUy1K9ImLb0zEu5mKh6PoC-8")
bot = Bot(token=TOKEN)
dp = Dispatcher()

MY_TEXT = "Great. Now take the parameters from the previous image, multi"

@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(MY_TEXT)

@dp.message(F.text)
async def any_text(message: Message):
    await message.answer(MY_TEXT)

# Точка входа ASGI, которую Vercel гарантированно распознает
async def app(scope, receive, send):
    if scope['type'] != 'http':
        return

    # Обработка POST-запросов от Telegram
    if scope['method'] == 'POST':
        body = b""
        more_body = True
        while more_body:
            message = await receive()
            body += message.get('body', b'')
            more_body = message.get('more_body', False)

        try:
            # Читаем JSON и скармливаем в aiogram
            json_data = json.loads(body.decode('utf-8'))
            update = Update.model_validate(json_data, context={"bot": bot})
            await dp.feed_update(bot, update)
            
            # Отвечаем серверу Telegram, что всё прошло успешно
            await send({
                'type': 'http.response.start',
                'status': 200,
                'headers': [[b'content-type', b'application/json']],
            })
            await send({
                'type': 'http.response.body',
                'body': json.dumps({"status": "ok"}).encode('utf-8'),
            })
        except Exception as e:
            # Ошибка обработки
            await send({
                'type': 'http.response.start',
                'status': 500,
                'headers': [[b'content-type', b'text/plain']],
            })
            await send({
                'type': 'http.response.body',
                'body': f"Error: {e}".encode('utf-8'),
            })
            
    # Ответ для обычного перехода через браузер (GET)
    elif scope['method'] == 'GET':
        await send({
            'type': 'http.response.start',
            'status': 200,
            'headers': [[b'content-type', b'text/plain; charset=utf-8']],
        })
        await send({
            'type': 'http.response.body',
            'body': "Бот-сервер работает отлично!".encode('utf-8'),
        })
