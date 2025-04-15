from enum import Enum
# from chains.evaluate import get_decision
# from chains.propose import get_propose
# from state import NegotiationState
#

# def calculate_increases(base_offer, step):
#     if step == 1:
#         return base_offer * 1.20  # +20%
#     elif step == 2:
#         return base_offer * 1.30  # Итого +30% от исходной
#     return base_offer
#
# def negotiate_node(state: NegotiationState) -> dict:
#     """Один шаг переговоров."""
#     # if state.propose_count >= 3:
#     #     state.decision = Decision.reject.value
#     #     state.reason = "Долго торгуется."
#     #     return {"next_node": "finalize", "state": state}
#     #
#     # # Расчёт нового предложения
#     # state.current_offer = calculate_increases(state.cpm, state.propose_count)
#     #
#     # user_message = state.user_message # Добавить получение сообщения из чата
#     # state.history.append(f"👨: {user_message}")
#     #
#     # state.decision = get_decision(state) # получаем решение пользователя
#     #
#     # if state.decision == Decision.accept.value or state.decision == Decision.reject: # проверяем, согласен ли он
#     #     if state.decision == Decision.reject:
#     #         state.reason = "Не смогли сторговаться"
#     #     return {"next_node": "finalize", "state": state}
#     #
#     # propose_text = get_propose(state)
#     #
#     # # Обновляем историю
#     # state.bot_message = propose_text
#     # state.history.append(f"🤖: {propose_text}")
#     #
#     # # Проверяем решение пользователя
#     # state.decision = get_decision(state)
#     # state.propose_count += 1
#     #
#     # return {"next_node": "negotiation", "state": state}  # Продолжаем торги
#
#     if state.propose_count >= 3:
#         state.decision = Decision.reject.value
#         state.reason = "Долго торгуется."
#         return {"next_node": "finalize", "state": state}
#
#     if not state.awaiting_user_response:
#         # Этап 1: Бот отправляет предложение
#         state.current_offer = calculate_increases(state.cpm, state.propose_count)
#         propose_text = get_propose(state)
#         state.history.append(f"🤖: {propose_text}")
#         state.awaiting_user_response = True  # <--- Ключевой флаг
#         state.bot_message = propose_text
#         state.propose_count += 1
#         return {"next_node": "negotiation", "state": state}
#
#     else:
#         # Этап 2: Обработка ответа пользователя
#         state.history.append(f"👤: {state.user_message}")
#         state.decision = get_decision(state)
#         state.awaiting_user_response = False  # <--- Сбрасываем флаг
#
#         if state.decision in {Decision.accept.value, Decision.reject.value}:
#             return {"next_node": "finalize", "state": state}
#
#         return {"next_node": "negotiation", "state": state}

from chains.evaluate import get_decision
from chains.propose import get_propose
from state import NegotiationState, Decision


def calculate_increases(base_offer, step):
    if step == 1:
        return base_offer * 1.20
    elif step == 2:
        return base_offer * 1.30
    return base_offer


def negotiate_node(state: NegotiationState) -> dict:
    # Завершение при превышении попыток
    if state['propose_count'] >= 3:
        state['decision'] = Decision.reject.value
        state['reason'] = "Превышено количество попыток"
        return {"next_node": "finalize", "state": state}

    if not state['awaiting_user_response']:
        # Этап 1: Бот генерирует предложение
        state['current_offer'] = calculate_increases(state['cpm'], state['propose_count'])
        state['bot_message'] = get_propose(state)
        state['history'].append(f"🤖: {state['bot_message']}")
        state['awaiting_user_response'] = True
        state['propose_count'] += 1
        return {"next_node": "negotiation", "state": state}

    else:
        # Этап 2: Обработка ответа пользователя
        state['history'].append(f"👤: {state['user_message']}")
        state['decision'] = get_decision(state).value
        state['awaiting_user_response'] = False

        if state['decision'] != "negotiation":
            return {"next_node": "finalize", "state": state}

        return {"next_node": "negotiation", "state": state}