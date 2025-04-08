from chains.propose import propose_chain


def propose_offer(state):
    # Рассчитываем предложение (пример)
    cpm = state.get('cpm', 10)  # Значение по умолчанию, если не задано
    min_views = state.get('min_views', 1000)
    max_views = state.get('max_views', 5000)
    current_offer = (cpm * (min_views + max_views) / 2) / 1000  # Пример расчета цены
    state["current_offer"] = current_offer

    state['user_message'] = state['message']
    # Генерируем сообщение с предложением
    response = propose_chain.run(
        {
            "cpm": cpm,
            "min_views": min_views,
            "max_views": max_views,
            "history": "\n".join(state["history"]),
            "current_offer": current_offer
        }
    )
    state["message"] = response
    state["history"].append("Bot: " + response)  # Добавляем сообщение бота в историю
    return state
