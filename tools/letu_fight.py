import os
import sys
import time
import argparse
import pyautogui
import threading

# 将父目录添加到sys.path中，以便能够导入上层目录的模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入必要的模块
from replay_keyboard import replay_keyboard_events
from photos.clicks_keyboard import is_complex_temp
from bh3_yolo_recognizer import bh3_yolo_recognize


def detect_monster_ui(monster_detected_event, monster_stop_event, stop_image_path, confidence, region=None, debug=False):
    """
    检测怪物UI的函数，持续运行直到收到停止信号
    
    :param monster_detected_event: 用于标记是否检测到怪物UI的事件对象
    :param monster_stop_event: 用于怪物UI线程发送停止信号的事件对象
    :param stop_image_path: 停止图片的路径
    :param confidence: 图片检测的置信度阈值
    :param region: 识别区域范围，格式为 (x1, y1, x2, y2)，表示左上角和右下角坐标，默认为None（全屏）
    :param debug: 是否显示调试信息，默认False
    :return: 无返回值
    """
    if debug:
        print("开始检测怪物UI...")
    
    start_time = time.time()
    
    try:
        while not monster_stop_event.is_set():
            current_time = time.time()
            
            # 使用YOLO检测guaiwu_xueliang_UI
            yolo_result = bh3_yolo_recognize(save_screenshot=False, save_detection_result=False)
            
            # 检查是否存在guaiwu_xueliang_UI
            guaiwu_xueliang_exists = False
            if yolo_result.get("success"):
                elements = yolo_result.get("elements", [])
                for elem in elements:
                    if elem.get("class_name") == "guaiwu_xueliang_UI":
                        guaiwu_xueliang_exists = True
                        if not monster_detected_event.is_set():
                            if debug:
                                print("检测到怪物UI，标记为已检测")
                            monster_detected_event.set()
                        break
            
            # 检测停止图片（从一开始就检测）
            result = is_complex_temp("", template_path=stop_image_path, confidence=confidence, time_sleep=0, region=region, debug=debug)
            if result[0]:
                # 检查是否满足停止条件：运行时间≥3秒 + 怪物UI不存在 + 怪物UI之前被检测到过
                if current_time - start_time >= 3:  # 最小运行时间3秒，确保稳定检测
                    if not guaiwu_xueliang_exists and monster_detected_event.is_set():
                        if debug:
                            print("怪物UI线程：检测到停止图片且无怪物UI，标记为停止")
                        monster_stop_event.set()
                    elif debug:
                        print("怪物UI线程：检测到停止图片，但条件不满足，继续检测")
                elif debug:
                    print(f"怪物UI线程：检测到停止图片，但运行时间不足3秒（{current_time - start_time:.1f}s），继续检测")
            
            # 每隔0.1秒检测一次
            time.sleep(0.1)
    except Exception as e:
        print(f"怪物UI检测过程中发生错误: {e}")


