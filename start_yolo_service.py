#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
YOLO服务启动脚本

文件说明：
    本脚本用于启动YOLO持久化服务，提供高效稳定的YOLO检测服务。
    脚本会自动检查服务是否已经在运行，避免重复启动，并提供详细的启动日志。

主要功能：
    - 检查YOLO服务是否已经在运行
    - 启动YOLO持久化服务
    - 验证服务是否成功启动
    - 提供详细的启动日志
    - 处理启动失败的情况

使用说明：
    1. 直接运行：
       ```
       python start_yolo_service.py
       ```
    
    2. 作为模块调用：
       ```python
       from start_yolo_service import start_yolo_service, check_service_status
       
       # 检查服务状态
       if check_service_status():
           print("YOLO服务已经在运行")
       else:
           # 启动服务
           process = start_yolo_service()
           if process:
               print("YOLO服务启动成功")
           else:
               print("YOLO服务启动失败")
       ```

配置信息：
    - YOLO服务脚本：yolo_server_final.py
    - Python解释器：默认使用虚拟环境中的Python
    - 监听地址：127.0.0.1:5001

依赖文件：
    - yolo_server_final.py：YOLO服务端实现
    - YOLO模型文件：默认存放在Python3.11/yolo/models目录下

注意事项：
    - 脚本会自动检查服务是否已经在运行
    - 启动过程中会等待3秒，确保服务有足够时间启动
    - 如果启动失败，会输出详细的错误信息
    - 服务启动后会在后台运行
    - 要停止服务，需要手动终止进程

输出示例：
    ================================================================
    YOLO服务启动脚本
    服务脚本: d:\TokusCode\python\hongkai\yolo_server_final.py
    Python解释器: d:\TokusCode\python\hongkai\Python3.11\python.exe
    监听地址: 127.0.0.1:5001
    ================================================================
    正在启动YOLO服务...
    YOLO服务已成功启动，监听: 127.0.0.1:5001
    
    YOLO服务启动成功！
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

# YOLO服务配置
YOLO_SERVER_SCRIPT = os.path.join(current_dir, 'yolo_server_final.py')
PYTHON_EXECUTABLE = os.path.join(current_dir, 'Python3.11', 'python.exe')
HOST = '127.0.0.1'
PORT = 5001


def check_service_status():
    """
    检查YOLO服务是否正在运行
    
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


def start_yolo_service():
    """
    启动YOLO服务
    
    Returns:
        subprocess.Popen: 服务进程对象
    """
    print("正在启动YOLO服务...")
    
    # 检查脚本是否存在
    if not os.path.exists(YOLO_SERVER_SCRIPT):
        print(f"错误：YOLO服务脚本不存在: {YOLO_SERVER_SCRIPT}")
        sys.exit(1)
    
    # 检查Python解释器是否存在
    if not os.path.exists(PYTHON_EXECUTABLE):
        print(f"错误：Python解释器不存在: {PYTHON_EXECUTABLE}")
        sys.exit(1)
    
    # 启动服务
    try:
        process = subprocess.Popen(
            [PYTHON_EXECUTABLE, YOLO_SERVER_SCRIPT],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8'
        )
        
        # 等待服务启动
        time.sleep(3)
        
        # 检查服务是否成功启动
        if check_service_status():
            print(f"YOLO服务已成功启动，监听: {HOST}:{PORT}")
            return process
        else:
            print("YOLO服务启动失败，无法连接")
            # 获取错误信息
            stderr_output = process.stderr.read()
            if stderr_output:
                print(f"错误信息: {stderr_output}")
            process.terminate()
            process.wait()
            return None
            
    except Exception as e:
        print(f"启动YOLO服务时出错: {e}")
        return None


def main():
    """
    主函数
    """
    print("=" * 60)
    print("YOLO服务启动脚本")
    print(f"服务脚本: {YOLO_SERVER_SCRIPT}")
    print(f"Python解释器: {PYTHON_EXECUTABLE}")
    print(f"监听地址: {HOST}:{PORT}")
    print("=" * 60)
    
    # 检查服务是否已经在运行
    if check_service_status():
        print("YOLO服务已经在运行")
        sys.exit(0)
    
    # 启动服务
    process = start_yolo_service()
    if process:
        print("\nYOLO服务启动成功！")
        print("服务正在后台运行...")
        print("要停止服务，请手动终止进程")
    else:
        print("\nYOLO服务启动失败")
        sys.exit(1)


if __name__ == "__main__":
    main()