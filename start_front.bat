@echo off
chcp 65001 >nul

rem 启动前端和Electron的批处理文件

cd /d "%~dp0"

echo ===============================================
echo 启动前端和Electron
echo ===============================================
echo.

rem 1. 启动Vite开发服务器
echo 1. 启动Vite开发服务器...
start "Vite开发服务器" cmd /c "cd front && npm run dev"
timeout /t 5 /nobreak >nul
echo ✓ Vite开发服务器启动完成

echo 前端运行在: http://localhost:5173/

rem 2. 启动Electron
echo.
echo 2. 启动Electron前端窗口...
start "Electron前端" cmd /c "cd front && npm run electron:dev"
timeout /t 3 /nobreak >nul
echo ✓ Electron前端窗口启动完成

echo.
echo ===============================================
echo 启动完成！
echo ===============================================
echo 提示：
echo 1. 关闭窗口时，对应服务也会停止
echo 2. 如果需要停止所有服务，请关闭所有弹出的命令行窗口
echo ===============================================

pause