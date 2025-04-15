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

# @router.message(CommandStart())
# async def handle_start(message: Message):
#     await message.answer("Пожалуйста, укажи желаемый CPM клиента и количество просмотров блогера (например, '10 5000-10000')")
#     user_states[message.from_user.id] = NegotiationState()
#
#
# @router.message(F.content_type == ContentType.TEXT)
# async def negotiation_handler(message: Message):
#     user_id = message.from_user.id
#     text = message.text
#
#     response = await
#     # Если это первый ввод после /start, парсим CPM и просмотры
#     if user_id in user_states and user_states[user_id].propose_count == 1:
#         try:
#             parts = text.split()
#             cpm = float(parts[0])
#             views = parts[1]
#             if "-" in views:
#                 min_views, max_views = map(int, views.split("-"))
#             else:
#                 min_views = max_views = int(views)
#             user_state = user_states[user_id]
#             user_state.cpm = cpm
#             user_state.min_views = min_views
#             user_state.max_views = max_views
#
#             await message.answer("Hey, please, provide your desired rate")
#             user_states[user_id]["history"].append("🤖: Hey, please, provide your desired rate")
#             return
#         except (ValueError, IndexError):
#             await message.answer("Неверный формат. Укажи CPM и просмотры, например: '100 5000-10000'")
#             return
#
#     # Обрабатываем последующие сообщения
#     try:
#         response = await run_graph(text, user_id)
#         await message.answer(response)
#     except Exception as e:
#         await message.answer("⚠️ Произошла ошибка. Попробуй позже.")
#         print(f"[ERROR] {e}")
#
from aiogram import Bot, Dispatcher, Router, F
from aiogram.enums import ContentType
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from ai import run_graph
from state import NegotiationState, user_states


@router.message(CommandStart())
async def handle_start(message: Message):
    user_states[message.from_user.id] = NegotiationState(
        cpm=0,
        min_views=0,
        max_views=0,
        user_message='',
        bot_message='',
        propose_count=1,
        decision='negotiation',
        history=[],
        current_offer=0,
        finalize_message=None,
        offer_type='fixed',
        reason='',
        awaiting_user_response=False,
        tg_id=message.from_user.id
    )
    await message.answer("Введите CPM и диапазон просмотров (например: '10 5000-10000')")


@router.message(F.content_type == ContentType.TEXT)
async def handle_text(message: Message):
    user_id = message.from_user.id
    user_state = user_states.get(user_id)

    if not user_state:
        await message.answer("Сначала запустите /start")
        return

    # Обновляем состояние
    user_state['user_message'] = message.text

    try:
        # Запускаем граф
        response, new_state = run_graph(user_state)

        # Сохраняем новое состояние
        user_states[user_id] = new_state

        # Отправляем ответ
        await message.answer(response)

        # Очищаем состояние при завершении
        if new_state['decision'] in {"accept", "reject"}:
            del user_states[user_id]

    except Exception as e:
        await message.answer("⚠️ Произошла ошибка. Попробуйте позже.")
        logging.error(f"Error: {str(e)}")
        del user_states[user_id]


dp.include_router(router)


async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
