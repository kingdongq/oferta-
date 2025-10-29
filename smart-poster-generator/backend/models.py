"""
数据库模型
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    """用户模型"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=True)  # Google登录用户可能没有密码
    is_verified = Column(Boolean, default=False)
    verification_token = Column(String, nullable=True)
    
    # OAuth信息
    provider = Column(String, default="email")  # email, google
    google_id = Column(String, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 关联关系
    posters = relationship("Poster", back_populates="owner")


class Poster(Base):
    """海报模型"""
    __tablename__ = "posters"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    products = Column(Text)  # JSON格式存储产品列表
    template = Column(String, default="default")
    style_config = Column(Text)  # JSON格式存储样式配置
    
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="posters")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    is_public = Column(Boolean, default=False)


