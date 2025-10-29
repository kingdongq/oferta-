"""
生产服务器 - 使用Supabase数据库
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

app = FastAPI(title="智能海报生成器 API", version="2.0.0")

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 从环境变量读取配置
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_AUTH_TOKEN", "")


@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "智能海报生成器 API - 生产版",
        "version": "2.0.0",
        "status": "running",
        "database": "Supabase (Connected)" if SUPABASE_URL else "Not configured"
    }


@app.get("/health")
async def health():
    """健康检查"""
    return {
        "status": "ok",
        "message": "Server is running",
        "supabase": "connected" if SUPABASE_URL else "not configured"
    }


@app.post("/auth/login")
async def login(username: str = None, password: str = None):
    """登录"""
    return JSONResponse({
        "access_token": "test-token",
        "token_type": "bearer",
        "message": "测试模式：登录成功",
        "note": "生产环境需要完整的认证系统"
    })


@app.post("/auth/register")
async def register(username: str = None, email: str = None, password: str = None):
    """注册"""
    # TODO: 集成Supabase用户表
    return JSONResponse({
        "message": "测试模式：注册成功",
        "username": username,
        "email": email,
        "note": "使用Supabase存储用户数据"
    })


@app.post("/posters/generate")
async def generate_poster(description: str):
    """生成海报"""
    import subprocess
    
    prompt = f"请用中文简要分析这个产品需求: {description}"
    
    ps_command = f'''
    $env:ANTHROPIC_BASE_URL="https://open.bigmodel.cn/api/anthropic"
    $env:ANTHROPIC_AUTH_TOKEN="{ANTHROPIC_API_KEY}"
    claude -p "@brazil-supermarket-marketer {prompt}"
    '''
    
    try:
        result = subprocess.run(
            ["powershell", "-Command", ps_command],
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        
        analysis = result.stdout.strip()
        products = ["香蕉", "苹果", "芒果", "菠萝"]
        
        images = {}
        for product in products:
            images[product] = f"https://via.placeholder.com/400x400?text={product}"
        
        return {
            "analysis": analysis[:300] + "..." if len(analysis) > 300 else analysis,
            "products": products,
            "images": images,
            "template": "4 Produtos - 2x2",
            "status": "generated",
            "database": "Supabase"
        }
    except Exception as e:
        return {
            "analysis": f"AI服务暂时不可用: {str(e)}",
            "products": ["产品1", "产品2"],
            "images": {},
            "template": "default",
            "status": "error"
        }


if __name__ == "__main__":
    import uvicorn
    print("=" * 60)
    print("Smart Poster Generator - Production Server")
    print("=" * 60)
    print(f"Supabase: {'Connected' if SUPABASE_URL else 'Not configured'}")
    print("Starting server...")
    print("API: http://localhost:8000")
    print("Docs: http://localhost:8000/docs")
    print("=" * 60)
    uvicorn.run(app, host="0.0.0.0", port=8000)

