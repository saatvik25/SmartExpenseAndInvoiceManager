from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Smart Expense & Invoice Manager"
    DATABASE_URL: str = "sqlite:///./expenses.db"

    model_config = SettingsConfigDict(case_sensitive=True)

settings = Settings()
