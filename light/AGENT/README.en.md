---
name: Agent Work Constraints
description: |
    This document records the constraints for the AI assistant when building the project.
    The AI assistant is generally not allowed to perform any operations unless it has read the necessary documents to ensure it can safely serve the user in building the project.
    When the AI assistant forgets how to help humans build, it can also read this document.
    [Necessary]
author: "lxz"
state: OK
created: 2026-01-01
path: "/AGENT"
---

# Structure
├── AGENT/{Agent Name}/
│   ├── MEMORY.md             # Agent memory. The agent can schedule all resources under this directory to recall everything about itself.
│   └── LOG /                 # Agent operation log (recommended to use date as filename, e.g., /LOG/2026-01-01.md). Generally, the Agent only needs to obtain operation records for the recent few days.

# Details
AGENT: 
    Description: Agent resource, including Agent memory and operation records, to provide Agent cross-task ultra-long cycle project development support. Each Agent should independently maintain the code it is responsible for and cannot interfere with other Agents' code unless authorized. The environment the Agent belongs to is Agent Resource/AgentName/
    Structure: 
        Memory: (Default: AgentName/MEMORY.md): Memory is an important basis for the Agent to understand the project and adjust and learn itself. The Agent will enable a human-like attention screening mechanism.
            The Agent's memory includes at least the following content:
            1. Minimal project concepts and module relationships for its own understanding.
            2. Key corrections, reasons, and operations derived from reflection and actual feedback during the project.
            3. The Agent's self-understanding of project development and abstract concepts of core code.
        Check if memory needs to be updated every time an operation is completed or a task is about to be finished.

        Operation Log: (Default: AgentName/LOG/...\): This is the area where records must be generated when the Agent performs any operation (including but not limited to dialogue, task claiming, Agent thinking, code submission, environment modification...). After each Agent operation, relevant operation records should be left in this area to ensure Agent operation consistency.
            This is an important basis for the Agent to check its own environment and resources. On one hand, humans can trace code based on this; on the other hand, it also facilitates the Agent in discovering unreasonable places in its own data code.
            Operation logs include at least the following content:
            1. Operation Time: Default format is YYYY-MM-DD HH:MM
            2. Operation Content (Summary)
            3. Operation Goal
            4. Operation Result

    When performing any operation, the Agent must leave execution evidence in the designed documents or code. For example, clearly write the reason, result, and operator of each modification in the code.

    Supplement: Agent memory is an important basis for the Agent to continuously develop the project. Through the memory module, the Agent can minimize dependence on global code and reduce code retrieval times. When the Agent cannot independently complete relevant metrics, the Agent should contact the administrator for adjustment in time.
