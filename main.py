import asyncio
import logging

from langchain_core.messages import get_buffer_string
from langchain_core.runnables import RunnableConfig

from core.settings import settings

from aiogram import Bot, Dispatcher, Router, F
from aiogram.enums import ContentType
from aiogram.filters import CommandStart
from aiogram.types import Message

from ai import run_graph
from state import NegotiationState, user_states

bot = Bot(token=settings.tg_bot_token)
dp = Dispatcher()
router = Router()


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
        requested_desired_rate=False
    )
    await message.answer("Введите CPM и диапазон просмотров (например: '10 5000-10000')")


@router.message(F.content_type == ContentType.TEXT)
async def handle_text(message: Message):
    """Обработчик сообщений. Запускает граф и даёт ответы"""
    user_id = message.from_user.id
    user_state = user_states.get(user_id)

    if not user_state:
        await message.answer("Сначала запустите /start")
        return

    # Обновляем состояние
    user_state['user_message'] = message.text

    try:
        response, new_state = await run_graph(user_state)

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
