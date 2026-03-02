<script setup>
import { ref, computed, onMounted, watch } from 'vue'

const activeNav = ref('home')
const isPinkTheme = ref(true)

const navItems = [
  { id: 'home', icon: '🏠', label: '主页' },
  { id: 'help', icon: '📖', label: '帮助' },
  { id: 'tools', icon: '🔧', label: '工具箱' },
  { id: 'theme', icon: '🎨', label: '主题' },
  { id: 'support', icon: '💖', label: '赞赏' },
  { id: 'settings', icon: '⚙️', label: '关于' }
]

const toggleTheme = () => {
  isPinkTheme.value = !isPinkTheme.value
  activeNav.value = 'home'
}

const themeColor = computed(() => {
  return isPinkTheme.value ? '#fce4ec' : '#e3f2fd'
})

const themeSecondaryColor = computed(() => {
  return isPinkTheme.value ? '#e3f2fd' : '#fce4ec'
})

const themeBorderColor = computed(() => {
  return isPinkTheme.value ? '#f8bbd0' : '#bbdefb'
})

const themeAccentColor = computed(() => {
  return isPinkTheme.value ? '#1976d2' : '#e91e63'
})

const themeWarningColor = computed(() => {
  return isPinkTheme.value ? '#1565c0' : '#e91e63'
})

const activeIconHue = computed(() => {
  return isPinkTheme.value ? '180deg' : '340deg'
})

const backgroundImage = computed(() => {
  const theme = isPinkTheme.value ? 'pink' : 'blue'
  return new URL(`./assets/images/background_${theme}.png`, import.meta.url).href
})

const tasks = computed(() => {
  const theme = isPinkTheme.value ? 'pink' : 'blue'
  return [
    { id: 1, name: '完整运行', icon: new URL(`./assets/tasks/${theme}/task1.png`, import.meta.url).href, script: 'full_operation.py' },
    { id: 2, name: '每日任务', icon: new URL(`./assets/tasks/${theme}/task2.png`, import.meta.url).href, script: 'everyday.py' },
    { id: 3, name: '每周减负', icon: new URL(`./assets/tasks/${theme}/task3.png`, import.meta.url).href, script: 'renwu_jianfu.py' },
    { id: 4, name: '记忆战场', icon: new URL(`./assets/tasks/${theme}/task4.png`, import.meta.url).href, script: 'zhanchang.py' },
    { id: 5, name: '往世乐土', icon: new URL(`./assets/tasks/${theme}/task5.png`, import.meta.url).href, script: 'letu.py' }
  ]
})

const runScript = async (scriptName) => {
  try {
    console.log(`运行脚本: ${scriptName}`)
    
    // 发送请求到后端API
    const response = await fetch(`http://localhost:8002/run-script?script=${scriptName}`)
    const result = await response.json()
    
    console.log('运行结果:', result)
    
    // 运行结束后显示结果
    if (result.status === 'success') {
      // 构建详情信息
      let details = `脚本运行成功: ${scriptName}\n`
      details += `退出码: ${result.exit_code}\n\n`
      details += `运行详情:\n`
      details += result.latest_log || '无最新日志信息'
      alert(details)
    } else {
      // 构建错误信息
      let details = `脚本运行失败: ${scriptName}\n\n`
      details += `错误信息:\n`
      details += result.error || result.stderr || '未知错误'
      details += '\n\n'
      details += `最新日志:\n`
      details += result.latest_log || '无最新日志信息'
      alert(details)
    }
  } catch (error) {
    console.error('运行脚本失败:', error)
    alert(`运行脚本失败: ${scriptName}\n网络错误: ${error.message}`)
  }
}

const helpTabs = ['使用教程', '常见问题']
const activeHelpTab = ref('使用教程')

const settingsTabs = ['日常', '战场', '深渊', '乐土', '委托', '舰团', '日志', '我']
const activeSettingsTab = ref('日常')

// 日志相关变量
const logFiles = ref([])
const selectedLogFile = ref(null)
const logFileContent = ref('')
const isLogFileOpen = ref(false)

// 任务名称映射（英文到中文）
const taskNameMapping = {
  "everyday.daily_operations()": "每日任务",
  "renwu_jianfu.renwu_jianfu()": "任务减负",
  "everyweek_gift.get_gift()": "每周礼包",
  "letu.letu()": "乐土",
  "simulation_combat_room.simulation_combat_room()": "模拟作战室",
  "zhanchang.zhanchang_jianfu()": "战场",
  "jiantuangongxian.jiantuangongxian()": "舰团贡献"
}

// 获取日志文件列表
const getLogFiles = async () => {
  console.log('调用getLogFiles函数')
  try {
    console.log('正在获取日志文件列表...')
    const response = await fetch('http://localhost:8002/get-log-files')
    console.log('获取日志文件列表成功，响应状态:', response.status)
    const result = await response.json()
    console.log('解析响应结果成功，结果:', result)
    if (result.status === 'success') {
      console.log('获取日志文件列表成功，文件数量:', result.files.length)
      logFiles.value = result.files
    } else {
      console.error('获取日志文件列表失败:', result.error)
    }
  } catch (error) {
    console.error('获取日志文件列表失败:', error)
  }
}

// 读取日志文件内容
const readLogFile = async (fileName) => {
  try {
    const response = await fetch(`http://localhost:8002/read-log-file?file=${fileName}`)
    const result = await response.json()
    if (result.status === 'success') {
      selectedLogFile.value = fileName
      logFileContent.value = result.content
      isLogFileOpen.value = true
    } else {
      console.error('读取日志文件失败:', result.error)
      alert(`读取日志文件失败: ${result.error}`)
    }
  } catch (error) {
    console.error('读取日志文件失败:', error)
    alert(`读取日志文件失败: ${error.message}`)
  }
}

// 关闭日志文件
const closeLogFile = () => {
  selectedLogFile.value = null
  logFileContent.value = ''
  isLogFileOpen.value = false
}

// 初始化时获取日志文件列表
onMounted(() => {
  if (activeSettingsTab.value === '日志') {
    getLogFiles()
  }
  if (activeNav.value === 'tools') {
    getToolsFiles()
  }
})

// 监听设置标签变化
watch(() => activeSettingsTab.value, (newTab) => {
  if (newTab === '日志') {
    getLogFiles()
  }
})

// 监听导航变化，实现实时刷新
watch(() => activeNav.value, (newNav) => {
  if (newNav === 'tools') {
    getToolsFiles()
  }
})

// 基于星期的任务分配映射（使用英文键，显示时转换为中文）
const weeklyTaskMapping = {
  "星期一": [
    "everyday.daily_operations()", 
    "renwu_jianfu.renwu_jianfu()", 
    "everyweek_gift.get_gift()", 
    "letu.letu()"
  ],
  "星期二": [
    "everyday.daily_operations()",
    "zhanchang.zhanchang_jianfu()"
  ],
  "星期三": [
    "everyday.daily_operations()",
    "zhanchang.zhanchang_jianfu()"
  ],
  "星期四": [
    "everyday.daily_operations()",
    "zhanchang.zhanchang_jianfu()"
  ],
  "星期五": [
    "everyday.daily_operations()"
  ],
  "星期六": [
    "everyday.daily_operations()"
  ],
  "星期日": [
    "everyday.daily_operations()",
    "jiantuangongxian.jiantuangongxian()",
    "simulation_combat_room.simulation_combat_room()"
  ]
}

