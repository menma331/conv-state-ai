# from chains.extract_desired_rate import extract_desired_rate
# from ex_without_graph import calculate_rate
# from state import NegotiationState
#
#
# def start_node(state: NegotiationState):
#     """Стартовая нода.
#      1) Запрашивает cpm и ранж по просмотрам пользователя. Вытягивает информацию из сообщения.
#      2) Запрашивает сообщение со ставкой. Мы получаем её с помощью чейна:
#        а) ставка указана. Мы смотрим, укладывается ли она в cpm:
#          а) укладывается. Мы сразу соглашаемся
#          б) не укладывается. Идем на переговоры
#     """
#     # user_input = input('Введите ваш cpm и ранж по просмотрам(10 1000-5000): ')
#     user_input = state.user_message
#     cpm, views_range = user_input.split(' ')
#     cpm = int(cpm)
#     min_views, max_views = map(int, views_range.split('-'))
#     current_offer = 0
#
#     state.min_views = min_views
#     state.max_views = max_views
#     state.cpm = cpm
#     state.current_offer = cpm
#
#     desired_rate = input('Введите вашу ставку: ')
#     state.user_message = desired_rate
#     extracted_rate = extract_desired_rate(state)
#
#     if extracted_rate == 'нет':
#         state.current_offer = calculate_rate(cpm=cpm, min_views=min_views, max_views=max_views)
#         return {'next_node': 'negotiation', 'state': state}
#     extracted_rate = int(extracted_rate)
#
#     if extracted_rate > cpm:
#         state.current_offer = calculate_rate(cpm=cpm, min_views=min_views, max_views=max_views)
#         return {'next_node': 'negotiation', 'state': state}
#
#     if extracted_rate <= cpm:
#         state.current_offer = current_offer
#         return {'next_node': 'finalize', 'state': state}
import copy

from chains.extract_desired_rate import extract_desired_rate
from state import NegotiationState, Decision, user_states


def calculate_rate(cpm: int, min_views, max_views):
    return (cpm * (((min_views + max_views) / 2) + max_views) / 2) / 1000


from state import NegotiationState


def start_node(state: NegotiationState):
    try:
        # Парсим CPM и просмотры
        parts = state['user_message'].split()
        state['cpm'] = float(parts[0])
        views_part = parts[1]

        if "-" in views_part:
            state['min_views'], state['max_views'] = map(int, views_part.split("-"))
        else:
            state['min_views'] = state['max_views'] = int(views_part)

        # Запрашиваем желаемую ставку
        state['bot_message'] = "Hey, please send your desired rate"

        return state

    except Exception as e:
        state['bot_message'] = f"Error: {str(e)}. Please use format: 'CPM min_views-max_views'"
        return {"next_node": "finalize", "state": state}