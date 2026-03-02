# replay_keyboard.py 使用说明

## 功能描述
该脚本用于复现之前通过record.py记录的键盘和鼠标操作，根据JSON记录文件执行相同的操作序列。

## 安装依赖
```bash
pip install pyautogui
```

## 使用方法
1. 以管理员身份运行脚本：
   - 右键点击脚本文件
   - 选择"以管理员身份运行"

2. 脚本会自动聚焦到BH3游戏窗口

3. 复现操作：
   - 脚本默认会复现`reproduce/letu_elysia_star_jiaxin_fangting_loop.json`文件中的操作
   - 也可以修改脚本中的文件路径参数，复现其他记录文件

## 复现内容
- **键盘事件**：按照记录的时间按下和松开对应的按键
- **鼠标事件**：按照记录的时间和位置执行鼠标点击和滚轮滚动

## 主要函数

### replay_keyboard_events(json_file_path, stop_event=None, debug=False)
- **功能**：复现JSON文件中记录的键盘事件和鼠标事件

- **参数**：
  - `json_file_path`：JSON记录文件的路径
  - `stop_event`：用于接收停止信号的事件对象（可选）
  - `debug`：是否显示调试信息（默认False）

- **返回值**：无

## 注意事项
1. 必须以管理员身份运行，否则可能无法正常工作
2. 脚本会自动聚焦到BH3游戏窗口，确保游戏窗口已经打开
3. 复现操作时，请确保游戏窗口处于可操作状态
4. 复现过程中，请勿手动操作鼠标和键盘，以免干扰复现

## 自定义复现文件
要复现不同的记录文件，需要修改脚本末尾的调用：

```python
# 修改这行代码中的文件路径
replay_keyboard_events(json_file_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), "reproduce", "your_recording_file.json"))
```

## 示例输出
```
0. 执行focus_bh3_window函数：
BH3窗口已聚焦！
按下 w 键
松开 w 键
按下 j 键
松开 j 键
按下 k 键
松开 k 键
# 其他操作...
```

## 调试模式
如果需要查看详细的复现过程，可以启用调试模式：

```python
replay_keyboard_events(
    json_file_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), "reproduce", "your_recording_file.json"),
    debug=True
)
```

启用调试模式后，会显示每个事件的详细信息，包括事件类型、时间、坐标等。