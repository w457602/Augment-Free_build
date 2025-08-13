#!/usr/bin/env python3
"""
AugmentCode-Free 发布版本打包脚本
为不同平台生成可执行文件
"""

import os
import sys
import shutil
import platform
import subprocess
from pathlib import Path
import zipfile
import tarfile

VERSION = "2.0.0"
PROJECT_NAME = "AugmentCode-Free"

def get_platform_info():
    """获取平台信息"""
    system = platform.system().lower()
    arch = platform.machine().lower()
    
    if system == "windows":
        return "windows", arch, ".exe"
    elif system == "darwin":
        return "macos", arch, ""
    elif system == "linux":
        return "linux", arch, ""
    else:
        return system, arch, ""

def clean_build():
    """清理构建目录"""
    dirs_to_clean = ['build', 'dist', '__pycache__']
    files_to_clean = ['*.spec']
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            print(f"🧹 清理目录: {dir_name}")
            shutil.rmtree(dir_name)
    
    # 清理 spec 文件
    for spec_file in Path('.').glob('*.spec'):
        spec_file.unlink()
        print(f"🧹 清理文件: {spec_file}")

def build_executable():
    """构建可执行文件"""
    system, arch, ext = get_platform_info()
    
    print(f"🚀 为 {system}-{arch} 平台构建可执行文件...")
    
    # 构建命令
    cmd = [
        'pyinstaller',
        '--onedir',  # 使用目录模式而不是单文件模式
        '--windowed',
        '--name=AugmentCode-Free',
        '--add-data=config:config',
        '--add-data=languages:languages',
        '--hidden-import=PyQt6.QtCore',
        '--hidden-import=PyQt6.QtGui',
        '--hidden-import=PyQt6.QtWidgets',
        '--hidden-import=sqlite3',
        '--hidden-import=json',
        '--hidden-import=pathlib',
        '--hidden-import=platform',
        '--hidden-import=subprocess',
        '--hidden-import=threading',
        '--hidden-import=queue',
        '--hidden-import=glob',
        '--hidden-import=shutil',
        '--hidden-import=uuid',
        '--hidden-import=hashlib',
        '--hidden-import=secrets',
        'main.py'
    ]
    
    print(f"📦 执行命令: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ 构建成功!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 构建失败: {e}")
        if e.stderr:
            print(f"错误输出: {e.stderr}")
        return False

def create_release_package():
    """创建发布包"""
    system, arch, ext = get_platform_info()
    
    # 创建发布目录
    release_dir = Path("release")
    release_dir.mkdir(exist_ok=True)
    
    # 平台特定的打包
    if system == "macos":
        # macOS 应用程序包
        app_path = Path("dist/AugmentCode-Free.app")
        if app_path.exists():
            target_path = release_dir / f"AugmentCode-Free-v{VERSION}-{system}-{arch}.app"
            if target_path.exists():
                shutil.rmtree(target_path)
            shutil.copytree(app_path, target_path)
            print(f"📱 macOS 应用程序包: {target_path}")
        
        # 也复制目录版本
        dir_path = Path("dist/AugmentCode-Free")
        if dir_path.exists():
            target_dir = release_dir / f"AugmentCode-Free-v{VERSION}-{system}-{arch}"
            if target_dir.exists():
                shutil.rmtree(target_dir)
            shutil.copytree(dir_path, target_dir)
            print(f"📁 macOS 目录版本: {target_dir}")
    
    else:
        # Windows/Linux 目录版本
        dir_path = Path("dist/AugmentCode-Free")
        if dir_path.exists():
            target_dir = release_dir / f"AugmentCode-Free-v{VERSION}-{system}-{arch}"
            if target_dir.exists():
                shutil.rmtree(target_dir)
            shutil.copytree(dir_path, target_dir)
            print(f"💻 {system} 可执行文件目录: {target_dir}")
    
    # 复制文档文件
    docs_to_copy = ["README.md", "LICENSE"]
    for doc in docs_to_copy:
        if Path(doc).exists():
            shutil.copy2(doc, release_dir / doc)
    
    print(f"📦 发布包已创建在: {release_dir}")

def create_archives():
    """创建压缩包"""
    system, arch, ext = get_platform_info()
    release_dir = Path("release")
    
    if not release_dir.exists():
        print("❌ 发布目录不存在")
        return
    
    # 为每个构建创建压缩包
    for item in release_dir.iterdir():
        if item.is_dir() and item.name.startswith("AugmentCode-Free-v"):
            archive_name = item.name
            
            if system == "windows":
                # Windows 使用 zip
                with zipfile.ZipFile(f"{archive_name}.zip", 'w', zipfile.ZIP_DEFLATED) as zf:
                    for file_path in item.rglob('*'):
                        if file_path.is_file():
                            arcname = file_path.relative_to(release_dir)
                            zf.write(file_path, arcname)
                print(f"📦 创建压缩包: {archive_name}.zip")
            else:
                # macOS/Linux 使用 tar.gz
                with tarfile.open(f"{archive_name}.tar.gz", 'w:gz') as tf:
                    tf.add(item, arcname=item.name)
                print(f"📦 创建压缩包: {archive_name}.tar.gz")

def test_executable():
    """测试可执行文件"""
    system, arch, ext = get_platform_info()
    
    if system == "macos":
        exe_path = Path("dist/AugmentCode-Free.app/Contents/MacOS/AugmentCode-Free")
    else:
        exe_path = Path(f"dist/AugmentCode-Free/AugmentCode-Free{ext}")
    
    if exe_path.exists():
        print(f"✅ 可执行文件存在: {exe_path}")
        print(f"📏 文件大小: {exe_path.stat().st_size / 1024 / 1024:.1f} MB")
        return True
    else:
        print(f"❌ 可执行文件不存在: {exe_path}")
        return False

def main():
    """主函数"""
    print("🏗️  AugmentCode-Free 发布版本构建脚本")
    print("=" * 60)
    
    system, arch, ext = get_platform_info()
    print(f"🖥️  平台: {system}-{arch}")
    print(f"🐍 Python: {sys.version}")
    print(f"📦 版本: v{VERSION}")
    
    # 步骤1: 清理构建目录
    print("\n📋 步骤1: 清理构建目录")
    clean_build()
    
    # 步骤2: 构建可执行文件
    print("\n📋 步骤2: 构建可执行文件")
    if not build_executable():
        print("❌ 构建失败!")
        return False
    
    # 步骤3: 测试可执行文件
    print("\n📋 步骤3: 测试可执行文件")
    if not test_executable():
        print("❌ 可执行文件测试失败!")
        return False
    
    # 步骤4: 创建发布包
    print("\n📋 步骤4: 创建发布包")
    create_release_package()
    
    # 步骤5: 创建压缩包
    print("\n📋 步骤5: 创建压缩包")
    create_archives()
    
    print("\n🎉 构建完成!")
    print(f"📁 发布文件位于 release/ 目录")
    print(f"📦 压缩包已创建")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⚠️ 构建被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 构建过程中出现错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
