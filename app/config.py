from pydantic_settings import BaseSettings
from functools import lru_cache
from pathlib import Path


class Settings(BaseSettings):
    app_name: str = "Finology"
    secret_key: str = "change-this-secret-key"
    debug: bool = True
    database_url: str = "sqlite+aiosqlite:///./finology.db"
    
    # AI Provider: "openai", "gemini", or "ollama"
    ai_provider: str = "openai"
    
    # OpenAI
    openai_api_key: str = ""
    
    # Google Gemini
    gemini_api_key: str = ""
    
    # Local LLM (Ollama)
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.2:latest"
    
    # JWT Settings
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    class Config:
        env_file = Path(__file__).parent.parent / ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
