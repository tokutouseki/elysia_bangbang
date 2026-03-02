import os
import sys
import smtplib
import json
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.header import Header
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

class EmailSender:
    def __init__(self):
        logger.info("初始化邮件发送器")
        # 从配置文件读取邮箱配置
        config_file = os.path.join(os.path.dirname(__file__), 'config.json')
        if os.path.exists(config_file):
            logger.info(f"读取配置文件: {config_file}")
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                self.email_config = config.get('email_config', {})
        else:
            logger.warning("配置文件不存在，使用默认配置")
            # 默认配置
            self.email_config = {
                "smtp_server": "smtp.qq.com",
                "smtp_port": 587,
                "sender_email": "3677481667@qq.com",
                "sender_password_encrypted": "",
                "receiver_email": "3398582158@qq.com"
            }
        
        logger.info(f"SMTP服务器: {self.email_config.get('smtp_server')}:{self.email_config.get('smtp_port')}")
        logger.info(f"发送者邮箱: {self.email_config.get('sender_email')}")
        logger.info(f"接收者邮箱: {self.email_config.get('receiver_email')}")
        
        # 验证配置
        if not self.email_config.get('sender_password_encrypted'):
            logger.warning("未配置邮箱密码，请在config.json中设置sender_password_encrypted")
        else:
            logger.info("邮箱密码已配置")
        
    def _decrypt_password(self):
        """解密邮箱密码"""
        encrypted_password = self.email_config.get('sender_password_encrypted', '')
        if not encrypted_password:
            logger.error("加密密码为空")
            return ''
        
        try:
            # 简单的Base64解密
            decrypted = base64.b64decode(encrypted_password).decode('utf-8')
            logger.info("密码解密成功")
            return decrypted
        except Exception as e:
            logger.error(f"密码解密失败: {e}")
            return ''
        
    def get_uploaded_images(self):
        """获取uploads目录中的所有图片文件"""
        upload_dir = os.path.join(os.path.dirname(__file__), 'uploads')
        if not os.path.exists(upload_dir):
            logger.warning(f"上传目录不存在: {upload_dir}")
            return []
        
        image_files = []
        for file_name in os.listdir(upload_dir):
            file_path = os.path.join(upload_dir, file_name)
            if os.path.isfile(file_path):
                # 检查是否为图片文件
                if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                    image_files.append(file_path)
                    logger.info(f"找到图片文件: {file_name}")
        
        logger.info(f"共找到 {len(image_files)} 个图片文件")
        return image_files
    
    def send_email_with_images(self):
        """发送带有图片附件的邮件"""
        logger.info("开始发送邮件")
        image_files = self.get_uploaded_images()
        
        if not image_files:
            logger.warning("没有找到图片文件，取消发送")
            return False
        
        try:
            # 获取解密后的密码
            sender_password = self._decrypt_password()
            if not sender_password:
                logger.error("邮箱密码未配置或解密失败")
                return False
            
            # 创建邮件
            msg = MIMEMultipart()
            
            # 正确设置From头 - 使用纯文本邮箱地址格式
            sender_email = self.email_config.get('sender_email')
            msg['From'] = sender_email
            logger.info(f"设置From头: {sender_email}")
            
            msg['To'] = self.email_config.get('receiver_email')
            msg['Subject'] = Header('上传的图片', 'utf-8')
            logger.info("邮件创建成功")
            
            # 添加邮件正文
            body = f"您好，这是自动发送的邮件，包含 {len(image_files)} 张上传的图片。\n"
            body += "图片列表：\n"
            for i, img_path in enumerate(image_files, 1):
                body += f"{i}. {os.path.basename(img_path)}\n"
            msg.attach(MIMEText(body, 'plain', 'utf-8'))
            logger.info("邮件正文添加成功")
            
            # 添加图片附件
            for img_path in image_files:
                try:
                    with open(img_path, 'rb') as f:
                        img = MIMEImage(f.read())
                        img.add_header('Content-Disposition', 'attachment', filename=os.path.basename(img_path))
                        msg.attach(img)
                    logger.info(f"添加附件成功: {os.path.basename(img_path)}")
                except Exception as e:
                    logger.error(f"添加附件失败 {os.path.basename(img_path)}: {e}")
            
            # 连接SMTP服务器并发送邮件
            logger.info(f"连接SMTP服务器: {self.email_config['smtp_server']}:{self.email_config['smtp_port']}")
            try:
                # 测试网络连接
                import socket
                socket.setdefaulttimeout(10)
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                result = sock.connect_ex((self.email_config['smtp_server'], self.email_config['smtp_port']))
                if result == 0:
                    logger.info("网络连接测试成功")
                else:
                    logger.error(f"网络连接测试失败，错误码: {result}")
                sock.close()
            except Exception as e:
                logger.error(f"网络连接测试失败: {e}")
            
            try:
                server = smtplib.SMTP(self.email_config['smtp_server'], self.email_config['smtp_port'], timeout=30)
                server.set_debuglevel(1)  # 启用SMTP调试
                logger.info("SMTP服务器连接成功")
            except Exception as e:
                logger.error(f"SMTP服务器连接失败: {e}")
                return False
            
            # 启用TLS
            try:
                server.starttls()
                logger.info("TLS启用成功")
            except Exception as e:
                logger.warning(f"TLS启用失败，继续尝试: {e}")
            
            # 登录
            try:
                server.login(self.email_config['sender_email'], sender_password)
                logger.info("SMTP登录成功")
            except Exception as e:
                logger.error(f"SMTP登录失败: {e}")
                server.quit()
                return False
            
            # 发送邮件
            try:
                # 使用sendmail方法，明确指定发送者、接收者
                server.sendmail(
                    self.email_config['sender_email'],
                    [self.email_config['receiver_email']],
                    msg.as_string()
                )
                logger.info("邮件发送成功")
            except Exception as e:
                logger.error(f"邮件发送失败: {e}")
                server.quit()
                return False
            
            # 退出
            server.quit()
            logger.info("SMTP连接关闭")
            
            # 发送成功后删除图片
            for img_path in image_files:
                try:
                    os.remove(img_path)
                    logger.info(f"已删除图片: {os.path.basename(img_path)}")
                except Exception as e:
                    logger.error(f"删除图片失败 {os.path.basename(img_path)}: {e}")
            
            logger.info(f"邮件发送完成，共发送 {len(image_files)} 张图片")
            return True
            
        except Exception as e:
            logger.error(f"发送邮件失败: {e}")
            return False

class EmailHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/send-email':
            logger.info(f"收到邮件发送请求: {self.client_address}")
            sender = EmailSender()
            result = sender.send_email_with_images()
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                'status': 'success' if result else 'error',
                'message': '邮件发送成功' if result else '邮件发送失败'
            }
            self.wfile.write(json.dumps(response).encode('utf-8'))
            logger.info(f"返回响应: {response}")
        else:
            logger.warning(f"未知请求路径: {self.path}")
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')

def run_server():
    logger.info("启动邮件服务器")
    server_address = ('', 8001)
    httpd = HTTPServer(server_address, EmailHandler)
    logger.info('Email server running at http://localhost:8001/')
    logger.info('Send email endpoint: http://localhost:8001/send-email')
    print('Email server running at http://localhost:8001/')
    print('Send email endpoint: http://localhost:8001/send-email')
    print('Press Ctrl+C to stop server')
    httpd.serve_forever()

def main():
    """直接执行邮件发送"""
    logger.info("直接执行邮件发送")
    sender = EmailSender()
    sender.send_email_with_images()

if __name__ == '__main__':
    # 可以选择直接发送邮件，或者启动服务器
    # main()  # 直接发送
    run_server()  # 启动服务器
