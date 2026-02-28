# 🚀 快速啟動指南

## 當前狀態

✅ **前端已完成並運行** - http://localhost:3000
⚠️ **後端需設定 API Key**

---

## 立即啟動（3 步驟）

### 1️⃣ 設定後端 API Key

```bash
cd backend

# 複製環境變數範例
cp .env.example .env

# 編輯 .env 檔案
# 將 GEMINI_API_KEY=your_gemini_api_key_here
# 改為你的真實 API Key
```

**取得 API Key：** https://makersuite.google.com/app/apikey

### 2️⃣ 啟動後端

```bash
cd backend
./start.sh
```

後端將運行於：http://localhost:8000

驗證：`curl http://localhost:8000/health`

### 3️⃣ 啟動前端（或驗證已運行）

```bash
cd frontend
npm run dev
# 或使用快速腳本
./dev.sh
```

前端將運行於：http://localhost:3000

---

## 驗證安裝

### 檢查前端
開啟瀏覽器：http://localhost:3000

應該看到：
- 🤖 AI Chat 助手標題
- 💬 空狀態提示「開始對話吧！」
- 輸入框與發送按鈕

### 檢查後端
```bash
# 健康檢查
curl http://localhost:8000/health

# API 文件
open http://localhost:8000/docs
```

### 測試完整流程
1. 在前端輸入：「你好」
2. 按 Enter 或點擊「發送」
3. 觀察 AI 回應逐字顯示
4. 測試清除對話功能

---

## 專案結構一覽

```
agent/
├── backend/              # FastAPI 後端
│   ├── app/
│   │   ├── routers/     # API 路由
│   │   ├── services/    # 業務邏輯
│   │   └── schemas/     # Pydantic 模型
│   ├── .env            # 需建立（從 .env.example 複製）
│   └── start.sh        # 啟動腳本
│
├── frontend/            # Nuxt 3 前端
│   ├── components/      # Vue 元件
│   │   └── chat/       # 聊天相關元件
│   ├── composables/     # Composition API
│   │   └── useChat.ts  # 聊天邏輯
│   ├── pages/          # 路由頁面
│   ├── types/          # TypeScript 型別
│   └── dev.sh          # 啟動腳本
│
└── 文件/
    ├── SETUP.md                # 詳細設定指南
    ├── COMPLETION_REPORT.md    # 開發完成報告
    └── QUICK_START.md          # 本檔案
```

---

## 常用指令

### 開發

```bash
# 啟動前端開發伺服器
cd frontend && npm run dev

# 啟動後端開發伺服器
cd backend && ./start.sh

# 建構前端生產版本
cd frontend && npm run build

# 預覽前端生產版本
cd frontend && npm run preview
```

### 檢查

```bash
# 檢查後端健康
curl http://localhost:8000/health

# 檢查前端
curl http://localhost:3000

# 檢查執行中的服務
lsof -ti:3000,8000
```

---

## 技術棧

### 前端
- **框架**: Nuxt 3 (Vue 3)
- **語言**: TypeScript
- **樣式**: Tailwind CSS
- **串流**: Server-Sent Events (SSE)

### 後端
- **框架**: FastAPI
- **AI**: Google Gemini API
- **語言**: Python 3.11+
- **伺服器**: Uvicorn

---

## API 端點

### 後端 API
- `POST /api/chat/send` - 發送訊息（SSE streaming）
- `DELETE /api/chat/clear` - 清除對話歷史
- `GET /health` - 健康檢查
- `GET /docs` - Swagger API 文件
- `GET /redoc` - ReDoc API 文件

---

## 疑難排解

### 前端無法連接後端？

1. 確認後端運行：`curl http://localhost:8000/health`
2. 檢查 CORS 設定（backend/.env）：
   ```
   ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
   ```
3. 確認防火牆允許 8000 埠

### SSE 串流不工作？

1. 開啟瀏覽器 DevTools → Network
2. 找到 `/api/chat/send` 請求
3. 檢查 Response Headers：`Content-Type: text/event-stream`
4. 確認 API Key 已正確設定

### Gemini API 錯誤？

1. 確認 API Key 有效：https://makersuite.google.com/app/apikey
2. 檢查 API 配額是否用完
3. 確認網路可連接 Google API

### 前端建構失敗？

```bash
cd frontend
rm -rf .nuxt node_modules
npm install
npm run dev
```

---

## 下一步

完成基本設定後，可以：

1. **自訂 AI 行為** - 編輯 `backend/app/services/chat_service.py`
2. **調整 UI 樣式** - 修改 `frontend/components/chat/*.vue`
3. **新增功能** - 參考 `COMPLETION_REPORT.md` 的架構說明
4. **部署上線** - 參考各框架的部署文件

---

## 文件資源

- **詳細設定指南**: `SETUP.md`
- **開發完成報告**: `COMPLETION_REPORT.md`
- **前端 README**: `frontend/README.md`
- **後端 README**: `backend/README.md`
- **前端檢查清單**: `frontend/CHECKLIST.md`

---

## 快速連結

- **前端**: http://localhost:3000
- **後端 API**: http://localhost:8000
- **API 文件**: http://localhost:8000/docs
- **Gemini API Key**: https://makersuite.google.com/app/apikey

---

**就是這麼簡單！享受與 AI 的對話吧！** 🎉
