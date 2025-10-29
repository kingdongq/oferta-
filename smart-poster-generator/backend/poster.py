"""
海报生成和处理模块
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import requests
import subprocess
import json

from .database import get_db
from .models import Poster, User
from .schemas import PosterCreate, PosterResponse
from .auth import get_current_user
from .config import settings

router = APIRouter(prefix="/posters", tags=["海报"])


def call_claude_agent(description: str):
    """调用Claude AI生成营销策略"""
    import subprocess
    
    prompt = f"请用中文分析这个产品需求并生成海报策略: {description}"
    
    ps_command = f'''
    $env:ANTHROPIC_BASE_URL="{settings.ANTHROPIC_BASE_URL}"
    $env:ANTHROPIC_AUTH_TOKEN="{settings.ANTHROPIC_API_KEY}"
    claude -p "@brazil-supermarket-marketer {prompt}"
    '''
    
    try:
        result = subprocess.run(
            ["powershell", "-Command", ps_command],
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        return result.stdout.strip()
    except Exception as e:
        return f"AI分析失败: {str(e)}"


@router.post("/generate", response_model=dict)
async def generate_poster(
    description: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    使用AI生成海报
    """
    # 调用AI生成策略
    ai_analysis = call_claude_agent(description)
    
    # 提取产品信息（简化版）
    products = ["香蕉", "苹果", "芒果", "菠萝"]  # 实际应从AI分析中提取
    
    # 生成图片URL（占位符）
    images = {}
    for product in products:
        images[product] = f"https://via.placeholder.com/400x400?text={product}"
    
    # 选择模板
    template = "4 Produtos - 2x2" if len(products) <= 4 else "8 Produtos - 4x2"
    
    return {
        "analysis": ai_analysis,
        "products": products,
        "images": images,
        "template": template,
        "status": "generated"
    }


@router.post("/create", response_model=PosterResponse)
async def create_poster(
    poster_data: PosterCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    保存海报到数据库
    """
    db_poster = Poster(
        title=poster_data.title,
        description=poster_data.description,
        products=poster_data.products,
        template=poster_data.template,
        owner_id=current_user.id,
        style_config=poster_data.style_config
    )
    
    db.add(db_poster)
    db.commit()
    db.refresh(db_poster)
    
    return db_poster


@router.get("/", response_model=List[PosterResponse])
async def get_user_posters(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取用户的所有海报
    """
    posters = db.query(Poster).filter(Poster.owner_id == current_user.id).all()
    return posters


@router.get("/{poster_id}", response_model=PosterResponse)
async def get_poster(
    poster_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取单个海报详情
    """
    poster = db.query(Poster).filter(
        Poster.id == poster_id,
        Poster.owner_id == current_user.id
    ).first()
    
    if not poster:
        raise HTTPException(status_code=404, detail="Poster not found")
    
    return poster

