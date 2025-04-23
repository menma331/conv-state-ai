import uuid

from graph import graph
from state import NegotiationState


async def run_graph(state: NegotiationState) -> tuple[str, NegotiationState]:
    """Запуск графа и проверка его состояния после исполнения"""
    config = {
        "configurable": {
            "thread_id": uuid.uuid4(),
        }
    }
    new_state = await graph.ainvoke(state, config)

    if new_state['decision'] == 'accept':
        response = f"🎉 Успех!\nФормат: {new_state['offer_type'].value}\nЦена: {new_state['current_offer']}"
    elif new_state['decision'] == 'reject':
        response = f"❌ Отказ: {new_state['reason']}"
    else:
        response = new_state['bot_message']

    return response, new_state
