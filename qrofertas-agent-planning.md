# QROfertas Agent 开发计划

## 项目概览

基于 https://www.qrofertas.com/criar-jornal/builder-v2/ 创建一个更智能的自动化海报生成系统，通过 AI Agent 理解产品需求并自动生成海报。

## 核心功能

### 现有 QROfertas 功能
- 手动上传产品图片
- 选择模板
- 手动编辑海报
- 生成多种格式（TV、社交媒体、打印）

### 新增加的 Agent 功能
- **自动理解产品需求**：通过自然语言描述产品
- **自动搜索产品图片**：从网络获取产品图片
- **自动匹配模板**：根据产品类型选择合适模板
- **自动生成海报**：无需手动编辑

## 需要准备的资源

### 1. 技术栈

#### 前端 (海报生成)
- **React/Vue.js** + **Fabric.js** 或 **Konva.js**（画布编辑）
- 或使用 **Canvas API** 进行图像合成
- **React/Vue 3** 用于现代UI

#### 后端 (API服务)
- **Node.js + Express** 或 **Python + FastAPI**
- 处理AI Agent逻辑
- 图片处理和模板管理

#### AI服务
- **Claude API** 或 **GPT-4** - 理解产品描述
- **图像搜索API**:
  - Google Custom Search API
  - Bing Image Search API
  - Unsplash API (免费图片)
  - Pixabay API (免费图片)
- **图像识别API** (可选):
  - Google Vision API - 产品识别
  - AWS Rekognition - 图像分析

### 2. 数据准备

#### 产品数据库
- 产品分类体系
- 产品图片库（备用）
- 模板库（类似QROfertas）

#### 模板系统
参考 QROfertas 的模板类型：
- Encarte feed facebook (quadrado)
- Formato para status e stories
- Formato feed/reels instagram
- Vídeo tabela rede social
- Encarte grande para impressão
- Encarte a4 para impressão
- Cartaz a4 vertical/horizontal
- Formato para tv horizontal/vertical
- Vídeo tabela tv

### 3. AI Agent 架构

```
用户输入
  ↓
AI Agent (Claude/GPT)
  ↓
理解需求 → 提取产品信息 → 搜索图片 → 选择模板
  ↓
生成海报 → 返回给用户
```

#### Agent 工作流程
1. **输入解析**:
   - 自然语言产品描述
   - 例如："我需要10种水果促销海报"
   
2. **智能理解**:
   - 识别产品类别（水果、蔬菜、肉类等）
   - 识别促销类型（BOGO、折扣、清仓等）
   - 提取关键信息（价格、期限等）

3. **图片搜索**:
   - 使用搜索引擎API获取产品图片
   - 质量控制（分辨率、背景、角度）
   - 图片预处理（裁剪、背景移除）

4. **模板匹配**:
   - 根据产品数量和类型选择模板
   - 动态调整布局

5. **海报生成**:
   - Canvas合成
   - 文字叠加
   - 品牌元素添加

### 4. 功能模块设计

#### 模块1: 产品理解 Agent
```python
# 伪代码
class ProductUnderstandingAgent:
    def analyze(self, description):
        # 使用 Claude API 分析产品描述
        # 返回: 产品列表、类别、促销信息
        pass
```

#### 模块2: 图片搜索 Agent
```python
class ImageSearchAgent:
    def search(self, product_name, category):
        # 使用 Google/Bing API 搜索产品图片
        # 返回: 图片URL列表
        pass
```

#### 模块3: 模板选择 Agent
```python
class TemplateSelectionAgent:
    def select_template(self, product_count, category):
        # 根据产品数量和类型选择最佳模板
        # 返回: 模板配置
        pass
```

#### 模块4: 海报生成 Agent
```python
class PosterGenerationAgent:
    def generate(self, products, template, images):
        # 使用 Canvas 生成海报
        # 返回: 海报图片
        pass
```

### 5. 需要的API Key

#### Claude API (已配置)
- 当前Token: `f6cc961bee5c423d82957cea7038a8e4.5T6q1s3ZzJaKkl9J`
- 需要切换到官方Claude API或继续使用智谱AI

#### 图片搜索API
1. **Google Custom Search**:
   - 申请: https://console.cloud.google.com/
   - 需要 API Key
   - 免费配额: 100次/天

2. **Bing Image Search**:
   - 申请: https://www.microsoft.com/en-us/bing/apis/bing-image-search-api
   - 免费配额有限

3. **Unsplash API** (推荐，免费):
   - 申请: https://unsplash.com/developers
   - 免费但需要认证

#### 图像处理服务
- **Remove.bg API** (去除背景): https://www.remove.bg/api
- **Cloudinary** (图片存储和处理): https://cloudinary.com/

