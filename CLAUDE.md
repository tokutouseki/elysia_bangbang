# hongkai_done — 崩坏3自动化脚本集合（参考项目）

此项目的核心功能已提取到 `D:\TokusCode\bbb_assistant\backend\src\modules\hongkai\`。

## 项目概述
基于 OCR (RapidOCR) + YOLO (ONNX) 的崩坏3游戏自动化脚本集合，覆盖日常、周常、往世乐土全流程。

## 核心文件速查

### 游戏自动化流程（process/）
| 脚本 | 功能 |
|------|------|
| `everyday.py` | 每日任务：登录领取 → 出击减负 → 家园委托 → 舰团 → 任务奖励 |
| `full_operation.py` | 主调度器：按星期几执行任务组合 |
| `letu.py` | 往世乐土入口 |
| `main_screen.py` | 主界面检测与导航 |

### 角色脚本（character/）— 往世乐土战斗AI
| 脚本 | 功能 | 大小 |
|------|------|------|
| `letu_elysia_star.py` | 乐土全流程编排 | 65KB |
| `letu_find_way.py` | 路径寻找/地图导航 | 110KB |
| `letu_fight.py` | 战斗逻辑（多线程） | — |
| `letu_normal_keyin.py` | 普通刻印选择（加权优先级） | — |
| `select_core_keyin.py` | 核心刻印选择 | — |
| `shangdian_buy.py` | 商店购买 | — |
| `keyin_all.py` | OCR刻印点击函数集 | 35KB |

### 底层服务
| 文件 | 功能 | 端口 |
|------|------|------|
| `yolo_server_final.py` | YOLO ONNX推理，24类游戏元素 | TCP 5001 |
| `ocr_server_final.py` | PP-OCRv4文字识别 | TCP 5002 |
| `call_YOLO.py` | YOLO调用层，自动管理服务端 | — |
| `ocr/ocr_functions.py` | OCR封装（37KB） | — |
| `ocr/ocr_click.py` | 100+游戏文本点击映射（17KB） | — |

### 输入/视觉
| 文件 | 功能 |
|------|------|
| `photos/clicks_keyboard.py` | 模板匹配 + 键鼠模拟（Win32 SendInput + PyAutoGUI） |
| `photos/*.png` | 112张模板图片 |
| `on_window.py` | Win32 API窗口查找、聚焦、管理员提权 |
| `replay_keyboard.py` | 键鼠录制JSON回放 |

### 配置
| 文件 | 功能 |
|------|------|
| `config.py` | JSON配置读写（点号嵌套key） |
| `config.json` | 运行时状态（任务完成追踪） |
| `config_ini.json` | 初始配置模板 |

## 环境
- Python 3.11（`Python3.11/python.exe`）
- 依赖：onnxruntime, opencv-python, pyautogui, pynput, psutil, rapidocr-onnxruntime, pywin32
- YOLO 模型：`yolo_config/To_use/best.onnx`（yolo11n, 640×384, 24类）
- OCR 模型：`ocr/models/ch_PP-OCRv4_*.onnx`

## 已提取到 bbb-assistant
路径：`D:\TokusCode\bbb_assistant\backend\src\modules\hongkai\`

提取内容：
- templates/clicks_keyboard.py + 112 PNGs
- on_window.py, config.py, replay_keyboard.py
- call_YOLO.py, yolo_client.py, yolo_server_final.py
- ocr/ (ocr_functions.py, ocr_click.py, ocr_client.py, ocr_server_final.py, models/)
- bh3_yolo_recognizer.py, save_output.py, vedio_log.py, time_date/custom_datetime.py

YOLO 模型：`backend/data/models/detect/yolo11n_elysian_realm_det.onnx`
