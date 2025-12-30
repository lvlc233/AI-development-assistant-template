<p align="center">
  <strong>English</strong> | <a href="README.zh-CN.md">中文</a>
</p>

# AI-development-assistant-template

A management template for unleashing Agent potential in development assistance, focusing on readability and code quality improvement, inspired by specification-driven development and Skill.

## Preface

We now frequently use AI programming tools, such as Cursor, Claude Code, Antigravity... there are many. While they are quite fascinating, we can have them handle repetitive and meaningless tasks to improve our development efficiency; we can also leverage these assistants to quickly learn technical content; sometimes, they even offer some good suggestions.

But... most of the time, they're not quite satisfactory, aren't they?

Why is this? There are many reasons, such as inherent limitations of LLM capabilities, poor context management and lack of control in IDEs, insufficient built-in tools/MCP Services, and unclear user instructions, among others...

So this is why this project exists. I will attempt to summarize some methodologies from a year of AI development experience and philosophy to improve our development experience.

## How to Use

Simply git clone this project and place the templates in your respective Agents.

## Core Principles

Two key philosophies:
1. Think from the Agent's perspective - understand what context they can see, be mindful of context drift phenomena, and maintain the cleanest and most core contextual information for each Agent.
2. Please don't treat your AI IDE (CLI) from a software engineer's perspective, but from an architect's perspective. Imagine you're operating a huge office, not just a computer.

## 1. Context Management

### Project Context

Project context manages the project and keeps it within a stable scope. This serves as the guiding criterion for all Agents when conducting project-level development. It includes the following:

1. **Specification Document (Important)**: I recommend you personally create such a specification document. This document requires you to manage your entire project from a system architect's perspective, including but not limited to:
   - Development style
   - Development tools
   - Environment
   - Basic resources
   - Technology selection
   - Version control
   - ...

```markdown
# Specification Document

## Introduction
The project will adopt Domain-Driven Development...

## Environment
- python: 3.11+
- langchain: 1.0.0+
- uv: environment

## Resources
- sql:

## Development Standards
1. Must be thread-safe
2. Asynchronous environment
3. Prohibit direct queries; use pagination queries instead
4. Pay attention to key security and other issues
5. Every important function and variable must be commented in Chinese
6. Proposed functions must use TODO markers
7. ....
```

2. **Task Metrics**: You can understand this as todo in Agent, but the todo content is constructed by you personally, not by the Agent creating potentially unnecessary todos. You can also attach relevant evaluation criteria and development conditions.

```markdown
# Task Metrics
1. Complete frontend project technology research [ ]
   Creation time: 2025-12-30 9:00
   Completion time: ...
   Responsible: UI Agent
2. Complete backend project technology research [√]
   Creation time: 2025-12-30 9:00
   Completion time: 2025-12-30 12:00
   Responsible: Backend Agent
   Note: Backend technology stack has been determined, and relevant materials have been stored in document/backend.md
3. Conduct business scenario analysis [×]
   Creation time: 2025-12-30 10:00
   Completion time: 2025-12-30 12:00
   Responsible: Human
   Note: Found a large number of unclear business scenarios, requiring more detailed planning.
4. Create sql [...]
...
```

3. **Project Records**: Record what happened in the project, including but not limited to:
   - Main project commit history
   - Developer feedback
   - Interaction records
   - Solutions
   - To-do items
   - ...

4. **Code Annotations**: When Agent writes code, be sure to clearly document the function and purpose of each module, and create a list indicating function-module relationships.

### Agent Memory Context

Agent memory capability. Generally, we can create a folder to represent Agent's memory. Of course, we can also encapsulate an MCP to provide cross-project memory functionality. Here, memory emphasizes more on cross-project capability. This solves the problem that when we restart a session or go to a new project, we have to let the Agent go through the process of reading, understanding, and memorizing again. But if we reverse the thinking - not having the project provide Agent's memory, but having Agent bring its own memory - then things become much more interesting. This means we emphasize Agent's growth capability more.

1. **Agent Operation Records**: Record all operations of the Agent
```
log.2025-12-30
# Backend Agent
2025-12-30 9:00 | I was asked to conduct backend project research
2025-12-30 9:00 | I used web tools to search for resources on topic xxx, trying to find some resources
...
```

2. **Agent Attention Filtering Memory**: This is a relatively abstract concept. Simply put, what is stored here is the Agent's understanding, including its understanding of tools and projects. This is the most important part of Agent's long-term memory and thinking. It's the important part that controls the output style of Agent's behavior.
   ...

3. **Manual Intervention Memory**

### Agent Runtime Context

This is ordinary context or prompts. Personal recommendations are:
1. **Instruction Set**: Agent's capability boundaries, used to express what Agent can and cannot do
2. **Knowledge Base**: Constrain Agent's domain, similar to... role-playing. Instead of traditional approach of giving it a bunch of knowledge, tell it what it needs to know
3. **System-level Prompts**: Generally just patches for corrections.

Nothing much to say; most IDEs/CLIs cannot directly manage context.

## 2. Security

Imagine if you were a project leader, and everyone on your team directly developed and committed to the main/master branch - how terrible that would be. The same applies to Agents. Even if you're a single Agent user, imagine how bad it would be if you didn't do project management during development. I believe everyone has complained about IDEs/CLIs always modifying their code. This "nature" seems uncontrollable. Of course, this is mainly a problem of instruction recognition. We can control it by optimizing instructions or setting permissions, but why don't we go along with this "nature"?

### Sandbox Environment

The sandbox environment here is an abstract representation. It can be a real sandbox environment or a simple folder. It represents an area where Agents can independently write code. You can imagine each sandbox as an employee's computer, where they can freely create without affecting the main, core, runnable code. You can create independent SANDBOXes for each Agent and store memories in the SANDBOX environment (if you plan to use the file system as your memory system).

Reference [SANDBOX\Agent\README.md]

### Code Review

Just like in company projects, not all submitted code can be directly merged into the main branch. We often consider code style, feature confirmation, whether it's destructive, etc., to review submitted code and inform developers of review results, providing suggestions when necessary to assist their development.

So, let Agent "submit" code to a designated area and conduct reviews. Perhaps you can create an Agent specifically for initial reviews.

### Version Control

Version control requires Agent/Human to introduce a version when writing code. To solve the code overwriting problem during human-Agent/MAS interaction, because Agent's context still stores old data when writing code. When Agent writes code, compare the version header so Agent always gets the latest data.

```python
"""
    writer: agent,human
    last writer: agent
    version: 15da1551d
    updated: 2025-12-30 9:00
"""
def web_search(top:str):
    ...
    pass
```

## 3. Other

### GitHub

You can implement the above ideas based on Git. I think that would be a good choice.

### Agent to MCP

For Agent developers:

You definitely know you can encapsulate your Agent as an MCP Service for other Agent tasks. You can boldly try to deploy your Agent MCP to your AI IDE (CLI) to improve your Agent reusability, thereby gradually reducing your repetitive tasks.

In addition, you can combine the idea of private memory into your Agent development, enabling them to use those solutions they consider safe and effective in different scenarios.

## Future Plans

1. Receive data feedback and iterate optimization.
2. Launch more specialized templates based on different scenarios to precisely solve problems in different contexts.
3. Consider making it an application, providing convenient cmd scripts to simplify the usage process.
...
