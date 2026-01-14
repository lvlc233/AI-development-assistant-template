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
│   ├── MEMORY/             # Agent memory. The agent can schedule all resources under this directory to recall everything about itself.
│   ├── OPERATION_LOG/      # Agent operation log. Generally, the Agent only needs to obtain operation records for the recent few days.
│   └── SANDBOX/            # Agent sandbox environment. All code development by the Agent should be placed in this resource.

# Details
AGENT (or similar content): 
    Description: Agent resource, including Agent memory, operation records, and safe sandbox environment, to provide Agent cross-task ultra-long cycle project development support. Each Agent should independently maintain the environment it is in. The environment the Agent belongs to is Agent Resource/AgentName/
    Structure: 
        Memory: (Default: Agent_name/MEMORY.md): Memory is an important basis for the Agent to understand the project and adjust and learn itself. The Agent will enable a human-like attention screening mechanism.
            The Agent's memory includes at least the following content:
            1. Minimal project concepts and module relationships for its own understanding.
            2. Key corrections, reasons, and operations derived from reflection and actual feedback during the project.
            3. The Agent's self-understanding of project development and abstract concepts of core code.

        Operation Log: (Default: Agent_name/OPERATION_LOG): This is the area where records must be generated when the Agent performs any operation (including but not limited to dialogue, task claiming, Agent thinking, code submission, environment modification...). After each Agent operation, relevant operation records should be left in this area to ensure Agent operation consistency.
            This is an important basis for the Agent to check its own environment and resources. On one hand, humans can trace code based on this; on the other hand, it also facilitates the Agent in discovering unreasonable places in its own data code.
            Operation logs include at least the following content:
            1. Operation Time
            2. Operation Content (Summary)
            3. Operation Goal
            4. Operation Result

        Sandbox Environment: (Default: Agent_name/SANDBOX): This is generally the main operation environment for Agents. This sandbox is often a mirror resource of the main project. Agents can develop any code in the sandbox environment.
            Acquisition of Sandbox Environment: Sandbox environments are often pulled by Agents from the main environment as needed. Agents do not pull parts unrelated to development to maintain code cleanliness. Or humans manually assign code to the sandbox environment. However, note that every time the main environment code is acquired, the sandbox environment will always be reset to the most primitive state to maintain the cleanliness of the sandbox environment. When the Agent wants to retain data, please move relevant data outside the sandbox environment.
            Code Submission: Agents can and can only submit code from the sandbox environment to the main project, and every time the Agent submits, it must check the submitted code to ensure the existence of remark information and provide a piece of code information involved in this submission.
            
    Supplement: Agent memory is an important basis for the Agent to continuously develop the project. Through the memory module, the Agent can minimize dependence on global code and reduce code retrieval times. When the Agent cannot independently complete relevant metrics, the Agent should contact the administrator for adjustment in time.
