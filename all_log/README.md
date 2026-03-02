# 自动输出记录工具使用说明

## 功能介绍

本工具提供了强大的自动日志记录功能，导入模块后会自动替换Python内置的`print`函数，将所有`print`语句的输出同时保存到文件和显示在控制台，无需手动调用任何函数。

同时，工具也提供了`save_log`函数用于更灵活的手动日志记录。

日志文件自动使用 `调用文件名_YYYYMMDD_HHMMSS.log` 的格式命名。

## 文件说明

- `save_output.py`：核心工具文件，实现了 `save_log` 函数
- `README.md`：使用说明文档
- `test_save_log.py`：测试文件，展示了如何使用该工具

## 基本使用方法

### 自动记录print输出（推荐）

只需在Python文件开头导入模块，所有`print`语句的输出都会自动被记录：

```python
# 在Python文件开头导入模块
import record_test.save_output

# 所有print语句的输出都会自动记录到日志文件
print("程序开始执行")
print("正在处理数据")
print("警告：磁盘空间不足")
print("错误：文件不存在")
print("调试信息：变量值为10")
print("程序执行完成")
```

### 手动调用save_log函数

如果需要更灵活的日志记录方式，也可以直接调用`save_log`函数：

```python
from record_test.save_output import save_log

# 基本用法
save_log("程序开始执行")
save_log("正在处理数据")
save_log("警告：磁盘空间不足")
save_log("错误：文件不存在")
save_log("调试信息：变量值为10")
save_log("程序执行完成")
```

## 应用到everyday.py

以下是如何将自动输出记录工具应用到everyday.py的示例：

### 方法1：自动记录所有print输出（推荐）

```python
# 在everyday.py文件开头导入模块
import record_test.save_output

# 然后所有print语句都会自动记录
def main():
    print("everyday.py程序启动")
    
    # 执行各种操作
    print("检查当前窗口状态")
    
    # 调用其他函数时记录
print("调用click_current_position函数")
    # click_current_position()
    
    print("程序执行完成")

if __name__ == "__main__":
    main()
```

### 方法2：手动调用save_log函数

```python
# 在everyday.py文件中导入save_log函数
from record_test.save_output import save_log

# 然后在需要记录日志的地方调用save_log函数
def main():
    save_log("everyday.py程序启动")
    
    # 执行各种操作
    save_log("检查当前窗口状态")
    
    # 调用其他函数时记录
save_log("调用click_current_position函数")
    # click_current_position()
    
    save_log("程序执行完成")

if __name__ == "__main__":
    main()
```

## 日志格式

日志信息同时显示在控制台和保存到文件，格式为：
```
[YYYY-MM-DD HH:MM:SS] 消息内容
```

## 注意事项

1. 确保record_test目录在Python的搜索路径中
2. 日志文件自动保存在save_output.py所在的目录
3. 每次程序运行都会生成新的日志文件，文件名包含时间戳
4. 日志文件使用UTF-8编码，可以正确显示中文
5. 导入模块后，内置的print函数会被替换为自动记录版本
6. 手动调用save_log函数和自动记录的print输出会保存在同一个日志文件中

## 故障排除

1. 如果日志文件没有生成，请检查：
   - 权限是否足够
   - 路径是否正确
   - 是否有异常发生导致程序提前退出

2. 如果中文显示乱码，请检查：
   - 日志查看工具是否支持utf-8编码

## 版本信息

- 版本：2.0.0
- 更新日期：2025-12-20
- 功能：简化版日志记录工具，支持同时输出到控制台和文件
