#!/bin/bash
# Claude Code 第三方API配置脚本 (Git Bash版本)

# 设置第三方API端点
export ANTHROPIC_BASE_URL="https://open.bigmodel.cn/api/anthropic"
export ANTHROPIC_AUTH_TOKEN="f6cc961bee5c423d82957cea7038a8e4.5T6q1s3ZzJaKkl9J"

echo "Claude Code 第三方API配置已设置"
echo "API Base URL: $ANTHROPIC_BASE_URL"
echo ""
echo "现在可以运行: claude"
echo "或者运行: claude -p '你的问题'"

