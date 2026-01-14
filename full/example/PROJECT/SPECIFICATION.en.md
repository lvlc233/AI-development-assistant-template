# Project Specification Document
## Introduction
This is a Langgraph-based DeepAgent project. The project aims to utilize powerful Agent orchestration, context engineering, and resource management technologies to provide better Agent services for any researcher, reducing the mental burden during the research and development process, allowing them to fully devote themselves to valuable content output.

## Project Architecture
### Backend
1. 3+1 Layer Architecture:
    - Controller Layer:
        1. Responsible for encapsulating service layer data to web layer data.
        2. Responsible for permission-related processing.
        3. This layer is also responsible for defining request-related data models.
    - Service Layer:
        1. Responsible for core data synthesis.
        2. Responsible for scheduling the infrastructure layer: including redis, sql, neo4j, etc.
    - Infrastructure Layer:
        1. Provides encapsulation of operation statements for related infrastructure.
    - Data Layer:
        1. This layer only stores data models and does not perform any logical processing.
        2. Data models in the data layer should be constructed starting from business logic and assembled by the service layer.

2. Security
    - Use PyJWT for authentication.
3. All data models in the web layer uniformly use Pydantic instead of TypeDict.
4. Use fastApi's container to manage thread resources and inject thread information.

### Agent:
Definition: In this project, an Agent refers to an independent compiled graph.
#### State
1. Any state uniformly uses TypeDict as the base class, not dataclass or BaseModel.
2. Any state should retain at least two fields:
    "messages": This field is used for user-facing historical information recording. In any case, the Agent's context should not directly use any data in messages unless it is processed or stored in other fields.
    "context": This field is used for Agent-facing context information, including but not limited to historical interaction records. This field is usually not content that users can directly query.
3. All Messages must be wrapped using langchain's Messages class and cannot use dictionaries {"role":"","message":""} directly.
4. The meaning, function, and scope of use of all fields in the state must be noted.
5. When the state uses a reduction function (characterized by fields marked with Annotated[type,func]), then when processing the state...
6. When a field needs to change during runtime, it should be a state, such as messages.

#### Tools
1. All tools should be as functionally cohesive as possible, and provide clear tool scheduling timing, parameter details, expected return structures, and potential exception information.
2. When tool information needs to update the state, use Command to wrap the return value of the tool, and when updating the field, it must carry at least {"messages": ToolMessages("Tool scheduled message {custom}", tool_call_id=tool_call_id)}.
3. tool_call_id is obtained through node injection runtime: ToolRuntime, runtime.tool_call_id.
4. Regardless of the specific logic, all tools must at least update the context state of the model upon return and pass in the call result of the information tool.
5. All tools must consider exception capturing and context handling during exceptions.

#### Model Context
1. All contexts must carry time information.
2. The encapsulation of context data must be dynamically assembled at the node scheduling the model. All non-natural language data structures (such as classes, etc.) must be converted into natural language or context information with data format (such as .md...).
3. When context data carries fields, the meaning of the fields should be explained in all cases before passing into the context.
4. When there are conversation history records in the context, the messages must be clearly distinguished as User: "" | Time, Agent_name: "" | Time.
5. All contexts must clarify what the current processing Agent is and what the task is.

#### Static Context & Config Configuration
1. All static contexts can only use serializable data models, and non-serializable data should not be stored in static contexts, for example: client_session_id: ok, client: can't.
2. If a non-serializable instance needs to be passed into a node or tool, it should be injected and obtained using config.
3. When a field does not need to change during runtime, it should be a static context: such as user_id.

#### Memory
1. The long-term memory part of the Agent is obtained by store injection of the node.

#### Nodes
1. All nodes use dictionaries to update required state fields when returning, rather than returning a state object.
2. All nodes must consider exception capturing and context handling during exceptions.
3. When using Command for node jumping, Literal[...] must be used to constrain the target node. Set ends in add_node to assist mermaid chart generation.

#### Output
1. The output of the graph uses astream to listen for events.
2. Listen-able types are: token, tool, and custom.
3. Use `from langgraph.config import get_stream_writer` to get the writer for custom event writing.

#### Human Intervention
When there is logic requiring human intervention, such as content review, external state injection, perform the following analysis:
1. Strong Human Intervention: When graph data must be input or confirmed by Human before proceeding to subsequent processes, use the interrupt function to throw an interruption. Note that after langgraph interruption recovery, it will re-execute from the node instead of continuing from the interrupt function.
2. Strong Human Intervention requires returning relevant statement prompts, and the receiving end must include at least one user input content for humans to perform natural language task orchestration.
3. Weak Human Intervention: Data requiring human intervention does not affect the normal operation of the graph, such as some to-do items, todo lists. When using, do not interrupt based on the interrupt function, but establish a to-do item pipeline in the state. Users can update pipeline data through Command operations. Thus performing human intervention.

#### Testing
Agent testing content includes 3 parts, and is based on nodes and tools.
1. Single Node or Tool Functional Testing:
Use pytest to test the input and output of the node, use mock data to verify the input data, output data, and internal data state of the node, making it completely conform to the function and implementation description within the node.
2. Model Testing:
- When a node contains an LLM, model testing should be performed on it. Need to analyze the potential context state in the node content, create possible context data (including tool results), and perform actual LLM calls on different context data to ensure its final actual output result conforms to the rough expectation.
- In model testing, all data that needs to be obtained and converted into context can be mocked, but the output of the model cannot be mocked.
- Use langfuse for link tracing.
- When generating potential contexts, mark test nodes, test content, expected results. And encapsulate it as part of the dataset.
- Model testing includes functional testing and specification testing: Specification testing means the model needs to output data structures conforming to the actual description, which can usually be judged using assertions. Functional testing refers to whether the output of the model ultimately meets requirements, such as instruction following degree, anti-interference degree, usually scored by a review Agent or human.
3. Cascade Testing:
- Based on the actual possible interaction process, perform comprehensive testing of the Agent with non-mock data.
- Need to create datasets.
- Use langfuse for link tracing.

### Frontend
1. Use config to specifically handle configuration items such as url connections.
2. Use specialized service for backend data connection and data conversion.
TODO: Unfamiliar with frontend content, need certain research.
