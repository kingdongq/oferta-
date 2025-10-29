# Stripe密钥配置说明

## 🔑 Stripe密钥类型

### 1. 公钥（Publishable Key）

**用途**: 前端JavaScript代码中使用
- **前缀**: `pk_test_...` 或 `pk_live_...`
- **安全性**: ✅ 可以暴露在前端代码中
- **使用位置**: HTML/JavaScript 文件中

**示例**:
```javascript
// 前端代码 - 可以安全暴露
const stripe = Stripe('pk_test_51AbCdEfGhIjKlMnO...');
```

### 2. 私钥（Secret Key）

**用途**: 后端服务器端使用
- **前缀**: `sk_test_...` 或 `sk_live_...`
- **安全性**: ⚠️ 必须严格保密，永远不要暴露
- **使用位置**: 后端环境变量

**示例**:
```python
# 后端代码 - 从环境变量读取
import stripe
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')  # sk_test_...
```

## 📋 配置方法

### 前端配置（Vercel）

在Vercel项目 → Settings → Environment Variables 添加：

```
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY = pk_test_51AbCdEfGhIjKlMnO...
```

**命名注意**: 使用 `NEXT_PUBLIC_` 前缀使变量在前端可用

### 后端配置（Railway）

在Railway项目 → Variables 添加：

```
STRIPE_SECRET_KEY = sk_test_51AbCdEfGhIjKlMnO...
```

**安全提示**: 永远不要提交私钥到GitHub

## 🎯 使用场景

### 前端需要（公钥）
- ✅ 收集支付信息（卡号、过期日期等）
- ✅ 创建支付意图
- ✅ 显示支付表单

### 后端需要（私钥）
- ✅ 处理支付确认
- ✅ 创建订阅
- ✅ 管理客户
- ✅ 处理退款
- ✅ 访问支付历史

## 🔒 安全最佳实践

### ✅ 正确做法
1. 公钥在前端：使用 `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY`
2. 私钥在后端：使用环境变量 `STRIPE_SECRET_KEY`
3. 私钥加密：使用Vercel/Railway的环境变量功能
4. .gitignore：确保.env文件不被提交

### ❌ 错误做法
1. ❌ 私钥放在前端代码
2. ❌ 私钥提交到GitHub
3. ❌ 在日志中打印私钥
4. ❌ 在API响应中返回私钥

## 💡 实际配置示例

### 前端代码（login.html或相关文件）

```javascript
// 使用公钥
const stripe = Stripe(process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY);

// 创建支付
const {error} = await stripe.redirectToCheckout({
  sessionId: sessionId
});
```

### 后端代码（production_server.py）

```python
import stripe
import os

# 从环境变量读取私钥
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

# 创建支付会话
@app.post("/create-checkout-session")
async def create_checkout():
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': 'Professional Plan',
                },
                'unit_amount': 1900,  # $19.00
            },
            'quantity': 1,
        }],
        mode='subscription',
        success_url='https://your-site.com/success',
        cancel_url='https://your-site.com/cancel',
    )
    return {'sessionId': session.id}
```

## 📝 Stripe密钥获取

### 1. 登录Stripe Dashboard
访问: https://dashboard.stripe.com/test/apikeys

### 2. 获取密钥
- **测试模式**:
  - 公钥: `pk_test_...`
  - 私钥: `sk_test_...`

- **生产模式**:
  - 公钥: `pk_live_...`
  - 私钥: `sk_live_...`

### 3. 复制密钥
点击 "Reveal test key" 查看完整密钥

## 🚀 快速配置

### Vercel环境变量
```
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_51AbCdEf...
```

### Railway环境变量
```
STRIPE_SECRET_KEY=sk_test_51AbCdEf...
```

## 🎯 总结

- **前端** = 公钥（`pk_`开头）- 可以暴露
- **后端** = 私钥（`sk_`开头）- 必须保密

**记住**: 私钥就像密码，永远不要公开！

