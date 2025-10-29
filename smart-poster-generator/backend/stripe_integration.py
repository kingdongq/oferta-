"""
Stripe支付集成模块
"""

import stripe
import os
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional

# 从环境变量读取Stripe密钥
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

router = APIRouter(prefix="/stripe", tags=["支付"])


@router.post("/create-checkout-session")
async def create_checkout_session(
    price_id: Optional[str] = None,
    amount: Optional[int] = 1900,  # $19.00
    plan_type: str = "pro"  # pro or enterprise
):
    """
    创建Stripe支付会话
    
    计划类型:
    - pro: $19/月
    - enterprise: $99/月
    """
    
    if not stripe.api_key:
        raise HTTPException(status_code=500, detail="Stripe未配置")
    
    try:
        # 根据计划类型设置价格
        prices = {
            "pro": {
                "amount": 1900,  # $19.00
                "name": "专业版 - Pro Plan"
            },
            "enterprise": {
                "amount": 9900,  # $99.00
                "name": "企业版 - Enterprise Plan"
            }
        }
        
        plan = prices.get(plan_type, prices["pro"])
        
        # 创建支付会话
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': plan["name"],
                        'description': '智能海报生成器订阅',
                    },
                    'unit_amount': amount or plan["amount"],
                    'recurring': {
                        'interval': 'month',
                    },
                },
                'quantity': 1,
            }],
            mode='subscription',
            success_url=os.getenv('STRIPE_SUCCESS_URL', 'https://your-app.vercel.app/success?session_id={CHECKOUT_SESSION_ID}'),
            cancel_url=os.getenv('STRIPE_CANCEL_URL', 'https://your-app.vercel.app/cancel'),
            metadata={
                'plan_type': plan_type
            }
        )
        
        return {
            "sessionId": session.id,
            "url": session.url,
            "publishableKey": os.getenv("STRIPE_PUBLISHABLE_KEY")
        }
        
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/webhook")
async def stripe_webhook(request: dict):
    """
    Stripe Webhook处理
    用于接收支付状态更新
    """
    # TODO: 验证webhook签名
    # TODO: 处理订阅创建、更新、取消等事件
    
    event = request.get('type')
    
    if event == 'checkout.session.completed':
        # 支付完成，激活订阅
        session = request.get('data', {}).get('object', {})
        customer_id = session.get('customer')
        # TODO: 更新用户订阅状态
        
    elif event == 'customer.subscription.deleted':
        # 订阅取消
        subscription = request.get('data', {}).get('object', {})
        # TODO: 取消用户订阅
        
    return {"status": "ok"}


@router.get("/plans")
async def get_plans():
    """
    获取可用的订阅计划
    """
    return {
        "plans": [
            {
                "id": "free",
                "name": "免费版",
                "price": 0,
                "features": ["5张海报/月", "基础模板", "水印导出"]
            },
            {
                "id": "pro",
                "name": "专业版",
                "price": 19,
                "features": ["无限生成", "所有模板", "无水印导出", "高清导出"]
            },
            {
                "id": "enterprise",
                "name": "企业版",
                "price": 99,
                "features": ["全部专业版功能", "团队协作", "API访问", "优先支持"]
            }
        ],
        "publishableKey": os.getenv("STRIPE_PUBLISHABLE_KEY")
    }