// 获取中文任务名称
const getChineseTaskName = (task) => {
  return taskNameMapping[task] || task
}

// 赞赏页面图片上传相关
const fileInput = ref(null)
const uploadedImages = ref([])
const emailStatus = ref(null)
const emailMessage = ref('')

const triggerFileInput = () => {
  fileInput.value?.click()
}

const handleFileSelect = (event) => {
  const files = event.target.files
  processFiles(files)
}

const handleDrop = (event) => {
  const files = event.dataTransfer.files
  processFiles(files)
}

const processFiles = (files) => {
  Array.from(files).forEach(file => {
    if (isImageFile(file)) {
      const reader = new FileReader()
      reader.onload = (e) => {
        uploadedImages.value.push({
          name: file.name,
          url: e.target.result
        })
        
        // 上传到后端服务
        uploadToServer(file)
      }
      reader.readAsDataURL(file)
    }
  })
}

const uploadToServer = async (file) => {
  try {
    const formData = new FormData()
    formData.append('image', file)
    
    const response = await fetch('http://localhost:8000/upload', {
      method: 'POST',
      body: formData
    })
    
    const result = await response.json()
    console.log('Upload result:', result)
  } catch (error) {
    console.error('Upload failed:', error)
  }
}

const isImageFile = (file) => {
  const allowedTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/bmp']
  return allowedTypes.includes(file.type)
}

const removeImage = (index) => {
  uploadedImages.value.splice(index, 1)
}

const sendEmail = async () => {
  try {
    emailStatus.value = 'loading'
    emailMessage.value = '发送中...'
    
    const response = await fetch('http://localhost:8001/send-email', {
      method: 'GET'
    })
    
    const result = await response.json()
    
    if (result.status === 'success') {
      emailStatus.value = 'success'
      emailMessage.value = '邮件发送成功！'
      uploadedImages.value = [] // 清空图片列表
    } else {
      emailStatus.value = 'error'
      emailMessage.value = '邮件发送失败：' + result.message
    }
  } catch (error) {
    console.error('Send email failed:', error)
    emailStatus.value = 'error'
    emailMessage.value = '邮件发送失败：网络错误'
  }
}

// 工具箱相关
const toolsFiles = ref([])
const selectedToolFile = ref(null)
const toolFileContent = ref('')
const isToolFileOpen = ref(false)

// 计算属性：分离md文件和py文件
const mdFiles = computed(() => {
  return toolsFiles.value.filter(file => file.endsWith('.md')).sort((a, b) => a.localeCompare(b))
})

const pyFiles = computed(() => {
  return toolsFiles.value.filter(file => file.endsWith('.py')).sort((a, b) => a.localeCompare(b))
})

// 读取工具箱文件内容
const readToolFile = async (fileName) => {
  try {
    const response = await fetch(`http://localhost:8002/read-tool-file?file=${fileName}`)
    const result = await response.json()
    
    if (result.status === 'success') {
      // 打开新窗口显示文件内容
      openFileInNewWindow(fileName, result.content)
    } else {
      console.error('读取文件失败:', result.error)
      alert(`读取文件失败: ${result.error}`)
    }
  } catch (error) {
    console.error('读取文件失败:', error)
    alert(`读取文件失败: ${error.message}`)
  }
}

// 打开新窗口显示文件内容
const openFileInNewWindow = (fileName, content) => {
  // 创建新窗口
  const windowFeatures = 'width=800,height=600,menubar=no,toolbar=no,location=yes,scrollbars=yes'
  const newWindow = window.open('', '_blank', windowFeatures)
  
  if (newWindow) {
    // 使用DOM API构建HTML内容，避免Vue模板解析错误
    buildFileWindowContent(newWindow, fileName, content)
  } else {
    alert('无法打开新窗口，请检查浏览器设置')
  }
}

// 使用DOM API构建文件窗口内容
const buildFileWindowContent = (windowObj, fileName, content) => {
  // 清空窗口
  windowObj.document.open()
  
  // 创建DOCTYPE
  const doctype = windowObj.document.implementation.createDocumentType('html', '', '')
  windowObj.document.appendChild(doctype)
  
  // 创建html元素
  const html = windowObj.document.createElement('html')
  html.lang = 'zh-CN'
  
  // 创建head元素
  const head = windowObj.document.createElement('head')
  
  // 创建meta charset
  const metaCharset = windowObj.document.createElement('meta')
  metaCharset.charset = 'UTF-8'
  head.appendChild(metaCharset)
  
  // 创建meta viewport
  const metaViewport = windowObj.document.createElement('meta')
  metaViewport.name = 'viewport'
  metaViewport.content = 'width=device-width, initial-scale=1.0'
  head.appendChild(metaViewport)
  
  // 创建title
  const title = windowObj.document.createElement('title')
  title.textContent = fileName
  head.appendChild(title)
  
  // 创建style
  const style = windowObj.document.createElement('style')
  style.textContent = `
    body {
      font-family: 'Courier New', Courier, monospace;
      background-color: #000;
      color: #fff;
      margin: 0;
      padding: 20px;
      line-height: 1.4;
    }
    .header {
      padding-bottom: 15px;
      margin-bottom: 15px;
      border-bottom: 1px solid #333;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .file-name {
      font-size: 18px;
      font-weight: bold;
    }
    .content {
      white-space: pre-wrap;
      word-wrap: break-word;
      overflow-x: auto;
    }
    .close-button {
      background-color: #f44336;
      color: white;
      border: none;
      padding: 5px 10px;
      border-radius: 4px;
      cursor: pointer;
      font-size: 14px;
    }
    .close-button:hover {
      background-color: #d32f2f;
    }
  `
  head.appendChild(style)
  
  // 添加head到html
  html.appendChild(head)
  
  // 创建body元素
  const body = windowObj.document.createElement('body')
  
  // 创建header
  const header = windowObj.document.createElement('div')
  header.className = 'header'
  
  // 创建file-name
  const fileNameElement = windowObj.document.createElement('div')
  fileNameElement.className = 'file-name'
  fileNameElement.textContent = fileName
  header.appendChild(fileNameElement)
  
  // 创建close-button
  const closeButton = windowObj.document.createElement('button')
  closeButton.className = 'close-button'
  closeButton.textContent = '关闭'
  closeButton.onclick = () => windowObj.close()
  header.appendChild(closeButton)
  
  // 添加header到body
  body.appendChild(header)
  
  // 创建content
  const contentElement = windowObj.document.createElement('div')
  contentElement.className = 'content'
  contentElement.textContent = content
  body.appendChild(contentElement)
  
  // 添加body到html
  html.appendChild(body)
  
  // 添加html到document
  windowObj.document.appendChild(html)
  
  // 关闭document
  windowObj.document.close()
}

