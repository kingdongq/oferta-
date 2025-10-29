# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概览

这是一个**Claude Code开发环境配置项目**，专注于构建AI辅助开发平台，集成了智谱AI作为第三方API服务。项目包含完整的开发工具链配置和针对巴西市场的专业化AI代理系统。

## 技术架构

### 核心组件
- **开发环境**: VSCode + Git Bash + Cursor IDE
- **AI服务**: Claude Code CLI + 智谱AI API
- **代理系统**: 三个专业化AI代理（HR、金融、营销）
- **配置管理**: 跨平台环境变量和任务自动化

### 项目结构
```
D:\Nova\
├── .claude/                    # Claude Code配置
│   ├── agents/                  # AI代理定义
│   └── settings.local.json      # 权限配置
├── .vscode/                     # VSCode配置
│   ├── settings.json           # IDE设置和环境变量
│   ├── tasks.json              # 预定义任务
│   └── 构思.md                 # 项目规划文档
├── claude_config.bat/sh        # 环境配置脚本
└── cursor_settings.json        # Cursor IDE配置
```

## 常用命令

### 启动Claude Code
```bash
# 交互模式
claude

# 打印模式（单次查询）
claude -p "你的问题"

# 通过VSCode任务运行
# Ctrl+Shift+P → Tasks: Run Task → "启动Claude Code" 或 "Claude Code - 打印模式"
```

### 环境配置
```bash
# Windows
claude_config.bat

# Linux/Mac
./claude_config.sh
```

## 环境变量配置

项目使用智谱AI作为第三方API服务，关键环境变量：
- `ANTHROPIC_BASE_URL`: `https://open.bigmodel.cn/api/anthropic`
- `ANTHROPIC_AUTH_TOKEN`: 配置在VSCode settings和脚本中

## AI代理系统

项目包含三个专业化AI代理，位于`.claude/agents/`：

1. **brazil-hr-specialist**: 巴西HR专家
   - 劳工法律合规和员工争议处理
   - 简历收集、数据库管理和候选人筛选
   - 巴西劳动法专业知识

2. **brazilian-finance-analyst**: 巴西金融分析师
   - 财务分析和投资规划
   - 巴西金融市场专业建议
   - 公司财务绩效分析

3. **brazil-supermarket-marketer**: 巴西超市营销专家
   - 基于实时天气的营销策略
   - 巴西节假日促销活动规划
   - 特定地区的零售市场分析

使用方法：通过Task工具调用相应的subagent_type

## 开发环境配置

### VSCode配置
- 默认终端：Git Bash
- 环境变量：自动配置智谱AI API
- 预定义任务：Claude Code启动和打印模式

### 权限管理
- 配置文件：`.claude/settings.local.json`
- 允许特定的文件和系统操作
- 安全的API密钥管理

## 项目规划

详细的发展路线图位于`.vscode/构思.md`，包括：
- 短期目标（1-2周）：文档完善、模板创建
- 中期目标（1个月）：工具集成、质量检查
- 长期目标（3个月）：自定义扩展、团队规范

## 特殊注意事项

1. **第三方API**: 使用智谱AI而非官方Anthropic API
2. **巴西市场专注**: 代理系统专门针对巴西市场设计
3. **跨平台兼容**: 支持Windows和Linux/Mac环境
4. **模块化设计**: 代理系统可扩展和自定义
5. **安全配置**: API密钥通过环境变量安全管理