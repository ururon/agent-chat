"""
Chat 相關 API Endpoints

提供聊天功能的 RESTful API，支援 Server-Sent Events (SSE) streaming
"""
import json
from typing import AsyncGenerator
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import StreamingResponse

from app.schemas.chat import (
    ChatMessageRequest,
    ChatHistoryResponse,
    ClearHistoryResponse,
    StreamStartEvent,
    StreamChunkEvent,
    StreamDoneEvent,
    MessageRole
)
from app.services.gemini_service import gemini_service


router = APIRouter(prefix="/api/chat", tags=["chat"])


async def generate_sse_stream(user_message: str) -> AsyncGenerator[str, None]:
    """
    生成 Server-Sent Events (SSE) 格式的串流回應

    Args:
        user_message: 使用者輸入的訊息

    Yields:
        str: SSE 格式的事件資料
    """
    try:
        # 發送 start 事件
        start_event = StreamStartEvent(role=MessageRole.ASSISTANT)
        yield f"event: start\ndata: {start_event.model_dump_json()}\n\n"

        # 收集完整回應
        complete_content_parts = []

        # 串流 Gemini 回應
        async for chunk in gemini_service.generate_streaming_response(user_message):
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
        request: 包含使用者訊息的請求

    Returns:
        StreamingResponse: SSE 格式的串流回應

    Raises:
        HTTPException: 當請求驗證失敗或 API 呼叫錯誤時
    """
    if not request.message.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="訊息內容不能為空白"
        )

    return StreamingResponse(
        generate_sse_stream(request.message),
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
