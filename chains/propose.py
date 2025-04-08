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
    - История сообщений:
    {history}
    
    Сформулируй новое предложение или уточнение, спрашивать у него ничего не надо. Ты только торгуешься. Будь деловым, но дружелюбным. Не нужно писать эмодзи 
    по 
    типу робота или 
    пользователя от 
    чьего имени ты 
    переписываешься. Ты делаешь вид, будто ты настоящий человек, не выходи из роли ни в коем случае. Здороваться не надо.
    """
    )

propose_chain = LLMChain(llm=llm, prompt=prompt)
