import time
import threading
from pynput import keyboard, mouse
from datetime import datetime
import json
import os
import sys

# 将父目录添加到sys.path中，以便能够导入上层目录的模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import all_log.save_output
from on_window import focus_bh3_window, run_as_admin, is_admin

class OperationRecorder:
    def __init__(self):
        self.start_time = time.time()
        self.end_time = None
        self.recording = False
        
        # 设置输出文件路径
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"recording_cn_{timestamp}.json"
        self.output_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reproduce", filename)
        
        # 记录数据
        self.data = {
            "开始时间": datetime.fromtimestamp(self.start_time).strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
            "结束时间": None,
            "持续时长(秒)": 0,
            "键盘事件": [],
            "鼠标事件": []
        }
        
        # 键盘和鼠标监听器
        self.keyboard_listener = None
        self.mouse_listener = None
        
        # 移除鼠标位置记录线程相关变量
        
        # 当前按下的键信息 {key: press_time}
        self.current_keys = {}
        
        # 当前按下的鼠标左键信息 (press_time, x, y)
        self.current_left_mouse = None
    
    def start(self):
        """开始记录"""
        if self.recording:
            print("记录已经开始")
            return False
        
        self.recording = True
        
        # 启动键盘监听器
        self.keyboard_listener = keyboard.Listener(
            on_press=self.on_key_press,
            on_release=self.on_key_release
        )
        self.keyboard_listener.start()
        
        # 启动鼠标监听器
        self.mouse_listener = mouse.Listener(
            on_move=self.on_mouse_move,
            on_click=self.on_mouse_click,
            on_scroll=self.on_mouse_scroll
        )
        self.mouse_listener.start()
        
        # 移除鼠标位置记录线程启动
        
        print(f"开始记录操作，输出文件: {self.output_file}")
        return True
    
    def stop(self):
        """停止记录"""
        if not self.recording:
            print("记录已经停止")
            return False
        
        self.recording = False
        self.end_time = time.time()
        
        # 停止监听器
        if self.keyboard_listener:
            self.keyboard_listener.stop()
            self.keyboard_listener = None
        
        if self.mouse_listener:
            self.mouse_listener.stop()
            self.mouse_listener = None
        
        # 记录结束时间和运行时间
        self.data["结束时间"] = datetime.fromtimestamp(self.end_time).strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        self.data["持续时长(秒)"] = round(self.end_time - self.start_time, 2)
        
        # 保存记录
        self.save_recording()
        
        print(f"记录已停止，总运行时间: {self.data['持续时长(秒)']}秒")
        print(f"记录已保存到: {os.path.join('reproduce', os.path.basename(self.output_file))}")
        return True
    
    def on_key_press(self, key):
        """键盘按键按下事件处理"""
        if not self.recording:
            return
        
        # 定义需要记录的按键列表
        allowed_keys = ['w', 'a', 's', 'd', 'j', 'k', 'l', 'u', 'i', 'f', '1', '2']
        
        try:
            key_str = key.char  # 字母数字键
        except AttributeError:
            key_str = str(key)  # 特殊键
            return  # 忽略特殊键
        
        # 只记录允许的按键
        if key_str not in allowed_keys:
            return
        
        press_time = time.time()
        
        # 只有当按键不在当前按下列表中时，才记录按下事件
        if key_str not in self.current_keys:
            # 记录按键按下事件
            self.current_keys[key_str] = press_time
            
            self.data["键盘事件"].append({
                "按键": key_str,
                "按下时间(秒)": round(press_time - self.start_time, 2),
                "按下绝对时间": datetime.fromtimestamp(press_time).strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
                "松开时间(秒)": None,
                "持续时长(秒)": None
            })
    
    def on_key_release(self, key):
        """键盘按键松开事件处理"""
        if not self.recording:
            return
        
        # 定义需要记录的按键列表
        allowed_keys = ['w', 'a', 's', 'd', 'j', 'k', 'l', 'u', 'i', 'f', '1', '2']
        
        try:
            key_str = key.char  # 字母数字键
        except AttributeError:
            key_str = str(key)  # 特殊键
            return  # 忽略特殊键
        
        # 只记录允许的按键
        if key_str not in allowed_keys:
            # 如果该键在当前按下列表中，移除它
            if key_str in self.current_keys:
                del self.current_keys[key_str]
            return
        
        release_time = time.time()
        
        # 检查按键是否在当前按下的键列表中
        if key_str in self.current_keys:
            press_time = self.current_keys[key_str]
            duration = round(release_time - press_time, 2)
            
            # 更新按下事件记录，添加松开信息
            for event in self.data["键盘事件"]:
                if event["按键"] == key_str and event["松开时间(秒)"] is None:
                    event["松开时间(秒)"] = round(release_time - self.start_time, 2)
                    event["持续时长(秒)"] = duration
                    break
            
            # 从当前按下的键列表中移除
            del self.current_keys[key_str]
    
    def on_mouse_move(self, x, y):
        """鼠标移动事件处理"""
        # 鼠标移动事件只用于实时跟踪，不单独记录
        # 鼠标位置将通过定时记录线程来记录
        pass
    
    def on_mouse_click(self, x, y, button, pressed):
        """鼠标点击事件处理"""
        if not self.recording:
            return
        
        click_time = time.time()
        
        # 只处理左键
        if str(button) != "Button.left":
            return
        
        if pressed:
            # 鼠标左键按下
            self.current_left_mouse = (click_time, x, y)
            
            self.data["鼠标事件"].append({
                "类型": "左键按下",
                "x坐标": round(x, 1),
                "y坐标": round(y, 1),
                "按下时间(秒)": round(click_time - self.start_time, 2),
                "按下绝对时间": datetime.fromtimestamp(click_time).strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
                "松开时间(秒)": None,
                "持续时长(秒)": None
            })
        else:
            # 鼠标左键松开
            if self.current_left_mouse:
                press_time, press_x, press_y = self.current_left_mouse
                duration = round(click_time - press_time, 2)
                
                # 更新按下事件记录，添加松开信息
                for event in self.data["鼠标事件"]:
                    if event["类型"] == "左键按下" and event["松开时间(秒)"] is None:
                        event["松开时间(秒)"] = round(click_time - self.start_time, 2)
                        event["持续时长(秒)"] = duration
                        break
                
                self.current_left_mouse = None
    
    def on_mouse_scroll(self, x, y, dx, dy):
        """鼠标滚轮事件处理"""
        if not self.recording:
            return
        
        scroll_time = time.time()
        
        # 记录滚动方向
        scroll_direction = "向上" if dy > 0 else "向下"
        
        self.data["鼠标事件"].append({
            "类型": "滑轮滚动",
            "x坐标": round(x, 1),
            "y坐标": round(y, 1),
            "开始滑动时间(秒)": round(scroll_time - self.start_time, 2),
            "绝对时间": datetime.fromtimestamp(scroll_time).strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
            "滚动方向": scroll_direction
        })
    
    # 移除鼠标位置记录方法
    
    def save_recording(self):
        """保存记录到JSON文件"""
        try:
            # 确保输出目录存在
            output_dir = os.path.dirname(self.output_file)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            with open(self.output_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"保存记录失败: {e}")
            return False

if __name__ == "__main__":
    # 检查是否以管理员身份运行
    if not is_admin():
        print("需要管理员权限，正在尝试自动提权...")
        if run_as_admin():
            print("请在弹出的UAC提示中选择'是'以继续...")
            sys.exit(0)  # 退出当前进程，等待管理员权限进程启动
        else:
            print("自动提权失败，请手动右键点击程序并选择'以管理员身份运行'")
            input("按回车键退出...")
            sys.exit(1)
    
    # 尝试聚焦到目标窗口
    focus_bh3_window()
    
    recorder = OperationRecorder()
    try:
        recorder.start()
        print("\n操作记录器")
        print("按 Ctrl+C 停止记录")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        recorder.stop()
    except Exception as e:
        print(f"发生错误: {e}")
        recorder.stop()