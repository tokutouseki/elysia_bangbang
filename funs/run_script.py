import os
import sys
import subprocess
import json
from http.server import HTTPServer, BaseHTTPRequestHandler

# 导入日志保存模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from all_log.save_output import save_log

# 重定向print函数
import builtins
builtins.print = save_log

# 定义日志函数
def logger_info(*args, **kwargs):
    message = ' '.join(map(str, args))
    save_log(f"INFO - {message}")

def logger_error(*args, **kwargs):
    message = ' '.join(map(str, args))
    save_log(f"ERROR - {message}")

def logger_warning(*args, **kwargs):
    message = ' '.join(map(str, args))
    save_log(f"WARNING - {message}")

# 替换logger
logger = type('Logger', (), {
    'info': logger_info,
    'error': logger_error,
    'warning': logger_warning
})()

class ScriptHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/run-script'):
            logger.info(f"收到脚本运行请求: {self.client_address}")
            
            # 解析请求参数
            import urllib.parse
            parsed_path = urllib.parse.urlparse(self.path)
            query_params = urllib.parse.parse_qs(parsed_path.query)
            
            script_name = query_params.get('script', [''])[0]
            logger.info(f"请求运行脚本: {script_name}")
            
            if not script_name:
                self.send_error(400, '脚本名称不能为空')
                return
            
            # 脚本路径
            script_dir = os.path.join(os.path.dirname(__file__), '..', 'process')
            script_path = os.path.join(script_dir, script_name)
            
            logger.info(f"脚本路径: {script_path}")
            
            if not os.path.exists(script_path):
                self.send_error(404, f'脚本不存在: {script_name}')
                return
            
            try:
                # 运行脚本
                logger.info(f"开始运行脚本: {script_name}")
                
                # 使用subprocess运行脚本
                result = subprocess.run(
                    ['python', script_path],
                    capture_output=True,
                    text=True,
                    timeout=3600  # 1小时超时
                )
                
                logger.info(f"脚本运行完成: {script_name}")
                logger.info(f"退出码: {result.returncode}")
                logger.info(f"标准输出: {result.stdout[:1000]}")  # 只记录前1000个字符
                if result.stderr:
                    logger.error(f"标准错误: {result.stderr[:1000]}")  # 只记录前1000个字符
                
                # 获取最新日志文件的最后一行
                latest_log_line = self._get_latest_log_line(script_name)
                
                # 构建响应
                response = {
                    'status': 'success' if result.returncode == 0 else 'error',
                    'script': script_name,
                    'exit_code': result.returncode,
                    'stdout': result.stdout,
                    'stderr': result.stderr,
                    'latest_log': latest_log_line
                }
                
                # 发送响应
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')  # 允许跨域
                self.end_headers()
                self.wfile.write(json.dumps(response).encode('utf-8'))
                
                logger.info(f"响应已发送: {response['status']}")
                
            except subprocess.TimeoutExpired:
                error_msg = f'脚本运行超时: {script_name}'
                logger.error(error_msg)
                
                # 获取最新日志文件的最后一行
                latest_log_line = self._get_latest_log_line(script_name)
                
                response = {
                    'status': 'error',
                    'script': script_name,
                    'error': error_msg,
                    'latest_log': latest_log_line
                }
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode('utf-8'))
                
            except Exception as e:
                error_msg = f'运行脚本时出错: {str(e)}'
                logger.error(error_msg, exc_info=True)
                
                # 获取最新日志文件的最后一行
                latest_log_line = self._get_latest_log_line(script_name)
                
                response = {
                    'status': 'error',
                    'script': script_name,
                    'error': error_msg,
                    'latest_log': latest_log_line
                }
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode('utf-8'))
                
        elif self.path.startswith('/get-latest-log'):
            # 处理获取最新日志的请求
            logger.info(f"收到获取最新日志请求: {self.client_address}")
            
            # 解析请求参数
            import urllib.parse
            parsed_path = urllib.parse.urlparse(self.path)
            query_params = urllib.parse.parse_qs(parsed_path.query)
            
            script_name = query_params.get('script', [''])[0]
            logger.info(f"请求获取脚本日志: {script_name}")
            
            if not script_name:
                self.send_error(400, '脚本名称不能为空')
                return
            
            # 获取最新日志文件的最后一行
            latest_log_line = self._get_latest_log_line(script_name)
            
            # 构建响应
            response = {
                'script': script_name,
                'latest_log': latest_log_line
            }
            
            # 发送响应
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')  # 允许跨域
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
            
        else:
            self.send_error(404, 'Not Found')
    
    def _get_latest_log_line(self, script_name):
        """
        获取指定脚本的最新日志文件的最后一行
        """
        try:
            # 日志目录
            log_dir = os.path.join(os.path.dirname(__file__), '..', 'all_log')
            
            # 获取脚本名称（不含扩展名）
            script_base_name = os.path.splitext(script_name)[0]
            
            # 查找所有相关的日志文件
            log_files = []
            for filename in os.listdir(log_dir):
                if filename.endswith('.log') and script_base_name in filename:
                    file_path = os.path.join(log_dir, filename)
                    # 获取文件的修改时间
                    mod_time = os.path.getmtime(file_path)
                    log_files.append((mod_time, file_path))
            
            # 按修改时间排序，获取最新的日志文件
            if log_files:
                log_files.sort(reverse=True)
                latest_log_file = log_files[0][1]
                logger.info(f"最新日志文件: {latest_log_file}")
                
                # 读取文件的最后一行
                with open(latest_log_file, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
                    if lines:
                        last_line = lines[-1].strip()
                        logger.info(f"最新日志行: {last_line}")
                        return last_line
            
            logger.warning(f"未找到脚本 {script_name} 的日志文件")
            return "未找到相关日志文件"
            
        except Exception as e:
            logger.error(f"获取最新日志失败: {str(e)}")
            return f"获取日志失败: {str(e)}"

def run_server():
    """启动服务器"""
    logger.info("启动脚本运行服务器")
    server_address = ('', 8002)
    httpd = HTTPServer(server_address, ScriptHandler)
    logger.info('Script server running at http://localhost:8002/')
    logger.info('Run script endpoint: http://localhost:8002/run-script?script=脚本名称')
    print('Script server running at http://localhost:8002/')
    print('Run script endpoint: http://localhost:8002/run-script?script=脚本名称')
    print('Press Ctrl+C to stop server')
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()
