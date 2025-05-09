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
builder.add_node('user_input', user_propose_node)
builder.add_node("negotiation", negotiate_node)
builder.add_node("finalize", finalize_node)

# Переходы
builder.set_entry_point("start")
builder.add_edge('start', 'desired_rate')
builder.add_edge('desired_rate', 'user_input')

builder.add_edge("finalize", END)

checkpointer = MemorySaver()
graph = builder.compile(checkpointer=checkpointer)
