from state import NegotiationState

async def start_node(state: NegotiationState):
    """Стартовая нода. Парсит cpm и просмотры"""
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
        state['bot_message'] = "Please send your desired rate"

        return state

    except Exception as e:
        state['bot_message'] = f"Error: {str(e)}. Please use format: 'CPM min_views-max_views'"
        return {"next_node": "finalize", "state": state}