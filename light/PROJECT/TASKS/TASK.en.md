
# This is a template

# Introduction
Supplement or description regarding a specific task in the project. Generally, indicating which Agent this belongs to is sufficient. You can add custom extension details here. Agent-specific TASKS are similar.

## Task Status Legend
- 🔴 **Pending**: Pending
- 🟡 **In Progress**: In Progress
- 🟢 **Completed**: Completed
- ⚪ **Depreciated**: Deprecated
- 🔵 **Review & Rework**: Review or Rework

## Task List

| ID | Module | Task Description | Owner | Status | Start Time | End Time | Acceptance Criteria | Related Tasks & Relations | Details |
| T-J001 | JavaBackend | Initialize Java Backend Project Structure | JavaBackendAgent | 🔴 | | | Complete Maven/Gradle project initialization, integrate MyBatis-Flex, Redis, Disruptor | | Tech stack must strictly follow Agent specifications |
| T-ASJ001 | AgentScopeJava | Initialize AgentScope Java Project Structure | AgentScopeJavaAgent | 🔴 | | | Complete Gradle/Maven configuration, integrate AgentScope Java SDK | | |
| T-ASP001 | AgentScopePython | Initialize AgentScope Python Project Structure | AgentScopePythonAgent | 🔴 | | | Complete Python environment configuration, install agentscope library, run Demo | | |


## Example
| ID | Module | Task Description | Owner | Status | Start Time | End Time | Acceptance Criteria | Related Tasks & Relations | Details |
| T-001 | Backend | Design and implementation of backend collection module | BackendAgent | 🟡 | 2026-01-01 16:51 |  | Complete all data models and logic code, pass unit tests based on design draft scenarios, and finally generate modular documentation for each layer |  | From database table design to service aggregation and controller integration, must comply with specification document and maintain consistency with other code styles |
| T-002 | Backend | Design database table structure according to project requirements and scenarios | BackendAgent | 🟢 | 2026-01-01 16:51 | 2026-01-01 16:55 | Complete PG Entity code for search module, verify basic CRUD execution, and generate documentation | T-001(Parent) | |
| T-003 | Backend | Complete Service for business scenarios and other related support layer functions | BackendAgent | 🔵 | 2026-01-01 16:55 | 2026-01-01 16:59 | Complete related code, unit tests, documentation | T-001(Parent), T-002(Dependency) | |
| T-003 | Backend | Complete Controller layer code for business scenarios and add permission verification | BackendAgent | 🔴 | | | Complete related code, unit tests, documentation | T-001(Parent), T-003(Dependency) | |
| T-004 | Backend | Acceptance and final documentation generation | BackendAgent | 🔴 | | | Complete cascade testing, generate documentation | T-001(Parent), Final | |
 

## Common Task Types.