// HTML转义函数
const escapeHtml = (text) => {
  return text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;')
}

// 移除文件后缀
const removeFileExtension = (fileName) => {
  return fileName.replace(/\.(md|py)$/, '')
}

// 获取工具箱文件列表
const getToolsFiles = async () => {
  try {
    const response = await fetch('http://localhost:8002/get-tools-files')
    const result = await response.json()
    
    if (result.status === 'success') {
      toolsFiles.value = result.files
    } else {
      console.error('获取工具箱文件失败:', result.error)
    }
  } catch (error) {
    console.error('获取工具箱文件失败:', error)
  }
}

// 运行Python文件
const runPythonFile = async (fileName) => {
  try {
    const response = await fetch(`http://localhost:8002/run-python-file?file=${fileName}`)
    const result = await response.json()
    
    if (result.status === 'success') {
      alert(`成功启动: ${fileName}`)
    } else {
      alert(`启动失败: ${fileName}\n${result.error}`)
    }
  } catch (error) {
    console.error('运行Python文件失败:', error)
    alert(`运行Python文件失败: ${error.message}`)
  }
}



// reproduce文件相关
const reproduceFiles = ref([])
const isReproduceFileOpen = ref(false)
const selectedReproduceFile = ref(null)
const reproduceFileContent = ref('')

// 获取reproduce文件列表
const getReproduceFiles = async () => {
  try {
    const response = await fetch('http://localhost:8002/get-reproduce-files')
    const result = await response.json()
    
    if (result.status === 'success') {
      reproduceFiles.value = result.files
    } else {
      console.error('获取reproduce文件失败:', result.error)
    }
  } catch (error) {
    console.error('获取reproduce文件失败:', error)
  }
}

// 读取reproduce文件内容
const readReproduceFile = async (fileName) => {
  try {
    const response = await fetch(`http://localhost:8002/read-reproduce-file?file=${fileName}`)
    const result = await response.json()
    
    if (result.status === 'success') {
      selectedReproduceFile.value = fileName
      reproduceFileContent.value = result.content
      isReproduceFileOpen.value = true
      
      // 打开新窗口显示文件内容
      openReproduceFileWindow(fileName, result.content)
    } else {
      console.error('读取reproduce文件失败:', result.error)
      alert(`读取reproduce文件失败: ${result.error}`)
    }
  } catch (error) {
    console.error('读取reproduce文件失败:', error)
    alert(`读取reproduce文件失败: ${error.message}`)
  }
}

// 打开reproduce文件窗口
const openReproduceFileWindow = (fileName, content) => {
  // 创建新窗口
  const reproduceWindow = window.open('', '_blank', 'width=800,height=600,top=100,left=100')
  
  if (reproduceWindow) {
    // 使用DOM API构建HTML内容，避免Vue模板解析错误
    buildReproduceWindowContent(reproduceWindow, fileName, content)
  } else {
    alert('无法打开新窗口，请检查浏览器弹窗设置')
  }
}

// 使用DOM API构建reproduce窗口内容
const buildReproduceWindowContent = (windowObj, fileName, content) => {
  // 清空窗口
  windowObj.document.open()
  
  // 创建DOCTYPE
  const doctype = windowObj.document.implementation.createDocumentType('html', '', '')
  windowObj.document.appendChild(doctype)
  
  // 创建html元素
  const html = windowObj.document.createElement('html')
  html.lang = 'zh-CN'
  
  // 创建head元素
  const head = windowObj.document.createElement('head')
  
  // 创建meta charset
  const metaCharset = windowObj.document.createElement('meta')
  metaCharset.charset = 'UTF-8'
  head.appendChild(metaCharset)
  
  // 创建meta viewport
  const metaViewport = windowObj.document.createElement('meta')
  metaViewport.name = 'viewport'
  metaViewport.content = 'width=device-width, initial-scale=1.0'
  head.appendChild(metaViewport)
  
  // 创建title
  const title = windowObj.document.createElement('title')
  title.textContent = 'reproduce文件: ' + fileName
  head.appendChild(title)
  
  // 创建style
  const style = windowObj.document.createElement('style')
  style.textContent = `
    body {
      background-color: #000;
      color: #fff;
      font-family: 'Courier New', monospace;
      padding: 20px;
      margin: 0;
      overflow: auto;
      height: 100vh;
    }
    .header {
      border-bottom: 1px solid #333;
      padding-bottom: 10px;
      margin-bottom: 20px;
    }
    .filename {
      font-size: 18px;
      font-weight: bold;
      margin-bottom: 5px;
    }
    .content {
      white-space: pre-wrap;
      line-height: 1.4;
      font-size: 14px;
    }
  `
  head.appendChild(style)
  
  // 添加head到html
  html.appendChild(head)
  
  // 创建body元素
  const body = windowObj.document.createElement('body')
  
  // 创建header
  const header = windowObj.document.createElement('div')
  header.className = 'header'
  
  // 创建filename
  const fileNameElement = windowObj.document.createElement('div')
  fileNameElement.className = 'filename'
  fileNameElement.textContent = fileName
  header.appendChild(fileNameElement)
  
  // 创建timestamp
  const timestampElement = windowObj.document.createElement('div')
  timestampElement.className = 'timestamp'
  timestampElement.textContent = '打开时间: ' + new Date().toLocaleString()
  header.appendChild(timestampElement)
  
  // 添加header到body
  body.appendChild(header)
  
  // 创建content
  const contentElement = windowObj.document.createElement('div')
  contentElement.className = 'content'
  contentElement.textContent = content
  body.appendChild(contentElement)
  
  // 添加body到html
  html.appendChild(body)
  
  // 添加html到document
  windowObj.document.appendChild(html)
  
  // 关闭document
  windowObj.document.close()
}

// 关闭reproduce文件
const closeReproduceFile = () => {
  selectedReproduceFile.value = null
  reproduceFileContent.value = ''
  isReproduceFileOpen.value = false
}

// 监听导航变化，实现实时刷新
watch(() => activeNav.value, (newNav) => {
  if (newNav === 'tools') {
    getToolsFiles()
    getReproduceFiles()
  }
})

// 初始化时获取reproduce文件列表
onMounted(() => {
  if (activeNav.value === 'tools') {
    getReproduceFiles()
  }
})
</script>

