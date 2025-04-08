from langchain.chains.llm import LLMChain
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.llms.openai import OpenAI
from core.settings import settings
from state import NegotiationState

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=settings.openai_api_key)

prompt = ChatPromptTemplate.from_template(
    """
Ты ведёшь переговоры с блогером о цене за рекламу. История переговоров:
{history}

Последнее сообщение блогера: "{message}"

Определи намерение блогера:
- accept, если блогер явно согласился на предложенные условия (например, "да", "согласен", "ок").
- reject, если блогер явно отказался от сотрудничества (например, "нет", "не интересно").
- negotiate, если блогер предложил другую цену (например, число) или выразил желание продолжить переговоры.

Если блогер назвал число, считай это предложением цены и выбери "negotiate".

Выбери одну из опций:
- accept 
- reject 
- negotiate 

Ответ:
"""
    )

evaluate_chain = LLMChain(llm=llm, prompt=prompt)

