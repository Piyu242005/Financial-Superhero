from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    app_name: str = "Finology"
    secret_key: str = "change-this-secret-key"
    debug: bool = True
    database_url: str = "sqlite+aiosqlite:///./finology.db"
    
    # OpenAI
    openai_api_key: str = ""
    
    # Local LLM (Ollama)
    use_local_llm: bool = False
    ollama_base_url: str = "http://localhost:11434"
    
    # JWT Settings
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
