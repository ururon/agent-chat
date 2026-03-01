"""
OpenAI Service 模組

使用 OpenAI SDK 搭配 Google Vertex AI OpenAI 兼容 API
實現對話生成與串流回應功能
"""
from typing import AsyncGenerator
from openai import AsyncOpenAI

from app.core.config import settings, OPENAI_BASE_URL
from app.schemas.chat import ChatMessage, MessageRole


class OpenAIService:
    """
    OpenAI 服務類

    使用 AsyncOpenAI 實現對話生成
    管理對話歷史記錄（記憶體版本）
    """

    def __init__(self):
        """初始化 OpenAI 客戶端"""
        self.client = AsyncOpenAI(
            api_key=settings.GEMINI_API_KEY,
            base_url=OPENAI_BASE_URL
        )
        # 對話歷史（記憶體存儲）
        self._message_history: list[ChatMessage] = []

    async def generate_streaming_response(
        self, user_message: str, model: str
    ) -> AsyncGenerator[str, None]:
        """
        生成串流回應

        Args:
            user_message: 使用者輸入的訊息
            model: 使用的模型 ID

        Yields:
            str: 生成的文字片段

        Raises:
            Exception: API 呼叫或串流處理錯誤
        """
        # 添加使用者訊息到歷史
        user_msg = ChatMessage(
            role=MessageRole.USER,
            content=user_message
        )
        self._message_history.append(user_msg)

        # 將對話歷史轉換為 OpenAI 訊息格式
        messages = [
            {
                "role": msg.role.value,
                "content": msg.content
            }
            for msg in self._message_history
        ]

        # 調用 OpenAI Chat Completions API（串流）
        try:
            stream = await self.client.chat.completions.create(
                model=model,
                messages=messages,
                stream=True,
                temperature=0.7,
                top_p=0.95,
                max_tokens=4096
            )

            # 收集完整回應文字
            complete_content = ""

            # 逐塊產生回應
            async for chunk in stream:
                if chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    complete_content += content
                    yield content

            # 將完整回應添加到歷史
            assistant_msg = ChatMessage(
                role=MessageRole.ASSISTANT,
                content=complete_content
            )
            self._message_history.append(assistant_msg)

        except Exception as e:
            # 移除該次使用者訊息（因為失敗了）
            self._message_history.pop()
            raise

    def get_history(self) -> list[ChatMessage]:
        """
        獲取對話歷史

        Returns:
            list[ChatMessage]: 對話記錄列表
        """
        return self._message_history.copy()

    def clear_history(self) -> None:
        """清除對話歷史"""
        self._message_history.clear()

    def add_message(
        self, role: MessageRole, content: str
    ) -> ChatMessage:
        """
        手動添加訊息到歷史

        Args:
            role: 訊息角色（user 或 assistant）
            content: 訊息內容

        Returns:
            ChatMessage: 新建的訊息物件
        """
        message = ChatMessage(role=role, content=content)
        self._message_history.append(message)
        return message


# 全域單例實例
openai_service = OpenAIService()
