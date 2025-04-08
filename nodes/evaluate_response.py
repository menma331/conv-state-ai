from chains.evaluate import evaluate_chain


def evaluate_response(state):
    response = evaluate_chain.invoke({"message": state["user_message"], "history": "\n".join(state["history"])})
    decision = response["text"].strip()

    if decision == "accept":
        state["agreed"] = True
        state["final_price"] = state.get("current_offer")  # Используем последнее предложение
        state["offer_type"] = "fixed"  # По умолчанию, можно добавить выбор формата
    elif decision == "reject":
        state["rejected"] = True
    # "negotiate" оставляет состояние как есть для следующего предложения

    return {"next_node": decision, "state": state}
