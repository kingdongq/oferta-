#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
后端API服务器 - 为前端提供API接口
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import json
import sys
import io

# 解决中文编码问题
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

app = Flask(__name__)
CORS(app)  # 允许跨域请求

# Claude API配置
ANTHROPIC_API_KEY = "f6cc961bee5c423d82957cea7038a8e4.5T6q1s3ZzJaKkl9J"
ANTHROPIC_BASE_URL = "https://open.bigmodel.cn/api/anthropic"


def call_claude_agent(description, cep="11720-090"):
    """调用Claude Agent生成海报"""
    import subprocess
    
    prompt = f"请用中文分析这个产品需求并生成海报策略: {description}"
    
    ps_command = f'''
    $env:ANTHROPIC_BASE_URL="{ANTHROPIC_BASE_URL}"
    $env:ANTHROPIC_AUTH_TOKEN="{ANTHROPIC_API_KEY}"
    claude -p "@brazil-supermarket-marketer {prompt}"
    '''
    
    result = subprocess.run(
        ["powershell", "-Command", ps_command],
        capture_output=True,
        text=True,
        encoding='utf-8'
    )
    
    return result.stdout.strip()


@app.route('/')
def index():
    """首页"""
    return '''
    <h1>智能海报生成器 API</h1>
    <p>访问前端: <a href="/index.html">/index.html</a></p>
    '''


@app.route('/api/generate-poster', methods=['POST'])
def generate_poster():
    """生成海报API"""
    try:
        data = request.json
        description = data.get('description', '')
        cep = data.get('cep', '11720-090')
        
        if not description:
            return jsonify({'error': '描述不能为空'}), 400
        
        # 调用AI分析
        analysis = call_claude_agent(description, cep)
        
        # 模拟产品列表（实际应该从AI分析中提取）
        products = ["banana", "apple", "mango", "pineapple"]
        images = {}
        for product in products:
            images[product] = f"https://via.placeholder.com/400x400?text={product}"
        
        # 构建响应
        result = {
            'status': 'success',
            'analysis': analysis[:500] + '...',  # 截断以便显示
            'products': products,
            'images': images,
            'template': '4 Produtos - 2x2',
            'cep': cep
        }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health():
    """健康检查"""
    return jsonify({'status': 'ok', 'message': 'API运行正常'})


if __name__ == '__main__':
    print("启动智能海报生成器API服务器...")
    print("前端地址: http://localhost:8080/index.html")
    print("API地址: http://localhost:8080/api/generate-poster")
    app.run(host='0.0.0.0', port=8080, debug=True)


