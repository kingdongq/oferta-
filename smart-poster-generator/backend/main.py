"""
FastAPI 主应用
"""

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from .auth import router as auth_router
from .database import Base, engine

# 创建数据库表
Base.metadata.create_all(bind=engine)

app = FastAPI(title="智能海报生成器 API", version="1.0.0")

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8080", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth_router)

# 导入海报路由
try:
    from .poster import router as poster_router
    app.include_router(poster_router)
except ImportError:
    # 如果没有海报模块，继续运行
    pass

@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "智能海报生成器 API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


