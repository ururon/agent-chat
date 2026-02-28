"""
應用程式設定管理

使用 Pydantic Settings 從環境變數載入設定
"""
from typing import TypedDict
from pydantic_settings import BaseSettings, SettingsConfigDict


class ModelInfo(TypedDict):
    """Gemini 模型資訊"""
    id: str
    name: str
    category: str  # "advanced", "recommended", "stable"
    description: str


# 可用的 Gemini 模型白名單
AVAILABLE_MODELS: dict[str, ModelInfo] = {
    "gemini-3.1-pro": {
        "id": "gemini-3.1-pro",
        "name": "Gemini 3.1 Pro",
        "category": "advanced",
        "description": "最新推出,推理能力最強,支持複雜問題解決"
    },
    "gemini-2.5-flash": {
        "id": "gemini-2.5-flash",
        "name": "Gemini 2.5 Flash",
        "category": "recommended",
        "description": "新一代快速模型,平衡速度與品質,推薦大多數應用"
    },
    "gemini-2.0-flash": {
        "id": "gemini-2.0-flash",
        "name": "Gemini 2.0 Flash",
        "category": "stable",
        "description": "成熟穩定的快速模型,適合高頻對話應用"
    },
}


def validate_model(model_id: str) -> bool:
    """
    驗證模型是否在白名單中

    Args:
        model_id: 要驗證的模型 ID

    Returns:
        bool: 是否為有效模型
    """
    return model_id in AVAILABLE_MODELS


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
