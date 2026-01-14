---
name: Project-Help MCP Service Documentation
description: |
    This document describes the installation and usage of the Project-Help MCP service.
    AI assistants should read this document to understand how to configure and use this MCP service.
    [Necessary]
author: "MCP Service"
state: OK
created: 2026-01-01
path: "/TOOLS/project_help"
---

# Project-Help MCP Service

This is a Project Help Service based on MCP (Model Context Protocol), specifically designed for the AI Development Assistant Template.

## Features

This service provides two core functions:

### 1. Get All Module Information (`get_all_modules`)

Scans all README.md files with YAML headers in the project, extracts module information, and returns a summary.

**Usage Example:**
```json
{
    "name": "get_all_modules",
    "arguments": {}
}
```

**Returns:**
- Module Name
- File Path
- Status
- Author
- Description

### 2. Get Module Details (`get_module_details`)

Gets the complete information and YAML header of the README.md file at the specified path.

**Usage Example:**
```json
{
    "name": "get_module_details",
    "arguments": {
        "path": "PROJECT/README.md"
    }
}
```

**Returns:**
- Full File Path
- YAML Header Information (name, description, state, author, etc.)
- Full File Content

## Installation

### Prerequisites

- Python 3.8+
- MCP Library (will be installed automatically)

### 1. Install Dependencies

```bash
cd TOOLS/project_help
pip install -r requirements.txt
```

Dependencies include:
- `mcp` - MCP protocol library
- `PyYAML` - YAML parsing library

### 2. Configure MCP Client

Add the following content to your MCP client configuration (such as Claude Desktop, Cursor, etc.):

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

**Note**: Please modify the above path according to your actual project path.

### 3. Verify Installation

Run the test script to verify if the service is working properly:
