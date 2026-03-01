"""
Model Service 模組

管理 AI 模型資訊的取得，從 Google Generative Language API 動態獲取
"""
import httpx
from typing import Optional

from app.core.config import settings, GOOGLE_MODELS_API_URL
from app.schemas.chat import ModelInfo


class ModelService:
    """
    模型服務類

    從 Google API 動態獲取可用模型列表
    """

    def __init__(self):
        """初始化模型服務"""
        self.api_url = GOOGLE_MODELS_API_URL
        self.api_key = settings.GEMINI_API_KEY
        self.timeout = 10.0

    async def get_available_models(self) -> list[ModelInfo]:
        """
        從 Google API 動態獲取可用模型列表

        Returns:
            list[ModelInfo]: 可用模型列表

        Raises:
            Exception: API 呼叫失敗時拋出異常
        """
        try:
            # 使用 httpx 非同步呼叫 Google API
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    self.api_url,
                    params={"key": self.api_key}
                )
                response.raise_for_status()

            data = response.json()
            models: list[ModelInfo] = []

            # 解析 API 回應
            for model_data in data.get("models", []):
                # 檢查是否支援 generateContent 方法
                supported_methods = model_data.get("supportedGenerationMethods", [])
                if "generateContent" not in supported_methods:
                    continue

                # 提取模型 ID（移除 "models/" 前綴）
                model_id = model_data.get("name", "").replace("models/", "")
                if not model_id:
                    continue

                # 判斷模型類別
                category = self._classify_model(model_id)

                # 構建 ModelInfo
                model_info: ModelInfo = {
                    "id": model_id,
                    "name": model_data.get("displayName", model_id),
                    "category": category,
                    "description": model_data.get("description", ""),
                    "context_window": model_data.get("inputTokenLimit", 0),
                }

                models.append(model_info)

            return models

        except httpx.HTTPError as e:
            raise Exception(f"Google API 呼叫失敗: {str(e)}")
        except Exception as e:
            raise Exception(f"模型列表解析失敗: {str(e)}")

    @staticmethod
    def _classify_model(model_id: str) -> str:
        """
        根據模型 ID 分類

        Args:
            model_id: 模型 ID（如 gemini-2.0-flash）

        Returns:
            str: 模型類別（advanced / recommended / stable）
        """
        if "pro" in model_id.lower():
            return "advanced"
        elif "2.0" in model_id or "2.5" in model_id:
            return "recommended"
        else:
            return "stable"

    def get_default_model(self) -> str:
        """
        取得預設模型 ID

        Returns:
            str: 預設模型 ID
        """
        return settings.GEMINI_MODEL


# 全域單例實例
model_service = ModelService()
