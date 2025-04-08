from aiogram import Router, F
from aiogram.enums import ContentType
from aiogram.types import Message
from aiogram.filters import CommandStart
from ai import run_graph
start_router = Router(name="Start router")


@start_router.message(CommandStart())
async def handle_start(message: Message):
    await message.answer("Hey, please, provide your desired rate")


@start_router.message(F.content_type == ContentType.TEXT)
async def negotiation_handler(message: Message):
    user_id = message.from_user.id
    text = message.text

    try:
        response = await run_graph(text, user_id=user_id)
        await message.answer(response)
    except Exception as e:
        await message.answer("⚠️ Произошла ошибка. Попробуй позже.")
        print(f"[ERROR] {e}")
