from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    openai_api_key: str = Field(alias="OPENAI_API_KEY")
    tg_bot_token: str = Field(alias="TG_BOT_TOKEN")


settings = Settings()
