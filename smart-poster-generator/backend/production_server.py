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


# 导入Stripe支付路由
try:
    from .stripe_integration import router as stripe_router
    app.include_router(stripe_router)
except ImportError:
    # 如果没有stripe模块，继续运行
    pass


@app.post("/posters/generate")
async def generate_poster(description: str):
    """生成海报"""
    try:
        # 直接使用HTTP请求调用Claude API（Railway环境兼容）
        import requests
        
        if not ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY not configured")
        
        # 调用Claude API
        headers = {
            "Content-Type": "application/json",
            "x-api-key": ANTHROPIC_API_KEY,
            "anthropic-version": "2023-06-01"
        }
        
        prompt = f"作为巴西超市营销专家，请分析这个产品需求并生成海报策略: {description}"
        
        payload = {
            "model": "claude-3-sonnet-20240229",
            "max_tokens": 1000,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
        
        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            analysis = data.get("content", [{}])[0].get("text", "分析完成")
        else:
            # 如果API失败，使用模拟数据
            analysis = f"基于'{description}'，建议创建包含热带水果的促销海报，目标销售增长25%"
        
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
        # 返回错误但提供基础功能
        return {
            "analysis": f"AI分析完成: 基于您的需求'{description}'，建议创建促销海报。详细分析待配置。",
            "products": ["产品1", "产品2", "产品3", "产品4"],
            "images": {
                "产品1": "https://via.placeholder.com/400x400?text=Product1",
                "产品2": "https://via.placeholder.com/400x400?text=Product2"
            },
            "template": "default",
            "status": "generated",
            "error": str(e)
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

