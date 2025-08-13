# AugmentCode-Free 跨平台构建指南

本指南说明如何为不同操作系统构建 AugmentCode-Free 可执行文件。

## 📋 构建要求

### 通用要求
- Python 3.7+
- PyQt6
- PyInstaller
- 所有项目依赖（见 requirements.txt）

### 平台特定要求

#### Windows
- Windows 7/10/11
- Visual Studio Build Tools（可选，用于某些依赖）

#### macOS
- macOS 10.13+
- Xcode Command Line Tools

#### Linux
- Ubuntu 18.04+ / CentOS 7+ / 其他主流发行版
- 开发工具包（build-essential）

## 🚀 快速构建

### 1. 安装依赖
```bash
# 安装 Python 依赖
pip install -r requirements.txt

# 安装 PyInstaller
pip install pyinstaller
```

### 2. 运行构建脚本
```bash
# 使用自动构建脚本
python build_release.py
```

## 🛠️ 手动构建

### Windows 构建
```cmd
# 清理之前的构建
rmdir /s build dist

# 构建可执行文件
pyinstaller --onedir --windowed ^
    --name=AugmentCode-Free ^
    --add-data=config;config ^
    --add-data=languages;languages ^
    --hidden-import=PyQt6.QtCore ^
    --hidden-import=PyQt6.QtGui ^
    --hidden-import=PyQt6.QtWidgets ^
    --hidden-import=sqlite3 ^
    main.py

# 创建发布包
mkdir release
xcopy /E /I dist\AugmentCode-Free release\AugmentCode-Free-v2.0.0-windows-x64
```

### macOS 构建
```bash
# 清理之前的构建
rm -rf build dist *.spec

# 构建可执行文件
pyinstaller --onedir --windowed \
    --name=AugmentCode-Free \
    --add-data=config:config \
    --add-data=languages:languages \
    --hidden-import=PyQt6.QtCore \
    --hidden-import=PyQt6.QtGui \
    --hidden-import=PyQt6.QtWidgets \
    --hidden-import=sqlite3 \
    main.py

# 创建发布包
mkdir -p release
cp -r dist/AugmentCode-Free.app release/AugmentCode-Free-v2.0.0-macos-arm64.app
cp -r dist/AugmentCode-Free release/AugmentCode-Free-v2.0.0-macos-arm64
```

### Linux 构建
```bash
# 清理之前的构建
rm -rf build dist *.spec

# 构建可执行文件
pyinstaller --onedir --windowed \
    --name=AugmentCode-Free \
    --add-data=config:config \
    --add-data=languages:languages \
    --hidden-import=PyQt6.QtCore \
    --hidden-import=PyQt6.QtGui \
    --hidden-import=PyQt6.QtWidgets \
    --hidden-import=sqlite3 \
    main.py

# 创建发布包
mkdir -p release
cp -r dist/AugmentCode-Free release/AugmentCode-Free-v2.0.0-linux-x64
```

## 📦 创建分发包

### Windows (ZIP)
```cmd
# 创建 ZIP 压缩包
powershell Compress-Archive -Path release\AugmentCode-Free-v2.0.0-windows-x64 -DestinationPath AugmentCode-Free-v2.0.0-windows-x64.zip
```

### macOS/Linux (TAR.GZ)
```bash
# 创建 tar.gz 压缩包
tar -czf AugmentCode-Free-v2.0.0-macos-arm64.tar.gz -C release AugmentCode-Free-v2.0.0-macos-arm64
tar -czf AugmentCode-Free-v2.0.0-linux-x64.tar.gz -C release AugmentCode-Free-v2.0.0-linux-x64
```

## 🧪 测试构建

### 功能测试
1. 启动应用程序
2. 测试 GUI 界面
3. 测试清理功能
4. 测试遥测修改功能
5. 测试自动搜索功能

### 测试命令
```bash
# 测试可执行文件
./dist/AugmentCode-Free/AugmentCode-Free --help

# 测试 GUI（如果支持）
./dist/AugmentCode-Free/AugmentCode-Free
```

## 📁 构建输出

构建完成后，将生成以下文件：

```
release/
├── AugmentCode-Free-v2.0.0-{platform}-{arch}/
│   ├── AugmentCode-Free(.exe)
│   ├── config/
│   ├── languages/
│   └── 其他依赖文件
├── README.md
└── LICENSE

压缩包:
├── AugmentCode-Free-v2.0.0-windows-x64.zip
├── AugmentCode-Free-v2.0.0-macos-arm64.tar.gz
└── AugmentCode-Free-v2.0.0-linux-x64.tar.gz
```

## ⚠️ 注意事项

### Windows
- 可能需要安装 Visual C++ Redistributable
- 某些杀毒软件可能误报，需要添加白名单

### macOS
- 首次运行可能需要在"系统偏好设置 > 安全性与隐私"中允许
- 对于未签名的应用，用户需要右键点击选择"打开"

### Linux
- 确保系统安装了必要的图形库
- 某些发行版可能需要额外的依赖包

## 🔧 故障排除

### 常见问题

1. **PyQt6 导入错误**
   ```bash
   pip install PyQt6
   ```

2. **权限错误**
   ```bash
   chmod +x AugmentCode-Free
   ```

3. **缺少依赖**
   ```bash
   pip install -r requirements.txt
   ```

4. **构建失败**
   - 检查 Python 版本
   - 确保所有依赖已安装
   - 查看构建日志中的错误信息

## 📞 支持

如果遇到构建问题，请：
1. 检查本指南的故障排除部分
2. 查看项目的 Issues 页面
3. 提交新的 Issue 并附上详细的错误信息
