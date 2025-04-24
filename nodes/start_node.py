from state import NegotiationState

async def start_node(state: NegotiationState):
    """Стартовая нода. Парсит ставку и просмотры и далее определяем формат работы:
        - С гэпом
        - Фиксированная"""
    try:
        # Парсим CPM и просмотры
        state['history'].append(state['user_message'])
        parts = state['user_message'].split()
        state['cpm'] = float(parts[0])
        views_part = parts[1]

        if "-" in views_part:
            state['min_views'], state['max_views'] = map(int, views_part.split("-"))
        else:
            state['min_views'] = state['max_views'] = int(views_part)

        # Запрашиваем желаемую ставку
        bot_message = "Введите желаемую ставку"
        state['bot_message'] = bot_message
        state['history'].append('Bot: ' +bot_message)

        return state

    except Exception as e:
        state['bot_message'] = f"Error: {str(e)}. Please use format: 'CPM min_views-max_views'"
        return {"next_node": "finalize", "state": state}