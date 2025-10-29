#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速原型 - 智能海报生成器
验证核心功能：AI理解 + 图片搜索 + 海报生成
"""

import json
import requests
from pathlib import Path
import sys
import io

# 解决Windows控制台中文编码问题
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Claude API配置
ANTHROPIC_API_KEY = "f6cc961bee5c423d82957cea7038a8e4.5T6q1s3ZzJaKkl9J"
ANTHROPIC_BASE_URL = "https://open.bigmodel.cn/api/anthropic"

# Unsplash API配置 (需要申请)
# 申请地址: https://unsplash.com/developers
# 或者使用 Pexels API (更容易申请): https://www.pexels.com/api/
UNSPLASH_ACCESS_KEY = "YOUR_UNSPLASH_KEY"  # 需要替换
PEXELS_API_KEY = "YOUR_PEXELS_KEY"  # 备选方案，免费且易申请


class SmartPosterGenerator:
    """智能海报生成器核心类"""
    
    def __init__(self):
        self.api_key = ANTHROPIC_API_KEY
        self.base_url = ANTHROPIC_BASE_URL
    
    def understand_product_description(self, description):
        """
        Step 1: 使用Claude AI理解产品描述
        例如: "我需要一个包含10种水果的促销海报"
        """
        import subprocess
        
        prompt = f"""
作为一个专业的巴西超市营销专家，请分析以下产品需求并提取关键信息：

{description}

请以JSON格式返回：
1. 产品列表（名称、类别、建议价格）
2. 促销类型
3. 推荐的海报模板类型
4. 目标受众
"""
        
        # 使用Claude CLI
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
        
        return result.stdout
    
    def search_product_images(self, product_names, use_api=False):
        """
        Step 2: 搜索产品图片
        使用 Unsplash API 或 Pexels API
        """
        images = {}
        
        if use_api and UNSPLASH_ACCESS_KEY != "YOUR_UNSPLASH_KEY":
            # 使用 Unsplash API
            print("使用 Unsplash API 搜索图片...")
            for product in product_names:
                try:
                    url = "https://api.unsplash.com/search/photos"
                    headers = {
                        "Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"
                    }
                    params = {
                        "query": product,
                        "per_page": 1
                    }
                    
                    response = requests.get(url, headers=headers, params=params)
                    if response.status_code == 200:
                        data = response.json()
                        if data.get("results"):
                            images[product] = data["results"][0]["urls"]["regular"]
                            print(f"✓ 找到 {product} 的图片")
                except Exception as e:
                    print(f"✗ 搜索 {product} 失败: {e}")
        else:
            # 使用占位符图片（无需API）
            print("使用占位符图片（无需API密钥）...")
            for product in product_names:
                images[product] = f"https://via.placeholder.com/400x400?text={product.replace(' ', '+')}"
                print(f"✓ 为 {product} 生成占位符")
        
        return images
    
    def select_template(self, product_count):
        """
        Step 3: 根据产品数量选择模板
        参考 QROfertas 的模板选择逻辑
        """
        templates = {
            4: "4 Produtos - 2x2",
            6: "6 Produtos - 3x2",
            8: "8 Produtos - 4x2",
            9: "9 Produtos - 3x3",
            12: "12 Produtos - 4x3",
        }
        
        # 选择最接近的模板
        closest = min(templates.keys(), key=lambda x: abs(x - product_count))
        return templates.get(closest, "4 Produtos - 2x2")
    
    def generate_poster_info(self, description):
        """
        Step 4: 生成完整的海报信息
        整合所有步骤
        """
        print("=" * 60)
        print("智能海报生成器 - 快速原型")
        print("=" * 60)
        
        # Step 1: AI理解
        print("\n步骤1: AI分析产品需求...")
        analysis = self.understand_product_description(description)
        print(f"AI分析结果: {analysis[:200]}...")
        
        # Step 2: 图片搜索
        print("\n步骤2: 搜索产品图片...")
        products = ["banana", "apple", "mango", "pineapple"]  # 使用英文关键词
        images = self.search_product_images(products, use_api=False)  # 先不使用API
        print(f"找到 {len(images)} 张图片")
        
        # Step 3: 选择模板
        print("\n步骤3: 选择海报模板...")
        template = self.select_template(len(products))
        print(f"使用模板: {template}")
        
        # Step 4: 返回结果
        result = {
            "description": description,
            "analysis": analysis,
            "products": products,
            "images": images,
            "template": template,
            "status": "ready"
        }
        
        return result


def main():
    """主函数"""
    generator = SmartPosterGenerator()
    
    # 测试示例
    description = "我需要一个包含10种热带水果的促销海报，价格要便宜，适合巴西超市"
    
    result = generator.generate_poster_info(description)
    
    print("\n" + "=" * 60)
    print("生成结果:")
    print("=" * 60)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    # 保存结果
    output_file = "marketing-reports/poster_result.json"
    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"\n结果已保存到: {output_file}")


if __name__ == "__main__":
    main()

