# Project Specification Document
Below is the recommended content

## Project Introduction
What does this project do? For example, rapid prototype development, large-scale project setup, or analysis and introduction from a product perspective. Anything is fine. The goal is to let administrators and Agents quickly understand the purpose of this project.

## Project Architecture
Includes frontend and backend components, communication protocols, concept definitions, etc. (Mainly for definitions, recommended to be solely responsible by the administrator.)

## Technology Overview (Optional but Recommended)
Declare the technology stack selection and reasons for the entire project. Including but not limited to frontend frameworks, backend frameworks, databases. Provide the overall main technology line. Let Agents have a reference when responsible for sub-component technology selection. (Selection needs to be based on this technology overview.)

Finally, declare what the role of each technology is? Mainly to let administrators quickly understand.

Agents internally will also be responsible for a technical document, but that document will be more detailed because the level targeted is component-level.

It is recommended to choose to merge technology selections when the project is completed, but try not to update the technology selection here while proceeding.

## Code Implementation Standards
Including but not limited to:
- Code Style
- Code Comments
- Code Structure
- ...

A reference

1. All functional modules should use logging.
2. All code modules must record complete logs.
3. Set the time zone to China Shanghai.
4. When a non-business logic function or similar logic is built more than 3 times, it should be considered for merging into a common utility, such as getting the current China time zone time.
5. All data in the project must be annotated with its return data type.
6. A function must remain in TODO status until it has passed test verification.
7. Use of any mock data to temporarily replace code logic is prohibited. If clearer logic is needed, use TODO to mark the position and attach requirements.
8. Everyone writing code must attach comments in the following data format, otherwise it will be considered non-compliant:
    '''
    Developer: agent_name/ human_name
    Current Version: Any unique marker in this module
    Created Time: Use YYYY-MM-DD HH:MM format, Agent uses Time tool to get current time
    Update Time: Use YYYY-MM-DD HH:MM format, Agent uses Time tool to get current time
    Update Record: 
        [Dev Time:Dev Version: Briefly describe input, output, effect, implementation in one sentence, where can it be used?]
    '''
9. If a module is intended to be deprecated, use the deprecated annotation flag, and submit a deprecation application record for MasterAgent or human review.
10. Backend projects always use modular imports instead of relative imports. If the module content is unclear, check the pyproject.toml file.

## Code Structure
