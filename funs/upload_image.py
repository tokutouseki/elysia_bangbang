import os
import sys
import json
from http.server import HTTPServer, BaseHTTPRequestHandler

# 导入日志保存模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from all_log.save_output import save_log

# 重定向print函数
import builtins
builtins.print = save_log

class ImageUploadHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/upload':
            # 处理文件上传
            content_type = self.headers.get('Content-Type', '')
            
            # 检查是否是multipart/form-data
            if not content_type.startswith('multipart/form-data'):
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {
                    'status': 'error',
                    'message': 'Invalid content type'
                }
                self.wfile.write(json.dumps(response).encode('utf-8'))
                return
            
            # 获取boundary
            boundary = content_type.split('boundary=')[1].encode('utf-8')
            
            # 读取请求体
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            
            # 解析multipart/form-data
            parts = body.split(b'--' + boundary)
            image_files = []
            
            for part in parts[1:-1]:  # 跳过第一个和最后一个空部分
                part = part.strip()
                if not part:
                    continue
                
                # 分离头部和内容
                header_end = part.find(b'\r\n\r\n')
                if header_end == -1:
                    continue
                
                header = part[:header_end].decode('utf-8')
                content = part[header_end + 4:]
                
                # 提取文件名
                filename = None
                for line in header.split('\r\n'):
                    if 'filename=' in line:
                        filename = line.split('filename=')[1].strip('"')
                        break
                
                if filename:
                    # 保存图片到uploads目录
                    upload_dir = os.path.join(os.path.dirname(__file__), 'uploads')
                    os.makedirs(upload_dir, exist_ok=True)
                    
                    # 确保文件名安全
                    filename = os.path.basename(filename)
                    filepath = os.path.join(upload_dir, filename)
                    
                    # 移除内容末尾的\r\n
                    content = content.rstrip(b'\r\n')
                    
                    with open(filepath, 'wb') as f:
                        f.write(content)
                    
                    image_files.append({
                        'name': filename,
                        'path': filepath
                    })
            
            # 返回上传成功的响应
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                'status': 'success',
                'files': image_files
            }
            self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')

    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'Image Upload Server')
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')

def run_server():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, ImageUploadHandler)
    print('Server running at http://localhost:8000/')
    print('Upload endpoint: http://localhost:8000/upload')
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()
