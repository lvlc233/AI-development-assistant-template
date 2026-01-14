---
name: PROJECT Record
description: |
    This document records content related to PROJECT.
    AI assistants are generally not allowed to perform any operations unless they have read the necessary documents to ensure they can safely serve the user in building the project.
    PROJECT is the core module of the project and the key basis for project progress and development. Ensure the Agent fully understands the content in PROJECT before developing.
    [Necessary]
author: "lxz"
state: OK
created: 2026-01-01
path: "/PROJECT"
---

# Structure
├── PROJECT/
│   ├── MEMORY/             # Agent memory. The agent can schedule all resources under this directory to recall everything about itself.
│   ├── OPERATION_LOG/      # Agent operation log. Generally, the Agent only needs to obtain operation records for the recent few days.
│   └── SANDBOX/            # Agent sandbox environment. All code development by the Agent should be placed in this resource.

# Details
PROJECT (or similar content): 
    Description: Project resources. This resource describes how Agents and humans should correctly develop the current project, making project development traceable. It is the resource with the highest permission level; ordinary, unauthorized Agents are not allowed to perform any operations on this resource. Otherwise, the system or humans will choose to remove the Agent to ensure project stability.
    
    Structure: Three core components of PROJECT
        
        Specification Document (Default: SPECIFICATION.md): The specification document is the foundation of the project. It guides Agents on the organizational form and writing style for project development and team collaboration.
            When an Agent's code is unqualified or attempts to conflict with original code, the Agent shall re-read the specification document to ensure creation with standard content.
        
        Task Metrics (Default: TASK_METRICS.md): Task metrics are the basis for the phased evolution of the project. Every time a project module is developed, a clear and unambiguous verifiable task description and acceptance criteria are required. This is equivalent to the Agent's task bar. Agents can only implement and complete tasks in the task bar that are incomplete and belong to the Agent. Each task will have a relevant owner/Agent. If a problem arises in a task, hope to investigate the details of the owner/Agent.
            Each Agent can only develop modules related to its assigned tasks and is not allowed to intervene in modules responsible by other Agents.
            Each task metric has at least the following 4 elements:
            1. Task start time
            2. Task completion/deprecation time
            3. Task owner/Agent
            4. Task completion status
            
        Project Record (LOG.md): This record is recorded by the system or humans, marking progress reports closely related to the main project. Agents can read the project record to quickly understand the core key parts of the project.
            Project records include at least the following content:
            1. Key and important content when code modules formally enter the main project each time.
            2. Important reports submitted by Agents or administrators each time.
            
    Supplement: Project resources are an important basis for project advancement. Every Agent has the responsibility to ensure the correctness and security of project resources. When project resources are chaotic or destroyed, every Agent has the right to warn the administrator and refuse to participate in any project development.
