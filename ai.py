from langgraph.types import Command

from graph import graph
from state import NegotiationState


async def run_graph(state: NegotiationState, user_config, resume=None) -> tuple[str, NegotiationState]:
    """Запуск графа и проверка его состояния после исполнения"""
    new_state: NegotiationState
    if resume:
        new_state = await graph.ainvoke(Command(resume=state['user_message']), config=user_config)
    else:
        new_state = await graph.ainvoke(state, config=user_config)

    if new_state['decision'] == 'accept':
        response = f"🎉 Успех!\nФормат: {new_state['offer_type']}\nЦена: {new_state['current_offer']}"
    elif new_state['decision'] == 'reject':
        response = f"❌ Отказ: {new_state['reason']}"
    else:
        response = new_state['bot_message']

    return response, new_state
