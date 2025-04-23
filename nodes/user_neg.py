from langgraph.types import interrupt

from state import NegotiationState


async def user_propose_node(state: NegotiationState):
    await interrupt(state['bot_message'])
    return state