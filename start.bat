@echo off
chcp 65001 >nul
echo ========================================
echo 智能海报生成器 - 启动
echo ========================================
echo.
echo 选择启动方式:
echo.
echo 1. 启动后端服务器
echo 2. 查看登录页面
echo 3. 查看项目文档
echo.
set /p choice="请输入选项 (1-3): "

if "%choice%"=="1" (
    echo.
    echo 正在启动后端服务器...
    cd smart-poster-generator\backend
    python simple_server.py
    goto end
)

if "%choice%"=="2" (
    echo.
    echo 正在打开登录页面...
    start login.html
    goto end
)

if "%choice%"=="3" (
    echo.
    echo 打开文档...
    start README.md
    goto end
)

echo 无效的选项！

:end
pause

