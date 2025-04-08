from chains.propose import propose_chain

def negotiate_fixed(state):
    # Проверяем, сколько раз цена была снижена
    if state["price_drop_count"] >= 2:
        state["message"] = "Мы не можем снизить цену дальше. Переговоры завершены."
        state["rejected"] = True
        return state

    # Иначе продолжаем торговаться
    counter_price = state.get('final_price') * 1.2  # например, на 20% больше
    message_to_user = propose_chain(state)
    state["message"] = message_to_user
    state["final_price"] = round(counter_price, 2)

    # Увеличиваем счетчик предложений о снижении
    state["price_drop_count"] += 1

    return state
