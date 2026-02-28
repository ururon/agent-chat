"""
Google Gemini API 整合服務

提供與 Gemini API 互動的功能，支援 streaming 回應
"""
import asyncio
import threading
from typing import AsyncGenerator
import google.generativeai as genai
from google.generativeai.types import GenerateContentResponse

from app.core.config import settings
from app.schemas.chat import ChatMessage, MessageRole


class GeminiService:
    """Google Gemini API 服務"""

    def __init__(self):
        """初始化 Gemini API client"""
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(settings.GEMINI_MODEL)

        # 記憶體對話歷史（全域共享）
        self._conversation_history: list[ChatMessage] = []

    def add_message(self, role: MessageRole, content: str) -> ChatMessage:
        """
        新增訊息到對話歷史

        Args:
            role: 訊息角色
            content: 訊息內容

        Returns:
            ChatMessage: 新增的訊息物件
        """
        message = ChatMessage(role=role, content=content)
        self._conversation_history.append(message)
        return message

    def get_history(self) -> list[ChatMessage]:
        """
        取得對話歷史

        Returns:
            list[ChatMessage]: 對話記錄列表
        """
        return self._conversation_history.copy()

    def clear_history(self) -> None:
        """清除對話歷史"""
        self._conversation_history.clear()

    def _build_context(self) -> str:
        """
        將對話歷史建構為 context 字串

        Returns:
            str: 對話歷史文字
        """
        if not self._conversation_history:
            return ""

        context_parts = []
        for msg in self._conversation_history:
            role_label = "User" if msg.role == MessageRole.USER else "Assistant"
            context_parts.append(f"{role_label}: {msg.content}")

        return "\n".join(context_parts)

    async def generate_streaming_response(
        self,
        user_message: str
    ) -> AsyncGenerator[str, None]:
        """
        生成 streaming 回應（真正的即時 streaming）

        Args:
            user_message: 使用者輸入的訊息

        Yields:
            str: 回應內容片段

        Raises:
            Exception: API 呼叫失敗時拋出例外
        """
        # 新增使用者訊息到歷史
        self.add_message(MessageRole.USER, user_message)

        # 建構完整的 prompt（包含對話歷史）
        context = self._build_context()
        prompt = f"{context}\nUser: {user_message}\nAssistant:"

        # 使用 asyncio.Queue 來實現真正的即時 streaming
        queue: asyncio.Queue[str | None] = asyncio.Queue()
        exception_holder = {'error': None}

        def streaming_thread():
            """在獨立執行緒中執行 Gemini streaming"""
            try:
                response = self.model.generate_content(prompt, stream=True)
                for chunk in response:
                    if chunk.text:
                        # 非阻塞方式放入 queue（使用 put_nowait）
                        try:
                            queue.put_nowait(chunk.text)
                        except asyncio.QueueFull:
                            # Queue 滿了，等待一下再試
                            pass
                # 發送完成信號
                queue.put_nowait(None)
            except Exception as e:
                exception_holder['error'] = e
                queue.put_nowait(None)

        try:
            # 啟動執行緒
            thread = threading.Thread(target=streaming_thread, daemon=True)
            thread.start()

            # 收集完整回應
            full_response_parts = []

            # 非同步讀取 queue 並即時 yield
            while True:
                try:
                    # 設定 timeout 避免無限等待
                    chunk = await asyncio.wait_for(queue.get(), timeout=30.0)
                except asyncio.TimeoutError:
                    raise Exception("Gemini API 回應超時")

                if chunk is None:
                    # 流已完成
                    break

                full_response_parts.append(chunk)
                # 逐字 yield，實現一個字一個字的自然顯示效果
                for char in chunk:
                    yield char

            # 檢查是否有例外
            if exception_holder['error']:
                raise exception_holder['error']

            # 將完整回應加入對話歷史
            complete_response = "".join(full_response_parts)
            self.add_message(MessageRole.ASSISTANT, complete_response)

        except Exception as e:
            # 移除使用者訊息（因為生成失敗）
            if self._conversation_history and self._conversation_history[-1].role == MessageRole.USER:
                self._conversation_history.pop()
            raise Exception(f"Gemini API 呼叫失敗: {str(e)}") from e


# 全域 service 實例（單例模式）
gemini_service = GeminiService()
