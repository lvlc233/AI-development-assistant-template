---
name: TOOLS Directory Description
description: |
    This directory contains all tool resources for the AI development assistant template, including MCP services, prompt templates, etc.
    This is an important toolset for Agent project development.
author: "lxz"
state: OK
created: 2026-01-01
path: "/TOOLS"
---

# TOOLS Directory

This directory contains all tool resources for the AI development assistant template.

## Directory Structure

```
TOOLS/
├── PROMPT/                     # Prompt templates
│   ├── GLOBAL_AGENT_PROMPT     # Global Agent prompt
│   └── AGENT_TEMPLATE          # Single Agent template
├── project_help/               # Project-Help MCP service
│   ├── service.py              # MCP service main program
│   ├── test_service.py         # Test script
│   ├── requirements.txt        # Dependency list
│   ├── mcp.json                # MCP configuration example
│   └── README.md               # Service usage document
└── README.md                   # This file
```

## Tool Description

### 1. PROMPT - Prompt Templates

Contains two core prompt files:

- **GLOBAL_AGENT_PROMPT**: Global Agent prompt, defining the Agent's basic constraints and behavioral norms.
- **AGENT_TEMPLATE**: Single Agent template, used to create specific role-based Agents.

Usage:
1. Copy GLOBAL_AGENT_PROMPT to your IDE/CLI global rules.
2. Create your dedicated Agent based on AGENT_TEMPLATE.

### 2. project_help - MCP Service

Project-Help is an MCP protocol-based service providing project module information query functions.

**Features:**
- Automatically scans README.md files in the project
- Extracts YAML header information
- Provides module list and detailed information queries

**Quick Start:**

```bash
cd TOOLS/project_help
pip install -r requirements.txt
```

Then add the service configuration to your MCP client configuration (see project_help/README.md for details).

**Included Tools:**

1. **get_all_modules** - Get all module information
   - Scans all README.md files with YAML headers in the project
   - Returns module name, path, status, author, and description

2. **get_module_details** - Get specific module details
   - Input README.md file path
   - Returns complete YAML header and file content


3. **get_current_time** - Get current time
   - Supports specifying time zone (default Asia/Shanghai)
   - Returns formatted time string (e.g., 2026-01-02 09:30)

4. **list_todos** - Scan project TODOs:
   - Scans all code files under the specified directory (default current project root)
   - Extracts lines containing TODO markers and their context
   - Automatically ignores common non-code directories (.git, node_modules, etc.)
   - Returns TODO list in JSON format

5. **get_todo_context** - Get TODO detailed context
   - Input file path and line number
   - Returns code context before and after the specified TODO (5 lines before + 20 lines after)
   - Used for in-depth analysis of specific TODO requirements

TODO: Git partition management function (managed independently by Agent), Document MCP-ization (supporting transferable intelligent agent capabilities, reducing project document dependencies).

## Usage Suggestions

1. **MCP Service Strongly Recommended**: Although optional, installing the project-help MCP service can significantly improve the Agent's ability to understand the project structure.

2. **Adjust Template According to Project**: AGENT_TEMPLATE provides a basic template, it is recommended to adjust it according to your specific needs.

3. **Keep Documentation Updated**: The README.md file in the TOOLS directory should be updated as tools are updated.

## Related Documents

- [How to use AI Development Assistant Template](../../README.md)
