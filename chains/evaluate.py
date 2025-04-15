from langchain.chains.llm import LLMChain
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from core.settings import settings

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=settings.openai_api_key)

# prompt = ChatPromptTemplate.from_template(
#     """
# Ты ведёшь переговоры с блогером о цене за рекламу. История переговоров:
# {history}
#
# Последнее сообщение блогера: "{message}"
#
# Определи намерение блогера:
# - accept, если блогер явно согласился на предложенные условия (например, "да", "согласен", "ок").
# - reject, если блогер явно отказался от сотрудничества (например, "нет", "не интересно").
# - negotiate, если блогер предложил другую цену (например, число) или выразил желание продолжить переговоры.
#
# Выбери одну из опций:
#     accept
#     reject
#     negotiate
#
# Ответ:
# """
#     )
prompt = ChatPromptTemplate.from_template(
    """
Ты ведёшь переговоры с блогером о цене за рекламу. История переговоров:
{history}

Последнее сообщение блогера: "{user_message}"

Определи намерение блогера:
- accept, если блогер согласился на предложенные условия (например, "да, давайте 500", "согласен, на ваше предложение", "уговорили, я согласен на 900").
- reject, если блогер явно отказался от сотрудничества (например, "нет, не хочу", "не интересно").
- negotiate, если блогер предложил другую цену (например, число) или выразил желание продолжить переговоры.

Выбери одну из опций:
    accept 
    reject
    negotiate 

Ответ:
"""
    )

evaluate_chain = prompt | llm

def get_decision(state): # изменить на асинхронный вариант окда
    return evaluate_chain.invoke(state.model_dump()).content

