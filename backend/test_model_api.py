"""
測試模型選擇功能的腳本
"""
import sys
from pathlib import Path

# 加入專案路徑
sys.path.insert(0, str(Path(__file__).parent))

from app.core.config import AVAILABLE_MODELS, validate_model, settings


def test_available_models():
    """測試可用模型列表"""
    print("=" * 60)
    print("測試: 可用模型列表")
    print("=" * 60)

    print(f"\n總共 {len(AVAILABLE_MODELS)} 個模型:\n")

    for model_id, info in AVAILABLE_MODELS.items():
        print(f"ID: {model_id}")
        print(f"  名稱: {info['name']}")
        print(f"  分類: {info['category']}")
        print(f"  描述: {info['description']}")
        print()

    print(f"預設模型: {settings.GEMINI_MODEL}")
    print()


def test_validate_model():
    """測試模型驗證功能"""
    print("=" * 60)
    print("測試: 模型驗證")
    print("=" * 60)

    # 有效模型
    valid_models = ["gemini-3-1-pro", "gemini-2-5-flash", "gemini-2-0-flash"]
    print("\n✓ 有效模型測試:")
    for model in valid_models:
        result = validate_model(model)
        print(f"  {model}: {result}")

    # 無效模型
    invalid_models = ["gpt-4", "claude-3", "invalid-model"]
    print("\n✗ 無效模型測試:")
    for model in invalid_models:
        result = validate_model(model)
        print(f"  {model}: {result}")

    print()


def test_models_endpoint_response():
    """測試 /models 端點回應格式"""
    print("=" * 60)
    print("測試: GET /api/chat/models 回應格式")
    print("=" * 60)

    # 模擬 endpoint 回應
    response = {
        "models": list(AVAILABLE_MODELS.values()),
        "default_model": settings.GEMINI_MODEL
    }

    import json
    print("\n回應內容:")
    print(json.dumps(response, ensure_ascii=False, indent=2))
    print()


if __name__ == "__main__":
    test_available_models()
    test_validate_model()
    test_models_endpoint_response()

    print("=" * 60)
    print("所有測試完成！")
    print("=" * 60)
