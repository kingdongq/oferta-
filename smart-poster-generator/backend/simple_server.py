"""
简化版服务器 - 无需数据库即可运行
适用于快速测试前端功能
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import subprocess

app = FastAPI(title="智能海报生成器 API", version="1.0.0")

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Claude API配置
ANTHROPIC_API_KEY = "f6cc961bee5c423d82957cea7038a8e4.5T6q1s3ZzJaKkl9J"
ANTHROPIC_BASE_URL = "https://open.bigmodel.cn/api/anthropic"


@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "智能海报生成器 API - 简化版",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health():
    """健康检查"""
    return {"status": "ok", "message": "Server is running"}


@app.post("/auth/login")
async def login(username: str = None, password: str = None):
    """简化登录 - 仅用于测试"""
    return JSONResponse({
        "access_token": "test-token",
        "token_type": "bearer",
        "message": "测试模式：登录成功"
    })


@app.post("/auth/register")
async def register(username: str = None, email: str = None, password: str = None):
    """简化注册 - 仅用于测试"""
    return JSONResponse({
        "message": "测试模式：注册成功",
        "username": username,
        "email": email
    })


@app.post("/posters/generate")
async def generate_poster(description: str):
    """使用AI生成海报"""
    import subprocess
    
    prompt = f"请用中文简要分析这个产品需求: {description}"
    
    ps_command = f'''
    $env:ANTHROPIC_BASE_URL="{ANTHROPIC_BASE_URL}"
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
            "status": "generated"
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
    print("Smart Poster Generator - Simplified Server")
    print("=" * 60)
    print("Starting...")
    print("API: http://localhost:8000")
    print("Docs: http://localhost:8000/docs")
    print("=" * 60)
    uvicorn.run(app, host="0.0.0.0", port=8000)

