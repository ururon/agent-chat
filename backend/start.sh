#!/bin/bash

# FastAPI 開發伺服器啟動腳本

echo "🚀 啟動 FastAPI 開發伺服器..."
echo ""

# 檢查 .env 是否存在
if [ ! -f .env ]; then
    echo "⚠️  警告：未找到 .env 檔案"
    echo "請複製 .env.example 並設定 GEMINI_API_KEY"
    echo ""
    echo "  cp .env.example .env"
    echo ""
    exit 1
fi

# 檢查是否安裝依賴
if ! python -c "import fastapi" 2>/dev/null; then
    echo "📦 安裝依賴套件..."
    pip install -r requirements.txt
    echo ""
fi

# 啟動服務
echo "🔥 啟動中..."
echo "📍 API 根路徑: http://localhost:8000"
echo "📚 API 文件: http://localhost:8000/docs"
echo "💚 健康檢查: http://localhost:8000/health"
echo ""

python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
