from langgraph.types import interrupt, Command

from state import NegotiationState


async def user_propose_node(state: NegotiationState):
    """Ввод пользователя"""
    user_message = interrupt(state['user_message'])
    state['user_message'] = user_message
    state['history'].append(user_message)
    return Command(goto='negotiation', update=state)