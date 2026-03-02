import sys
import os
import time
import pyautogui
from pynput import mouse

# 将父目录添加到sys.path中，以便能够导入上层目录的模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import all_log.save_output
from on_window import focus_bh3_window, run_as_admin, is_admin
import photos.clicks_keyboard as ck

def click_and_print_position():
    """
    等待用户点击，输出点击坐标
    """
    try:
        print("请执行左键点击操作（按下Ctrl+C可以退出）...")
        print("等待用户点击...")
        
        # 定义点击事件处理函数
        def on_click(x, y, button, pressed):
            if pressed and button == mouse.Button.left:
                print(f"用户点击了坐标: ({x}, {y})")
                # 停止监听
                return False
        
        # 创建并启动鼠标监听器
        with mouse.Listener(on_click=on_click) as listener:
            listener.join()
        
        return True
    except KeyboardInterrupt:
        print("\n已退出监听")
        return False
    except Exception as e:
        print(f"执行错误: {e}")
        return False

def record_two_clicks_and_show_rectangle():
    """
    记录两次手动点击并显示框选的矩形坐标范围
    """
    try:
        clicks = []
        
        print("请执行两次左键点击操作（按下Ctrl+C可以退出）...")
        print("等待第1次点击...")
        
        # 定义点击事件处理函数
        def on_click(x, y, button, pressed):
            if pressed and button == mouse.Button.left:
                clicks.append((x, y))
                print(f"第{len(clicks)}次点击坐标: ({x}, {y})")
                
                if len(clicks) == 1:
                    print("等待第2次点击...")
                elif len(clicks) == 2:
                    # 停止监听
                    return False
        
        # 创建并启动鼠标监听器
        with mouse.Listener(on_click=on_click) as listener:
            listener.join()
        
        # 计算矩形的左上角和右下角坐标
        x1, y1 = clicks[0]
        x2, y2 = clicks[1]
        
        left = min(x1, x2)
        top = min(y1, y2)
        right = max(x1, x2)
        bottom = max(y1, y2)
        
        # 计算矩形的宽度和高度
        width = right - left
        height = bottom - top
        
        print(f"\n矩形坐标范围: ({left}, {top}) - ({right}, {bottom})")
        print(f"矩形尺寸: 宽度 = {width}, 高度 = {height}")
        
        return (left, top, right, bottom)
    except KeyboardInterrupt:
        print("\n已退出监听")
        return None
    except Exception as e:
        print(f"执行错误: {e}")
        return None

if __name__ == "__main__":
    # 检查是否以管理员身份运行
    if not is_admin():
        print("程序需要以管理员身份运行才能正常工作！")
        print("正在尝试自动提权...")
        
        if run_as_admin():
            print("请在弹出的UAC提示中选择'是'以继续...")
            sys.exit(0)  # 退出当前进程，等待管理员权限进程启动
        else:
            print("自动提权失败，请手动右键点击程序并选择'以管理员身份运行'")
            input("按回车键退出...")
            sys.exit(1)
            
    # 聚焦BH3窗口
    print("\n0. 执行focus_bh3_window函数：")
    success_focus = focus_bh3_window()
    if success_focus:
        print("BH3窗口已聚焦！")
    else:
        print("BH3窗口聚焦失败！")
    
    # click_and_print_position()
    record_two_clicks_and_show_rectangle()
    