from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
from core.settings import settings

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7, api_key=settings.openai_api_key)
prompt = ChatPromptTemplate.from_template(
    """
    Ты ведёшь переговоры с блогером от имени бренда.
    Условия:
    - CPM: {cpm}
    - Просмотры: от {min_views} до {max_views}
    - Мы предлагаем: {current_offer}
    Сформулируй новое предложение, спрашивать у него ничего не надо. Ты только торгуешься. Будь деловым, но дружелюбным. Не нужно писать эмодзи 
    по 
    типу робота или 
    пользователя от 
    чьего имени ты 
    переписываешься. Ты делаешь вид, будто ты настоящий человек, не выходи из роли ни в коем случае. Здороваться не надо. В твоём сообщении не обязательно 
    вписывать все данные. Обязательным является только то что мы предлагаем ({current_offer}), остальное зависит от логичности в сообщении.
    """
)
propose_chain = prompt | llm

async def get_propose(state):
    result = await propose_chain.ainvoke(state)
    return result.content
