import uuid

from langgraph.checkpoint.memory import MemorySaver
from langgraph.constants import END
from langgraph.graph import StateGraph

from nodes.finalize_node import finalize_node
from nodes.negotiation_node import negotiate_node
from nodes.start_node import start_node
from nodes.desired_rate_node import desired_rate_node
from nodes.user_neg import user_propose_node
from state import NegotiationState

builder = StateGraph(NegotiationState)

# Узлы
builder.add_node("start", start_node)
builder.add_node('desired_rate', desired_rate_node)
builder.add_node("negotiation", negotiate_node)
builder.add_node('user_propose_node', user_propose_node)
builder.add_node("finalize", finalize_node)

# Переходы
builder.set_entry_point("start")
builder.add_edge('start', 'desired_rate')
builder.add_edge('desired_rate', 'negotiation')
builder.add_edge('negotiation', 'user_propose_node')
builder.add_edge('negotiation', 'finalize')

builder.add_conditional_edges(
    "desired_rate",
    lambda state: "negotiation" if state.decision == "negotiation" else "finalize"
)
builder.add_conditional_edges(
    "negotiation",
    lambda state: "finalize" if state.decision == "accept" else "negotiation"
)
builder.add_edge("finalize", END)

config = {

    "thread_id": uuid.uuid4(),

}
checkpointer = MemorySaver()
graph = builder.compile(checkpointer=checkpointer)
