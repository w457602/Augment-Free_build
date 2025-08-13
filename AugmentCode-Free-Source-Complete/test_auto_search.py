#!/usr/bin/env python3
"""
测试自动搜索功能
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from augment_tools_core.common_utils import get_ide_paths, IDEType, print_info, print_success, print_warning
from augment_tools_core.extension_finder import ExtensionFinder

def test_auto_search():
    """测试自动搜索功能"""
    print_info("🧪 开始测试自动搜索功能...")
    print_info("=" * 60)

    # 只测试已知存在的IDE
    ide_types = [IDEType.VSCODE, IDEType.CURSOR]

    for ide_type in ide_types:
        print_info(f"\n📋 测试 {ide_type.value.upper()} 自动搜索:")
        print_info("-" * 40)

        # 测试配置文件路径搜索
        print_info("1. 测试配置文件路径搜索:")
        paths = get_ide_paths(ide_type, auto_search=True)
        if paths:
            print_success(f"✅ 找到配置文件路径:")
            for key, path in paths.items():
                exists = "✅" if path.exists() else "❌"
                print_info(f"   {key}: {path} {exists}")
        else:
            print_warning(f"❌ 未找到 {ide_type.value} 配置文件路径")

        # 跳过扩展文件搜索以节省时间
        print_info("\n2. 扩展文件搜索已跳过（节省时间）")

        print_info("\n" + "=" * 60)

def test_without_auto_search():
    """测试不启用自动搜索的情况"""
    print_info("\n🔒 测试禁用自动搜索功能...")
    print_info("=" * 60)
    
    ide_types = [IDEType.VSCODE, IDEType.CURSOR, IDEType.WINDSURF]
    
    for ide_type in ide_types:
        print_info(f"\n📋 测试 {ide_type.value.upper()} (禁用自动搜索):")
        print_info("-" * 40)
        
        # 测试配置文件路径搜索（禁用自动搜索）
        paths = get_ide_paths(ide_type, auto_search=False)
        if paths:
            print_success(f"✅ 默认路径找到配置文件:")
            for key, path in paths.items():
                exists = "✅" if path.exists() else "❌"
                print_info(f"   {key}: {path} {exists}")
        else:
            print_warning(f"❌ 默认路径未找到 {ide_type.value} 配置文件")

if __name__ == "__main__":
    try:
        # 测试启用自动搜索
        test_auto_search()
        
        # 测试禁用自动搜索
        test_without_auto_search()
        
        print_info("\n🎉 测试完成!")
        
    except KeyboardInterrupt:
        print_warning("\n⚠️ 测试被用户中断")
    except Exception as e:
        print_warning(f"\n❌ 测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()
