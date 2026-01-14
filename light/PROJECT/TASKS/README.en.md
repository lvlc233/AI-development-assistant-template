---
name: TASKS
description: |
    In the TASK resource, Agent task documents are stored. Generally, each Agent will have its own unique task document. The task document name is usually {AgentName}_TASKS.md.
    There are also cases where a TASKS.md file exists in the project, where TASK tasks are more general. Priority is lower.
author: "lxz"
state: OK
created: 2026-01-01
path: "/PROJECT"
---
# Introduction
The TASKS resource stores all task documents in this project. Including tasks that each Agent needs to complete in various stages. It is recommended that an Agent claims one task at a time, and claims the next task after updating the completion status to ensure project progress. When claiming a task, the Agent needs to first understand the task requirements and create a corresponding task document. The task document records the initial state of project-related tasks at the start of the task, accumulates the execution status during the task execution, and marks the task status as completed upon completion.

If the task is a subtask of another task, the requirements, progress, and completion status of the subtask can be directly described in the parent task.

For specific task formats, refer to the respective Agent's task document format.
Task documents generally contain the following content:
- Task requirement description
- Task completion status
- Task creation time
- Task update time
- Subtasks (if any)
- Task owner (usually the Agent, used to distinguish TASKS and identify if the Agent is the person in charge of the task)
- Output requirements (Recommended)
