# Railway部署方案 - 使用Docker

## 🎯 情况说明

Railway默认使用Docker构建，找不到Nixpacks选项是正常的。

## ✅ 解决方案

### 方案1: 使用根目录Dockerfile（推荐）

如果在**项目根目录**部署：

1. **Root Directory**: 设置为 `.` 或留空
2. **Railway会自动使用**: 根目录的 `Dockerfile`
3. **已创建**: `Dockerfile`（在根目录）

### 方案2: 使用backend目录Dockerfile

如果在**backend目录**部署：

1. **Root Directory**: 设置为 `smart-poster-generator/backend`
2. **Railway会自动使用**: `smart-poster-generator/backend/Dockerfile`
3. **已创建**: `smart-poster-generator/backend/Dockerfile`

## 🛠️ Railway配置步骤

### 步骤1: 设置工作目录

**选项A - 根目录部署**:
- Root Directory: `.` 或留空
- 使用: 根目录 `Dockerfile`

**选项B - Backend目录部署**（推荐）:
- Root Directory: `smart-poster-generator/backend`
- 使用: `backend/Dockerfile`

### 步骤2: 不设置构建命令

- **Build Command**: 留空（Dockerfile会处理）
- **Start Command**: 留空（Dockerfile CMD会处理）

### 步骤3: 配置环境变量

在 **Variables** 标签页添加：

```
SUPABASE_URL=https://zcpqvzgezobfqwhtvtav.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpjcHF2emdlem9iZnF3aHR2dGF2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjE3MDMxMzEsImV4cCI6MjA3NzI3OTEzMX0.TJ1oeXTSHP5SX9e-Rq4MHk4tFwjpNq9dSGYEbgE6FhI
ANTHROPIC_AUTH_TOKEN=f6cc961bee5c423d82957cea7038a8e4.5T6q1s3ZzJaKkl9J
PORT=8000
```

**注意**: Railway会自动提供`PORT`，但可以设置默认值。

### 步骤4: 重新部署

Railway会自动：
1. 检测Dockerfile
2. 构建Docker镜像
3. 启动容器

## 📋 两个Dockerfile说明

### 根目录Dockerfile
用于从项目根目录部署，会自动进入backend目录。

### backend/Dockerfile  
用于Root Directory设置为`smart-poster-generator/backend`时使用。

## 🔍 验证部署

部署成功标志：
```
✓ Building Docker image
✓ Starting container
✓ Server running on port 8000
```

## 💡 推荐配置

**建议使用方案B**：
- Root Directory: `smart-poster-generator/backend`
- Build Command: （留空）
- Start Command: （留空）
- 环境变量: 已配置

这样Railway会使用`smart-poster-generator/backend/Dockerfile`。

## 🚀 立即操作

1. 打开Railway Dashboard
2. Settings → Source
3. Root Directory 设置为: `smart-poster-generator/backend`
4. Settings → Deploy → 清空 Build Command 和 Start Command
5. Variables 标签添加环境变量
6. 点击 Redeploy

**代码已包含两个Dockerfile，现在应该可以部署了！** ✅

