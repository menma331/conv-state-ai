import asyncio
import logging

from aiogram import Bot, Dispatcher, Router, F
from aiogram.enums import ContentType
from aiogram.filters import CommandStart
from aiogram.types import Message

from ai import run_graph
from core.settings import settings
from state import user_states, NegotiationState

bot = Bot(token=settings.tg_bot_token)
dp = Dispatcher()
router = Router()


@router.message(CommandStart())
async def handle_start(message: Message):
    await message.answer("Пожалуйста, укажи желаемый CPM клиента и количество просмотров блогера (например, '10 5000-10000')")
    user_states[message.from_user.id] = NegotiationState(
        message="",
        history=[],
        offer_type=None,
        final_price=None,
        final_format=None,
        agreed=False,
        rejected=False,
        price_drop_count=0,
        cpm=None,
        min_views=None,
        max_views=None
    )


@router.message(F.content_type == ContentType.TEXT)
async def negotiation_handler(message: Message):
    user_id = message.from_user.id
    text = message.text

    # Если это первый ввод после /start, парсим CPM и просмотры
    if user_id in user_states and user_states[user_id]["cpm"] is None:
        try:
            parts = text.split()
            cpm = float(parts[0])
            views = parts[1]
            if "-" in views:
                min_views, max_views = map(int, views.split("-"))
            else:
                min_views = max_views = int(views)
            user_states[user_id].update({"cpm": cpm, "min_views": min_views, "max_views": max_views})
            await message.answer("Hey, please, provide your desired rate")
            user_states[user_id]["history"].append("🤖: Hey, please, provide your desired rate")
            return
        except (ValueError, IndexError):
            await message.answer("Неверный формат. Укажи CPM и просмотры, например: '10 5000-10000'")
            return

    # Обрабатываем последующие сообщения
    try:
        response = await run_graph(text, user_id)
        await message.answer(response)
    except Exception as e:
        await message.answer("⚠️ Произошла ошибка. Попробуй позже.")
        print(f"[ERROR] {e}")

dp.include_router(router)

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
