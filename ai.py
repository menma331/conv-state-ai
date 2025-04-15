# from graph import graph
# from state import user_states, NegotiationState
#
#
# async def run_graph(message_text: str, user_id: int):
#     print('Запустили граф')
#     if user_id not in user_states:
#         user_states[user_id] = NegotiationState()
#     else:
#         user_state = user_states[user_id]
#         user_state.user_message = message_text
#         user_state.history.append(f"🧑: {message_text}")
#
#     # Запускаем граф
#     result: NegotiationState = graph.invoke(user_states[user_id])
#
#     # Сохраняем новое состояние (для следующего хода)
#     # user_states[user_id].update(result)
#
#     # Если результат — соглашение или отказ, формируем сообщение для клиента
#
#     # user_states.pop(user_id)  # очищаем после завершения
#
#     if result.decision == 'accept':
#         return f"""
#                 🎉 Переговоры завершены с успехом!
#                 - Решение: Принято
#                 - Формат: {result.offer_type.value}
#                 - Стоимость: {result.current_offer}
#         """.strip()
#
#     if result.decision == 'reject':
#         return f"""
#                 ❌ Переговоры завершены с отказом.
#                 - Решение: {result['decision']}
#                 - Причина: {result['reason']}
#         """.strip()
#
#     # Если переговоры продолжаются — возвращаем сообщение от бота
#     return result.bot_message
import copy

from graph import graph
from state import NegotiationState

def run_graph(state: NegotiationState) -> tuple[str, NegotiationState]:
    """Упрощённая версия без дублирования логики"""
    new_state: NegotiationState = graph.invoke(state)

    if new_state['decision'] == 'accept':
        response = f"🎉 Успех!\nФормат: {new_state['offer_type'].value}\nЦена: {new_state['current_offer']}"
    elif new_state['decision'] == 'reject':
        response = f"❌ Отказ: {new_state['reason']}"
    else:
        response = new_state['bot_message']

    return response, new_state