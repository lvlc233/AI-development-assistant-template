---
name: SUBMISSION Record
description: |
    This document records content related to SUBMISSION.
    AI assistants are generally not allowed to perform any operations unless they have read the necessary documents to ensure they can safely serve the user in building the project.
    SUBMISSION is the intermediate transition environment for the main project and various Agent developments. If an Agent needs to upload code, it needs to upload the code to this directory. Awaiting review.
    [Necessary]
author: "lxz"
state: OK
created: 2026-01-01
path: "/SUBMISSION"
---

# Structure
├── SUBMISSION/

# Details
    Description: Pending submission resource. This is the intermediate zone between Agent development code and the main project. Code confirmed by the Agent will be cached in this area. For human review or administrator Agent review.
    Structure:
        Agent_name/Code Package: This is the code submitted by the Agent.
        Agent_name/commit.log: This is the Agent's submission log.
    Supplement:
        Administrator related content:
            Administrator usually refers to humans or Agents granted administrator status. Administrators have the authority to operate files in the main project, but when an administrator Agent operates on non-record modules (i.e., code) in the main project, it must be approved by humans. Administrators can record record-class modules in the main project.
            Administrator Agents generally need to have the following functions:
                1. Code Review: Administrator Agents often need to have a sufficient understanding of the entire project, and when reviewing submitted code each time, they can score and provide feedback on the code based on the materials in PROJECT. The content of the feedback will be directly written in the corresponding operation log of each Agent.
                2. Conflict Reporting: When the administrator Agent discovers that there is a conflict in the Agent code in the submission area, the administrator Agent will inform the conflicting Agents, return the relevant code, and inform the respective Agents where the parts that should be resolved are, thereby reducing the situation of writing duplicate modules.
                3. Code Approval and Rejection: The administrator Agent can pass the submitted code, remove the code from the submission area, update the corresponding area of the main project, and update the version. When rejecting, remove the code from the submission area and inform the Agent where modifications are needed.
                4. Generally, administrators do not directly participate in code writing.
