#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OCR服务启动脚本

文件说明：
    本脚本用于启动OCR持久化服务，提供高效稳定的OCR文本识别服务。
    脚本会自动检查服务是否已经在运行，避免重复启动，并提供详细的启动日志。

主要功能：
    - 检查OCR服务是否已经在运行
    - 启动OCR持久化服务
    - 验证服务是否成功启动
    - 提供详细的启动日志
    - 处理启动失败的情况

使用说明：
    1. 直接运行：
       ```
       python start_ocr_service.py
       ```
    
    2. 作为模块调用：
       ```python
       from start_ocr_service import start_ocr_service, check_service_status
       
       # 检查服务状态
       if check_service_status():
           print("OCR服务已经在运行")
       else:
           # 启动服务
           process = start_ocr_service()
           if process:
               print("OCR服务启动成功")
           else:
               print("OCR服务启动失败")
       ```

配置信息：
    - OCR服务脚本：ocr_server_final.py
    - Python解释器：使用Python 3.11
    - 监听地址：127.0.0.1:5002

依赖文件：
    - ocr_server_final.py：OCR服务端实现
    - PP-OCRv4模型：使用指定目录中的模型文件 (d:\TokusCode\python\hongkai\ocr\models)

注意事项：
    - 脚本会自动检查服务是否已经在运行
    - 启动过程中会等待3秒，确保服务有足够时间启动
    - 如果启动失败，会输出详细的错误信息
    - 服务启动后会在后台运行
    - 要停止服务，需要手动终止进程

输出示例：
    ================================================================
    OCR服务启动脚本
    服务脚本: d:\TokusCode\python\hongkai\ocr_server_final.py
    Python解释器: d:\TokusCode\python\hongkai\Python3.11\python.exe
    监听地址: 127.0.0.1:5002
    ================================================================
    正在启动OCR服务...
    OCR服务已成功启动，监听: 127.0.0.1:5002
    
    OCR服务启动成功！
    服务正在后台运行...
    要停止服务，请手动终止进程
"""

import os
import sys
import subprocess
import time
import socket

# 获取当前脚本所在目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# OCR服务配置
OCR_SERVER_SCRIPT = os.path.join(current_dir, 'ocr_server_final.py')
PYTHON_EXECUTABLE = os.path.join(current_dir, 'Python3.11', 'python.exe')
HOST = '127.0.0.1'
PORT = 5002


def check_service_status():
    """
    检查OCR服务是否正在运行
    
    Returns:
        bool: 服务是否正在运行
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        s.close()
        return True
    except ConnectionRefusedError:
        return False
    except Exception as e:
        print(f"检查服务状态时出错: {e}")
        return False


def start_ocr_service():
    """
    启动OCR服务
    
    Returns:
        bool: 服务是否启动成功
    """
    print("正在启动OCR服务...")
    
    # 检查脚本是否存在
    if not os.path.exists(OCR_SERVER_SCRIPT):
        print(f"错误：OCR服务脚本不存在: {OCR_SERVER_SCRIPT}")
        sys.exit(1)
    
    # 检查Python解释器是否存在
    if not os.path.exists(PYTHON_EXECUTABLE):
        print(f"错误：Python解释器不存在: {PYTHON_EXECUTABLE}")
        sys.exit(1)
    
    # 启动服务
    try:
        # 在新的命令行窗口中启动OCR服务（最小化启动，不置顶）
        # 使用cmd.exe /c start /MIN命令，这样窗口关闭时服务也会关闭，且窗口最小化不置顶
        # 正确处理引号，确保Windows命令行能正确解析
        cmd_command = f'cmd.exe /c start /MIN "OCR服务" "{PYTHON_EXECUTABLE}" "{OCR_SERVER_SCRIPT}"'
        
        # 执行命令
        subprocess.Popen(
            cmd_command,
            shell=True
        )
        
        # 等待服务启动
        time.sleep(3)
        
        # 检查服务是否成功启动
        if check_service_status():
            print(f"OCR服务已成功启动，监听: {HOST}:{PORT}")
            print(f"服务在新的命令行窗口中运行")
            print(f"窗口标题: OCR服务")
            print(f"窗口关闭时，服务也会停止")
            return True
        else:
            print("OCR服务启动失败，无法连接")
            return False
            
    except Exception as e:
        print(f"启动OCR服务时出错: {e}")
        return None


def main():
    """
    主函数
    """
    print("=" * 60)
    print("OCR服务启动脚本")
    print(f"服务脚本: {OCR_SERVER_SCRIPT}")
    print(f"Python解释器: {PYTHON_EXECUTABLE}")
    print(f"监听地址: {HOST}:{PORT}")
    print("=" * 60)
    
    # 检查服务是否已经在运行
    if check_service_status():
        print("OCR服务已经在运行")
        sys.exit(0)
    
    # 启动服务
    success = start_ocr_service()
    if success:
        print("\nOCR服务启动成功！")
        print("服务在新的命令行窗口中运行...")
        print("窗口标题: OCR服务")
        print("窗口关闭时，服务也会停止")
    else:
        print("\nOCR服务启动失败")
        sys.exit(1)


if __name__ == "__main__":
    main()
