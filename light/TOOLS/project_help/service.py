"""
项目助手MCP服务
用于基于AI开发助手模板的项目，提供模块信息读取功能
"""

import os
import yaml
import asyncio
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


from mcp.server import Server
from mcp.types import (
    Resource,
    Tool,
    TextContent,
    LoggingLevel
)
import mcp.server.stdio




class ProjectModuleExplorer:
    """项目模块探索器，用于读取和解析项目中的README.md文件"""

    def __init__(self, project_root: Optional[str] = None):
        """
        初始化探索器

        Args:
            project_root: 项目根目录路径，如果为None则使用当前工作目录
        """
        self.project_root = Path(project_root) if project_root else Path.cwd()
    
    """
        辅助工具
    """
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
app = Server("project-help")

# 自动检测项目根目录（当前文件的 PROJECT_ROOT/TOOLS/project_help/service.py）
PROJECT_ROOT = Path(__file__).parent.parent.parent
explorer = ProjectModuleExplorer(str(PROJECT_ROOT))


@app.list_resources()
async def list_resources() -> list[Resource]:
    """列出可用资源"""
    return [
        Resource(
            uri="project://modules",
            name="项目模块列表",
            description="项目中所有带YAML头的README.md模块信息",
            mimeType="application/json"
        )
    ]


@app.list_tools()
async def list_tools() -> list[Tool]:
    """列出可用工具"""
    return [
        Tool(
            name="get_all_modules",
            description="你必须调用该工具以确保你对整个项目的了解，除非你已经查看过相关的记录",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="get_module_details",
            description="你可以使用这个工具获取项目的部分详情。",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "README.md文件的路径（相对路径或绝对路径），例如: PROJECT/README.md"
                    }
                },
                "required": ["path"]
            }
        ),
        Tool(
            name="get_current_time",
            description="获取指定时区的当前时间，返回格式：年月日 时分（例如：2026年01月02日 09:30）",
            inputSchema={
                "type": "object",
                "properties": {
                    "timezone": {
                        "type": "string",
                        "description": "时区（支持UTC/UTC+8/+08:00/Asia/Shanghai等）。默认Asia/Shanghai"
                    }
                },
                "required": []
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """调用工具"""
    try:
        if name == "get_all_modules":
            modules = explorer.get_all_modules_info()

            if not modules:
                return [TextContent(
                    type="text",
                    text="未找到带有YAML头的README.md文件。"
                )]

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

            return [TextContent(type="text", text="\n".join(output))]

        elif name == "get_module_details":
            path = arguments.get("path", "")
            if not path:
                return [TextContent(type="text", text="错误: 请提供path参数")]

            details = explorer.get_module_details(path)

            if not details:
                return [TextContent(
                    type="text",
                    text=f"未找到指定路径的文件: {path}\n请确保路径正确且文件名为README.md"
                )]

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

            return [TextContent(type="text", text="\n".join(output))]

        elif name == "get_current_time":
            tz = arguments.get("timezone", "Asia/Shanghai")
            time_text = format_current_time_in_timezone(tz)
            return [TextContent(type="text", text=time_text)]

        else:
            return [TextContent(type="text", text=f"未知工具: {name}")]

    except Exception as e:
        return [TextContent(type="text", text=f"工具调用出错: {str(e)}")]


async def main():
    """主函数，运行MCP服务器"""
    from mcp.server.stdio import stdio_server

    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    # 运行服务器
    asyncio.run(main())
