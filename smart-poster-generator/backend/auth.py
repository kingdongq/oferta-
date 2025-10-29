"""
用户认证模块 - Google登录和Email注册
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
import secrets
from email.mime.text import MIMEText
import smtplib

from .database import get_db
from .models import User
from .schemas import UserCreate, UserResponse, Token
from .config import settings

router = APIRouter(prefix="/auth", tags=["认证"])

# 密码加密
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 配置
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """加密密码"""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """创建JWT token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """获取当前用户"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception
    return user


@router.post("/register", response_model=UserResponse)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    用户注册
    
    支持邮箱注册，将发送验证邮件
    """
    # 检查用户是否已存在
    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    # 检查用户名是否已存在
    if db.query(User).filter(User.username == user_data.username).first():
        raise HTTPException(
            status_code=400,
            detail="Username already taken"
        )
    
    # 创建新用户
    hashed_password = get_password_hash(user_data.password)
    verification_token = secrets.token_urlsafe(32)
    
    db_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password,
        verification_token=verification_token,
        is_verified=False,
        provider="email"
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # 发送验证邮件
    await send_verification_email(db_user.email, verification_token)
    
    return UserResponse.from_orm(db_user)


@router.post("/verify-email")
async def verify_email(token: str, db: Session = Depends(get_db)):
    """验证邮箱"""
    user = db.query(User).filter(User.verification_token == token).first()
    
    if not user:
        raise HTTPException(status_code=400, detail="Invalid token")
    
    user.is_verified = True
    user.verification_token = None
    db.commit()
    
    return {"message": "Email verified successfully"}


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    用户登录
    
    支持用户名或邮箱登录
    """
    # 尝试通过邮箱或用户名查找用户
    user = db.query(User).filter(
        (User.email == form_data.username) | (User.username == form_data.username)
    ).first()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_verified:
        raise HTTPException(
            status_code=403,
            detail="Email not verified"
        )
    
    # 创建token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/google")
async def google_login():
    """
    Google OAuth 登录入口
    """
    from google.oauth2 import id_token
    from google.auth.transport import requests
    
    google_client_id = settings.GOOGLE_CLIENT_ID
    google_auth_url = f"https://accounts.google.com/o/oauth2/v2/auth?client_id={google_client_id}&redirect_uri={settings.GOOGLE_REDIRECT_URI}&response_type=code&scope=openid email profile"
    
    return {"auth_url": google_auth_url}


@router.get("/google/callback")
async def google_callback(code: str, db: Session = Depends(get_db)):
    """
    Google OAuth 回调处理
    """
    from google.auth.transport import requests
    from google.oauth2 import id_token
    
    try:
        # 交换code获取token
        token_url = "https://oauth2.googleapis.com/token"
        token_data = {
            "code": code,
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "redirect_uri": settings.GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code"
        }
        
        token_response = requests.post(token_url, data=token_data)
        token_json = token_response.json()
        id_token_value = token_json["id_token"]
        
        # 验证token并获取用户信息
        idinfo = id_token.verify_oauth2_token(id_token_value, requests.Request(), settings.GOOGLE_CLIENT_ID)
        
        # 检查用户是否已存在
        user = db.query(User).filter(User.email == idinfo["email"]).first()
        
        if not user:
            # 创建新用户
            db_user = User(
                username=idinfo["name"],
                email=idinfo["email"],
                hashed_password=None,
                is_verified=True,
                provider="google",
                google_id=idinfo["sub"]
            )
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            user = db_user
        
        # 创建token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(user.id)}, expires_delta=access_token_expires
        )
        
        return {"access_token": access_token, "token_type": "bearer"}
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


async def send_verification_email(email: str, token: str):
    """发送验证邮件"""
    try:
        verification_url = f"{settings.BASE_URL}/auth/verify-email?token={token}"
        
        msg = MIMEText(f'请点击以下链接验证您的邮箱: {verification_url}')
        msg['Subject'] = '验证您的邮箱'
        msg['From'] = settings.SMTP_USER
        msg['To'] = email
        
        server = smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT)
        server.starttls()
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()
    except Exception as e:
        print(f"Failed to send email: {e}")


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """获取当前用户信息"""
    return UserResponse.from_orm(current_user)


