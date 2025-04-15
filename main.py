# import asyncio
# import logging
#
# from aiogram import Bot, Dispatcher, Router, F
# from aiogram.enums import ContentType
# from aiogram.filters import CommandStart
# from aiogram.types import Message
#
# from ai import run_graph
# from core.settings import settings
# from state import user_states, NegotiationState
#
# bot = Bot(token=settings.tg_bot_token)
# dp = Dispatcher()
# router = Router()
#
# # @router.message(CommandStart())
# # async def handle_start(message: Message):
# #     await message.answer("Пожалуйста, укажи желаемый CPM клиента и количество просмотров блогера (например, '10 5000-10000')")
# #     user_states[message.from_user.id] = NegotiationState()
# #
# #
# # @router.message(F.content_type == ContentType.TEXT)
# # async def negotiation_handler(message: Message):
# #     user_id = message.from_user.id
# #     text = message.text
# #
# #     response = await
# #     # Если это первый ввод после /start, парсим CPM и просмотры
# #     if user_id in user_states and user_states[user_id].propose_count == 1:
# #         try:
# #             parts = text.split()
# #             cpm = float(parts[0])
# #             views = parts[1]
# #             if "-" in views:
# #                 min_views, max_views = map(int, views.split("-"))
# #             else:
# #                 min_views = max_views = int(views)
# #             user_state = user_states[user_id]
# #             user_state.cpm = cpm
# #             user_state.min_views = min_views
# #             user_state.max_views = max_views
# #
# #             await message.answer("Hey, please, provide your desired rate")
# #             user_states[user_id]["history"].append("🤖: Hey, please, provide your desired rate")
# #             return
# #         except (ValueError, IndexError):
# #             await message.answer("Неверный формат. Укажи CPM и просмотры, например: '100 5000-10000'")
# #             return
# #
# #     # Обрабатываем последующие сообщения
# #     try:
# #         response = await run_graph(text, user_id)
# #         await message.answer(response)
# #     except Exception as e:
# #         await message.answer("⚠️ Произошла ошибка. Попробуй позже.")
# #         print(f"[ERROR] {e}")
# #
# from aiogram import Bot, Dispatcher, Router, F
# from aiogram.enums import ContentType
# from aiogram.filters import CommandStart
# from aiogram.types import Message
# from aiogram.fsm.context import FSMContext
#
# from ai import run_graph
# from state import NegotiationState, user_states
#
#
# @router.message(CommandStart())
# async def handle_start(message: Message):
#     user_states[message.from_user.id] = NegotiationState(
#         cpm=0,
#         min_views=0,
#         max_views=0,
#         user_message='',
#         bot_message='',
#         propose_count=1,
#         decision='negotiation',
#         history=[],
#         current_offer=0,
#         finalize_message=None,
#         offer_type='fixed',
#         reason='',
#         awaiting_user_response=False,
#         tg_id=message.from_user.id
#     )
#     await message.answer("Введите CPM и диапазон просмотров (например: '10 5000-10000')")
#
#
# @router.message(F.content_type == ContentType.TEXT)
# async def handle_text(message: Message):
#     user_id = message.from_user.id
#     user_state = user_states.get(user_id)
#
#     if not user_state:
#         await message.answer("Сначала запустите /start")
#         return
#
#     # Обновляем состояние
#     user_state['user_message'] = message.text
#
#     try:
#         # Запускаем граф
#         response, new_state = run_graph(user_state)
#
#         # Сохраняем новое состояние
#         user_states[user_id] = new_state
#
#         # Отправляем ответ
#         await message.answer(response)
#
#         # Очищаем состояние при завершении
#         if new_state['decision'] in {"accept", "reject"}:
#             del user_states[user_id]
#
#     except Exception as e:
#         await message.answer("⚠️ Произошла ошибка. Попробуйте позже.")
#         logging.error(f"Error: {str(e)}")
#         del user_states[user_id]
#
#
# dp.include_router(router)
#
#
# async def main():
#     logging.basicConfig(level=logging.INFO)
#     await dp.start_polling(bot)
#
#
# if __name__ == "__main__":
#     asyncio.run(main())

import asyncio
import logging

from aiogram import Bot, Dispatcher, Router, F
from aiogram.enums import ContentType
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from ai import run_graph
from core.settings import settings

# FSM States
class NegotiationStates(StatesGroup):
    START = State()
    DESIRED_RATE = State()
    NEGOTIATION = State()
    FINALIZE = State()

bot = Bot(token=settings.tg_bot_token)
dp = Dispatcher()
router = Router()

# Start command handler
@router.message(CommandStart())
async def handle_start(message: Message, state: FSMContext):
    await state.set_state(NegotiationStates.START)
    await state.update_data(
        user_id=message.from_user.id,
        cpm=None,
        min_views=None,
        max_views=None,
        bot_message="",
        user_message="",
        history=[]
    )
    await message.answer("Введите CPM и диапазон просмотров (например: '10 5000-10000')")

# Handler for START state
@router.message(NegotiationStates.START, F.content_type == ContentType.TEXT)
async def handle_start_input(message: Message, state: FSMContext):
    try:
        parts = message.text.split()
        cpm = float(parts[0])
        views = parts[1]

        if "-" in views:
            min_views, max_views = map(int, views.split("-"))
        else:
            min_views = max_views = int(views)

        await state.update_data(cpm=cpm, min_views=min_views, max_views=max_views)
        await state.set_state(NegotiationStates.DESIRED_RATE)
        await message.answer("Hey, please send your desired rate")
    except (ValueError, IndexError):
        await message.answer("Неверный формат. Укажи CPM и просмотры, например: '100 5000-10000'")

# Handler for DESIRED_RATE state
@router.message(NegotiationStates.DESIRED_RATE, F.content_type == ContentType.TEXT)
async def handle_desired_rate(message: Message, state: FSMContext):
    data = await state.get_data()
    user_message = message.text

    # Logic for processing desired rate
    data["user_message"] = user_message
    response, new_state = run_graph(data)

    await state.update_data(**new_state)

    if new_state["decision"] in {"accept", "reject"}:
        await state.clear()
        await message.answer(response)
    else:
        await state.set_state(NegotiationStates.NEGOTIATION)
        await message.answer(response)

# Handler for NEGOTIATION state
@router.message(NegotiationStates.NEGOTIATION, F.content_type == ContentType.TEXT)
async def handle_negotiation(message: Message, state: FSMContext):
    data = await state.get_data()
    user_message = message.text

    # Logic for negotiation
    data["user_message"] = user_message
    response, new_state = run_graph(data)

    await state.update_data(**new_state)

    if new_state["decision"] in {"accept", "reject"}:
        await state.clear()
        await message.answer(response)
    else:
        await message.answer(response)

# Finalize handler
@router.message(NegotiationStates.FINALIZE)
async def handle_finalize(message: Message, state: FSMContext):
    await message.answer("Переговоры завершены.")
    await state.clear()


dp.include_router(router)


async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())