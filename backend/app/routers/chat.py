"""
Chat 相關 API Endpoints

提供聊天功能的 RESTful API，支援 Server-Sent Events (SSE) streaming
"""
import json
from typing import AsyncGenerator
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import StreamingResponse

from app.core.config import AVAILABLE_MODELS, validate_model, settings
from app.schemas.chat import (
    ChatMessageRequest,
    ChatHistoryResponse,
    ClearHistoryResponse,
    StreamStartEvent,
    StreamChunkEvent,
    StreamDoneEvent,
    MessageRole
)
from app.services.gemini_service import gemini_service, GeminiService


router = APIRouter(prefix="/api/chat", tags=["chat"])


@router.get(
    "/models",
    summary="取得可用模型列表",
    description="取得所有可用的 Gemini 模型清單及預設模型"
)
async def get_available_models():
    """
    取得可用的 Gemini 模型列表

    Returns:
        dict: 包含模型列表與預設模型的回應
            - models: 模型資訊列表
            - default_model: 預設模型 ID
    """
    return {
        "models": list(AVAILABLE_MODELS.values()),
        "default_model": settings.GEMINI_MODEL
    }


async def generate_sse_stream(user_message: str, model: str) -> AsyncGenerator[str, None]:
    """
    生成 Server-Sent Events (SSE) 格式的串流回應

    Args:
        user_message: 使用者輸入的訊息
        model: 使用的 Gemini 模型 ID

    Yields:
        str: SSE 格式的事件資料
    """
    try:
        # 發送 start 事件（包含使用的模型資訊）
        start_event = StreamStartEvent(role=MessageRole.ASSISTANT, model=model)
        yield f"event: start\ndata: {start_event.model_dump_json()}\n\n"

        # 收集完整回應
        complete_content_parts = []

        # 串流 Gemini 回應（傳遞模型參數）
        async for chunk in gemini_service.generate_streaming_response(user_message, model=model):
            complete_content_parts.append(chunk)

            # 發送 chunk 事件
            chunk_event = StreamChunkEvent(content=chunk)
            yield f"event: chunk\ndata: {chunk_event.model_dump_json()}\n\n"

        # 發送 done 事件
        complete_content = "".join(complete_content_parts)
        done_event = StreamDoneEvent(
            role=MessageRole.ASSISTANT,
            complete_content=complete_content
        )
        yield f"event: done\ndata: {done_event.model_dump_json()}\n\n"

    except Exception as e:
        # 發送錯誤事件
        error_data = {"error": str(e)}
        yield f"event: error\ndata: {json.dumps(error_data)}\n\n"


@router.post(
    "/send",
    response_class=StreamingResponse,
    summary="發送訊息",
    description="發送使用者訊息並取得 AI streaming 回應（Server-Sent Events）"
)
async def send_message(request: ChatMessageRequest) -> StreamingResponse:
    """
    發送訊息到 Gemini API 並回傳 streaming 回應

    使用 Server-Sent Events (SSE) 格式即時傳輸 AI 回應內容

    Args:
        request: 包含使用者訊息與可選模型的請求

    Returns:
        StreamingResponse: SSE 格式的串流回應

    Raises:
        HTTPException: 當請求驗證失敗或 API 呼叫錯誤時
    """
    # 驗證訊息
    if not request.message.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="訊息內容不能為空白"
        )

    # 驗證模型（如果提供的話）
    model_to_use = request.model or settings.GEMINI_MODEL
    if request.model and not validate_model(request.model):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"無效的模型: {request.model}。可用模型: {list(AVAILABLE_MODELS.keys())}"
        )

    return StreamingResponse(
        generate_sse_stream(request.message.strip(), model_to_use),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"  # 停用 nginx 緩衝（若使用 nginx）
        }
    )


@router.get(
    "/history",
    response_model=ChatHistoryResponse,
    summary="取得對話歷史",
    description="取得目前對話歷史（記憶體版本）"
)
async def get_chat_history() -> ChatHistoryResponse:
    """
    取得對話歷史

    Returns:
        ChatHistoryResponse: 包含對話記錄列表的回應
    """
    messages = gemini_service.get_history()
    return ChatHistoryResponse(messages=messages)


@router.delete(
    "/clear",
    response_model=ClearHistoryResponse,
    summary="清除對話歷史",
    description="清除目前對話歷史"
)
async def clear_chat_history() -> ClearHistoryResponse:
    """
    清除對話歷史

    Returns:
        ClearHistoryResponse: 清除結果回應
    """
    gemini_service.clear_history()
    return ClearHistoryResponse(
        success=True,
        message="對話歷史已清除"
    )
