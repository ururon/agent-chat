# Swagger / OpenAPI 集成指南

本文檔說明如何在本專案中使用和管理 Swagger API 文檔。

## 後端（FastAPI）

### 自動 Swagger UI

FastAPI 已內置 OpenAPI 支援，自動生成以下文件：

| 端點 | 說明 |
|------|------|
| `http://localhost:8000/docs` | Swagger UI（互動式文檔） |
| `http://localhost:8000/redoc` | ReDoc（美化文檔） |
| `http://localhost:8000/openapi.json` | OpenAPI 規格（JSON 格式） |

### 啟動 Backend 伺服器

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

訪問 `http://localhost:8000/docs` 查看 API 文檔。

### 生成 OpenAPI YAML 規格

為了將 OpenAPI 規格納入版本控制，可以使用以下腳本導出為 YAML 格式：

```bash
cd backend
pip install pyyaml
python scripts/generate-openapi.py
```

這將生成 `backend/openapi.yaml` 檔案，包含完整的 API 定義。

**注意**：生成的 `openapi.yaml` 已納入 `.gitignore`，如需版本控制，請移除該行。

## 前端（Nuxt）

### 生成 TypeScript 類型

使用 `openapi-typescript` 從 OpenAPI 規格自動生成 TypeScript 類型：

#### 1. 安裝依賴

```bash
cd frontend
npm install
```

#### 2. 生成 API 類型

```bash
npm run gen:types
```

這將從 `http://localhost:8000/openapi.json` 生成 TypeScript 類型，輸出至 `frontend/types/api.generated.ts`。

**前置條件**：Backend 伺服器必須運行中

#### 3. 在 Composables 中使用

生成的 types 可在 composables 中引用：

```typescript
import type { paths } from '~/types/api.generated'

// 使用自動生成的 types
type ChatRequest = paths['/api/chat/send']['post']['requestBody']['content']['application/json']
type ChatResponse = paths['/api/chat/send']['post']['responses']['200']
```

### 整合到開發流程

#### 自動化方案（推薦）

在 CI/CD 中自動執行 `gen:types`：

```bash
# 在 build 前生成最新 types
npm run gen:types && npm run build
```

#### 手動方案

開發期間手動執行：

```bash
npm run gen:types  # 當 Backend API 有更新時執行
npm run dev         # 開發伺服器
```

## API 文檔維護

### Schema 與 Examples

所有 Schema 都應包含清晰的說明和範例：

**Python (FastAPI)**

```python
from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    message: str = Field(..., description="使用者訊息")
    model: Optional[str] = Field(None, description="模型 ID")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"message": "Hello", "model": "gemini-2.0-flash"}
            ]
        }
    }
```

### Endpoint 回應定義

所有 endpoint 應明確定義 responses：

```python
@router.post(
    "/send",
    responses={
        200: {"description": "成功發送訊息"},
        400: {"description": "驗證錯誤"},
        500: {"description": "伺服器錯誤"}
    }
)
async def send_message(request: ChatRequest):
    ...
```

## 工作流程

### 新增 API Endpoint

1. **後端**：在 `app/routers/` 新增 endpoint 及完整文檔
   ```bash
   # 檢查 Swagger UI
   curl http://localhost:8000/docs
   ```

2. **前端**：重新生成 types
   ```bash
   cd frontend
   npm run gen:types
   ```

3. **驗證**：使用生成的 types 編寫 composable

### 修改 Schema

1. 更新 `app/schemas/` 中的 Pydantic 模型
2. 重新生成 OpenAPI YAML（若需版本控制）
   ```bash
   python backend/scripts/generate-openapi.py
   ```
3. 前端重新生成 types
   ```bash
   npm run gen:types
   ```

## 常見問題

### Q: 為什麼生成的 types 檔案未出現？

**A**: 確保 Backend 伺服器運行中：
```bash
cd backend
python -m uvicorn app.main:app --reload
```

### Q: 如何驗證 OpenAPI 規格的有效性？

**A**: 使用 OpenAPI 驗證工具：
```bash
# 線上驗證：https://editor.swagger.io/
# 或使用 spectacle 在本地檢查
npm install -g @stoplight/spectacle
spectacle openapi.yaml
```

### Q: TypeScript 類型生成出現錯誤？

**A**: 檢查 OpenAPI 規格的有效性：
```bash
curl http://localhost:8000/openapi.json | jq .
```

## 參考資源

- [FastAPI - OpenAPI 文檔](https://fastapi.tiangolo.com/how-to/extending-openapi/)
- [openapi-typescript](https://openapi-ts.dev/)
- [OpenAPI 規範](https://spec.openapis.org/oas/v3.1.0)
