# Railway根目录Dockerfile
FROM python:3.10-slim

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# 设置工作目录
WORKDIR /app

# 复制backend目录
COPY smart-poster-generator/backend/ ./backend/

# 切换到backend目录
WORKDIR /app/backend

# 安装Python依赖
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 暴露端口
EXPOSE ${PORT:-8000}

# 启动命令
CMD uvicorn production_server:app --host 0.0.0.0 --port ${PORT:-8000}

