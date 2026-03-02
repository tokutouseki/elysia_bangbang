# Electron 配置说明

## 项目概述

本项目已配置为使用 Electron 将前端应用打包为桌面窗口应用，确保可移植性和独立运行能力。

## 配置文件说明

### 1. package.json

已添加以下配置：

- 项目名称：`hongkai-helper`
- 主入口文件：`electron/main.js`
- 脚本命令：
  - `electron:dev`：在开发模式下运行 Electron
  - `electron:build`：构建生产版本并打包为可执行文件
- Electron 相关依赖：
  - `electron`：^28.2.0
  - `electron-builder`：^24.12.0
- 构建配置：
  - 应用 ID：`com.hongkai.helper`
  - 产品名称：`Hongkai Helper`
  - 输出目录：`dist-electron`
  - 支持的 Windows 目标：`nsis` 和 `portable`
  - 便携版文件名：`HongkaiHelper-${version}-portable.exe`

### 2. electron/main.js

Electron 主进程文件，负责：

- 创建桌面窗口（尺寸：960x720）
- 加载应用（开发模式下加载 http://localhost:5173，生产模式下加载本地文件）
- 处理窗口事件和应用生命周期

### 3. .gitignore

已添加 Electron 相关文件的忽略规则：

- `dist-electron/`：Electron 构建输出目录
- 其他标准忽略项

## 安装和运行步骤

### 1. 安装依赖

```bash
# 在 front 目录下运行
npm install
```

**注意**：如果遇到网络问题导致 Electron 下载失败，可以尝试以下方法：

- 使用代理服务器
- 切换网络环境
- 手动下载 Electron 并放置到指定目录

### 2. 开发模式运行

```bash
# 启动 Vite 开发服务器
npm run dev

# 在另一个终端中启动 Electron
npm run electron:dev
```

### 3. 构建生产版本

```bash
# 构建前端应用并打包为可执行文件
npm run electron:build
```

构建完成后，可执行文件将生成在 `dist-electron` 目录中：

- 安装版：`Hongkai Helper Setup ${version}.exe`
- 便携版：`HongkaiHelper-${version}-portable.exe`

## 可移植性说明

- **便携版**：`HongkaiHelper-${version}-portable.exe` 是一个独立的可执行文件，无需安装，可直接运行
- **安装版**：会在系统中创建快捷方式和相关注册表项

## 技术栈

- **前端**：Vue 3 + Vite
- **桌面打包**：Electron
- **构建工具**：electron-builder

## 注意事项

1. 确保网络环境良好，以便下载 Electron 依赖
2. 构建过程可能需要较长时间，请耐心等待
3. 如有问题，请查看控制台输出或日志文件

## 故障排除

### 常见问题

1. **Electron 下载失败**
   - 解决方案：使用代理或手动下载 Electron

2. **构建失败**
   - 解决方案：确保所有依赖已正确安装，检查网络连接

3. **应用无法启动**
   - 解决方案：检查前端应用是否正常运行，确保端口 5173 未被占用

### 手动下载 Electron

如果自动下载失败，可以手动下载对应版本的 Electron：

1. 访问 https://github.com/electron/electron/releases
2. 下载对应平台的 Electron 包（例如：`electron-v28.2.0-win32-x64.zip`）
3. 解压到 `node_modules/electron/dist` 目录

## 总结

本项目已完成 Electron 配置，确保前端应用可以在独立的桌面窗口中运行，提高用户体验和可移植性。通过便携版可执行文件，用户可以在不同设备上轻松使用该工具，无需安装额外依赖。