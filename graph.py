from langgraph.graph import StateGraph, END
from state import NegotiationState
from nodes import propose_offer, evaluate_response, finalize

builder = StateGraph(NegotiationState)

builder.set_entry_point("Propose")
builder.add_node("Propose", propose_offer.propose_offer)
builder.add_node("Evaluate", evaluate_response.evaluate_response)
builder.add_node("Finalize", finalize.finalize)

builder.add_edge("Propose", "Evaluate")

# Условные переходы должны возвращать строку
def route_evaluate(state) -> str:
    next_node = state.get("next_node", "Finalize")  # По умолчанию идем в Finalize
    if next_node == "negotiate":
        return "Propose"
    return next_node  # "accept" или "reject" ведут в Finalize

builder.add_conditional_edges("Evaluate", route_evaluate, {
    "accept": "Finalize",
    "reject": "Finalize",
    "negotiate": "Propose",
    "Propose": "Propose",
    "Finalize": "Finalize"
})

builder.add_edge("Finalize", END)

graph = builder.compile()