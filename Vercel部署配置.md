# Vercel部署配置指南

## ✅ 前端已部署到Vercel

根据您的部署页面：https://vercel.com/kingdongqs-projects/oferta-jcx1/7Pjmv7M7zFZPvaHQXx2UTByCN3zt

前端已经成功部署！

## 🔧 需要配置：连接Railway后端

### 步骤1: 获取Railway后端URL

1. 打开Railway Dashboard
2. 找到您的服务
3. 复制生成的URL（例如：`https://xxx.up.railway.app`）

### 步骤2: 在Vercel中配置环境变量

1. 打开Vercel项目：https://vercel.com/kingdongqs-projects/oferta-jcx1
2. 进入 **Settings** → **Environment Variables**
3. 添加以下变量：

```
NEXT_PUBLIC_API_URL = https://your-railway-app.up.railway.app
```

**注意**: 替换 `your-railway-app` 为您的Railway实际URL

### 步骤3: 重新部署

配置环境变量后：
1. 点击 **Deployments**
2. 点击最新部署的 **Redeploy**
3. 或者等待下次Git推送自动部署

## 🔄 或者手动设置API地址

### 方法1: 通过JavaScript设置

在浏览器控制台运行：
```javascript
localStorage.setItem('API_BASE_URL', 'https://your-railway-app.up.railway.app');
location.reload();
```

### 方法2: 修改代码

更新 `login.html` 中的默认API地址：
```javascript
'https://your-railway-app.up.railway.app'
```

替换为您的Railway实际URL。

## 📋 当前配置状态

### ✅ 已完成
- 前端部署到Vercel
- API地址配置代码已更新
- 支持环境变量

### ⏳ 待完成
- [ ] 获取Railway后端URL
- [ ] 在Vercel中配置环境变量
- [ ] 测试前后端连接

## 🧪 测试连接

### 测试步骤
1. 打开Vercel部署的网站
2. 打开浏览器开发者工具（F12）
3. 控制台输入：
```javascript
fetch('https://your-railway-app.up.railway.app/health')
  .then(r => r.json())
  .then(console.log)
```
4. 应该返回：`{"status": "ok"}`

## 💡 完整工作流程

```
用户访问 Vercel前端
    ↓
前端调用 Railway后端API
    ↓
Railway调用 Claude AI
    ↓
返回结果给前端
    ↓
用户看到海报
```

## 🎯 下一步

1. **获取Railway URL**: 从Railway Dashboard复制
2. **配置Vercel环境变量**: 添加API_URL
3. **重新部署**: 让配置生效
4. **测试**: 验证前后端连接

## 📞 需要帮助？

- Railway URL获取问题 → 查看Railway Dashboard
- Vercel配置问题 → 查看Vercel文档
- 连接测试失败 → 检查CORS设置

---

**前端已部署，现在需要连接Railway后端！** 🚀

