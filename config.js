// API配置 - 根据环境自动切换
const API_CONFIG = {
  // 开发环境（本地）
  development: {
    API_BASE_URL: 'http://localhost:8000',
  },
  // 生产环境（Railway）
  production: {
    // Railway后端地址 - 需要在Vercel环境变量中设置
    API_BASE_URL: process.env.NEXT_PUBLIC_API_URL || 'https://your-railway-app.up.railway.app',
  }
};

// 自动检测环境
const getApiUrl = () => {
  // 如果是Vercel环境，使用环境变量
  if (typeof window !== 'undefined' && window.location.hostname !== 'localhost') {
    // 生产环境
    const apiUrl = window.API_BASE_URL || 
                   localStorage.getItem('API_BASE_URL') || 
                   'https://your-railway-app.up.railway.app';
    return apiUrl;
  }
  // 开发环境
  return API_CONFIG.development.API_BASE_URL;
};

// 导出API基础URL
window.API_BASE_URL = getApiUrl();

// 方便全局使用
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { API_BASE_URL: getApiUrl() };
}

