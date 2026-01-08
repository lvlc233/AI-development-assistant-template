"""
项目助手MCP服务
用于基于AI开发助手模板的项目，提供模块信息读取功能
"""

import os
import yaml
import re
import json
import logging
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastmcp import FastMCP

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("project-help")

class ProjectModuleExplorer:
    """项目模块探索器，用于读取和解析项目中的README.md文件"""

    def __init__(self, project_root: Optional[str] = None):
        """
        初始化探索器

        Args:
            project_root: 项目根目录路径，如果为None则使用当前工作目录
        """
        self.project_root = Path(project_root) if project_root else Path.cwd()
    
    def find_all_readme_files(self) -> List[Path]:
        """
        查找项目中所有README.md文件

        Returns:
            README.md文件路径列表
        """
        readme_files = []
        for path in self.project_root.rglob("README.md"):
            # 排除一些常见的依赖目录
            if any(excluded in str(path) for excluded in ['node_modules', '.git', '__pycache__', 'venv', '.venv']):
                continue
            readme_files.append(path)
        return readme_files

    def parse_yaml_header(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """
        解析README.md文件中的YAML头

        Args:
            file_path: README.md文件路径

        Returns:
            解析后的YAML数据，如果没有YAML头则返回None
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # 检查是否以---开头
            if not content.startswith('---'):
                return None

            # 查找第二个---
            parts = content.split('---', 2)
            if len(parts) < 3:
                return None

            yaml_content = parts[1]
            yaml_data = yaml.safe_load(yaml_content)

            return yaml_data if isinstance(yaml_data, dict) else None

        except Exception as e:
            print(f"解析YAML头失败 {file_path}: {e}")
            return None

    def get_module_content(self, file_path: Path) -> str:
        """
        获取README.md的完整内容

        Args:
            file_path: README.md文件路径

        Returns:
            文件内容
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f"读取文件失败: {e}"

    def get_all_modules_info(self) -> List[Dict[str, Any]]:
        """
        获取所有模块的信息

        Returns:
            模块信息列表
        """
        modules = []
        readme_files = self.find_all_readme_files()

        for readme_path in readme_files:
            yaml_data = self.parse_yaml_header(readme_path)

            if yaml_data:
                # 计算相对路径
                try:
                    relative_path = readme_path.relative_to(self.project_root)
                except ValueError:
                    relative_path = readme_path

                module_info = {
                    'path': str(relative_path),
                    'absolute_path': str(readme_path),
                    'yaml_header': yaml_data,
                    'has_yaml': True
                }

                # 提取关键信息用于简介
                name = yaml_data.get('name', '未命名模块')
                description = yaml_data.get('description', '暂无描述')
                state = yaml_data.get('state', 'unknown')
                author = yaml_data.get('author', '未知')

                module_info['summary'] = {
                    'name': name,
                    'description': description.strip() if isinstance(description, str) else description,
                    'state': state,
                    'author': author
                }

                modules.append(module_info)

        return modules

    def get_module_details(self, path: str) -> Optional[Dict[str, Any]]:
        """
        获取指定路径下README.md的详情

        Args:
            path: 相对路径或绝对路径

        Returns:
            模块详情，如果找不到返回None
        """
        # 尝试作为相对路径
        file_path = self.project_root / path
        if not file_path.exists():
            # 尝试作为绝对路径
            file_path = Path(path)

        if not file_path.exists() or file_path.name != 'README.md':
            return None

        yaml_data = self.parse_yaml_header(file_path)
        content = self.get_module_content(file_path)

        try:
            relative_path = file_path.relative_to(self.project_root)
        except ValueError:
            relative_path = file_path

        return {
            'path': str(relative_path),
            'absolute_path': str(file_path),
            'yaml_header': yaml_data,
            'has_yaml': yaml_data is not None,
            'full_content': content
        }


def format_current_time_in_timezone(tz: str) -> str:
    tz_value = (tz or "").strip()
    if not tz_value:
        raise ValueError("timezone不能为空")

    tz_fallback_to_offset = {
        "Asia/Shanghai": "+08:00",
        "Asia/Chongqing": "+08:00",
        "Asia/Hong_Kong": "+08:00",
        "Asia/Taipei": "+08:00",
        "Etc/UTC": "UTC",
    }

    def parse_offset(value: str) -> Optional[timezone]:
        v = value.strip().upper()
        if v in {"UTC", "GMT", "Z"}:
            return timezone.utc

        m = re.match(r"^(?:UTC|GMT)?\s*([+-])\s*(\d{1,2})(?::?(\d{2}))?\s*$", v)
        if not m:
            return None

        sign, hours_s, minutes_s = m.groups()
        hours = int(hours_s)
        minutes = int(minutes_s) if minutes_s else 0

        if hours > 23 or minutes > 59:
            return None

        delta = timedelta(hours=hours, minutes=minutes)
        if sign == "-":
            delta = -delta
        return timezone(delta)

    tzinfo = parse_offset(tz_value)
    if tzinfo is None and tz_value in tz_fallback_to_offset:
        tzinfo = parse_offset(tz_fallback_to_offset[tz_value])

    if tzinfo is None:
        try:
            from zoneinfo import ZoneInfo

            tzinfo = ZoneInfo(tz_value)
        except Exception as e:
            raise ValueError(
                f"无法识别或加载timezone: {tz_value}。"
                f"建议使用UTC/UTC+8/+08:00这类偏移格式，或安装tzdata以支持IANA时区（例如Asia/Shanghai）。"
                f"错误: {e}"
            )

    now = datetime.now(tzinfo)
    return f"{now.year}年{now.month:02d}月{now.day:02d}日 {now.hour:02d}:{now.minute:02d}"


# 创建MCP应用
mcp = FastMCP("project-help")

# 自动检测项目根目录（当前文件的 PROJECT_ROOT/TOOLS/project_help/service.py）
PROJECT_ROOT = Path(__file__).parent.parent.parent
explorer = ProjectModuleExplorer(str(PROJECT_ROOT))


@mcp.resource("project://modules")
def list_resources() -> List[Dict[str, Any]]:
    """项目中所有带YAML头的README.md模块信息"""
    return explorer.get_all_modules_info()


@mcp.tool(name="get_all_modules")
def get_all_modules() -> str:
    """你必须调用该工具以确保你对整个项目的了解，除非你已经查看过相关的记录"""
    modules = explorer.get_all_modules_info()

    if not modules:
        return "未找到带有YAML头的README.md文件。"

    # 构建输出
    output = []
    output.append("=" * 60)
    output.append(f"找到 {len(modules)} 个模块")
    output.append("=" * 60)
    output.append("")

    for i, module in enumerate(modules, 1):
        summary = module['summary']
        output.append(f"【模块 {i}】")
        output.append(f"名称: {summary['name']}")
        output.append(f"路径: {module['path']}")
        output.append(f"状态: {summary['state']}")
        output.append(f"作者: {summary['author']}")
        output.append(f"描述:")
        output.append(summary['description'])
        output.append("-" * 40)
        output.append("")

    return "\n".join(output)


@mcp.tool(name="get_module_details")
def get_module_details(path: str) -> str:
    """你可以使用这个工具获取项目的部分详情。
    
    Args:
        path: README.md文件的路径（相对路径或绝对路径），例如: PROJECT/README.md
    """
    if not path:
        return "错误: 请提供path参数"

    details = explorer.get_module_details(path)

    if not details:
        return f"未找到指定路径的文件: {path}\n请确保路径正确且文件名为README.md"

    # 构建输出
    output = []
    output.append("=" * 60)
    output.append("模块详细信息")
    output.append("=" * 60)
    output.append("")
    output.append(f"文件路径: {details['path']}")
    output.append(f"包含YAML头: {'是' if details['has_yaml'] else '否'}")
    output.append("")

    if details['yaml_header']:
        output.append("YAML头信息:")
        output.append("-" * 40)
        for key, value in details['yaml_header'].items():
            output.append(f"{key}: {value}")
        output.append("-" * 40)
        output.append("")

    output.append("完整内容:")
    output.append("=" * 60)
    output.append(details['full_content'])

    return "\n".join(output)


@mcp.tool(name="get_current_time")
def get_current_time(timezone: str = "Asia/Shanghai") -> str:
    """获取指定时区的当前时间，返回格式：年月日 时分（例如：2026年01月02日 09:30）
    
    Args:
        timezone: 时区（支持UTC/UTC+8/+08:00/Asia/Shanghai等）。默认Asia/Shanghai
    """
    try:
        return format_current_time_in_timezone(timezone)
    except Exception as e:
        return f"获取时间出错: {str(e)}"


def _scan_todos(root_dir: str) -> List[Dict[str, Any]]:
    """
    扫描指定目录下的 TODO，并提取上下文。
    """
    todos = []
    # 遍历文件
    for root, dirs, files in os.walk(root_dir):
        # 忽略常见的非代码目录
        if any(ignore in root for ignore in ['.git', '__pycache__', 'node_modules', '.venv', 'venv']):
            continue
            
        for file in files:
            if not file.endswith(('.py', '.java', '.js', '.ts', '.md')): # 支持常见代码文件
                continue
                
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    
                for i, line in enumerate(lines):
                    if 'TODO' in line:
                        # 上下文提取：TODO 行 + 后续 15 行
                        context_lines = lines[i:min(i+15, len(lines))]
                        context = "".join(context_lines).strip()
                        
                        rel_path = os.path.relpath(file_path, root_dir)
                        todos.append({
                            'file': rel_path,
                            'line': i + 1,
                            'content': line.strip(),
                            'context': context
                        })
            except Exception as e:
                # 忽略读取错误
                pass
    return todos


@mcp.tool()
def list_todos(directory: str = ".") -> str:
    """
    列出指定目录（默认为当前目录）下所有的 TODO 项及其代码上下文。
    返回 JSON 格式的字符串。
    
    Args:
        directory: 要扫描的根目录路径。
    """
    return _list_todos_impl(directory)

def _list_todos_impl(directory: str = ".") -> str:
    # 如果是 "."，则使用 PROJECT_ROOT
    if directory == ".":
        abs_dir = str(PROJECT_ROOT)
    else:
        abs_dir = os.path.abspath(directory)
        
    if not os.path.exists(abs_dir):
        return json.dumps({"error": f"Directory not found: {abs_dir}"})
        
    logger.info(f"Scanning TODOs in {abs_dir}")
    todos = _scan_todos(abs_dir)
    return json.dumps(todos, ensure_ascii=False, indent=2)


@mcp.tool()
def get_todo_context(file_path: str, line_number: int) -> str:
    """
    获取特定文件中特定行号附近的 TODO 上下文。
    用于深入查看某个 TODO 的详细信息。
    
    Args:
        file_path: 文件路径
        line_number: TODO 所在的行号
    """
    return _get_todo_context_impl(file_path, line_number)

def _get_todo_context_impl(file_path: str, line_number: int) -> str:
    try:
        # 尝试处理相对路径
        if not os.path.isabs(file_path):
             file_path = str(PROJECT_ROOT / file_path)

        if not os.path.exists(file_path):
             return json.dumps({"error": f"File not found: {file_path}"})

        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        target_index = line_number - 1
        if target_index < 0 or target_index >= len(lines):
             return json.dumps({"error": "Line number out of range"})

        # 获取更宽的上下文：前后各 20 行
        start = max(0, target_index - 5)
        end = min(len(lines), target_index + 20)
        
        context_lines = lines[start:end]
        context = "".join(context_lines)
        
        return json.dumps({
            "file": file_path,
            "line": line_number,
            "content": lines[target_index].strip(),
            "full_context": context
        }, ensure_ascii=False, indent=2)
        
    except Exception as e:
        return json.dumps({"error": str(e)})


if __name__ == "__main__":
    # 运行服务器
    mcp.run()
