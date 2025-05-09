from langchain.chains.llm import LLMChain
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from core.settings import settings


llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=settings.openai_api_key)

prompt = ChatPromptTemplate.from_template(
    """
Ты будешь извлекать из сообщения пользователя желаемую ставку за рекламу на его ютуб канале (desired_rate)
Ты будешь возвращать только желаемую ставку, если в сообщении её нет, возвращаешь "нет". В ответе только извлеченная ставка
Примеры: 
[Пример 1]
Сообщение пользователя:Привет. Я хотел бы 1500 рублей в качестве оплаты. 
Ответ от тебя: 1500
[Пример 2]
Сообщение пользователя: 3900 
Ответ от тебя: 3900

Извлеки из этого сообщения "{user_message}"

Ответ: 
"""
    )

extract_desired_rate_chain = prompt | llm

async def extract_desired_rate(state):
    result = await extract_desired_rate_chain.ainvoke(state)
    return result.content
