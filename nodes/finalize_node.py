# from langgraph.constants import END
#
# from state import NegotiationState
#
#
# def finalize_node(state: NegotiationState):
#     print(state.finalize_message)
#     return {"next_node": END, 'state': state}

from state import NegotiationState
from langgraph.constants import END


def finalize_node(state: NegotiationState):
    if state.decision == "accept":
        state.finalize_message = f"Сделка заключена! Ставка: {state.current_offer}"
    else:
        state.finalize_message = f"Переговоры провалились. Причина: {state.reason}"

    return {"next_node": END, "state": state}