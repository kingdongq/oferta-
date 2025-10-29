// 智能海报生成器 - 前端JavaScript

document.addEventListener('DOMContentLoaded', function() {
    const generateBtn = document.getElementById('generateBtn');
    const clearBtn = document.getElementById('clearBtn');
    const productDescription = document.getElementById('productDescription');
    const aiAnalysis = document.getElementById('aiAnalysis');
    const productList = document.getElementById('productList');
    const posterPreview = document.getElementById('posterPreview');
    const downloadSection = document.getElementById('downloadSection');
    const downloadBtn = document.getElementById('downloadBtn');

    // 生成海报
    generateBtn.addEventListener('click', async function() {
        const description = productDescription.value.trim();
        const cep = document.getElementById('cep').value;
        
        if (!description) {
            alert('请输入产品描述！');
            return;
        }

        // 显示加载动画
        showLoading(aiAnalysis);
        showLoading(productList);
        showLoading(posterPreview);

        try {
            // 调用后端API
            const response = await fetch('/api/generate-poster', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    description: description,
                    cep: cep
                })
            });

            if (!response.ok) {
                throw new Error('生成失败');
            }

            const result = await response.json();
            
            // 显示AI分析结果
            displayAnalysis(result.analysis);
            
            // 显示产品列表
            displayProducts(result.products, result.images);
            
            // 显示海报预览
            displayPoster(result);
            
            // 显示下载按钮
            downloadSection.style.display = 'block';

        } catch (error) {
            console.error('Error:', error);
            alert('生成失败，请重试！');
        }
    });

    // 清空内容
    clearBtn.addEventListener('click', function() {
        productDescription.value = '';
        aiAnalysis.innerHTML = '<h3>🤖 AI分析</h3><p class="placeholder">请描述您的需求，然后点击"生成海报"</p>';
        productList.innerHTML = '<h3>🛒 产品列表</h3><p class="placeholder">等待生成...</p>';
        posterPreview.innerHTML = '<h3>🖼️ 海报预览</h3><p class="placeholder">等待生成...</p>';
        downloadSection.style.display = 'none';
    });

    // 显示加载动画
    function showLoading(element) {
        element.innerHTML = `
            <div class="loading">
                <div class="spinner"></div>
                <p>正在生成中...</p>
            </div>
        `;
    }

    // 显示AI分析结果
    function displayAnalysis(analysis) {
        aiAnalysis.innerHTML = `
            <h3>🤖 AI分析</h3>
            <div class="content">${formatText(analysis)}</div>
        `;
    }

    // 显示产品列表
    function displayProducts(products, images) {
        let html = '<h3>🛒 产品列表</h3><ul>';
        
        products.forEach(product => {
            const image = images[product] || 'https://via.placeholder.com/100x100?text=' + product;
            html += `
                <li>
                    <img src="${image}" alt="${product}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 5px; margin-right: 10px; vertical-align: middle;">
                    <strong>${product}</strong>
                </li>
            `;
        });
        
        html += '</ul>';
        productList.innerHTML = html;
    }

    // 显示海报预览
    function displayPoster(result) {
        // 这里可以生成Canvas海报
        // 现在先显示简单预览
        posterPreview.innerHTML = `
            <h3>🖼️ 海报预览</h3>
            <div class="content">
                <p><strong>模板:</strong> ${result.template}</p>
                <p><strong>产品数量:</strong> ${result.products.length}</p>
                <p><strong>状态:</strong> ${result.status}</p>
                <div style="margin-top: 20px; padding: 20px; background: white; border-radius: 10px;">
                    <h4>海报布局预览</h4>
                    <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; margin-top: 10px;">
                        ${result.products.map((p, i) => `
                            <div style="padding: 10px; background: #f5f5f5; border-radius: 5px; text-align: center;">
                                <img src="${result.images[p]}" alt="${p}" style="width: 100%; height: 120px; object-fit: cover; border-radius: 5px; margin-bottom: 5px;">
                                <strong>${p}</strong>
                            </div>
                        `).join('')}
                    </div>
                </div>
            </div>
        `;
    }

    // 格式化文本
    function formatText(text) {
        return text.replace(/\n/g, '<br>').replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
    }

    // 下载海报
    downloadBtn.addEventListener('click', function() {
        // TODO: 实现海报下载功能
        alert('海报下载功能开发中...');
    });
});


