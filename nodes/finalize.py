# nodes/finalize.py
from state import NegotiationState

def finalize(state: NegotiationState) -> NegotiationState:
    if state["agreed"]:
        state["Решение"] = "Согласен"
        state["Формат"] = state["offer_type"]
        state["Стоимость"] = state["final_price"]
    elif state["rejected"]:
        state["Решение"] = "Отказ"
        state["Причина"] = "Блогер не согласился на условия"
    return state