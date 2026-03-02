# clear_vedio_log.py 使用说明

## 功能描述

该脚本用于清除项目根目录下的 `vedio_log` 目录中的所有内容，包括文件和子目录。脚本使用相对路径，因此可以在任何位置执行。

## 脚本特点

- **自动处理目录不存在的情况**：如果 `vedio_log` 目录不存在，脚本会自动创建它
- **详细的操作输出**：执行过程中会显示每个删除的文件和目录
- **安全可靠**：只操作指定目录，不会影响其他文件

## 使用方法

### 方法一：直接运行

1. 打开命令行终端（如 PowerShell）
2. 切换到项目根目录：`cd c:\Users\33985\Desktop\hongkai`
3. 运行脚本：`python tools\clear_vedio_log.py`

### 方法二：作为模块导入

```python
from tools.clear_vedio_log import clear_vedio_log

# 调用函数清除目录
clear_vedio_log()
```

## 执行示例

```
$ python tools\clear_vedio_log.py
Clearing contents of c:\Users\33985\Desktop\hongkai\vedio_log...
Removed file: example.txt
Removed directory: subfolder
Directory cleared successfully.
```

## 注意事项

1. 执行此脚本会删除 `vedio_log` 目录中的所有内容，请确保该目录中没有需要保留的文件
2. 脚本需要有足够的权限来删除目录中的文件和子目录
3. 如果 `vedio_log` 目录不存在，脚本会自动创建它
4. 脚本使用相对路径，因此可以在任何位置执行，不受工作目录影响

## 脚本路径

`tools/clear_vedio_log.py` (相对于项目根目录)
