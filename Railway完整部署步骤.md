# Railway完整部署步骤

## 🎯 目标：成功部署到Railway

根据您的Railway项目页面，以下是详细的部署步骤。

## 📋 步骤1：验证GitHub代码（✅ 已完成）

代码已推送到GitHub：
- ✅ 修复了PowerShell依赖
- ✅ 添加了Railway配置文件
- ✅ 代码已更新并推送

**GitHub仓库**: https://github.com/kingdongq/oferta-

## 🔧 步骤2：在Railway中配置

### 2.1 打开Railway项目
访问您的项目页面：
https://railway.com/project/2a71e6b4-1747-4ee9-a4f6-ec6be932660b/service/63ac48d4-16a0-4416-92e0-57fbd5fe15a8

### 2.2 设置源代码（如果还没有）

1. **连接到GitHub**
   - 点击 "Connect GitHub"
   - 选择仓库: `kingdongq/oferta-`
   - 选择分支: `main`

### 2.3 配置服务设置

点击服务 → **Settings** → 配置以下：

#### Root Directory（工作目录）
```
smart-poster-generator/backend
```

#### Build Command（构建命令）
```
pip install -r requirements.txt
```

#### Start Command（启动命令）
```
uvicorn production_server:app --host 0.0.0.0 --port $PORT
```

### 2.4 配置环境变量

点击 **Variables** 标签页，添加：

```
SUPABASE_URL=https://zcpqvzgezobfqwhtvtav.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpjcHF2emdlem9iZnF3aHR2dGF2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjE3MDMxMzEsImV4cCI6MjA3NzI3OTEzMX0.TJ1oeXTSHP5SX9e-Rq4MHk4tFwjpNq9dSGYEbgE6FhI
ANTHROPIC_AUTH_TOKEN=f6cc961bee5c423d82957cea7038a8e4.5T6q1s3ZzJaKkl9J
ANTHROPIC_BASE_URL=https://open.bigmodel.cn/api/anthropic
PORT=8000
```

**重要**: Railway会自动提供`$PORT`变量，无需手动设置。

### 2.5 重新部署

1. 点击 **Deployments**
2. 点击 **Redeploy** 或等待自动部署

## 📊 步骤3：检查部署日志

### 查看构建日志
在Railway Dashboard：
- 点击 **Deployments**
- 选择最新的部署
- 查看 **Build Logs**

### 查看运行日志
- 点击 **Logs** 标签页
- 查看实时日志

### 常见日志信息

#### ✅ 成功标志
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

#### ❌ 错误标志
```
ERROR: Could not import module 'production_server'
ModuleNotFoundError: No module named 'requests'
```

## 🔍 步骤4：验证部署

### 4.1 获取部署URL

Railway会自动分配一个URL，格式：
```
https://your-service-name.up.railway.app
```

### 4.2 测试端点

#### 健康检查
```
GET https://your-app.railway.app/health
```
应该返回：
```json
{"status": "ok", "message": "Server is running", "supabase": "connected"}
```

#### API文档
```
GET https://your-app.railway.app/docs
```

#### 根路径
```
GET https://your-app.railway.app/
```

## 🛠️ 故障排除

### 问题1: 部署失败 - 找不到模块

**解决方案**:
1. 检查 `requirements.txt` 是否包含所有依赖
2. 确保 `Root Directory` 设置为 `smart-poster-generator/backend`

### 问题2: 端口错误

**解决方案**:
- 使用 `$PORT` 变量，不要硬编码端口
- Railway会自动注入正确的端口

### 问题3: 工作目录错误

**解决方案**:
- 在Settings中设置 `Root Directory` 为 `smart-poster-generator/backend`
- 确保 `requirements.txt` 在该目录下

### 问题4: 环境变量未读取

**解决方案**:
- 在Railway Variables中重新添加
- 重启服务让变量生效

## 📝 配置文件说明

### Procfile
```
web: uvicorn production_server:app --host 0.0.0.0 --port $PORT
```
- Railway会识别Procfile
- `$PORT`由Railway自动提供

### nixpacks.toml
```toml
[phases.setup]
nixPkgs = ["python310"]

[phases.install]
cmds = ["pip install -r requirements.txt"]

[start]
cmd = "uvicorn production_server:app --host 0.0.0.0 --port $PORT"
```

### railway.json
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS",
    "buildCommand": "pip install -r smart-poster-generator/backend/requirements.txt"
  },
  "deploy": {
    "startCommand": "cd smart-poster-generator/backend && uvicorn production_server:app --host 0.0.0.0 --port $PORT"
  }
}
```

## ✅ 部署检查清单

在Railway Dashboard中验证：

- [ ] GitHub仓库已连接
- [ ] Root Directory设置为 `smart-poster-generator/backend`
- [ ] Start Command设置为 `uvicorn production_server:app --host 0.0.0.0 --port $PORT`
- [ ] 环境变量已配置（SUPABASE_URL, SUPABASE_KEY, ANTHROPIC_AUTH_TOKEN）
- [ ] 部署状态为 "Active"
- [ ] 日志显示 "Application startup complete"
- [ ] 可以访问健康检查端点

## 🎉 部署成功标志

1. **状态**: Deployments显示 "Active"
2. **日志**: 显示 "Uvicorn running"
3. **URL**: 可以访问并获得响应
4. **健康检查**: `/health` 返回正常

## 🚀 部署后下一步

1. **更新前端**: 修改 `login.html` 中的API地址
2. **测试功能**: 测试所有API端点
3. **配置域名**: 在Railway中设置自定义域名
4. **监控**: 设置错误监控（可选）

## 📞 需要帮助？

如果部署仍然失败：
1. 查看 `Railway部署指南.md`
2. 检查Build Logs中的错误信息
3. 验证环境变量配置
4. 确认工作目录设置

---

**按照以上步骤操作，部署应该会成功！** 🎯