### 6. 基础设施

#### 开发环境
- **代码仓库**: GitHub/GitLab
- **本地开发**: 
  - Node.js 18+ / Python 3.9+
  - Docker (可选)

#### 部署
- **前端**: Vercel / Netlify
- **后端**: Railway / Render / VPS
- **数据库**: PostgreSQL / MongoDB
- **文件存储**: AWS S3 / Cloudinary

### 7. 项目结构

```
smart-poster-generator/
├── frontend/                # React/Vue 前端
│   ├── src/
│   │   ├── components/     # 组件
│   │   ├── agent/          # Agent交互
│   │   ├── canvas/         # 画布编辑
│   │   └── templates/       # 模板
│   └── package.json
├── backend/                # Node.js/Python 后端
│   ├── src/
│   │   ├── agents/         # AI Agents
│   │   ├── api/            # API路由
│   │   ├── services/       # 业务逻辑
│   │   └── utils/          # 工具函数
│   └── requirements.txt / package.json
├── database/               # 数据库schema
├── templates/              # 海报模板
└── docs/                   # 文档
```

### 8. 开发步骤

#### 第一阶段 (2周)
1. ✅ 搭建前端基础框架
2. ✅ 集成 Claude API
3. ✅ 实现基础Canvas编辑
4. ✅ 创建几个基础模板

#### 第二阶段 (2周)
1. ✅ 实现图片搜索功能
2. ✅ 产品理解Agent
3. ✅ 模板自动匹配
4. ✅ 海报自动生成

#### 第三阶段 (2周)
1. ✅ 优化图片质量
2. ✅ 添加AI抠图功能
3. ✅ 批量生成功能
4. ✅ 格式导出（PDF、JPG等）

#### 第四阶段 (持续)
1. ✅ 用户系统
2. ✅ 模板市场
3. ✅ 协作功能
4. ✅ 数据分析

### 9. 技术挑战

#### 挑战1: 图片质量
- 解决方案: 使用多个图片来源，设置质量过滤

#### 挑战2: 模板适配
- 解决方案: 动态布局引擎，智能调整

#### 挑战3: 文字排版
- 解决方案: 使用成熟的文字排版算法（如后端渲染）

#### 挑战4: 性能优化
- 解决方案: 缓存常用图片、CDN、懒加载

### 10. 成本估算

#### 开发成本
- AI API: $50-200/月 (Claude/GPT)
- 图片搜索API: $0-50/月 (免费配额可能够用)
- 存储: $10-50/月
- 托管: $5-20/月

#### 总计
- **MVP版本**: ~$65-320/月
- **生产版本**: ~$200-500/月

### 11. 立即开始的步骤

#### 第一步 (今天)
1. 创建项目结构
2. 申请API密钥
3. 搭建基础开发环境

#### 第二步 (本周)
1. 实现Claude API集成
2. 创建基础前端
3. 实现一个简单的海报生成器

#### 第三步 (下周)
1. 添加图片搜索功能
2. 实现Agent逻辑
3. 测试完整流程

### 12. 竞品分析

#### QROfertas 现有功能
- ✅ 丰富的模板库
- ✅ 多种输出格式
- ✅ 简单易用
- ❌ 需要手动操作
- ❌ 需要上传图片

#### 我们的优势
- ✅ AI自动理解
- ✅ 自动搜索图片
- ✅ 全自动生成
- ✅ 无需手动操作

### 13. 快速原型建议

创建一个简化版本来验证概念：

```python
# 快速原型 - Python版
import anthropic
import requests

class QuickPosterGenerator:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key="YOUR_KEY")
    
    def generate_poster(self, description):
        # 1. 让AI理解需求
        response = self.client.messages.create(
            model="claude-3-sonnet-20241022",
            messages=[{
                "role": "user",
                "content": f"请分析这个产品需求: {description}"
            }]
        )
        
        # 2. 提取产品列表
        products = self.extract_products(response)
        
        # 3. 搜索图片
        images = self.search_images(products)
        
        # 4. 生成海报
        poster = self.create_poster(products, images)
        
        return poster
```

## 总结

### 必须准备
1. ✅ Claude API Key (已有)
2. ⏳ Google Custom Search API 或 Bing Search API
3. ⏳ 图片处理服务 (Remove.bg 或类似)
4. ⏳ 前端框架选择 (React 推荐)
5. ⏳ 后端框架选择 (Python FastAPI 推荐)

### 可选准备
- 产品数据库
- 模板库
- 用户认证系统

### 立即行动
我建议创建一个快速原型来验证整个流程！

