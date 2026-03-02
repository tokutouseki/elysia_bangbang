import os
import shutil

def clear_vedio_log():
    # 使用相对路径，相对于脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    vedio_log_path = os.path.join(script_dir, "..", "vedio_log")
    
    if not os.path.exists(vedio_log_path):
        print(f"Directory {vedio_log_path} does not exist. Creating it...")
        os.makedirs(vedio_log_path)
        print("Directory created successfully.")
        return
    
    print(f"Clearing contents of {vedio_log_path}...")
    
    # Remove all files and subdirectories
    for item in os.listdir(vedio_log_path):
        item_path = os.path.join(vedio_log_path, item)
        if os.path.isfile(item_path):
            os.remove(item_path)
            print(f"Removed file: {item}")
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)
            print(f"Removed directory: {item}")
    
    print("Directory cleared successfully.")

if __name__ == "__main__":
    clear_vedio_log()
