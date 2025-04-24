from langgraph.types import interrupt, Command

from chains.extract_desired_rate import extract_desired_rate
from chains.propose import get_propose
from state import NegotiationState, Decision, OfferType


def calculate_rate_for_gap(cpm, min_views, max_views):
    return (cpm * (((min_views + max_views) / 2) + max_views) / 2) / 1000


async def desired_rate_node(state: NegotiationState):
    """Нода запроса ставки. Формирует первое предложение"""
    user_message = interrupt('Please provide your desired rate')
    state['user_message'] = user_message
    state['history'].append(user_message)
    extracted_rate = await extract_desired_rate(state)

    cpm = state['cpm']

    if extracted_rate == 'нет':
        state['offer_type'] = OfferType.gap.value
        current_offer = calculate_rate_for_gap(state['cpm'], state['min_views'], state['max_views'])
        state['current_offer'] = current_offer

        return Command(goto='user_input', update=state)

    extracted_rate = int(extracted_rate)
    predict_offer = ((cpm * state['min_views']) / 1000)
    state['current_offer'] = predict_offer

    if predict_offer > extracted_rate:
        state['decision'] = 'accept'
        state['current_offer'] = extracted_rate
        return Command(goto='finalize', update=state)

    bot_propose = await get_propose(state)
    state['bot_message'] = bot_propose
    if extracted_rate > predict_offer:
        return Command(goto='user_input', update=state)

    state['decision'] = Decision.accept.value
    return Command(goto='finalize', update=state)
