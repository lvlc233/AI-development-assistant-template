<p align="center">
  <strong>English</strong> | <a href="README.zh-CN.md">中文</a>
</p>

AI Development Assistant Template

A management template for unlocking the potential of Agent-based development assistants, focused on enhancing readability and code quality, inspired by Specification-Driven Development and Skill.

# Preface

We now frequently use AI programming tools like Cursor, Claude Code, Antigravity... there are many. While they are quite interesting, allowing us to delegate repetitive and meaningless tasks to improve development efficiency; we can also leverage these assistants to quickly learn technical content; sometimes they even offer decent suggestions.

But... most of the time, they leave us feeling underwhelming, don't they?

Why is that? There are many reasons, such as inherent LLM capability limitations, poor context management and uncontrollability in IDEs, insufficient embedded tools/MCP Services, and unclear user instructions...

This is precisely why this project exists. I will distill methodologies from a year of AI development experience and philosophy to enhance our development experience.

# How to Use

1. Clone this project via git
2. Open TOOLS/PROMPT and place GLOBAL_AGENT_PROMPT into your rules
3. Create your role-based Agent following the AGENT_TEMPLATE and insert it into the Agent's system prompt
4. Create your project specification document
5. Install MCP services from TOOLS/MCP (optional, but recommended)
6. A project case is provided for your reference
7. After completing the above preparations, you can type "check" to ensure your Agent can correctly build the project

# How It Works

1. First, GLOBAL_AGENT_PROMPT in the global rules defines the Agent's basic constraints to ensure it understands how to develop projects based on this template's philosophy
2. Define your Agent's role, and it can automatically build projects in a safe working environment
3. Referencing Claude Skill, README.md+yaml header descriptions are provided for 3 major modules to ensure the Agent always remembers them during project development (based on the provided MCP implementation). Of course this isn't necessary, as GLOBAL_AGENT_PROMPT already specifies everything clearly. If you're token-conscious, I recommend manually modifying GLOBAL_AGENT_PROMPT to make the Agent retrieve this information entirely via MCP(Remove the three core module descriptions from GLOBAL_AGENT_PROMPT and fetch them from MCP instead.)
4. Start your work
5. While not mandatory, it's recommended to build a README.md+yaml header description in each project module, using the provided MCP capabilities to keep your Agent consistently aware of the project. Refer to the case study.

# Future Plans

1. Receive data feedback for iterative optimization
2. Launch more specialized templates for different scenarios to precisely address problems in various contexts
3. Consider making this an application with convenient cmd scripts to simplify the workflow
...

# Concepts (For Your Understanding)

Two Core Ideas:
1. Think from the Agent's perspective: what context can they see? Watch for context drift, maintain the cleanest and most core contextual information for each Agent
2. Don't approach your AI IDE (CLI) as a software engineer, but as an architect. Imagine you're operating a huge office, not a single computer

## 1. Context

### Project Context

Project context manages the project and keeps it within a stable scope. This is also the reference criterion for all Agents during project-level development. It includes:

1. **Specification Document (Important)**: I recommend creating such a specification document yourself. It requires you to manage your entire project from a system architect's perspective, including but not limited to:
   - Development style
   - Development tools
   - Environment
   - Basic resources
   - Technology selection
   - Version control
   - ...

```md
# Specification Document

## Introduction
Project will adopt Domain-Driven Development...
## Environment
- python: 3.11+
- langchain: 1.0.0+
- uv: environment
## Resources
- sql:
## Development Standards
1. Must be thread-safe
2. Async environment
3. Prohibit direct queries, use pagination instead
4. Pay attention to key security
5. Every important function and variable must be commented in Chinese
6. Proposed functions must use TODO markers
7. ...
```

2. **Task Metrics**: You can understand these as Agent todo items, but todo content is built by you personally, not by the Agent creating potentially unnecessary todos. You can also attach relevant evaluation criteria and development conditions.

