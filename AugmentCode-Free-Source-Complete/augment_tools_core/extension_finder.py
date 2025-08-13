#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
扩展文件查找器
自动查找不同IDE的AugmentCode扩展文件，支持多版本和便携版
"""

import os
import glob
from pathlib import Path
from typing import List, Dict, Optional
import platform

from .common_utils import IDEType, print_info, print_warning, print_error, print_success


class ExtensionFinder:
    """扩展文件查找器"""
    
    def __init__(self):
        self.system = platform.system().lower()
        
        # 扩展文件路径模式
        self.extension_patterns = {
            IDEType.VSCODE: {
                "windows": [
                    # 用户级扩展目录（最常见）
                    os.path.expanduser("~/.vscode/extensions/augment.vscode-augment-*/out/extension.js"),
                    # 系统级扩展目录（较少见）
                    os.path.expanduser("~/AppData/Roaming/Code/User/extensions/augment.vscode-augment-*/out/extension.js"),
                ],
                "linux": [
                    os.path.expanduser("~/.vscode/extensions/augment.vscode-augment-*/out/extension.js"),
                    os.path.expanduser("~/.config/Code/User/extensions/augment.vscode-augment-*/out/extension.js"),
                ],
                "darwin": [
                    os.path.expanduser("~/.vscode/extensions/augment.vscode-augment-*/out/extension.js"),
                    os.path.expanduser("~/Library/Application Support/Code/User/extensions/augment.vscode-augment-*/out/extension.js"),
                ]
            },
            IDEType.CURSOR: {
                "windows": [
                    # Cursor specific extensions (用户级)
                    os.path.expanduser("~/.cursor/extensions/augment.cursor-augment-*/out/extension.js"),
                    # Cursor specific extensions (AppData)
                    os.path.expanduser("~/AppData/Roaming/Cursor/User/extensions/augment.cursor-augment-*/out/extension.js"),
                    # Cursor often shares VS Code extensions (用户级)
                    os.path.expanduser("~/.vscode/extensions/augment.vscode-augment-*/out/extension.js"),
                    # VS Code extensions (AppData)
                    os.path.expanduser("~/AppData/Roaming/Code/User/extensions/augment.vscode-augment-*/out/extension.js"),
                ],
                "linux": [
                    # Cursor specific extensions
                    os.path.expanduser("~/.cursor/extensions/augment.cursor-augment-*/out/extension.js"),
                    os.path.expanduser("~/.config/Cursor/User/extensions/augment.cursor-augment-*/out/extension.js"),
                    # Cursor often shares VS Code extensions
                    os.path.expanduser("~/.vscode/extensions/augment.vscode-augment-*/out/extension.js"),
                    os.path.expanduser("~/.config/Code/User/extensions/augment.vscode-augment-*/out/extension.js"),
                ],
                "darwin": [
                    # Cursor specific extensions
                    os.path.expanduser("~/.cursor/extensions/augment.cursor-augment-*/out/extension.js"),
                    os.path.expanduser("~/Library/Application Support/Cursor/User/extensions/augment.cursor-augment-*/out/extension.js"),
                    # Cursor often shares VS Code extensions on macOS
                    os.path.expanduser("~/.vscode/extensions/augment.vscode-augment-*/out/extension.js"),
                    os.path.expanduser("~/Library/Application Support/Code/User/extensions/augment.vscode-augment-*/out/extension.js"),
                ]
            },
            IDEType.WINDSURF: {
                "windows": [
                    # Windsurf 用户级扩展目录
                    os.path.expanduser("~/.windsurf/extensions/augment.windsurf-augment-*/out/extension.js"),
                    # Windsurf AppData 扩展目录
                    os.path.expanduser("~/AppData/Roaming/Windsurf/User/extensions/augment.windsurf-augment-*/out/extension.js"),
                    # Codeium Windsurf 路径
                    os.path.expanduser("~/.codeium/windsurf/extensions/augment.windsurf-augment-*/out/extension.js"),
                ],
                "linux": [
                    os.path.expanduser("~/.windsurf/extensions/augment.windsurf-augment-*/out/extension.js"),
                    os.path.expanduser("~/.config/Windsurf/User/extensions/augment.windsurf-augment-*/out/extension.js"),
                ],
                "darwin": [
                    os.path.expanduser("~/.windsurf/extensions/augment.windsurf-augment-*/out/extension.js"),
                    os.path.expanduser("~/Library/Application Support/Windsurf/User/extensions/augment.windsurf-augment-*/out/extension.js"),
                ]
            }
        }
        
        # 通用扩展名模式（用于模糊匹配）
        self.generic_patterns = [
            "*augment*extension.js",
            "*augment*/out/extension.js", 
            "*augment*/dist/extension.js",
            "*augment*/build/extension.js"
        ]
    
    def find_extension_files(self, ide_type: IDEType, portable_root: Optional[str] = None, auto_search: bool = True) -> List[str]:
        """查找指定IDE的扩展文件"""
        found_files = []

        # 如果指定了便携版根目录
        if portable_root:
            portable_files = self._find_portable_extensions(ide_type, portable_root)
            found_files.extend(portable_files)

        # 查找标准安装位置
        standard_files = self._find_standard_extensions(ide_type)
        found_files.extend(standard_files)

        # 去重并验证文件
        unique_files = list(set(found_files))
        valid_files = [f for f in unique_files if os.path.exists(f) and self._is_valid_extension_file(f)]

        # 如果标准位置没找到且启用了自动搜索，尝试自动搜索
        if not valid_files and auto_search:
            print_info(f"标准位置未找到 {ide_type.value} 扩展文件，尝试自动搜索...")
            auto_found_files = self._auto_search_extensions(ide_type)
            valid_files.extend(auto_found_files)

        if valid_files:
            print_info(f"找到 {len(valid_files)} 个 {ide_type.value} 扩展文件:")
            for file in valid_files:
                print_info(f"  - {file}")
        else:
            print_warning(f"未找到 {ide_type.value} 的扩展文件")

        return valid_files
    
    def _find_standard_extensions(self, ide_type: IDEType) -> List[str]:
        """查找标准安装位置的扩展文件"""
        found_files = []
        
        if ide_type not in self.extension_patterns:
            print_warning(f"不支持的IDE类型: {ide_type}")
            return found_files
        
        patterns = self.extension_patterns[ide_type].get(self.system, [])
        
        for pattern in patterns:
            try:
                matches = glob.glob(pattern)
                found_files.extend(matches)
            except Exception as e:
                print_warning(f"搜索模式失败 {pattern}: {e}")
        
        return found_files
    
    def _find_portable_extensions(self, ide_type: IDEType, portable_root: str) -> List[str]:
        """查找便携版扩展文件"""
        found_files = []
        
        try:
            portable_path = Path(portable_root)
            if not portable_path.exists():
                print_warning(f"便携版路径不存在: {portable_root}")
                return found_files
            
            # 在便携版目录中搜索扩展文件
            search_patterns = [
                "extensions/augment*/out/extension.js",
                "data/extensions/augment*/out/extension.js",
                "user-data/extensions/augment*/out/extension.js",
                "resources/app/extensions/augment*/out/extension.js"
            ]
            
            for pattern in search_patterns:
                search_path = portable_path / pattern
                matches = glob.glob(str(search_path))
                found_files.extend(matches)
            
            # 递归搜索（限制深度）
            for root, dirs, files in os.walk(portable_root):
                # 限制搜索深度
                level = root.replace(portable_root, '').count(os.sep)
                if level >= 4:
                    dirs[:] = []  # 不再深入
                    continue
                
                for file in files:
                    if file == "extension.js" and "augment" in root.lower():
                        full_path = os.path.join(root, file)
                        found_files.append(full_path)
        
        except Exception as e:
            print_error(f"搜索便携版扩展失败: {e}")
        
        return found_files

    def _auto_search_extensions(self, ide_type: IDEType) -> List[str]:
        """自动搜索扩展文件的非默认位置"""
        found_files = []
        system = platform.system().lower()

        # 定义搜索位置
        search_locations = []

        if system == "windows":
            search_locations.extend([
                Path.home(),
                Path(os.environ.get("APPDATA", "")),
                Path(os.environ.get("LOCALAPPDATA", "")),
                Path("C:/Program Files"),
                Path("C:/Program Files (x86)"),
            ])
        elif system == "darwin":  # macOS
            search_locations.extend([
                Path.home(),
                Path.home() / "Library" / "Application Support",
                Path("/Applications"),
            ])
        elif system == "linux":
            search_locations.extend([
                Path.home(),
                Path.home() / ".config",
                Path.home() / ".local" / "share",
                Path("/opt"),
                Path("/usr/share"),
            ])

        # 搜索模式
        search_patterns = [
            "**/augment*/out/extension.js",
            "**/augment*/dist/extension.js",
            "**/augment*/build/extension.js",
            "**/augment*extension.js",
        ]

        print_info(f"🔍 开始自动搜索 {ide_type.value} 扩展文件...")

        for location in search_locations:
            if not location.exists():
                continue

            try:
                # 使用更高效的搜索方法，限制搜索深度
                self._search_location_with_depth_limit(location, ide_type, found_files, max_depth=3)

            except (PermissionError, OSError) as e:
                print_warning(f"搜索 {location} 时出错: {e}")
                continue

        # 去重
        found_files = list(set(found_files))

        if found_files:
            print_success(f"✅ 自动搜索找到 {len(found_files)} 个扩展文件")
        else:
            print_warning(f"❌ 自动搜索未找到 {ide_type.value} 扩展文件")

        return found_files

    def _search_location_with_depth_limit(self, location: Path, ide_type: IDEType, found_files: List[str], max_depth: int = 3):
        """在指定位置搜索扩展文件，限制搜索深度"""
        def _recursive_search(current_path: Path, current_depth: int):
            if current_depth > max_depth:
                return

            try:
                for item in current_path.iterdir():
                    if item.is_file():
                        # 检查是否是扩展文件
                        if (item.name == "extension.js" and
                            "augment" in str(item).lower() and
                            self._is_valid_extension_file(str(item)) and
                            self._is_extension_for_ide(str(item), ide_type)):
                            found_files.append(str(item))
                            print_success(f"✅ 找到扩展文件: {item}")
                    elif item.is_dir():
                        # 跳过一些明显不相关的目录以提高性能
                        skip_dirs = {
                            'node_modules', '.git', '.svn', '__pycache__',
                            'cache', 'temp', 'tmp', 'logs', 'log',
                            'build', 'dist', 'target', 'bin', 'obj'
                        }
                        if item.name.lower() not in skip_dirs:
                            _recursive_search(item, current_depth + 1)
            except (PermissionError, OSError):
                # 忽略权限错误，继续搜索其他目录
                pass

        print_info(f"   搜索位置: {location} (最大深度: {max_depth})")
        _recursive_search(location, 0)

    def _is_extension_for_ide(self, file_path: str, ide_type: IDEType) -> bool:
        """检查扩展文件是否属于指定的IDE"""
        file_path_lower = file_path.lower()

        # 根据路径特征判断
        ide_indicators = {
            IDEType.VSCODE: ["vscode", "code", "visual studio code"],
            IDEType.CURSOR: ["cursor"],
            IDEType.WINDSURF: ["windsurf", "codeium"],
        }

        if ide_type in ide_indicators:
            for indicator in ide_indicators[ide_type]:
                if indicator in file_path_lower:
                    return True

        # 如果路径中没有明确的IDE标识，检查扩展名称
        extension_names = {
            IDEType.VSCODE: ["vscode-augment"],
            IDEType.CURSOR: ["cursor-augment", "vscode-augment"],  # Cursor可能使用VS Code扩展
            IDEType.WINDSURF: ["windsurf-augment"],
        }

        if ide_type in extension_names:
            for ext_name in extension_names[ide_type]:
                if ext_name in file_path_lower:
                    return True

        return False

    def _is_valid_extension_file(self, file_path: str) -> bool:
        """验证是否为有效的扩展文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read(1000)  # 只读取前1000字符
                
            # 检查是否包含关键标识
            indicators = [
                "callApi",
                "augment",
                "extension",
                "vscode",
                "activate"
            ]
            
            return any(indicator in content.lower() for indicator in indicators)
            
        except Exception:
            return False
    
    def find_all_extensions(self, portable_roots: Optional[Dict[IDEType, str]] = None) -> Dict[IDEType, List[str]]:
        """查找所有支持的IDE的扩展文件"""
        results = {}
        
        for ide_type in [IDEType.VSCODE, IDEType.CURSOR, IDEType.WINDSURF]:
            portable_root = None
            if portable_roots and ide_type in portable_roots:
                portable_root = portable_roots[ide_type]
            
            files = self.find_extension_files(ide_type, portable_root)
            if files:
                results[ide_type] = files
        
        return results
    
    def get_latest_extension(self, ide_type: IDEType, portable_root: Optional[str] = None) -> Optional[str]:
        """获取最新版本的扩展文件"""
        files = self.find_extension_files(ide_type, portable_root)
        
        if not files:
            return None
        
        # 按修改时间排序，返回最新的
        try:
            latest_file = max(files, key=lambda f: os.path.getmtime(f))
            return latest_file
        except Exception:
            # 如果获取修改时间失败，返回第一个
            return files[0]
    
    def search_by_keyword(self, keyword: str = "augment", search_paths: Optional[List[str]] = None) -> List[str]:
        """通过关键词搜索扩展文件"""
        found_files = []
        
        if not search_paths:
            # 默认搜索路径
            search_paths = [
                os.path.expanduser("~/.vscode"),
                os.path.expanduser("~/.cursor"), 
                os.path.expanduser("~/.windsurf"),
                os.path.expanduser("~/AppData/Roaming") if self.system == "windows" else "",
                os.path.expanduser("~/.config") if self.system == "linux" else "",
                os.path.expanduser("~/Library/Application Support") if self.system == "darwin" else ""
            ]
            search_paths = [p for p in search_paths if p and os.path.exists(p)]
        
        for search_path in search_paths:
            try:
                for root, dirs, files in os.walk(search_path):
                    # 限制搜索深度
                    level = root.replace(search_path, '').count(os.sep)
                    if level >= 5:
                        dirs[:] = []
                        continue
                    
                    if keyword.lower() in root.lower():
                        for file in files:
                            if file == "extension.js":
                                full_path = os.path.join(root, file)
                                if self._is_valid_extension_file(full_path):
                                    found_files.append(full_path)
            
            except Exception as e:
                print_warning(f"搜索路径失败 {search_path}: {e}")
        
        return list(set(found_files))  # 去重
