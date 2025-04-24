from langgraph.types import Command

from chains.evaluate import get_decision
from chains.propose import get_propose
from state import NegotiationState, Decision, OfferType


def calculate_increases(base_offer, step):
    if step == 1:
        return base_offer * 1.20
    elif step == 2:
        return base_offer * 1.30
    return base_offer


async def negotiate_node(state: NegotiationState):
    """Узел переговоров. В зависимости от типа офера мы идем на переговоры."""
    # Завершение при превышении попыток
    if state['propose_count'] >= 3:
        state['decision'] = Decision.reject.value
        state['reason'] = "Превышено количество попыток"
        return Command(goto='finalize', update=state)

    state['propose_count'] += 1

    neg_decision = await get_decision(state)
    state['decision'] = neg_decision

    if state['offer_type'] == OfferType.gap.value:
        if neg_decision == 'reject':
            state['reason'] = 'Пользователь отказывается от нашего предложения'
            return Command(goto='finalize', update=state)
        if neg_decision == 'accept':
            return Command(goto='finalize', update=state)
        if neg_decision == 'negotiate':
            state['current_offer'] = state['current_offer'] * 1.3
            return Command(goto='user_input', update=state)

    state['user_message'] = ''
    if neg_decision == 'negotiate':
        # если пользователь в переговорах, увеличиваем предложение и отправляем обратно в узел переговоров
        state['current_offer'] = calculate_increases(state['current_offer'], state['propose_count'])
        bot_propose = await get_propose(state)
        state['bot_message'] = bot_propose
        state['history'].append(f"Bot: {state['bot_message']}")
        return Command(goto='user_input', update=state)

    if neg_decision == 'accept':
        return Command(goto='finalize', update=state)
    if neg_decision == 'reject':
        state['reason'] = 'Пользователь не согласен с условиями. Отказался явно'
        return Command(goto='finalize', update=state)

    return Command(goto='user_input', update=state)