<template>
  <div class="app-container" :style="{
    '--primary-color': themeColor,
    '--secondary-color': themeSecondaryColor,
    '--border-color': themeBorderColor,
    '--accent-color': themeAccentColor,
    '--warning-color': themeWarningColor,
    '--active-icon-hue': activeIconHue,
    '--card-bg-color': '#ffffff'
  }">
    <!-- 左侧导航栏 -->
    <nav class="sidebar">
      <div 
        class="nav-item" 
        :class="{ active: activeNav === 'home' }"
        @click="activeNav = 'home'"
      >
        <img src="./assets/icons/主页.svg" alt="主页" class="nav-icon-svg" />
        <span class="nav-label">{{ navItems[0].label }}</span>
      </div>
      <div 
        class="nav-item" 
        :class="{ active: activeNav === 'help' }"
        @click="activeNav = 'help'"
      >
        <img src="./assets/icons/帮助.svg" alt="帮助" class="nav-icon-svg" />
        <span class="nav-label">{{ navItems[1].label }}</span>
      </div>
      <div 
        class="nav-item" 
        :class="{ active: activeNav === 'tools' }"
        @click="activeNav = 'tools'"
      >
        <img src="./assets/icons/工具.svg" alt="工具箱" class="nav-icon-svg" />
        <span class="nav-label">{{ navItems[2].label }}</span>
      </div>
      <div 
        class="nav-item" 
        :class="{ active: activeNav === 'theme' }"
        @click="toggleTheme"
      >
        <img src="./assets/icons/主题.svg" alt="主题" class="nav-icon-svg" />
        <span class="nav-label">{{ navItems[3].label }}</span>
      </div>
      <div 
        class="nav-item" 
        :class="{ active: activeNav === 'support' }"
        @click="activeNav = 'support'"
      >
        <img src="./assets/icons/赞赏.svg" alt="赞赏" class="nav-icon-svg" />
        <span class="nav-label">{{ navItems[4].label }}</span>
      </div>
      <div 
        class="nav-item" 
        :class="{ active: activeNav === 'settings' }"
        @click="activeNav = 'settings'"
      >
        <img src="./assets/icons/设置.svg" alt="关于" class="nav-icon-svg" />
        <span class="nav-label">{{ navItems[5].label }}</span>
      </div>
    </nav>

    <!-- 右侧主内容区 -->
    <main class="main-content">
      <!-- 主页 -->
      <div v-if="activeNav === 'home'" class="home-page">
        <div class="background-image">
              <img :src="backgroundImage" alt="Background" />
              <div class="overlay-content">
            <div class="header">
              <h1>Elysia_BangBang♪~</h1>
              <h3>tokutouseki</h3>
            </div>
          </div>
        </div>
        <div class="tasks-section">
          <h3>常用 &gt;</h3>
          <div class="tasks-grid">
            <div v-for="task in tasks" :key="task.id" class="task-card" @click="task.script && runScript(task.script)">
              <img :src="task.icon" :alt="task.name" class="task-icon" />
              <span class="task-name">{{ task.name }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 帮助页面 -->
      <div v-else-if="activeNav === 'help'" class="help-page">
        <h2>帮助</h2>
        <div class="help-tabs-container">
          <div class="help-tabs">
            <div 
              v-for="tab in helpTabs" 
              :key="tab" 
              class="help-tab" 
              :class="{ active: activeHelpTab === tab }"
              @click="activeHelpTab = tab"
            >
              {{ tab }}
            </div>
          </div>
        </div>
        <div class="help-content-container">
          <!-- 使用教程内容 -->
          <div v-if="activeHelpTab === '使用教程'" class="help-content">
            <h3>要求</h3>
            <p>必须使用PC端 1920*1080分辨率全屏运行游戏</p>
            <p>将爱愿妖精作为舰桥展示人物</p>
            <p>建议：</p>
            <ul>
              <li>电脑配置至少可以运行崩三的同时刷b站</li>
              <li>使用永恒的礼堂作为舰桥</li>
            </ul>
            
            <h3>使用步骤</h3>
            <ol>
              <li>启动游戏登上舰桥</li>
              <li>以管理员权限启动本工具</li>
              <li>在左侧导航栏选择需要的功能模块</li>
            </ol>
            
            <h3>功能说明</h3>
            <ul>
              <li><strong>主页</strong>：显示常用功能和工具信息，包括完整运行、每日任务、每周减负、记忆战场、往世乐土快捷入口</li>
              <li><strong>帮助</strong>：查看使用教程和常见问题</li>
              <li><strong>工具箱</strong>：显示tools文件夹中的文档文件(.md)和Python文件(.py)，分两列展示，可直接运行Python文件或启动命令行窗口</li>
              <li><strong>主题</strong>：切换工具界面主题（粉色/蓝色）</li>
              <li><strong>赞赏</strong>：支持开发者</li>
              <li><strong>关于</strong>：查看工具信息、每周任务分配、各项功能说明和日志</li>
            </ul>
            
            <h3>注意事项</h3>
            <ul>
              <li>确保游戏窗口处于前台且未最小化</li>
              <li>使用过程中不要遮挡游戏画面</li>
              <li>使用工具可能导致的后果自负</li>
              <li>工具需要以管理员权限运行，否则可能无法正常操作游戏窗口</li>
              <li>如有问题，请查看常见问题或联系开发者</li>
            </ul>
          </div>
          
          <!-- 常见问题内容 -->
          <div v-else-if="activeHelpTab === '常见问题'" class="help-content">
            <h3>常见问题解答</h3>
            
            <div class="faq-item">
              <h4>Q: 工具无法识别游戏窗口怎么办？</h4>
              <p>A: 请确保游戏以全屏模式运行，分辨率设置为1920*1080，并重启工具。如果问题仍存在，请检查游戏是否为最新版本。</p>
            </div>
            
            <div class="faq-item">
              <h4>Q: 功能执行失败如何处理？</h4>
              <p>A: 检查游戏画面是否正确显示，确保网络连接正常，尝试重启工具。如果问题持续，请查看关于-日志获取详细错误信息。</p>
            </div>
            

            
            <div class="faq-item">
              <h4>Q: 如何更新工具？</h4>
              <p>A: 关注up主，更新了会发b站，但是不一定更新</p>
            </div>
            
            <div class="faq-item">
              <h4>Q: 工具支持哪些操作系统？</h4>
              <p>A: 本工具目前仅支持Windows操作系统，推荐使用Windows 10或Windows 11。</p>
            </div>
            
            <div class="faq-item">
              <h4>Q: 如何联系开发者？</h4>
              <p>A: 查看关于-我</p>
            </div>
            
            <div class="faq-item">
              <h4>Q: 工具需要管理员权限吗？</h4>
              <p>A: 是的，为了能够正常操作游戏窗口，工具需要以管理员权限运行。</p>
            </div>
            
            <div class="faq-item">
              <h4>Q: 为什么工具会占用较多内存？</h4>
              <p>A: 启动了两个本地服务端加载onnx和ppv4这两个模型</p>
            </div>
          </div>
          

        </div>
      </div>

      <!-- 关于页面 -->
      <div v-else-if="activeNav === 'settings'" class="settings-page">
        <h2>关于</h2>
        <div class="settings-tabs">
          <div 
            v-for="tab in settingsTabs" 
            :key="tab" 
            class="settings-tab" 
            :class="{ active: activeSettingsTab === tab }"
            @click="activeSettingsTab = tab"
          >
            {{ tab }}
          </div>
        </div>
        
        <!-- 日常设置内容 -->
        <div v-if="activeSettingsTab === '日常'" class="settings-content">
          
          <!-- 每周任务分配表格 -->
          <div class="weekly-task-table">
            <h4>每周任务分配</h4>
            <table class="task-schedule-table">
              <thead>
                <tr>
                  <th>星期</th>
                  <th>任务</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(tasks, day) in weeklyTaskMapping" :key="day">
                  <td class="day-cell">{{ day }}</td>
                  <td class="tasks-cell">
                    <ul class="task-list">
                      <li v-for="(task, index) in tasks" :key="index">
                        {{ getChineseTaskName(task) }}
                      </li>
                    </ul>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
        
        <!-- 战场设置内容 -->
        <div v-else-if="activeSettingsTab === '战场'" class="settings-content">
          <p>日常处理的战场只有减负部分，强敌最后的战斗请手动或者使用工具箱的复现工具完成</p>
        </div>
        
        <!-- 深渊设置内容 -->
        <div v-else-if="activeSettingsTab === '深渊'" class="settings-content">
          <h3>深渊设置</h3>
          <p>深渊设置页面开发中...</p>
        </div>
        
        <!-- 乐土设置内容 -->
        <div v-else-if="activeSettingsTab === '乐土'" class="settings-content">
          <div class="leitu-description">
            <p>乐土功能仅提供周常的减负战斗内容</p>
            <p>固定角色为爱神使者，支援为迷城骇兔和云墨丹心，追忆之证为水晶蔷薇和《因你而在的故事》</p>
            <p>神之键默认不开启</p>
            <p>固定选择增幅的最后两个15的，难度戒约2.25</p>
            <p>该难度不会获取最高等级的奖励（勋章，无水晶）</p>
            <p>浅层序列和完整的深层序列请手动或者使用工具箱完成</p>
            <p class="leitu-warning">请确保爱神使者练度足够！</p>
          </div>
        </div>
        
        <!-- 委托设置内容 -->
        <div v-else-if="activeSettingsTab === '委托'" class="settings-content">
          <div class="delegate-content">
            <p class="delegate-main">固定减负后崩坏书一的冒险任务</p>
            <p class="delegate-warning">确保体力充足再运行！</p>
          </div>
        </div>
        
        <!-- 舰团设置内容 -->
        <div v-else-if="activeSettingsTab === '舰团'" class="settings-content">
          <div class="fleet-content">
            <p class="fleet-item">委托回收会交满8次</p>
            <p class="fleet-item">舰团奖池自动领取</p>
            <p class="fleet-item">舰团贡献周日领取</p>
            <p class="fleet-item">模拟作战室每周二、日运行</p>
            <div class="warning-section">
              <p class="fleet-warning">请确保崩坏碎片足够！</p>
              <img src="./assets/images/benghuaisuipian.png" alt="崩坏碎片" class="fleet-image" />
            </div>
          </div>
        </div>
        
        <!-- 日志设置内容 -->
        <div v-else-if="activeSettingsTab === '日志'" class="settings-content">
          <!-- 日志文件列表 -->
          <div class="log-files-list">
            <h4>日志文件</h4>
            <div class="log-files-grid">
              <div 
                v-for="file in logFiles" 
                :key="file"
                class="log-file-item"
                @dblclick="readLogFile(file)"
              >
                <span class="log-file-name">{{ file }}</span>
              </div>
              <div v-if="logFiles.length === 0" class="no-log-files">
                暂无日志文件
              </div>
            </div>
          </div>
          
          <!-- 日志文件内容 -->
          <div v-if="isLogFileOpen" class="log-file-content">
            <div class="log-file-header">
              <h4>{{ selectedLogFile }}</h4>
              <button class="close-log-file-button" @click="closeLogFile">关闭</button>
            </div>
            <div class="log-file-text">
              <pre>{{ logFileContent }}</pre>
            </div>
          </div>
        </div>
        
        <!-- 我设置内容 -->
        <div v-else-if="activeSettingsTab === '我'" class="settings-content">
          <div class="me-content">
            <h3>关于我</h3>
            <p>b站主页: <a href="https://space.bilibili.com/457079828?spm_id_from=333.1007.0.0" target="_blank">https://space.bilibili.com/457079828?spm_id_from=333.1007.0.0</a></p>
            <p>项目主页：<a href="https://github.com/tokutouseki/Elysia_Bang_Bang" target="_blank">https://github.com/tokutouseki/Elysia_Bang_Bang</a></p>
          </div>
        </div>

      </div>

      <!-- 赞赏页面 -->
      <div v-else-if="activeNav === 'support'" class="support-page">
        <h2>赞赏</h2>
        <div class="support-content">
          <div class="upload-section">
            <h3>上传好看的图片作为对我的赞赏吧</h3>
            <div 
              class="upload-area" 
              @drop.prevent="handleDrop" 
              @dragover.prevent 
              @click="triggerFileInput"
            >
              <input 
                type="file" 
                ref="fileInput" 
                style="display: none" 
                accept=".jpg,.jpeg,.png,.gif,.bmp" 
                multiple 
                @change="handleFileSelect"
              />
              <div class="upload-icon">📁</div>
              <p>拖放文件到这里，或点击选择文件</p>
              <p class="supported-formats">支持格式：JPG、PNG、GIF、BMP</p>
            </div>
            
            <div v-if="uploadedImages.length > 0" class="send-section">
              <button @click="sendEmail" class="send-button">发送邮件</button>
              <p v-if="emailStatus" :class="emailStatus === 'success' ? 'success-message' : 'error-message'">
                {{ emailMessage }}
              </p>
            </div>
            
            <div v-if="uploadedImages.length > 0" class="uploaded-images">
              <h4>已上传的图片</h4>
              <div class="images-grid">
                <div v-for="(image, index) in uploadedImages" :key="index" class="image-item">
                  <img :src="image.url" :alt="image.name" class="uploaded-image" />
                  <p class="image-name">{{ image.name }}</p>
                  <button @click="removeImage(index)" class="remove-button">删除</button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 工具箱页面 -->
      <div v-else-if="activeNav === 'tools'" class="tools-page">
        <div class="tools-header">
          <h2>{{ navItems[2].label }}</h2>
        </div>
        <div class="tools-grid">
          <!-- 使用说明列 -->
          <div class="tools-panel">
            <h4 class="panel-title">
              <span class="file-type-icon md-icon">📄</span>
              使用说明
            </h4>
            <div class="file-list">
              <div 
                v-for="file in mdFiles" 
                :key="file"
                class="file-item"
                @dblclick="readToolFile(file)"
              >
                <span class="file-name">{{ removeFileExtension(file) }}</span>
              </div>
              <div v-if="mdFiles.length === 0" class="empty-message">
                暂无使用说明文件
              </div>
            </div>
          </div>
          
          <!-- Python文件列 -->
          <div class="tools-panel">
            <h4 class="panel-title">
              <span class="file-type-icon py-icon">🐍</span>
              Python文件
            </h4>
            <div class="file-list">
              <div 
                v-for="file in pyFiles" 
                :key="file"
                class="file-item"
                @dblclick="readToolFile(file)"
              >
                <span class="file-name">{{ removeFileExtension(file) }}</span>
                <div class="file-actions">
                  <button class="run-button" @click="runPythonFile(file)">运行</button>
                </div>
              </div>
              <div v-if="pyFiles.length === 0" class="empty-message">
                暂无Python文件
              </div>
            </div>
          </div>
          
          <!-- Reproduce文件区域 -->
          <div class="tools-panel">
            <h4 class="panel-title">
              <span class="file-type-icon reproduce-icon">🔄</span>
              Reproduce
            </h4>
            <div class="file-list">
              <div 
                v-for="file in reproduceFiles" 
                :key="file"
                class="file-item"
                @dblclick="readReproduceFile(file)"
              >
                <span class="file-name">{{ removeFileExtension(file) }}</span>
              </div>
              <div v-if="reproduceFiles.length === 0" class="empty-message">
                暂无reproduce文件
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 其他页面 -->
      <div v-else class="other-page">
        <h2>{{ navItems.find(item => item.id === activeNav)?.label }}</h2>
        <p>页面开发中...</p>
      </div>
    </main>
  </div>
</template>

<style>
:root {
  --primary-color: #fce4ec;
  --secondary-color: #f8bbd0;
  --accent-color: #f48fb1;
  --border-color: #f48fb1;
  --text-color: #333;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  background-color: #ffffff;
  height: 100%;
  overflow: hidden;
}

body {
  font-family: 'Arial', sans-serif;
  color: #333;
}

.app-container {
  display: flex;
  width: 960px;
  height: 720px;
  max-width: 100%;
  max-height: 100%;
  margin: 0 auto;
  overflow: hidden;
  background-color: var(--primary-color);
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

/* 左侧导航栏 */
.sidebar {
  width: 80px;
  background-color: var(--primary-color);
  border-right: 1px solid var(--border-color);
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px 0;
  gap: 20px;
}

.nav-item {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 12px;
  background-color: var(--primary-color);
}

.nav-item:hover {
  background-color: #f0f0f0;
}

.nav-item.active {
  background-color: var(--secondary-color);
  color: var(--accent-color);
}

.nav-icon {
  font-size: 24px;
  margin-bottom: 4px;
}

.nav-icon-svg {
  width: 24px;
  height: 24px;
  margin-bottom: 4px;
  transition: all 0.3s ease;
  filter: invert(60%) sepia(0%) saturate(0%) hue-rotate(0deg) brightness(90%) contrast(80%);
}

.nav-item:hover .nav-icon-svg {
  filter: invert(50%) sepia(0%) saturate(0%) hue-rotate(0deg) brightness(80%) contrast(70%);
}

.nav-item.active .nav-icon-svg {
  filter: invert(40%) sepia(90%) saturate(300%) hue-rotate(var(--active-icon-hue));
}

.nav-label {
  transition: all 0.3s ease;
}

.nav-item.active .nav-label {
  color: var(--accent-color);
}

/* 右侧主内容区 */
.main-content {
  flex: 1;
  padding: 30px;
  overflow-y: hidden;
  background-color: var(--primary-color);
  display: flex;
  flex-direction: column;
}

/* 主页样式 */
.home-page {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.header {
  margin-bottom: 20px;
}

.header h1 {
  font-size: 24px;
  color: #333;
  margin-bottom: 8px;
}

.header h2 {
  font-size: 20px;
  color: #666;
}

.background-image {
  width: 100%;
  height: 400px;
  border-radius: 12px;
  overflow: hidden;
  margin-bottom: 5px;
  position: relative;
}

.overlay-content {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  padding: 30px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  background: linear-gradient(to bottom, rgba(0,0,0,0.2) 0%, rgba(0,0,0,0) 100%);
}

.overlay-content .header {
  color: white;
  text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
  text-align: left;
}

.overlay-content .header h1 {
  font-size: 28px;
  margin-bottom: 8px;
  color: white;
  text-align: left;
}

.overlay-content .header h2 {
  font-size: 22px;
  color: white;
  text-align: left;
}

.overlay-content .header h3 {
  font-size: 16px;
  color: white;
  text-align: left;
  margin-top: 8px;
  font-weight: normal;
}

.overlay-content .github-repo {
  background: rgba(255,255,255,0.9);
  border-radius: 12px;
  padding: 16px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  max-width: 400px;
  margin-top: auto;
  margin-bottom: 20px;
}

.background-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
}

.background-image img.stretch-horizontal {
  object-fit: fill;
}

.github-repo {
  display: flex;
  align-items: center;
  gap: 16px;
  background-color: var(--primary-color);
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
  border: 1px solid var(--border-color);
}

.repo-icon {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background-color: #f0f0f0;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #333;
}

.repo-info h3 {
  font-size: 16px;
  margin-bottom: 4px;
}

.repo-info p {
  font-size: 14px;
  color: #666;
  margin-bottom: 4px;
}

.tasks-section {
  margin-top: 5px;
  text-align: left;
}

.tasks-section h3 {
  font-size: 18px;
  margin-bottom: 16px;
  text-align: left;
}

.tasks-grid {
  display: flex;
  gap: 10px;
  justify-content: space-between;
  align-items: flex-start;
  width: 100%;
  max-width: 1000px;
}

.task-card {
  background-color: var(--primary-color);
  border-radius: 12px;
  padding: 10px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  gap: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: transform 0.3s ease;
  flex: 1;
  min-width: 100px;
  max-width: 180px;
  border: 1px solid var(--border-color);
}

.task-card:hover {
  transform: translateY(-4px);
}

.task-icon {
  width: 100px;
  height: 100px;
  border-radius: 8px;
  object-fit: cover;
}

.task-name {
  font-size: 14px;
  text-align: center;
  font-weight: 500;
  text-align: center;
  width: 100%;
}

/* 帮助页面样式 */
.help-page {
  background-color: var(--primary-color);
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border: 1px solid var(--border-color);
  height: 500px;
  display: flex;
  flex-direction: column;
}

.help-page h2,
.settings-page h2,
.support-page h2,
.tools-page h2,
.other-page h2 {
  font-size: 24px;
  margin-bottom: 20px;
  text-align: left;
}

.help-tabs-container {
  margin-bottom: 20px;
  border-bottom: 1px solid #e0e0e0;
  padding-bottom: 12px;
}

.help-tabs {
  display: flex;
  gap: 16px;
}

.help-tab {
  padding: 8px 16px;
  cursor: pointer;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.help-tab:hover {
  background-color: #f0f0f0;
}

.help-tab.active {
  background-color: var(--secondary-color);
  color: var(--accent-color);
  font-weight: bold;
}

.help-content-container {
  flex: 1;
  overflow: hidden;
}

.help-content {
  display: flex;
  flex-direction: column;
  gap: 16px;
  height: 100%;
  overflow-y: auto;
  padding-right: 8px;
}

.help-content::-webkit-scrollbar {
  width: 6px;
}

.help-content::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.help-content::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.help-content::-webkit-scrollbar-thumb:hover {
  background: #a1a1a1;
}

.help-content h3 {
  font-size: 18px;
  margin-bottom: 12px;
  margin-top: 20px;
  text-align: left;
}

.help-content h4 {
  font-size: 16px;
  margin-bottom: 8px;
  margin-top: 16px;
  text-align: left;
}

.help-content p {
  font-size: 14px;
  line-height: 1.5;
  color: #666;
  margin-bottom: 12px;
  text-align: left;
}

.help-content ol,
.help-content ul {
  font-size: 14px;
  line-height: 1.5;
  color: #666;
  margin-left: 24px;
  margin-bottom: 16px;
  text-align: left;
}

.help-content li {
  margin-bottom: 6px;
  text-align: left;
}

.faq-item {
  margin-bottom: 16px;
  padding-bottom: 16px;
  border-bottom: 1px solid #f0f0f0;
}

.faq-item:last-child {
  border-bottom: none;
}

.log-item {
  margin-bottom: 20px;
  padding-bottom: 20px;
  border-bottom: 1px solid #f0f0f0;
}

.log-item:last-child {
  border-bottom: none;
}

/* 设置页面样式 */
.settings-page {
  background-color: var(--primary-color);
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border: 1px solid var(--border-color);
}

.settings-page h2 {
  font-size: 24px;
  margin-bottom: 20px;
}

.settings-tabs {
  display: flex;
  gap: 8px;
  margin-bottom: 20px;
  flex-wrap: wrap;
  border-bottom: 1px solid #e0e0e0;
  padding-bottom: 12px;
}

.settings-tab {
  padding: 6px 12px;
  cursor: pointer;
  border-radius: 8px;
  font-size: 14px;
  transition: all 0.3s ease;
}

.settings-tab:hover {
  background-color: #f0f0f0;
}

.settings-tab.active {
  background-color: var(--secondary-color);
  color: var(--accent-color);
  font-weight: bold;
}

.settings-content {
  display: flex;
  flex-direction: column;
  gap: 16px;
  max-height: 500px;
  overflow-y: auto;
  padding-right: 8px;
}

.settings-content::-webkit-scrollbar {
  width: 6px;
}

.settings-content::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.settings-content::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.settings-content::-webkit-scrollbar-thumb:hover {
  background: #a1a1a1;
}

.setting-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 12px 0;
  border-bottom: 1px solid #f0f0f0;
}

.setting-item label {
  flex: 1;
  font-size: 14px;
}

.setting-item input[type="text"] {
  flex: 2;
  padding: 8px 12px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  font-size: 14px;
}

.setting-item select {
  padding: 8px 12px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  font-size: 14px;
}

.setting-item span {
  flex: 3;
  font-size: 14px;
  color: #666;
}

/* 开关样式 */
.switch {
  position: relative;
  display: inline-block;
  width: 50px;
  height: 24px;
}

.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  transition: .4s;
  border-radius: 24px;
}

.slider:before {
  position: absolute;
  content: "";
  height: 16px;
  width: 16px;
  left: 4px;
  bottom: 4px;
  background-color: white;
  transition: .4s;
  border-radius: 50%;
}

input:checked + .slider {
  background-color: #1976d2;
}

input:focus + .slider {
  box-shadow: 0 0 1px #1976d2;
}

input:checked + .slider:before {
  transform: translateX(26px);
}

/* 赞赏页面样式 */
.support-page {
  background-color: var(--primary-color);
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border: 1px solid var(--border-color);
}

.support-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.upload-section {
  margin-top: 20px;
}

.upload-section h3 {
  font-size: 18px;
  margin-bottom: 16px;
}

.upload-area {
  border: 2px dashed var(--border-color);
  border-radius: 12px;
  padding: 40px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  background-color: rgba(255, 255, 255, 0.5);
}

.upload-area:hover {
  border-color: var(--accent-color);
  background-color: rgba(255, 255, 255, 0.8);
}

.upload-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.upload-area p {
  margin-bottom: 8px;
  font-size: 16px;
  color: #666;
}

.supported-formats {
  font-size: 14px;
  color: #999;
}

.send-section {
  margin: 20px 0;
  text-align: center;
}

.send-button {
  background-color: var(--accent-color);
  color: white;
  border: none;
  border-radius: 8px;
  padding: 12px 24px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.send-button:hover {
  background-color: #d81b60;
}

.success-message {
  color: #4caf50;
  margin-top: 12px;
  font-size: 14px;
}

.error-message {
  color: #f44336;
  margin-top: 12px;
  font-size: 14px;
}

.uploaded-images {
  margin-top: 20px;
}

.uploaded-images h4 {
  font-size: 16px;
  margin-bottom: 12px;
}

.images-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 16px;
}

.image-item {
  background-color: white;
  border-radius: 8px;
  padding: 12px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.uploaded-image {
  width: 100%;
  max-height: 120px;
  object-fit: cover;
  border-radius: 4px;
  margin-bottom: 8px;
}

.image-name {
  font-size: 12px;
  margin-bottom: 8px;
  word-break: break-all;
}

.remove-button {
  background-color: #ff4757;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 4px 8px;
  font-size: 12px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.remove-button:hover {
  background-color: #ff3742;
}

/* 每周任务分配表格样式 */
.weekly-task-table {
  margin: 20px 0;
  background-color: #ffffff;
  border-radius: 8px;
  padding: 16px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border: 1px solid var(--border-color);
}

.weekly-task-table h4 {
  margin-bottom: 12px;
  font-size: 16px;
  color: #000000;
}

.task-schedule-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
  border: 1px solid var(--border-color);
}

.task-schedule-table th {
  background-color: #ffffff;
  color: #000000;
  padding: 10px;
  text-align: center;
  vertical-align: middle;
  border: 1px solid var(--border-color);
}

.task-schedule-table td {
  padding: 10px;
  border: 1px solid var(--border-color);
}

.task-schedule-table tr:hover {
  background-color: rgba(0, 0, 0, 0.02);
}

.day-cell {
  font-weight: bold;
  width: 100px;
  text-align: center;
  vertical-align: middle;
}

.tasks-cell {
  vertical-align: top;
}

.task-list {
  list-style-type: none;
  margin: 0;
  padding: 0;
}

.task-list li {
  margin-bottom: 6px;
  padding-left: 0;
  position: relative;
}

/* 乐土描述样式 */
.leitu-description p {
  margin-bottom: 11px; /* 增加5px间距 */
  line-height: 1.4;
}

.leitu-warning {
  font-size: 24px;
  font-weight: bold;
  color: var(--warning-color);
  margin-top: 20px;
  text-align: center;
  margin: 0;
}

/* 委托页面样式 */
.delegate-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding: 20px;
}

.delegate-main {
  font-size: 18px;
  font-weight: normal;
  margin: 0;
}

.delegate-warning {
  font-size: 24px;
  font-weight: bold;
  color: var(--warning-color);
  margin: 0;
  text-align: center;
}

/* 舰团页面样式 */
.fleet-content {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 20px;
}

.fleet-item {
  font-size: 16px;
  margin: 0;
  line-height: 1.4;
}

.warning-section {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px;
  margin-top: 20px;
}

.fleet-warning {
  font-size: 24px;
  font-weight: bold;
  color: var(--warning-color);
  margin: 0;
  text-align: center;
}

.fleet-image {
  width: 80px;
  height: 80px;
  border-radius: 8px;
  object-fit: contain;
}

/* 我页面样式 */
.me-content {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 20px;
}

.me-content h3 {
  margin-bottom: 16px;
  color: var(--accent-color);
}

.me-content p {
  margin: 0;
  line-height: 1.4;
}

.me-content a {
  color: var(--accent-color);
  text-decoration: underline;
  cursor: pointer;
}

.me-content a:hover {
  color: var(--warning-color);
  text-decoration: none;
}

/* 日志文件列表样式 */
.log-files-list {
  margin: 20px 0;
  background-color: #ffffff;
  border-radius: 8px;
  padding: 16px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border: 1px solid var(--border-color);
}

.log-files-list h4 {
  margin-bottom: 12px;
  font-size: 16px;
  color: #000000;
}

.log-files-grid {
  max-height: 180px;
  overflow-y: auto;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  padding: 8px;
  background-color: #f9f9f9;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  grid-gap: 8px;
}

.log-file-item {
  padding: 8px 12px;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s ease;
  background-color: #ffffff;
  border: 1px solid #e0e0e0;
}

.log-file-item:hover {
  background-color: #f0f0f0;
  border-color: var(--border-color);
}

.log-file-name {
  font-size: 14px;
  color: #333333;
}

.no-log-files {
  text-align: center;
  padding: 20px;
  color: #999999;
  font-style: italic;
  grid-column: 1 / -1;
}

/* 日志文件内容样式 */
.log-file-content {
  margin: 20px 0;
  background-color: #000000;
  border-radius: 4px;
  padding: 0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border: 1px solid #333333;
}

.log-file-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
  padding-bottom: 4px;
  border-bottom: 1px solid #333333;
  background-color: #000000;
  padding: 8px 12px;
  border-radius: 4px 4px 0 0;
}

