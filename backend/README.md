# AI Chat Backend (FastAPI)

AI 對話聊天後端服務，整合 Google Gemini API，提供 Server-Sent Events (SSE) streaming 回應。

## 技術棧

- **FastAPI**: 現代化 Python Web 框架
- **Pydantic v2**: 資料驗證與設定管理
- **Google Gemini API**: AI 對話生成
- **Uvicorn**: ASGI 伺服器

## 專案結構

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI 應用程式入口
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py           # Pydantic Settings 設定
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── chat.py             # Chat 相關 Pydantic models
│   ├── services/
│   │   ├── __init__.py
│   │   └── gemini_service.py   # Gemini API 整合
│   └── routers/
│       ├── __init__.py
│       └── chat.py             # Chat API endpoints
├── requirements.txt
├── .env.example
└── README.md
```

## 環境設定

### 1. 複製環境變數範例

```bash
cp .env.example .env
```

### 2. 設定 Google Gemini API Key

前往 [Google AI Studio](https://makersuite.google.com/app/apikey) 取得 API Key，並更新 `.env` 檔案：

```env
GEMINI_API_KEY=your_actual_api_key_here
```

### 3. 安裝依賴套件

```bash
pip install -r requirements.txt
```

## 啟動服務

### 開發模式（支援熱重載）

```bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 生產模式

```bash
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

服務啟動後可透過以下網址存取：

- **API 根路徑**: http://localhost:8000
- **API 文件 (Swagger)**: http://localhost:8000/docs
- **健康檢查**: http://localhost:8000/health

## API Endpoints

### POST /api/chat/send

發送訊息並取得 AI streaming 回應（Server-Sent Events）

**Request:**
```json
{
  "message": "你好，請介紹一下自己"
}
```

**Response (SSE Stream):**
```
event: start
data: {"role": "assistant"}

event: chunk
data: {"content": "你好"}

event: chunk
data: {"content": "！"}

...

event: done
data: {"role": "assistant", "complete_content": "完整回應內容"}
```

### GET /api/chat/history

取得對話歷史（記憶體版本）

**Response:**
```json
{
  "messages": [
    {
      "role": "user",
      "content": "你好",
      "timestamp": "2024-01-01T12:00:00Z"
    },
    {
      "role": "assistant",
      "content": "你好！我能幫你什麼嗎？",
      "timestamp": "2024-01-01T12:00:05Z"
    }
  ]
}
```

### DELETE /api/chat/clear

清除對話歷史

**Response:**
```json
{
  "success": true,
  "message": "對話歷史已清除"
}
```

## 開發注意事項

- 對話歷史目前儲存於記憶體（重啟後清除）
- 全域共享對話歷史（無會話隔離）
- 使用 SSE streaming 即時傳輸 AI 回應
- 所有 I/O 操作使用 async/await 模式
- 完整型別提示與 Pydantic 驗證

## 未來擴充

- [ ] 加入會話隔離（Session Management）
- [ ] 持久化儲存（PostgreSQL / Redis）
- [ ] 速率限制（Rate Limiting）
- [ ] 使用者認證與授權
- [ ] 對話摘要與搜尋功能
