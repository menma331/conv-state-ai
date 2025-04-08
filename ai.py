from graph import graph
from state import user_states


async def run_graph(message_text: str, user_id: int):
    print('Запустили граф')
    if user_id not in user_states:
        user_states[user_id] = {
            "message": message_text,
            "history": [f"🧑: {message_text}"],
            "offer_type": None,
            "final_price": None,
            "final_format": None,
            "agreed": False,
            "rejected": False,
            "price_drop_count": 0  # Изначально 0 предложений о снижении цены
        }
    else:
        user_states[user_id]["message"] = message_text
        user_states[user_id]["history"].append(f"🧑: {message_text}")

    # Запускаем граф
    result = graph.invoke(user_states[user_id])

    # Сохраняем новое состояние (для следующего хода)
    user_states[user_id].update(result)

    # Если результат — соглашение или отказ, формируем сообщение для клиента
    if result.get("Решение"):
        user_states.pop(user_id)  # очищаем после завершения

        if result["Решение"] == "Согласен":
            return f"""
🎉 Переговоры завершены с успехом!
- Решение: {result['Решение']}
- Формат: {result['Формат']}
- Стоимость: {result['Стоимость']}
            """.strip()

        if result["Решение"] == "Отказ":
            return f"""
❌ Переговоры завершены с отказом.
- Решение: {result['Решение']}
- Причина: {result['Причина']}
            """.strip()

    # Если переговоры продолжаются — возвращаем сообщение от бота
    return result.get("message", "🤖 Нет ответа")