def detect_stop_image(stop_image_path, confidence, image_stop_event, monster_detected_event, region=None, debug=False):
    """
    检测停止图片的函数，持续运行直到检测到图片或收到停止信号
    
    :param stop_image_path: 停止图片的路径
    :param confidence: 图片检测的置信度阈值
    :param image_stop_event: 用于停止图片线程发送停止信号的事件对象
    :param monster_detected_event: 用于标记是否检测到怪物UI的事件对象
    :param region: 识别区域范围，格式为 (x1, y1, x2, y2)，表示左上角和右下角坐标，默认为None（全屏）
    :param debug: 是否显示调试信息，默认False
    :return: 无返回值
    """
    if debug:
        print(f"开始检测停止图片: {stop_image_path}")
        if region is not None:
            print(f"识别区域: ({region[0]}, {region[1]}) - ({region[2]}, {region[3]})")
    
    start_time = time.time()
    
    try:
        while not image_stop_event.is_set():
            current_time = time.time()
            
            # 调用is_complex_temp函数，获取返回值
            result = is_complex_temp("", template_path=stop_image_path, confidence=confidence, time_sleep=0, region=region, debug=debug)
            if result[0]:  # 只检查第一个返回值（是否找到图片）
                print("检测到停止图片，检查怪物UI状态...")
                
                # 使用YOLO检测guaiwu_xueliang_UI
                yolo_result = bh3_yolo_recognize(save_screenshot=False, save_detection_result=False)
                
                # 检查是否存在guaiwu_xueliang_UI
                guaiwu_xueliang_exists = False
                if yolo_result.get("success"):
                    elements = yolo_result.get("elements", [])
                    for elem in elements:
                        if elem.get("class_name") == "guaiwu_xueliang_UI":
                            guaiwu_xueliang_exists = True
                            break
                
                if current_time - start_time >= 3:  # 最小运行时间3秒，确保稳定检测
                    if not guaiwu_xueliang_exists and monster_detected_event.is_set():
                        print("停止图片线程：未检测到guaiwu_xueliang_UI，且怪物已被检测到，标记为停止")
                        # 发送停止信号
                        image_stop_event.set()
                    elif not guaiwu_xueliang_exists and not monster_detected_event.is_set():
                        print("停止图片线程：未检测到guaiwu_xueliang_UI，且从未检测到怪物")
                    else:
                        print("停止图片线程：检测到guaiwu_xueliang_UI存在，继续战斗")
            # 每隔0.1秒检测一次
            time.sleep(0.1)
    except Exception as e:
        print(f"图片检测过程中发生错误: {e}")
        # 发生错误时也发送停止信号
        image_stop_event.set()


def letu_fight(recording_file_path, stop_image_path=r"photos\letu_stop_fight_loop.png", confidence=0.8, region=(1598, 945, 1719, 1064), debug=False):
    """
    循环复现按键操作直到检测到指定图片（使用多线程分离复现和检测）
    
    :param recording_file_path: 记录按键操作的JSON文件路径
    :param stop_image_path: 停止图片的路径，如果提供，则检测到该图片时停止复现
    :param confidence: 图片检测的置信度阈值
    :param region: 识别区域范围，格式为 (x1, y1, x2, y2)，表示左上角和右下角坐标，默认为(1598, 945, 1719, 1064)
    :param debug: 是否显示调试信息，默认False
    :return: bool: True表示未检测到怪物UI错误，False表示正常完成
    """
    # 标记是否检测到未检测到怪物UI的错误
    no_monster_ui_error = False
    if debug:
        print(f"开始循环复现按键操作，记录文件: {recording_file_path}")
        print(f"停止图片: {stop_image_path if stop_image_path else '未指定'}")
        print(f"图片检测置信度: {confidence}")
        if region is not None:
            print(f"识别区域: ({region[0]}, {region[1]}) - ({region[2]}, {region[3]})")
        print("按 Ctrl+C 手动停止循环")
    
    max_fight_time = 5 * 60  # 最大战斗时间5分钟
    
    try:
        loop_count = 0
        total_start_time = time.time()
        
        while time.time() - total_start_time < max_fight_time:
            loop_count += 1
            if debug:
                print(f"\n=== 第 {loop_count} 次循环开始 ===")
                print(f"已战斗时间: {int(time.time() - total_start_time)}秒，剩余时间: {int(max_fight_time - (time.time() - total_start_time))}秒")
            
            # 创建事件对象
            monster_detected_event = threading.Event()  # 标记是否检测到怪物UI
            monster_stop_event = threading.Event()      # 怪物UI线程的停止信号
            image_stop_event = threading.Event()        # 停止图片线程的停止信号
            global_stop_event = threading.Event()       # 全局停止信号
            
            loop_start_time = time.time()
            
            # 启动怪物UI检测线程
            monster_thread = threading.Thread(
                target=detect_monster_ui,
                args=(monster_detected_event, monster_stop_event, stop_image_path, confidence, region, debug)
            )
            monster_thread.daemon = True  # 设置为守护线程，主程序退出时自动退出
            monster_thread.start()
            
            # 启动检测线程（如果指定了停止图片）
            if stop_image_path:
                detection_thread = threading.Thread(
                    target=detect_stop_image,
                    args=(stop_image_path, confidence, image_stop_event, monster_detected_event, region, debug)
                )
                detection_thread.daemon = True  # 设置为守护线程，主程序退出时自动退出
                detection_thread.start()
            
            # 执行复现操作（在单独的线程中）
            replay_thread = threading.Thread(
                target=replay_keyboard_events,
                args=(recording_file_path, global_stop_event, debug)
            )
            replay_thread.daemon = True
            replay_thread.start()
            
            # 检查是否需要停止
            if stop_image_path:
                # 持续检查停止条件，直到复现线程结束或检测到停止信号
                while replay_thread.is_alive():
                    if monster_stop_event.is_set() or image_stop_event.is_set():
                        print("检测到停止信号，停止循环")
                        global_stop_event.set()
                        break
                    time.sleep(0.1)
                
                # 检查是否从未检测到怪物UI
                if not monster_detected_event.is_set() and time.time() - loop_start_time >= 10:
                    print("错误：未检测到怪物UI，可能未进入战斗层")
                    global_stop_event.set()
                    no_monster_ui_error = True
                    break
                
                if global_stop_event.is_set():
                    break
            
            if debug:
                print(f"\n本次复现完成")
            
            # 短暂延迟后开始下一次循环
            if not stop_image_path:
                if debug:
                    print("未指定停止图片，继续下一次循环")
                time.sleep(1)
            else:
                if debug:
                    print("继续下一次复现...")
                time.sleep(1)
        
        # 检查是否超时
        if time.time() - total_start_time >= max_fight_time:
            print(f"战斗已持续 {max_fight_time} 秒，超时停止")
            
    except KeyboardInterrupt:
        print("\n用户手动停止循环")
    except Exception as e:
        print(f"\n执行过程中发生错误: {e}")
    
    print("循环复现操作结束")
    return no_monster_ui_error

