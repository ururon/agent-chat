"""
Chat 相關的 Pydantic Schemas
"""
from datetime import datetime
from enum import Enum
from typing import Optional, TypedDict
from pydantic import BaseModel, Field


class MessageRole(str, Enum):
    """訊息角色"""
    USER = "user"
    ASSISTANT = "assistant"


class ModelInfo(TypedDict):
    """AI 模型資訊"""
    id: str
    name: str
    category: str
    description: str
    context_window: int


class ChatMessageRequest(BaseModel):
    """使用者發送訊息的 Request Schema"""
    message: str = Field(
        ...,
        min_length=1,
        max_length=10000,
        description="使用者輸入的訊息內容"
    )
    model: Optional[str] = Field(
        default=None,
        description="使用的 Gemini 模型,留空則使用預設值"
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "message": "請用 Python 寫一個 Hello World 程式",
                    "model": "gemini-2.0-flash"
                },
                {
                    "message": "什麼是機器學習？",
                    "model": None
                }
            ]
        }
    }


class ChatMessage(BaseModel):
    """單筆對話記錄"""
    role: MessageRole = Field(..., description="訊息角色（user 或 assistant）")
    content: str = Field(..., description="訊息內容")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="訊息時間戳記")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "role": "user",
                    "content": "你好，請介紹一下自己",
                    "timestamp": "2024-01-01T12:00:00Z"
                }
            ]
        }
    }


class ChatHistoryResponse(BaseModel):
    """對話歷史回應 Schema"""
    messages: list[ChatMessage] = Field(default_factory=list, description="對話記錄列表")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "messages": [
                        {
                            "role": "user",
                            "content": "你好",
                            "timestamp": "2024-01-01T12:00:00Z"
                        },
                        {
                            "role": "assistant",
                            "content": "你好！我是 AI 助手，有什麼我可以幫助你的嗎？",
                            "timestamp": "2024-01-01T12:00:01Z"
                        }
                    ]
                }
            ]
        }
    }


class ClearHistoryResponse(BaseModel):
    """清除對話歷史回應 Schema"""
    success: bool = Field(default=True, description="是否成功")
    message: str = Field(default="Chat history cleared", description="回應訊息")


class StreamEvent(BaseModel):
    """SSE 串流事件基礎 Schema"""
    pass


class StreamStartEvent(StreamEvent):
    """串流開始事件"""
    role: MessageRole = Field(default=MessageRole.ASSISTANT, description="回應角色")
    model: str = Field(..., description="使用的 Gemini 模型")


class StreamChunkEvent(StreamEvent):
    """串流內容片段事件"""
    content: str = Field(..., description="內容片段")


class StreamDoneEvent(StreamEvent):
    """串流完成事件"""
    role: MessageRole = Field(default=MessageRole.ASSISTANT, description="回應角色")
    complete_content: str = Field(..., description="完整回應內容")
