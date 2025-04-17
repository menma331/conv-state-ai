from graph import graph
from state import NegotiationState

def run_graph(state: NegotiationState) -> tuple[str, NegotiationState]:
    """Запуск графа и проверка его состояния после исполнения"""
    new_state = graph.invoke(state)

    if new_state['decision'] == 'accept':
        response = f"🎉 Успех!\nФормат: {new_state['offer_type'].value}\nЦена: {new_state['current_offer']}"
    elif new_state['decision'] == 'reject':
        response = f"❌ Отказ: {new_state['reason']}"
    else:
        response = new_state['bot_message']

    return response, new_state
