# Railway部署指南

## ⚠️ 部署失败修复

### 问题诊断

根据Railway项目页面，可能的问题：
1. ❌ 使用了PowerShell命令（Railway是Linux环境）
2. ❌ 依赖claude CLI（Railway环境不存在）
3. ❌ 工作目录配置错误
4. ❌ 启动命令不正确

### ✅ 已修复

#### 1. 修复了production_server.py
- ✅ 移除PowerShell依赖
- ✅ 使用HTTP API调用Claude
- ✅ Railway Linux环境兼容

#### 2. 创建了配置文件
- ✅ `Procfile` - Railway启动命令
- ✅ `nixpacks.toml` - Railway构建配置
- ✅ `railway.json` - Railway项目配置

#### 3. 更新了依赖
- ✅ 移除了不必要的flask-cors
- ✅ 确保所有依赖兼容

## 🚀 重新部署步骤

### 第一步：提交修复
```bash
git add .
git commit -m "Fix Railway deployment - remove PowerShell dependency"
git push
```

### 第二步：在Railway配置

1. **设置工作目录**
   - Settings → Source → Root Directory
   - 设置为: `smart-poster-generator/backend`

2. **设置启动命令**
   - Settings → Deploy → Start Command
   - 设置为: `uvicorn production_server:app --host 0.0.0.0 --port $PORT`

3. **配置环境变量**
   - Settings → Variables
   - 添加:
     ```
     SUPABASE_URL=https://zcpqvzgezobfqwhtvtav.supabase.co
     SUPABASE_KEY=your-supabase-key
     ANTHROPIC_AUTH_TOKEN=your-claude-key
     PORT=8000
     ```

### 第三步：重新部署
点击 "Deploy" 或等待自动部署

## 🔧 如果仍然失败

### 检查日志
在Railway中查看Build Logs和Deploy Logs

### 常见问题

#### 问题1: 找不到模块
```
解决方案: 确保requirements.txt所有依赖都在
```

#### 问题2: 端口错误
```
解决方案: 使用$PORT环境变量，不要硬编码
```

#### 问题3: 工作目录错误
```
解决方案: 设置为smart-poster-generator/backend
```

## 📝 配置文件说明

### Procfile
```
web: uvicorn production_server:app --host 0.0.0.0 --port $PORT
```

### nixpacks.toml
```toml
[phases.setup]
nixPkgs = ["python310"]

[phases.install]
cmds = ["pip install -r requirements.txt"]

[start]
cmd = "uvicorn production_server:app --host 0.0.0.0 --port $PORT"
```

## ✅ 验证部署

部署成功后：
1. 访问健康检查: `https://your-app.railway.app/health`
2. 应该返回: `{"status": "ok"}`
3. 访问API文档: `https://your-app.railway.app/docs`

## 💡 提示

- Railway会自动检测Python项目
- 确保requirements.txt在正确位置
- PORT变量由Railway自动提供
- 查看日志找出具体错误

现在可以重新部署了！

