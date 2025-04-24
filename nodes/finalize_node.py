from langgraph.types import Command

from state import NegotiationState
from langgraph.constants import END


def finalize_node(state: NegotiationState):
    """Финальный узел. Формирует сообщение для пользователя и заканчивает работу графа."""
    if state['decision'] == "accept":
        state['finalize_message'] = f"Сделка заключена! Ставка:\n {state['current_offer']}\nФормат: {state['offer_type']}"
    else:
        state['finalize_message'] = f"Переговоры провалились. Причина: {state['reason']}"

    return Command(goto=END, update=state)