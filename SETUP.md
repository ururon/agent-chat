# AI Chat 專案設定指南

## 專案狀態

✅ **前端已完成** - Nuxt 3 + Vue 3 Composition API
⚠️ **後端需設定** - FastAPI (需要 Gemini API Key)

## 當前運行狀態

- **前端**: http://localhost:3000 ✅ 運行中
- **後端**: http://localhost:8000 ⚠️ 需設定 API Key

## 快速啟動步驟

### 1. 設定後端環境變數

```bash
cd backend

# 複製環境變數範例
cp .env.example .env

# 編輯 .env 檔案，設定你的 Gemini API Key
# GEMINI_API_KEY=your_actual_api_key_here
```

**取得 Gemini API Key:**
- 訪問: https://makersuite.google.com/app/apikey
- 登入 Google 帳號
- 建立並複製 API Key
- 貼到 `.env` 檔案中

### 2. 啟動後端

```bash
cd backend
./start.sh
```

後端將運行於: http://localhost:8000

### 3. 啟動前端（已運行）

```bash
cd frontend
npm run dev
```

前端已運行於: http://localhost:3000

## 驗證安裝

### 測試後端健康狀態

```bash
curl http://localhost:8000/health
# 應回傳: {"status":"healthy"}
```

### 測試 API 文件

開啟瀏覽器訪問: http://localhost:8000/docs

### 測試前端

開啟瀏覽器訪問: http://localhost:3000

## 完整測試流程

1. ✅ 前端頁面載入正常
2. ✅ UI 元件顯示正確
3. ⏳ 輸入訊息並發送
4. ⏳ 觀察 AI 回應即時顯示（逐字）
5. ⏳ 測試清除對話功能
6. ⏳ 測試錯誤處理

## 專案結構

```
agent/
├── backend/           # FastAPI 後端
│   ├── app/
│   ├── .env          # 需要建立並設定
│   ├── .env.example
│   └── start.sh
├── frontend/         # Nuxt 3 前端
│   ├── components/
│   ├── composables/
│   ├── pages/
│   ├── types/
│   └── nuxt.config.ts
└── SETUP.md         # 本檔案
```

## 技術棧

### 前端
- Nuxt 3
- Vue 3 (Composition API)
- Tailwind CSS
- TypeScript
- SSE (Server-Sent Events)

### 後端
- FastAPI
- Google Gemini API
- Python 3.11+
- Uvicorn

## 下一步

1. **設定 Gemini API Key** - 必須完成才能測試完整功能
2. **啟動後端服務**
3. **測試完整對話流程**
4. **檢查 SSE streaming 是否正常**

## 常見問題

### 前端無法連接後端？

檢查 CORS 設定（backend/.env）：
```
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### SSE streaming 不工作？

1. 確認後端正確啟動
2. 檢查瀏覽器 Network 工具
3. 確認 API Key 已正確設定

### 前端顯示錯誤？

查看瀏覽器 Console 的詳細錯誤訊息