.log-file-header h4 {
  margin: 0;
  font-size: 14px;
  color: #ffffff;
}

.close-log-file-button {
  background-color: #f44336;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 4px 8px;
  font-size: 12px;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.close-log-file-button:hover {
  background-color: #d32f2f;
}

.log-file-text {
  max-height: 400px;
  overflow-y: auto;
  border: 1px solid #333333;
  border-radius: 0 0 4px 4px;
  padding: 12px;
  background-color: #000000;
  margin-top: 0;
}

.log-file-text pre {
  margin: 0;
  font-size: 13px;
  line-height: 1.4;
  color: #ffffff;
  font-family: 'Courier New', Courier, monospace;
  white-space: pre-wrap;
  word-wrap: break-word;
  text-align: left;
}

/* 日志文件内容滚动条样式 */
.log-file-text::-webkit-scrollbar {
  width: 8px;
}

.log-file-text::-webkit-scrollbar-track {
  background: #111111;
  border-radius: 4px;
}

.log-file-text::-webkit-scrollbar-thumb {
  background: #444444;
  border-radius: 4px;
}

.log-file-text::-webkit-scrollbar-thumb:hover {
  background: #555555;
}



/* 其他页面样式 */
.other-page {
  background-color: #fff;
  border-radius: 12px;
  padding: 40px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 80vh;
}

.other-page h2 {
  font-size: 24px;
  margin-bottom: 16px;
}

.other-page p {
  font-size: 16px;
  color: #666;
}

/* 工具箱页面样式 */
.tools-page {
  background-color: var(--primary-color);
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border: 1px solid var(--border-color);
  height: 600px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  box-sizing: border-box;
}

.tools-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  flex-shrink: 0;
}

