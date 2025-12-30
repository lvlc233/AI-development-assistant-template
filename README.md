<p align="center">
  <a href="README.md"><strong>English</strong></a> | Chinese
</p>

# AI Development Assistant Template

A management template for unlocking the potential of development assistant Agents, focusing on improving readability and code quality, inspired by Specification-Driven Development and Skill.

## Preface

We now frequently use AI programming tools like Cursor, Claude Code, Antigravity... there are many. While they are quite interesting—we can have them handle repetitive and meaningless tasks to improve our development efficiency; we can also use these assistants to quickly learn technical content; sometimes they even offer decent suggestions.

But... most of the time, they always leave us feeling less than satisfied, don't they?

Why is this? There are many reasons, such as insufficient capabilities of LLMs themselves, poor context management and uncontrollability in IDEs, inadequate embedded tools/MCP services, and unclear user instructions, etc...

That's why this project exists. I will summarize methodologies from a year of trial-and-error experience and philosophy in AI development to improve our development experience.

## How to Use

Simply `git clone` this project, open `TOOLS/PROMPT`, and place `GLOBAL_AGENT_PROMPT` into your rules. Create your role-based Agent following the `AGENT_TEMPLATE` and put it into the Agent's system prompt.

## Core Principles

Two key ideas:
1. **Think from the Agent's perspective**, consider what context they can see, be mindful of context drift, and keep the context for each Agent clean while retaining the core information.
2. **Don't treat your AI IDE (CLI) as a software engineer**, but as an architect. Imagine you're managing a massive office, not a single computer.

## 1. Context

### Project Context

Project context manages the project and keeps it within a stable scope. This is also the reference guideline for all Agents when conducting project-level development. It includes the following:

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
2. Async environment
3. Direct queries are prohibited; pagination must be used.
4. Pay attention to secrets security and other issues
5. Every important function and variable must be commented in Chinese
6. Proposed functions must be marked with TODO
7. ....
```

2. **Task Metrics**: You can understand this as a todo list in the Agent, but the todo content is built by you personally, not by the Agent creating potentially unnecessary todos. You can also attach relevant evaluation criteria and development conditions.

```markdown
# Task Metrics
1. Complete frontend project technology research []
   Creation time: 2025-12-30 9:00
   Completion time: ...
   Responsible: UI Agent
2. Complete backend project technology research [√]
   Creation time: 2025-12-30 9:00
   Completion time: 2025-12-30 12:00
   Responsible: Backend Agent
   Note: Backend technology stack has been determined, related materials stored in document/backend.md
3. Conduct business scenario analysis [×]
   Creation time: 2025-12-30 10:00
   Completion time: 2025-12-30 12:00
   Responsible: Human
   Note: Found many unclear business scenarios, need more detailed planning.
4. Create sql [...]
...
```

3. **Project Log**: This records what happened in the project, including but not limited to:
   - Main project commit history
   - Developer feedback
   - Interaction records
   - Solutions
   - Todo items
   - ...

4. **Code Comments**: When having Agents write code, they must clearly document the function and purpose of each module and provide a list indicating the relationship between functions and modules.

### Agent Memory Context

This is the Agent's memory capability. Generally, we can create a folder to represent the Agent's memory. Of course, we can also encapsulate an MCP to provide cross-project memory functionality. Yes, the memory here emphasizes cross-project capability more. The problem it solves is: when we restart a session or go to a new project, we have to make the Agent go through the process of reading, understanding, and memorizing again. But if we reverse the thinking—not having the project provide the Agent's memory, but the Agent bringing its own memory—then things become much more interesting. This means we emphasize the Agent's growth more.

1. **Agent Operation Log**: Records all Agent operations

```log.2025-12-30
# Backend Agent
2025-12-30 9:00 | I was asked to conduct backend project research,
2025-12-30 9:00 | I used a web tool to search for resources on topic xxx, trying to find some resources
...
```

2. **Agent Attention-Filtered Memory**: This is a relatively abstract concept. Simply put, what is stored here is the Agent's understanding, including its understanding of tools, projects—this is the Agent's long-term memory and thinking. It's the most important part of Agent memory and controls the output style of Agent behavior.
...

3. **Manual Intervention Memory**

### Agent Runtime Context

This is ordinary context or prompts. Personally, the recommendation is:
1. **Instruction Set**: The capability boundaries of what the Agent can do—what it can and cannot do
2. **Knowledge Base**: Constrains the Agent's domain, like role-playing. Instead of feeding it a bunch of knowledge, tell it what it needs to know
3. **System-level Prompts**: Generally used as correction patches.

No need to say much—most IDEs/CLIs cannot directly manage context.

## 2. Safety

Imagine if you were a project leader, and everyone in your team developed and committed directly to the main/master branch—how terrible that would be. The same applies to Agents. Even if you're a single Agent user, imagine how bad it would be if you also skip project management during development. I believe everyone has complained that IDEs/CLIs always modify their code. This "nature" seems unstoppable. Of course, this is mainly an instruction recognition issue. We can control it by optimizing instructions or setting permissions, but why not go with this "nature"?

### Sandbox Environment

The sandbox environment here is an abstract representation. It can be a real sandbox environment or a simple folder. It represents an area where Agents can independently write code. You can imagine each sandbox as an employee's computer, where they can freely create without affecting the main, core, runnable code. You can create independent SANDBOX environments for each Agent and store memory in the SANDBOX environment (if you plan to use the file system as your memory system).
Reference [SANDBOX/Agent/README.md]

### Code Review

Just like in company projects, not all submitted code can be directly merged into the main branch. We often consider code style, feature confirmation, and potential destructiveness to review submitted code, inform developers of the results, and provide suggestions when necessary to assist their development.
Therefore, have the Agent "submit" code to a designated area and conduct a review. Perhaps you can create an Agent specifically for preliminary review.

### Version Control

Version control requires Agents/humans to include a version when writing code. To solve the code overwriting issue caused by Agents still storing old version data in context during human-machine/MAS interaction. When the Agent writes code, compare version headers—Agents always get the latest data.

```python
"""
    writer: agent,human
    last writer: agent
    version: 15da1551d
    update: 2025-12-30 9:00
"""
def web_search(top:str):
    ...
    pass
```

## 3. Others

### Git Hub

You can implement the above ideas based on Git. I think that would be a good choice.

### Agent to MCP

For Agent developers.

You certainly know you can encapsulate your Agent as an MCP Service to make it available to other Agent tasks. You can boldly try deploying your Agent MCP into your AI IDE (CLI) to improve your Agent's reusability, thereby gradually reducing your repetitive tasks.

Additionally, you can combine the idea of private memory into the Agents you develop, enabling them to use those solutions they consider safe and effective in different scenarios.

## Future Plans

1. Receive data feedback for iterative optimization.
2. Launch more specialized templates based on different scenarios to precisely solve problems in different contexts.
3. Consider it as an application, providing convenient cmd scripts to simplify the usage process.
...