---
name: TOOLS目录说明
description: |
    该目录包含AI开发助手模板的所有工具资源，包括MCP服务、提示词模板等。
    这是Agent进行项目开发的重要工具集。
author: "lxz"
state: OK
created: 2026-01-01
path: "/TOOLS"
---

# TOOLS 目录

该目录包含AI开发助手模板的所有工具资源。

## 目录结构

```
TOOLS/
├── PROMPT/                     # 提示词模板
│   ├── GLOBAL_AGENT_PROMPT     # 全局Agent提示词
│   └── AGENT_TEMPLATE          # 单个Agent模板
├── project_help/               # Project-Help MCP服务
│   ├── service.py              # MCP服务主程序
│   ├── test_service.py         # 测试脚本
│   ├── requirements.txt        # 依赖列表
│   ├── mcp.json                # MCP配置示例
│   └── README.md               # 服务使用文档
└── README.md                   # 本文件
```

## 工具说明

### 1. PROMPT - 提示词模板

包含两个核心提示词文件：

- **GLOBAL_AGENT_PROMPT**：全局Agent提示词，定义了Agent的基本约束和行为规范
- **AGENT_TEMPLATE**：单个Agent模板，用于创建特定角色的Agent

使用方式：
1. 将GLOBAL_AGENT_PROMPT复制到你的IDE/CLI的全局规则中
2. 基于AGENT_TEMPLATE创建你的专用Agent

### 2. project_help - MCP服务

Project-Help是一个基于MCP协议的服务，提供项目模块信息查询功能。

**功能特性：**
- 自动扫描项目中的README.md文件
- 提取YAML头信息
- 提供模块列表和详细信息查询

**快速开始：**

```bash
cd TOOLS/project_help
pip install -r requirements.txt
```

然后在你的MCP客户端配置中添加服务配置（详见project_help/README.md）。

**包含的工具：**

1. **get_all_modules** - 获取所有模块信息
   - 扫描项目中所有带YAML头的README.md
   - 返回模块名称、路径、状态、作者和描述

2. **get_module_details** - 获取指定模块详情
   - 输入README.md文件路径
   - 返回完整的YAML头和文件内容


3. **get_current_time** - 获取当前时间
   - 支持指定时区（默认Asia/Shanghai）
   - 返回格式化的时间字符串（如：2026年01月02日 09:30）

4. **list_todos** - 扫描项目TODO: 
   - 扫描指定目录（默认当前项目根目录）下的所有代码文件
   - 提取包含TODO标记的行及其上下文
   - 自动忽略常见非代码目录（.git, node_modules等）
   - 返回JSON格式的TODO列表

5. **get_todo_context** - 获取TODO详细上下文
   - 输入文件路径和行号
   - 返回指定TODO前后的代码上下文（前5行+后20行）
   - 用于深入分析TODO的具体需求

TODO: git分区管理功能(由Agent独立管理项目),文档mcp化(支持可以迁移的智能体能力,减少项目的文档依赖。)
## 使用建议

1. **MCP服务强烈推荐安装**：虽然可选，但安装project-help MCP服务可以显著提升Agent对项目结构的理解能力

2. **根据项目调整模板**：AGENT_TEMPLATE提供了基础模板，建议根据你的具体需求进行调整

3. **保持文档更新**：TOOLS目录下的README.md文件应该随工具的更新而更新

## 相关文档

- [如何使用AI开发助手模板](../../README.md)
- [Project-Help MCP服务详细文档](./project_help/README.md)
- [Agent工作约束](../../AGENT/README.md)
- [项目核心资源](../../PROJECT/README.md)

