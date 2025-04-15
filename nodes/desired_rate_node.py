from chains.extract_desired_rate import extract_desired_rate
from state import NegotiationState, Decision


def calculate_rate(cpm: int, min_views, max_views):
    return (cpm * (((min_views + max_views) / 2) + max_views) / 2) / 1000

def desired_rate_node(state: NegotiationState):
    extracted_rate = extract_desired_rate(state)

    if extracted_rate == 'нет' or int(extracted_rate) > state['cpm']:
        state.current_offer = calculate_rate(state['cpm'], state['min_views'], state['max_views'])
        return {"next_node": "negotiation", "state": state}

    extracted_rate = int(extracted_rate)
    cpm = state['cpm']

    if extracted_rate > cpm:
        state.current_offer = calculate_rate(cpm=cpm, min_views=state['min_views'], max_views=state['max_views'])
        return {'next_node': 'negotiation', 'state': state}

    if extracted_rate <= cpm:
        state['decision'] = Decision.accept.value
        state['current_offer'] = extracted_rate
        return {'next_node': 'finalize', 'state': state}

    state['decision'] = Decision.accept.value
    return {"next_node": "finalize", "state": state}