.tools-header h2 {
  font-size: 24px;
  margin: 0;
  color: #333;
}

.command-prompt-button {
  background-color: var(--accent-color);
  color: white;
  border: none;
  border-radius: 8px;
  padding: 8px 16px;
  font-size: 14px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.command-prompt-button:hover {
  background-color: #d81b60;
}

.tools-grid {
  flex: 1;
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 0;
  overflow: hidden;
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border: 1px solid var(--border-color);
  height: 100%;
}

.tools-panel {
  display: flex;
  flex-direction: column;
  overflow: hidden;
  border-right: 1px solid var(--border-color);
  height: 100%;
}

.file-list {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  height: calc(100% - 60px); /* 减去标题栏高度 */
}

.tools-panel:last-child {
  border-right: none;
}

.panel-title {
  font-size: 16px;
  font-weight: bold;
  padding: 12px 16px;
  margin: 0;
  background-color: var(--primary-color);
  border-bottom: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  gap: 8px;
  flex-shrink: 0;
}

.file-type-icon {
  font-size: 18px;
}

.md-icon {
  color: #4fc3f7;
}

.py-icon {
  color: #81c784;
}

.reproduce-icon {
  color: #ff9800;
}

.file-list {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.file-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  border-radius: 8px;
  background-color: var(--primary-color);
  border: 1px solid var(--border-color);
  transition: all 0.3s ease;
  height: 60px;
  box-sizing: border-box;
}

.file-item:hover {
  background-color: #f9f9f9;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.file-name {
  font-size: 16px;
  color: #333;
  font-weight: 500;
  flex: 1;
  word-break: break-all;
}

.file-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.file-badge {
  font-size: 12px;
  padding: 4px 8px;
  border-radius: 4px;
  font-weight: bold;
}

.md-badge {
  background-color: #4fc3f7;
  color: white;
}

.py-badge {
  background-color: #81c784;
  color: white;
}

.record-badge {
  background-color: #ff9800;
  color: white;
}

.record-icon {
  color: #ff9800;
}

.record-files-section {
  margin-top: 20px;
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border: 1px solid var(--border-color);
  overflow: hidden;
}

.run-button {
  background-color: var(--accent-color);
  color: white;
  border: none;
  border-radius: 8px;
  padding: 6px 12px;
  font-size: 14px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  white-space: nowrap;
}

.run-button:hover {
  background-color: #d81b60;
}

.empty-message {
  text-align: center;
  padding: 40px;
  color: #999;
  font-style: italic;
  margin: 0;
}

/* 滚动条样式 */
.file-list::-webkit-scrollbar {
  width: 6px;
}

.file-list::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.file-list::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.file-list::-webkit-scrollbar-thumb:hover {
  background: #a1a1a1;
}
</style>