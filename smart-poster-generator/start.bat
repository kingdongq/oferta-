@echo off
echo ========================================
echo 智能海报生成器 - 启动
echo ========================================
echo.
echo 选择启动方式:
echo 1. 仅打开前端 (浏览器)
echo 2. 启动完整服务 (API + 前端)
echo.
set /p choice="请选择 (1 或 2): "

if "%choice%"=="1" goto open_html
if "%choice%"=="2" goto start_server

:open_html
echo.
echo 正在打开浏览器...
start "" "%cd%\frontend\index.html"
echo.
echo 前端已在浏览器中打开！
goto end

:start_server
echo.
echo 正在启动API服务器...
cd frontend
python api-server.py
goto end

:end
pause


