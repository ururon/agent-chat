# AI Chat Frontend - Nuxt 3

基於 Vue 3 + Nuxt 3 的 AI 聊天應用前端，支援即時串流（SSE）對話。

## 技術棧

- **框架**: Nuxt 3 (Vue 3 Composition API)
- **樣式**: Tailwind CSS
- **串流**: Server-Sent Events (SSE)
- **API**: FastAPI 後端 (http://localhost:8000)

## 專案結構

```
frontend/
├── components/
│   └── chat/
│       ├── ChatMessage.vue      # 訊息氣泡元件
│       ├── ChatInput.vue        # 輸入框元件
│       └── ChatContainer.vue    # 聊天容器
├── composables/
│   └── useChat.ts               # 聊天邏輯 composable
├── pages/
│   └── index.vue                # 主頁面
├── types/
│   └── chat.ts                  # TypeScript 型別定義
├── app.vue                      # 應用程式根元件
├── nuxt.config.ts              # Nuxt 配置
└── tailwind.config.js          # Tailwind 配置
```

## 核心功能

### useChat Composable

提供完整的聊天功能：

- `messages` - 對話歷史（響應式）
- `isLoading` - 載入狀態
- `error` - 錯誤訊息
- `sendMessage(message)` - 發送訊息並接收 SSE 串流
- `clearHistory()` - 清除對話歷史
- `autoScroll()` - 自動滾動到最新訊息

### SSE Streaming 實作

使用 Fetch API + ReadableStream 實現即時串流：

```typescript
const response = await fetch('http://localhost:8000/api/chat/send', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ message })
})

const reader = response.body.getReader()
const decoder = new TextDecoder()

while (true) {
  const { done, value } = await reader.read()
  if (done) break

  const chunk = decoder.decode(value, { stream: true })
  // 逐字更新 AI 回應...
}
```

## 安裝與執行

### 1. 安裝依賴

```bash
npm install
```

### 2. 啟動開發伺服器

```bash
npm run dev
```

前端將運行於: http://localhost:3000

### 3. 確認後端運行

確保 FastAPI 後端已啟動於: http://localhost:8000

```bash
cd ../backend
./start.sh
```

## 使用方式

1. 開啟瀏覽器訪問 http://localhost:3000
2. 在輸入框輸入訊息
3. 按 Enter 或點擊「發送」按鈕
4. 即時觀看 AI 回應（逐字顯示）
5. 點擊「清除對話」可重置對話歷史

## API 端點

- `POST /api/chat/send` - 發送訊息（SSE streaming）
- `DELETE /api/chat/clear` - 清除對話歷史

## 建構生產版本

```bash
npm run build
npm run preview
```

## 技術特點

- ✅ Vue 3 Composition API + `<script setup>`
- ✅ TypeScript 型別安全
- ✅ SSE 即時串流
- ✅ 響應式設計
- ✅ 自動滾動至最新訊息
- ✅ 錯誤處理與使用者提示
- ✅ 載入狀態管理
- ✅ 清晰的元件化架構
