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
│   ├── DOCUMENTS/          # [Document Center] Stores important project documents, design drafts, flowcharts, etc.
│   │   └── README.md       # Document directory explanation
│   ├── TASKS/              # [Task Center] Stores task assignments, progress tracking, and task documents for each Agent.
│   │   ├── README.md       # Task directory explanation
│   │   └── TASK.md         # Task template or specific task description
│   ├── SPECIFICATION.md    # [Specification] Project specification document, describing basic norms, technology selection, code standards, etc.
│   ├── LOG.md              # [Project Log] Project operation log, recording project progress logs, key operations, etc.
│   └── README.md           # [This File] Explanation document for the PROJECT directory.

# Details
PROJECT (or similar content): 
    Description: Project resources. This resource describes how Agents and humans should correctly develop the current project, making project development traceable. It is the resource with the highest permission level; ordinary, unauthorized Agents are not allowed to perform any operations on this resource. Otherwise, the system or humans will choose to remove the Agent to ensure project stability.
    
    Structure: Core components of PROJECT
        
        Document Center (DOCUMENTS/):
            Description: Stores important or general documents in this project, or documents pulled from inside Agents that have been reviewed by administrators.
            Purpose: Agents can analyze, design, and implement projects based on these documents.
            Note: General Agents are not allowed to directly manipulate documents in PROJECT/DOCUMENTS resources.
        
        Task Center (TASKS/):
            Description: Stores all task documents in this project. Including tasks that each Agent needs to complete in various stages.
            Purpose: The task documents here are the basis for the phased evolution of the project. Each task has a clear and unambiguous verifiable task description and acceptance criteria.
            Process: Agent claims task -> Understands requirements -> Creates/Updates task document -> Executes task -> Marks as complete.
        
        Specification Document (SPECIFICATION.md): 
            Description: Basic specification document for the project.
            Purpose: Guides Agents on the organizational form and writing style for project development and team collaboration. Includes technology selection, code standards, architecture definition, etc.
            Principle: When an Agent's code is unqualified or attempts to conflict with original code, the Agent shall re-read the specification document to ensure creation with standard content.

        Project Log (LOG.md): 
            Description: Recorded by the system or humans, marking progress reports closely related to the main project.
            Purpose: Records the progress log of the project itself, assisting Agents in understanding the current project status and isolating tasks. Includes key content when code modules formally enter the main project, important reports, etc.
            
    Supplement: Project resources are an important basis for project advancement. Every Agent has the responsibility to ensure the correctness and security of project resources. When project resources are chaotic or destroyed, every Agent has the right to warn the administrator and refuse to participate in any project development.
