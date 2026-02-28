"""
整合測試: 驗證 ChatMessageRequest schema 與模型驗證邏輯
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from pydantic import ValidationError
from app.schemas.chat import ChatMessageRequest
from app.core.config import validate_model, AVAILABLE_MODELS


def test_chat_message_request_schema():
    """測試 ChatMessageRequest Schema"""
    print("=" * 60)
    print("測試: ChatMessageRequest Schema")
    print("=" * 60)

    # 測試 1: 僅包含 message（model 為 None）
    print("\n1. 僅包含 message (model 預設為 None):")
    try:
        req1 = ChatMessageRequest(message="Hello, AI!")
        print(f"   ✓ message: {req1.message}")
        print(f"   ✓ model: {req1.model}")
    except ValidationError as e:
        print(f"   ✗ 驗證失敗: {e}")

    # 測試 2: 包含 message 和 model
    print("\n2. 包含 message 和有效 model:")
    try:
        req2 = ChatMessageRequest(message="Test message", model="gemini-3-1-pro")
        print(f"   ✓ message: {req2.message}")
        print(f"   ✓ model: {req2.model}")
    except ValidationError as e:
        print(f"   ✗ 驗證失敗: {e}")

    # 測試 3: 空訊息（應該失敗）
    print("\n3. 空訊息 (應該失敗):")
    try:
        req3 = ChatMessageRequest(message="")
        print(f"   ✗ 不應該通過驗證!")
    except ValidationError as e:
        print(f"   ✓ 正確拒絕: 訊息長度不足")

    # 測試 4: 超長訊息（應該失敗）
    print("\n4. 超長訊息 (應該失敗):")
    try:
        req4 = ChatMessageRequest(message="x" * 10001)
        print(f"   ✗ 不應該通過驗證!")
    except ValidationError as e:
        print(f"   ✓ 正確拒絕: 訊息超過長度限制")

    print()


def test_send_message_validation_logic():
    """測試發送訊息的驗證邏輯"""
    print("=" * 60)
    print("測試: POST /api/chat/send 驗證邏輯")
    print("=" * 60)

    from app.core.config import settings

    # 模擬不同的請求情境
    test_cases = [
        {
            "name": "使用預設模型",
            "request": ChatMessageRequest(message="Hello"),
            "expected_model": settings.GEMINI_MODEL
        },
        {
            "name": "指定有效模型",
            "request": ChatMessageRequest(message="Hello", model="gemini-3-1-pro"),
            "expected_model": "gemini-3-1-pro"
        },
        {
            "name": "指定另一個有效模型",
            "request": ChatMessageRequest(message="Hello", model="gemini-2-0-flash"),
            "expected_model": "gemini-2-0-flash"
        },
    ]

    for i, case in enumerate(test_cases, 1):
        print(f"\n{i}. {case['name']}:")
        request = case['request']

        # 模擬 endpoint 邏輯
        model_to_use = request.model or settings.GEMINI_MODEL

        # 驗證模型
        if request.model and not validate_model(request.model):
            print(f"   ✗ 無效模型: {request.model}")
        else:
            print(f"   ✓ 使用模型: {model_to_use}")
            print(f"   ✓ 預期模型: {case['expected_model']}")
            assert model_to_use == case['expected_model'], "模型不匹配!"

    # 測試無效模型
    print(f"\n4. 指定無效模型:")
    invalid_request = ChatMessageRequest(message="Hello", model="gpt-4")
    if invalid_request.model and not validate_model(invalid_request.model):
        print(f"   ✓ 正確拒絕無效模型: {invalid_request.model}")
        print(f"   ✓ 可用模型: {list(AVAILABLE_MODELS.keys())}")

    print()


def test_stream_start_event_schema():
    """測試 StreamStartEvent 包含 model 欄位"""
    print("=" * 60)
    print("測試: StreamStartEvent 包含 model 欄位")
    print("=" * 60)

    from app.schemas.chat import StreamStartEvent, MessageRole

    print("\n建立 StreamStartEvent:")
    try:
        event = StreamStartEvent(
            role=MessageRole.ASSISTANT,
            model="gemini-3-1-pro"
        )
        print(f"   ✓ role: {event.role}")
        print(f"   ✓ model: {event.model}")

        # 測試序列化
        json_data = event.model_dump_json()
        print(f"   ✓ JSON: {json_data}")
    except Exception as e:
        print(f"   ✗ 失敗: {e}")

    print()


if __name__ == "__main__":
    test_chat_message_request_schema()
    test_send_message_validation_logic()
    test_stream_start_event_schema()

    print("=" * 60)
    print("所有整合測試完成！")
    print("=" * 60)
