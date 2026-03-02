from flask import Flask, request, jsonify
import subprocess
import os
import sys

app = Flask(__name__)

# 设置CORS头
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# 获取脚本目录路径
SCRIPT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'process')

@app.route('/run-script', methods=['GET'])
def run_script():
    script_name = request.args.get('script')
    if not script_name:
        return jsonify({'status': 'error', 'message': '缺少脚本名称参数'})
    
    # 构建脚本路径
    script_path = os.path.join(SCRIPT_DIR, script_name)
    
    # 检查脚本是否存在
    if not os.path.exists(script_path):
        return jsonify({'status': 'error', 'message': f'脚本 {script_name} 不存在'})
    
    try:
        # 运行脚本并捕获输出
        # 使用shell=True并以管理员身份运行
        result = subprocess.run(
            f'powershell -Command "Start-Process python -ArgumentList \"{script_path}\" -Verb RunAs -Wait"',
            shell=True,
            capture_output=True,
            text=True
        )
        
        # 返回运行结果
        return jsonify({
            'status': 'success' if result.returncode == 0 else 'error',
            'exit_code': result.returncode,
            'stdout': result.stdout,
            'stderr': result.stderr,
            'latest_log': result.stdout.split('\n')[-10:] if result.stdout else []
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

# 获取日志文件列表
@app.route('/get-log-files', methods=['GET'])
def get_log_files():
    try:
        # 构建all_log目录路径
        log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'all_log')
        
        # 检查目录是否存在
        if not os.path.exists(log_dir):
            return jsonify({'status': 'success', 'files': []})
        
        # 获取目录中的所有文件
        files = os.listdir(log_dir)
        
        # 过滤出.log文件
        log_files = [f for f in files if f.endswith('.log')]
        
        # 按文件名排序（默认按字母顺序）
        log_files.sort()
        
        return jsonify({'status': 'success', 'files': log_files})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

# 读取日志文件内容
@app.route('/read-log-file', methods=['GET'])
def read_log_file():
    try:
        # 获取文件名参数
        file_name = request.args.get('file')
        if not file_name:
            return jsonify({'status': 'error', 'message': '缺少文件名参数'})
        
        # 构建日志文件路径
        log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'all_log')
        file_path = os.path.join(log_dir, file_name)
        
        # 检查文件是否存在
        if not os.path.exists(file_path):
            return jsonify({'status': 'error', 'message': f'日志文件 {file_name} 不存在'})
        
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return jsonify({'status': 'success', 'content': content})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

# 获取工具箱文件列表
@app.route('/get-tools-files', methods=['GET'])
def get_tools_files():
    try:
        # 构建tools目录路径
        tools_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tools')
        
        # 检查目录是否存在
        if not os.path.exists(tools_dir):
            return jsonify({'status': 'success', 'files': []})
        
        # 获取目录中的所有文件
        files = os.listdir(tools_dir)
        
        # 过滤出文件（排除目录）
        files = [f for f in files if os.path.isfile(os.path.join(tools_dir, f))]
        
        return jsonify({'status': 'success', 'files': files})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

# 运行Python文件
@app.route('/run-python-file', methods=['GET'])
def run_python_file():
    file_name = request.args.get('file')
    if not file_name:
        return jsonify({'status': 'error', 'message': '缺少文件名参数'})
    
    # 构建文件路径
    tools_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tools')
    file_path = os.path.join(tools_dir, file_name)
    
    # 检查文件是否存在
    if not os.path.exists(file_path):
        return jsonify({'status': 'error', 'message': f'文件 {file_name} 不存在'})
    
    # 检查是否为Python文件
    if not file_name.endswith('.py'):
        return jsonify({'status': 'error', 'message': '只能运行Python文件'})
    
    try:
        # 在新的命令行窗口中运行Python文件
        # 使用powershell的Start-Process命令，不等待进程结束
        subprocess.Popen(
            f'powershell -Command "Start-Process python -ArgumentList \"{file_path}\" -WindowStyle Normal"',
            shell=True
        )
        
        return jsonify({'status': 'success', 'message': f'已启动: {file_name}'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})



# 读取工具箱文件内容
@app.route('/read-tool-file', methods=['GET'])
def read_tool_file():
    try:
        # 获取文件名参数
        file_name = request.args.get('file')
        if not file_name:
            return jsonify({'status': 'error', 'message': '缺少文件名参数'})
        
        # 构建工具文件路径
        tools_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tools')
        file_path = os.path.join(tools_dir, file_name)
        
        # 检查文件是否存在
        if not os.path.exists(file_path):
            return jsonify({'status': 'error', 'message': f'文件 {file_name} 不存在'})
        
        # 读取文件内容
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            # 如果utf-8解码失败，尝试使用gbk编码
            with open(file_path, 'r', encoding='gbk') as f:
                content = f.read()
        
        return jsonify({'status': 'success', 'content': content})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

# 获取reproduce文件列表
@app.route('/get-reproduce-files', methods=['GET'])
def get_reproduce_files():
    try:
        # 构建reproduce目录路径
        reproduce_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tools', 'reproduce')
        
        # 检查目录是否存在
        if not os.path.exists(reproduce_dir):
            return jsonify({'status': 'success', 'files': []})
        
        # 获取目录中的所有文件
        files = os.listdir(reproduce_dir)
        
        # 过滤出文件（排除目录）
        files = [f for f in files if os.path.isfile(os.path.join(reproduce_dir, f))]
        
        return jsonify({'status': 'success', 'files': files})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

# 读取reproduce文件内容
@app.route('/read-reproduce-file', methods=['GET'])
def read_reproduce_file():
    try:
        # 获取文件名参数
        file_name = request.args.get('file')
        if not file_name:
            return jsonify({'status': 'error', 'message': '缺少文件名参数'})
        
        # 构建reproduce文件路径
        reproduce_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tools', 'reproduce')
        file_path = os.path.join(reproduce_dir, file_name)
        
        # 检查文件是否存在
        if not os.path.exists(file_path):
            return jsonify({'status': 'error', 'message': f'文件 {file_name} 不存在'})
        
        # 读取文件内容
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            # 如果utf-8解码失败，尝试使用gbk编码
            with open(file_path, 'r', encoding='gbk') as f:
                content = f.read()
        
        return jsonify({'status': 'success', 'content': content})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8002, debug=True)