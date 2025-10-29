"""
Pydantic schemas
"""

from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """用户基础模型"""
    username: str
    email: EmailStr


class UserCreate(UserBase):
    """创建用户"""
    password: str


class UserResponse(UserBase):
    """用户响应模型"""
    id: int
    is_verified: bool
    provider: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    """Token响应"""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Token数据"""
    user_id: Optional[int] = None


class PosterBase(BaseModel):
    """海报基础模型"""
    title: str
    description: Optional[str] = None
    template: str = "default"


class PosterCreate(PosterBase):
    """创建海报"""
    products: str
    style_config: Optional[str] = None


class PosterResponse(PosterBase):
    """海报响应模型"""
    id: int
    owner_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


