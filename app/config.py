from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    # LLM 제공자
    llm_provider: str = "openai"

    # 모델명 (환경변수로 재정의 가능)
    openai_model: str = "gpt-4.1-mini"
    gemini_model: str = "gemini-3-flash-preview"
    claude_model: str = "claude-haiku-4-5-20251001"

    # API 키
    openai_api_key: str = ""
    gemini_api_key: str = ""
    anthropic_api_key: str = ""

    # LLM 공통 설정
    llm_timeout_seconds: float = 5.0
    llm_max_tokens: int = 600
    llm_temperature: float = 0.7

    # DB 설정
    db_user: str = "moodping"
    db_password: str = "moodping123"
    db_host: str = "localhost"
    db_port: int = 3306
    db_name: str = "moodping"

    @property
    def database_url(self) -> str:
        return (
            f"mysql+mysqlconnector://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
            f"?charset=utf8mb4"
        )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