if __name__ == "__main__":
    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(description="循环复现按键操作直到检测到指定图片")
    
    # 添加参数
    parser.add_argument(
        "-r", "--recording", 
        type=str, 
        default=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "reproduce", "letu_elysia_star_jiaxin_fangting_loop.json"),
        help="记录按键操作的JSON文件路径，默认使用reproduce文件夹下的letu_elysia_star_jiaxin_fangting_loop.json"
    )
    
    parser.add_argument(
        "-s", "--stop-image", 
        type=str, 
        default=None,
        help="停止图片的路径，检测到该图片时停止复现"
    )
    
    parser.add_argument(
        "-c", "--confidence", 
        type=float, 
        default=0.6,
        help="图片检测的置信度阈值，默认0.6"
    )
    
    parser.add_argument(
        "--region", 
        type=str, 
        default=None,
        help="识别区域范围，格式为 'x1,y1,x2,y2'，表示左上角和右下角坐标，默认为None（全屏）"
    )
    
    parser.add_argument(
        "--debug", 
        action="store_true",
        help="是否显示调试信息，默认False"
    )
    
    # 解析命令行参数
    args = parser.parse_args()
    
    # 处理 region 参数
    region = None
    if args.region:
        try:
            region = tuple(map(int, args.region.split(',')))
            if len(region) != 4:
                raise ValueError("区域参数必须包含4个数值")
        except ValueError as e:
            print(f"错误: 区域参数格式不正确，应为 'x1,y1,x2,y2' 格式")
            sys.exit(1)
    
    # 执行主函数
    # 根据参数情况调用letu_fight函数
    if args.stop_image is not None and region is not None:
        # 如果同时指定了stop_image和region
        letu_fight(args.recording, args.stop_image, args.confidence, region, debug=args.debug)
    elif args.stop_image is not None:
        # 如果只指定了stop_image
        letu_fight(args.recording, args.stop_image, args.confidence, debug=args.debug)
    elif region is not None:
        # 如果只指定了region
        letu_fight(args.recording, region=region, debug=args.debug)
    else:
        # 如果都未指定，使用默认值
        letu_fight(args.recording, debug=args.debug)
