# letu_fight.py 使用说明

## 功能描述
该脚本用于游戏战斗自动化，通过循环复现预记录的按键操作，直到检测到指定的停止图片或满足其他停止条件。脚本使用多线程分离操作复现和图像检测功能，提高执行效率。

## 安装依赖
```bash
pip install pyautogui argparse
```

## 使用方法

### 基本用法
1. 以管理员身份运行脚本：
   - 右键点击脚本文件
   - 选择"以管理员身份运行"

2. 默认情况下，脚本会使用以下配置：
   - 记录文件：`reproduce/letu_elysia_star_jiaxin_fangting_loop.json`
   - 置信度阈值：0.6
   - 无默认停止图片

### 命令行参数
脚本支持以下命令行参数：

```bash
python letu_fight.py [OPTIONS]
```

| 参数 | 简写 | 说明 | 默认值 |
|------|------|------|--------|
| `--recording` | `-r` | 记录按键操作的JSON文件路径 | `reproduce/letu_elysia_star_jiaxin_fangting_loop.json` |
| `--stop-image` | `-s` | 停止图片的路径，检测到该图片时停止复现 | `None` |
| `--confidence` | `-c` | 图片检测的置信度阈值 | `0.6` |
| `--region` | | 识别区域范围，格式为 `x1,y1,x2,y2` | `None`（全屏） |
| `--debug` | | 是否显示调试信息 | `False` |

## 主要函数

### letu_fight(recording_file_path, stop_image_path=None, confidence=0.8, region=(1598, 945, 1719, 1064), debug=False)
- **功能**：循环复现按键操作直到检测到指定图片

- **参数**：
  - `recording_file_path`：记录按键操作的JSON文件路径
  - `stop_image_path`：停止图片的路径，检测到该图片时停止复现
  - `confidence`：图片检测的置信度阈值
  - `region`：识别区域范围，格式为 (x1, y1, x2, y2)
  - `debug`：是否显示调试信息

- **返回值**：
  - `True`：表示未检测到怪物UI错误
  - `False`：表示正常完成

### detect_monster_ui(monster_detected_event, monster_stop_event, stop_image_path, confidence, region=None, debug=False)
- **功能**：检测怪物UI的函数，持续运行直到收到停止信号

### detect_stop_image(stop_image_path, confidence, image_stop_event, monster_detected_event, region=None, debug=False)
- **功能**：检测停止图片的函数，持续运行直到检测到图片或收到停止信号

## 工作原理
1. 脚本启动多个线程：
   - 怪物UI检测线程：检测游戏中的怪物UI
   - 停止图片检测线程：检测指定的停止图片
   - 操作复现线程：复现预记录的按键操作

2. 停止条件：
   - 检测到停止图片且未检测到怪物UI
   - 未检测到怪物UI超过10秒
   - 战斗时间超过5分钟（超时）
   - 用户手动停止（Ctrl+C）

## 使用示例

### 1. 使用默认配置运行
```bash
python letu_fight.py
```

### 2. 指定记录文件和停止图片
```bash
python letu_fight.py --recording "reproduce/my_recording.json" --stop-image "photos/stop.png"
```

### 3. 设置置信度和识别区域
```bash
python letu_fight.py --confidence 0.7 --region "1500,900,1700,1000"
```

### 4. 启用调试模式
```bash
python letu_fight.py --debug
```

## 注意事项
1. 必须以管理员身份运行，否则可能无法正常工作
2. 确保游戏窗口已经打开并可操作
3. 记录文件必须是通过 `record.py` 生成的有效JSON文件
4. 停止图片必须清晰，以便准确检测
5. 识别区域应设置为停止图片可能出现的区域，以提高检测速度
6. 战斗过程中，请勿手动操作鼠标和键盘，以免干扰复现
7. 脚本会自动检测怪物UI，如果未检测到，会在10秒后停止并报错

## 常见问题

### 问题：未检测到怪物UI错误
**解决方法**：
- 确保游戏已进入战斗界面
- 检查YOLO模型是否正确识别怪物UI
- 调整置信度阈值

### 问题：无法检测到停止图片
**解决方法**：
- 确保停止图片清晰且与游戏中的实际图像一致
- 降低置信度阈值
- 调整识别区域，确保包含停止图片

### 问题：战斗超时停止
**解决方法**：
- 检查停止图片是否正确
- 确保战斗流程能够正常结束
- 如果战斗确实需要更长时间，修改脚本中的 `max_fight_time` 参数

## 依赖关系
- **replay_keyboard.py**：提供操作复现功能
- **bh3_yolo_recognizer.py**：提供YOLO目标识别功能
- **photos/clicks_keyboard.py**：提供图像检测辅助功能