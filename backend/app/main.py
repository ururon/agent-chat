"""
FastAPI 應用程式主入口

初始化 FastAPI app、註冊路由與 middleware
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.routers import chat


# 建立 FastAPI 應用程式
app = FastAPI(
    title=settings.APP_NAME,
    description="AI 對話聊天 API，整合 Google Gemini",
    version="1.0.0",
    debug=settings.DEBUG
)


# CORS 設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 註冊路由
app.include_router(chat.router)


@app.get("/", tags=["root"])
async def root() -> JSONResponse:
    """根路徑，顯示 API 基本資訊"""
    return JSONResponse({
        "message": "AI Chat API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "running"
    })


@app.get("/health", tags=["health"])
async def health_check() -> JSONResponse:
    """健康檢查 endpoint"""
    return JSONResponse({
        "status": "healthy",
        "service": settings.APP_NAME
    })


# 全域例外處理（可選，未來擴充）
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """全域例外處理器"""
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "message": str(exc) if settings.DEBUG else "發生系統錯誤，請稍後再試"
        }
    )
