# 工作环境结构

## 目录结构

```
hongkai\
├── all_log/                    # 日志文件目录
│   ├── README.md
│   ├── run_script.py
│   └── save_output.py          # 日志保存模块
├── character/                  # 角色相关脚本
│   ├── __init__.py
│   ├── __pycache__/
│   ├── check_next_done.py
│   ├── core_done.json
│   ├── elysia_star.py          # 爱莉希雅星脚本
│   ├── keyin_all.py
│   ├── letu_elysia_star.py     # 乐土爱莉希雅星脚本
│   ├── letu_fight.py           # 乐土战斗脚本
│   ├── letu_find_way.py        # 乐土寻路脚本
│   ├── letu_normal_keyin.py    # 乐土普通刻印脚本
│   ├── select_core_keyin.py    # 核心选择脚本
│   ├── shangdian_buy.py        # 商店购买脚本
│   ├── wuli_character.py       # 物理角色脚本
│   └── yuansu_character.py     # 元素角色脚本
├── front/                      # 前端项目目录
│   ├── .vscode/
│   ├── dist/
│   ├── dist-electron/
│   ├── electron/
│   ├── public/
│   ├── src/
│   ├── .gitignore
│   ├── ELECTRON_SETUP.md
│   ├── README.md
│   ├── index.html
│   ├── package-lock.json
│   ├── package.json
│   └── vite.config.js
├── funs/                       # 功能脚本目录
│   ├── config.json
│   ├── run_script.py
│   ├── send_email.py
│   └── upload_image.py
├── node/                       # Node.js目录
├── ocr/                        # OCR文字识别模块
│   ├── __pycache__/
│   ├── models/                 # OCR模型目录
│   ├── keyin.json
│   ├── keyin_detail.json
│   ├── ocr_click.py
│   └── ocr_functions.py        # OCR核心功能
├── photos/                     # 图片资源目录
│   ├── __pycache__/
│   ├── clicks_keyboard.py      # 点击和键盘操作模块
│   └── *.png                   # 各种游戏界面截图
├── process/                    # 流程脚本目录
│   ├── __pycache__/
│   ├── chaoxiankongjian.py     # 超限空间流程
│   ├── everyday.py             # 每日流程
│   ├── everyweek_gift.py       # 每周礼物流程
│   ├── full_operation.py
│   ├── jiantuangongxian.py     # 舰团贡献流程
│   ├── letu.py                 # 乐土流程
│   ├── main_screen.py
│   ├── maoxian_weituo.py       # 冒险委托流程
│   ├── renwu_jianfu.py         # 任务减负流程
│   ├── shenzhijian.py          # 神之键流程
│   ├── simulation_combat_room.py # 模拟作战室流程
│   ├── zhanchang.py            # 战场流程
│   └── zhuzhanrenwu_set.py     # 主战人物设置
├── Python3.11/                 # Python 3.11 解释器
├── Python3.13/                 # Python 3.13 解释器
├── reproduce/                  # 复现配置目录
│   ├── clear_letu_chuzhan_set.json
│   ├── letu_elysia_star_jiaxin_fangting_loop.json
│   ├── letu_level.json
│   ├── renwu_jianfu.json
│   ├── shenzhijian.json
│   └── zhuiyizhizheng.json
├── time_date/                  # 时间日期模块
│   ├── __pycache__/
│   ├── current_datetime.json
│   └── custom_datetime.py
├── tools/                      # 工具脚本目录
│   ├── __pycache__/
│   ├── reproduce/
│   ├── clear_vedio_log.md
│   ├── clear_vedio_log.py
│   ├── everyweek_gift.md
│   ├── everyweek_gift.py
│   ├── get_mouse_position.md
│   ├── get_mouse_position.py
│   ├── jiantuangongxian.md
│   ├── jiantuangongxian.py
│   ├── letu_fight.md
│   ├── letu_fight.py
│   ├── maoxian_weituo.md
│   ├── maoxian_weituo.py
│   ├── record.md
│   ├── record.py
│   ├── replay_keyboard.md
│   ├── replay_keyboard.py
│   ├── simulation_combat_room.md
│   └── simulation_combat_room.py
├── vedio_log/                  # 视频日志目录
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
├── yolo_config/                # YOLO备份，正式使用需放到Python3.11下命名为yolo的文件夹
│   ├── To_use/                 # 待使用的模型和脚本
│   │   ├── best.onnx           # YOLO模型
│   │   └── predict.py          # 预测脚本
│   └── configs/                # 配置文件
│       └── data.yaml           # 数据配置文件
└── yolo_server_final.py        # YOLO服务器最终版
```

# 注意
1.OCR使用的是ppv4
2.使用yolo11n转化为best.onnx的模型
