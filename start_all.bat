@echo off

rem Start all services batch file

cd /d "%~dp0"

echo ===============================================
echo Starting Hongkai Helper All Services
echo ===============================================
echo.

rem 1. Start OCR Server
echo 1. Starting OCR Server...
start "OCR Server" cmd /k "echo OCR Server: && Python3.11\python.exe ocr_server_final.py"
timeout /t 3 /nobreak >nul

rem 2. Start YOLO Server
echo.
echo 2. Starting YOLO Server...
start "YOLO Server" cmd /k "echo YOLO Server: && Python3.11\python.exe yolo_server_final.py"
timeout /t 3 /nobreak >nul

rem 3. Start API Server
echo.
echo 3. Starting API Server...
start "API Server" cmd /k "echo API Server: && Python3.13\python.exe api_server.py"
timeout /t 3 /nobreak >nul

rem 4. Start Frontend
echo.
echo 4. Starting Frontend...
echo 4.1 Starting Vite Dev Server...
start "Vite Dev Server" cmd /k "echo Vite Dev Server: && cd front && echo Current directory: && cd && set "PATH=..\node\node-v20.11.1-win-x64;%PATH%" && echo Node version: && node.exe -v && echo npm version: && npm.cmd -v && echo Starting Vite... && npm.cmd run dev"
start "Electron Frontend" cmd /k "echo Electron Frontend: && cd front && echo Current directory: && cd && set "PATH=..\node\node-v20.11.1-win-x64;%PATH%" && echo Node version: && node.exe -v && echo npm version: && npm.cmd -v && echo Checking if Vite is running... && timeout /t 2 /nobreak >nul && echo Starting Electron... && npm.cmd run electron:dev"
timeout /t 8 /nobreak >nul

echo.
echo ===============================================
echo All services started!
echo ===============================================
echo Frontend running at: http://localhost:5173/
echo Note: Close windows to stop services
echo Check command windows for error messages
echo ===============================================

pause