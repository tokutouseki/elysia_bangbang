# 崩坏3自动化工具集

## 项目简介

这是一个针对崩坏3游戏的自动化工具集，主要功能包括：
- OCR文字识别
- YOLO目标检测
- 游戏流程自动化
- 角色脚本
- 工具脚本集合

## 项目结构

```
hongkai\
├── all_log/                    # 日志文件目录
├── character/                  # 角色相关脚本
├── front/                      # 前端项目目录
├── funs/                       # 功能脚本目录
├── node/                       # Node.js目录
├── ocr/                        # OCR文字识别模块
├── photos/                     # 图片资源目录
├── process/                    # 流程脚本目录
├── Python3.11/                 # Python 3.11 解释器
├── Python3.13/                 # Python 3.13 解释器
├── reproduce/                  # 复现配置目录
├── time_date/                  # 时间日期模块
├── tools/                      # 工具脚本目录
├── vedio_log/                  # 视频日志目录
├── yolo_config/                # YOLO备份，正式使用需放到Python3.11下命名为yolo的文件夹
├── api_server.py               # API服务器
├── bh3_yolo_recognizer.py      # 崩坏3 YOLO识别器
├── call_YOLO.py                # YOLO调用脚本
├── config.json                 # 配置文件
├── config.py                   # 配置模块
├── config_ini.json             # 初始配置文件
├── get_mouse_position.py       # 获取鼠标位置脚本
├── ocr_client.py               # OCR客户端
├── ocr_server_final.py         # OCR服务器最终版
├── on_window.py                # 窗口操作模块
├── record.py                   # 录制脚本
├── replay_keyboard.py          # 键盘重放脚本
├── start_all.bat               # 启动所有服务脚本
├── start_front.bat             # 启动前端脚本
├── start_ocr_service.py        # 启动OCR服务脚本
├── start_yolo_service.py       # 启动YOLO服务脚本
├── vedio_log.py                # 视频日志模块
├── WORKSPACE_STRUCTURE.md      # 工作空间结构说明
├── yolo_client.py              # YOLO客户端
└── yolo_server_final.py        # YOLO服务器最终版
```

## 核心功能

### 1. OCR文字识别

- **OCR服务器**: `ocr_server_final.py`
- **OCR客户端**: `ocr_client.py`
- **核心功能**: 识别游戏界面文字，支持文本查找和点击

### 2. YOLO目标检测

- **YOLO服务器**: `yolo_server_final.py`
- **YOLO客户端**: `yolo_client.py`
- **核心功能**: 检测游戏界面目标，支持目标查找和点击

### 3. 自动化流程

- **每日流程**: `process/everyday.py`
- **乐土流程**: `process/letu.py`
- **冒险委托流程**: `process/maoxian_weituo.py`
- **任务减负流程**: `process/renwu_jianfu.py`
- **每周礼物**: `process/everyweek_gift.py`
- **舰团贡献**: `process/jiantuangongxian.py`
- **模拟作战室**: `process/simulation_combat_room.py`
- **超限空间流程**: `process/chaoxiankongjian.py`
- **神之键流程**: `process/shenzhijian.py`
- **战场流程**: `process/zhanchang.py`

### 4. 角色脚本

- **爱莉希雅星脚本**: `character/elysia_star.py`
- **乐土爱莉希雅星脚本**: `character/letu_elysia_star.py`
- **乐土战斗脚本**: `character/letu_fight.py`
- **乐土寻路脚本**: `character/letu_find_way.py`
- **元素角色脚本**: `character/yuansu_character.py`
- **物理角色脚本**: `character/wuli_character.py`
- **商店购买脚本**: `character/shangdian_buy.py`
- **核心选择脚本**: `character/select_core_keyin.py`
- **乐土普通刻印脚本**: `character/letu_normal_keyin.py`

### 5. 工具脚本

- **录制和重放**: `tools/record.py` 和 `tools/replay_keyboard.py`
- **获取鼠标位置**: `tools/get_mouse_position.py`
- **视频日志清理**: `tools/clear_vedio_log.py`

## 环境要求

- **Python**: 3.11 或 3.13
- **Node.js**: 用于前端项目
- **依赖库**: 
  - RapidOCR (OCR识别)
  - OpenCV (图像处理)
  - PyAutoGUI (自动化操作)
  - NumPy (数值计算)

## 安装与运行

### 1. 安装依赖

```bash
# 安装Python依赖
pip install rapidocr_onnxruntime opencv-python numpy pyautogui

# 安装Node.js依赖（如果需要前端）
npm install
```

### 2. 启动服务

```bash
# 启动所有服务
start_all.bat

# 或单独启动
start_ocr_service.py  # 启动OCR服务
start_yolo_service.py  # 启动YOLO服务
start_front.bat  # 启动前端
```

### 3. 使用方法

#### OCR文字识别

```python
from ocr.ocr_functions import is_ocr_text, click_ocr_text

# 查找文字
found, x, y, region, text = is_ocr_text('目标文字')

# 点击文字
success = click_ocr_text('目标文字')
```

#### 自动化流程

```python
# 运行每日流程
from process.everyday import run_everyday
run_everyday()

# 运行乐土流程
from process.letu import run_letu
run_letu()
```

## 配置说明

### 配置文件

- **config.json**: 主配置文件
- **config_ini.json**: 初始配置文件
- **config.py**: 配置模块，用于加载和管理配置

### 环境变量

- 无需特殊环境变量，所有配置均通过配置文件管理

## 性能优化

1. **OCR优化**:
   - 使用RapidOCR引擎，性能提升3-5倍
   - 区域限制，减少处理图像大小
   - 懒加载模式，避免重复初始化

2. **YOLO优化**:
   - 使用ONNX Runtime加速推理
   - 模型文件存储在项目目录，便于部署

3. **流程优化**:
   - 并行处理，提高自动化效率
   - 错误处理，增强稳定性

## 注意事项

1. **管理员权限**:
   - 部分操作需要管理员权限，可使用 `run_as_admin()` 函数

2. **窗口聚焦**:
   - 使用前确保游戏窗口已聚焦，可通过 `focus_bh3_window()` 函数

3. **调试模式**:
   - 遇到问题时，启用调试模式查看详细信息

4. **模型文件**:
   - OCR模型已包含在项目中，无需额外下载

5. **模型文件**:
   - YOLO模型转的onnx已包含在项目中，无需额外下载

6. **正式使用**:
   - 正式使用时按照工作环境的样式放置依赖最好

## 常见问题

### OCR识别失败

- 确保游戏窗口已聚焦
- 调整识别区域
- 启用图像预处理
- 检查模型文件是否完整

### YOLO检测失败

- 确保YOLO服务已启动
- 检查模型文件是否正确
- 调整置信度阈值

### 自动化流程卡住

- 检查游戏界面是否与预期一致
- 调整流程参数
- 查看日志文件定位问题


## 许可证

本项目采用MIT许可证，详见LICENSE文件。

### 署名要求

在使用、修改或分发本软件时，请确保：
1. 保留本许可证文件中的版权声明
2. 在软件的所有副本或重要部分中包含本许可证通知
3. 对于基于本软件的衍生作品，请在文档中明确注明来源

### 开源声明

本软件完全开源，欢迎：
- 自由使用和修改代码
- 自由分发和 sublicense
- 用于商业和非商业目的

