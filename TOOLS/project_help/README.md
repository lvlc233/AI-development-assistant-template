---
name: Project-Help MCP服务文档
description: |
    本文档描述了Project-Help MCP服务的安装和使用方法。
    AI助手应阅读此文档以了解如何配置和使用该MCP服务。
    [必要]
author: "MCP Service"
state: OK
created: 2026-01-01
path: "/TOOLS/project_help"
---

# Project-Help MCP服务

这是一个基于MCP（Model Context Protocol）的项目帮助服务，专门为AI开发助手模板设计。

## 功能

该服务提供两个核心功能：

### 1. 获取所有模块信息 (`get_all_modules`)

扫描项目中所有带有YAML头的README.md文件，提取模块信息并返回简介。

**使用示例：**
```json
{
    "name": "get_all_modules",
    "arguments": {}
}
```

**返回内容：**
- 模块名称
- 文件路径
- 状态
- 作者
- 描述

### 2. 获取指定模块详情 (`get_module_details`)

获取指定路径下README.md文件的完整信息和YAML头。

**使用示例：**
```json
{
    "name": "get_module_details",
    "arguments": {
        "path": "PROJECT/README.md"
    }
}
```

**返回内容：**
- 完整文件路径
- YAML头信息（name, description, state, author等）
- 完整文件内容

## 安装

### 前置要求

- Python 3.8+
- MCP库（会自动安装）

### 1. 安装依赖

```bash
cd TOOLS/project_help
pip install -r requirements.txt
```

依赖包括：
- `mcp` - MCP协议库
- `PyYAML` - YAML解析库

### 2. 配置MCP客户端

将以下内容添加到您的MCP客户端配置中（如Claude Desktop、Cursor等）：

```json
{
  "mcpServers": {
    "project-help": {
      "command": "python",
      "args": ["G:/work/project/self_project/template/AI-development-assistant-template/TOOLS/project_help/service.py"],
      "env": {
        "PYTHONPATH": "G:/work/project/self_project/template/AI-development-assistant-template/TOOLS/project_help"
      }
    }
  }
}
```

**注意**：请根据您的实际项目路径修改上述路径。

### 3. 验证安装

运行测试脚本验证服务是否正常工作：

```bash
python test_service.py
```

预期输出应显示找到项目中的模块信息。

## 文件说明

- `service.py` - MCP服务主程序
- `test_service.py` - 测试脚本
- `mcp.json` - MCP配置示例
- `requirements.txt` - 依赖列表

## YAML头格式

服务会自动识别以下格式的README.md文件：

```yaml
---
name: 模块名称
description: |
    模块的详细描述
    可以包含多行文本
author: "作者名"
state: OK
created: 2026-01-01
path: "/模块路径"
---

# 正文内容
```

## 注意事项

1. **自动排除目录**：服务会自动排除以下目录中的README.md文件：
   - `node_modules`
   - `.git`
   - `__pycache__`
   - `venv` / `.venv`

2. **路径处理**：服务支持相对路径和绝对路径，会自动计算相对于项目根目录的路径。

3. **项目根目录自动检测**：服务会自动检测项目根目录（service.py文件的父级的父级目录）。

## 故障排除

### 问题：找不到模块

**原因**：
- README.md文件没有YAML头
- YAML头格式不正确
- 文件不在项目目录中

**解决**：
确保README.md文件以`---`开始，并包含有效的YAML头。

### 问题：MCP客户端无法连接

**原因**：
- 路径配置错误
- 依赖未安装
- MCP库版本不兼容

**解决**：
1. 检查mcp.json中的路径是否正确
2. 运行`pip install -r requirements.txt`安装依赖
3. 确保Python环境可以访问这些路径
4. 如果遇到`AttributeError: module 'mcp.server.stdio' has no attribute 'run'`错误，请确保使用最新版本的service.py（已修复为使用async/await方式）

### 问题：启动时提示AttributeError

**错误信息**：
```
AttributeError: module 'mcp.server.stdio' has no attribute 'run'
```

**原因**：MCP库版本更新导致的API变化

**解决**：已在新版本中修复，使用async/await方式启动服务器。如果仍有问题，请确保：
1. 使用最新版本的`service.py`
2. Python版本 >= 3.8
3. 重新安装依赖：`pip install --upgrade -r requirements.txt`

## 更新日志

- 2026-01-01 - 初始版本
  - 实现get_all_modules功能
  - 实现get_module_details功能
  - 支持YAML头解析

