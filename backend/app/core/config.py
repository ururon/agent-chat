"""
應用程式設定管理

使用 Pydantic Settings 從環境變數載入設定
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """應用程式設定"""

    # Google Gemini API 設定
    GEMINI_API_KEY: str
    GEMINI_MODEL: str = "gemini-2.0-flash"

    # 應用程式基本設定
    APP_NAME: str = "AI Chat API"
    DEBUG: bool = False

    # CORS 設定
    ALLOWED_ORIGINS: str = "http://localhost:3000,http://localhost:3001"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

    @property
    def cors_origins(self) -> list[str]:
        """將 ALLOWED_ORIGINS 字串轉換為列表"""
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]


# 全域設定實例
settings = Settings()