```md
# Task Metrics
1. Complete frontend project technical research []
   Created: 2025-12-30 9:00
   Completed: ...
   Owner: Design Agent
2. Complete backend project technical research [√]
   Created: 2025-12-30 9:00
   Completed: 2025-12-30 12:00
   Owner: Backend Agent
   Notes: Backend stack confirmed, relevant materials stored in document/backend.md
3. Conduct business scenario analysis [×]
   Created: 2025-12-30 10:00
   Completed: 2025-12-30 12:00
   Owner: Human
   Notes: Found large amount of unclear business scenarios, needs more detailed planning
4. Create sql [...]
...
```

3. **Project Records**: Documenting what happened in the project, including but not limited to:
   - Main project commit history
   - Developer feedback
   - Interaction records
   - Solutions
   - Todo items
   - ...

4. **Code Notes**: Require Agents to clearly document each module's purpose and functionality when writing code, and list an inventory of functions and module relationships

### Agent Memory Context

This is the Agent's memory capability. Generally, we can create a folder to represent Agent memory. Of course, we can also encapsulate an MCP to provide cross-project memory capabilities. Yes, the memory here emphasizes cross-project capability. The problem to solve is: when we restart a session or go to a new project, we have to make the Agent re-read, understand, and memorize. But if we reverse the thinking—not the project providing Agent memory, but the Agent bringing its own memory—things become much more interesting. This means we emphasize the Agent's growth capability more.

1. **Agent Operation Records**: Record all Agent operations
```log.2025-12-30
# Backend Agent
2025-12-30 9:00 | I was asked to research backend project,
2025-12-30 9:00 | I used web tool to search for resources on xxx, trying to find some resources
...
```

2. **Agent Attention-Filtered Memory**: This is a relatively abstract concept. Simply put, what is stored here is the Agent's understanding, including its comprehension of tools and projects—the Agent's long-term memory and thinking. This is the most important part of Agent memory and crucial for controlling the Agent's output style.

3. **Manual Intervention Memory**

### Agent Runtime Context

This is ordinary context or prompts. Personal recommendations:

1. **Instruction Set**: The Agent's capability boundaries, expressing what it can and cannot do
2. **Knowledge Base**: Constrains the Agent's domain, like... role-playing. Rather than giving it a pile of knowledge, tell it what it needs to know
3. **System-level Prompts**: Generally just patches for corrections

Not much to say—most IDEs/CLIs can't directly manage context.

## 2. Security

Imagine you're a project leader. How terrible would it be if everyone on your team directly developed and committed to the main/master branch? The same applies to Agents. Even if you're a single-Agent user, imagine how bad it would be if development didn't include project management. I'm sure we've all complained about IDEs/CLIs always modifying our code—this "nature" seems uncontrollable. Of course this is mainly an instruction recognition issue. We could control it by optimizing instructions or setting permissions, but why not embrace this "nature"?

### Sandbox Environment

The sandbox environment here is an abstract representation. It could be a real sandbox environment or a simple folder. It represents an area where Agents can independently write code. Imagine each sandbox is an employee's computer where they can freely create without affecting the main, runnable code. You can create independent SANDBOX environments for each Agent (if you plan to use the file system as your memory system).

### Code Review

Just like in company projects, not all submitted code can be directly merged into the main branch. We often review submitted code from perspectives like code style, feature confirmation, and whether it's destructive, then inform developers of review results and provide suggestions when necessary to assist their development.

So, let Agents "submit" code to a designated area and conduct reviews. Perhaps you can create an Agent specifically for primary review.

### Version Control

Version control requires Agents/humans to introduce a version when writing code. To solve the code overwriting problem caused by Agents' contexts still storing old data during human-machine/MAS interaction. When Agents write code, compare version headers—Agents always get the latest data.

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

You definitely know you can encapsulate your Agent as an MCP Service for other Agent tasks. You can boldly try deploying your Agent MCP into your AI IDE (CLI) to improve your Agent reuse rate, thereby gradually reducing your repetitive tasks.

Furthermore, you can combine the private memory concept into your developed Agent, enabling it to use those safe and effective solutions in different scenarios.