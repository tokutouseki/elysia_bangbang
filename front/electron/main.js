const { app, BrowserWindow } = require('electron');
const path = require('path');
const url = require('url');

console.log('Electron main process starting...');
console.log('Current directory:', __dirname);
console.log('ELECTRON_START_URL:', process.env.ELECTRON_START_URL);

let mainWindow;

function createWindow() {
  console.log('Creating window...');
  
  // 强制应用在前台运行
  app.focus();
  
  mainWindow = new BrowserWindow({
    width: 960,
    height: 720,
    resizable: false,
    maximizable: false,
    title: 'HongkaiHelper',
    show: false, // 先隐藏，等ready-to-show事件后再显示
    alwaysOnTop: false, // 不强制置顶，但确保能正常显示
    frame: true, // 保持窗口框架
    backgroundColor: '#fce4ec', // 设置窗口背景色为粉色主题色
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
      devTools: false
    }
  });

  // 禁用默认菜单
  const { Menu } = require('electron');
  Menu.setApplicationMenu(null);

  const startUrl = process.env.ELECTRON_START_URL || url.format({
    pathname: path.join(__dirname, '../dist/index.html'),
    protocol: 'file:',
    slashes: true
  });

  console.log('Loading URL:', startUrl);
  mainWindow.loadURL(startUrl);



  // 监听页面加载完成事件
  mainWindow.webContents.on('did-finish-load', function() {
    console.log('Page finished loading');
  });

  mainWindow.on('closed', function () {
    console.log('Window closed');
    mainWindow = null;
  });

  mainWindow.on('ready-to-show', function () {
    console.log('Window ready to show');
    // 显示窗口并聚焦
    mainWindow.show();
    mainWindow.focus();
    console.log('Window shown and focused');
  });

  mainWindow.on('error', function (error) {
    console.error('Window error:', error);
  });

  // 监听窗口显示事件
  mainWindow.on('show', function() {
    console.log('Window is now visible');
  });

  // 监听窗口聚焦事件
  mainWindow.on('focus', function() {
    console.log('Window is now focused');
  });
}

// 确保应用完全就绪后再创建窗口
app.on('ready', function() {
  console.log('App ready, creating window...');
  // 延迟一下确保应用完全初始化
  setTimeout(() => {
    createWindow();
  }, 1000);
});

app.on('window-all-closed', function () {
  console.log('All windows closed');
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', function () {
  console.log('App activated');
  if (mainWindow === null) {
    createWindow();
  }
});

app.on('quit', function() {
  console.log('App quitting');
});

// 监听应用激活事件
app.on('browser-window-focus', function() {
  console.log('Browser window focused');
});