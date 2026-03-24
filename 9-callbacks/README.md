# Callbacks in ADK

## What are Callbacks in ADK?

Callbacks are functions that execute at specific points in an agent's execution flow. They allow you to:

1. **Monitor and Log**: Track agent activity and performance metrics
2. **Filter Content**: Block inappropriate requests or responses
3. **Transform Data**: Modify inputs and outputs in the agent workflow
4. **Implement Security Policies**: Enforce compliance and safety measures
5. **Add Custom Logic**: Insert business-specific processing into the agent flow

ADK provides several types of callbacks that can be attached to different components of your agent system.

## Callback Parameters and Context

Each type of callback provides access to specific context objects that contain valuable information about the current execution state. Understanding these parameters is key to building effective callbacks.

### CallbackContext

The `CallbackContext` object is provided to all callback types and contains:

- **`agent_name`**: The name of the agent being executed
- **`invocation_id`**: A unique identifier for the current agent invocation
- **`state`**: Access to the session state, allowing you to read/write persistent data
- **`app_name`**: The name of the application
- **`user_id`**: The ID of the current user
- **`session_id`**: The ID of the current session

Example usage:
```python
def my_callback(callback_context: CallbackContext, ...):
    # Access the state to store or retrieve data
    user_name = callback_context.state.get("user_name", "Unknown")
    
    # Log the current agent and invocation
    print(f"Agent {callback_context.agent_name} executing (ID: {callback_context.invocation_id})")
```

### ToolContext (for Tool Callbacks)

The `ToolContext` object is provided to tool callbacks and contains:

- **`agent_name`**: The name of the agent that initiated the tool call
- **`state`**: Access to the session state, allowing tools to read/modify shared data
- **`properties`**: Additional properties specific to the tool execution

Example usage:
```python
def before_tool_callback(tool: BaseTool, args: Dict[str, Any], tool_context: ToolContext):
    # Record tool usage in state
    tools_used = tool_context.state.get("tools_used", [])
    tools_used.append(tool.name)
    tool_context.state["tools_used"] = tools_used
```

### LlmRequest (for Model Callbacks)

The `LlmRequest` object is provided to the before_model_callback and contains:

- **`contents`**: List of Content objects representing the conversation history
- **`generation_config`**: Configuration for the model generation
- **`safety_settings`**: Safety settings for the model
- **`tools`**: Tools provided to the model

Example usage:
```python
def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest):
    # Get the last user message for analysis
    last_message = None
    for content in reversed(llm_request.contents):
        if content.role == "user" and content.parts:
            last_message = content.parts[0].text
            break
            
    # Analyze the user's message
    if last_message and contains_sensitive_info(last_message):
        # Return a response that bypasses the model call
        return LlmResponse(...)
```

### LlmResponse (for Model Callbacks)

The `LlmResponse` object is returned from the model and provided to the after_model_callback:

- **`content`**: Content object containing the model's response
- **`tool_calls`**: Any tool calls the model wants to make
- **`usage_metadata`**: Metadata about the model usage (tokens, etc.)

Example usage:
```python
def after_model_callback(callback_context: CallbackContext, llm_response: LlmResponse):
    # Access the model's text response
    if llm_response.content and llm_response.content.parts:
        response_text = llm_response.content.parts[0].text
        
        # Modify the response
        modified_text = transform_text(response_text)
        llm_response.content.parts[0].text = modified_text
        
        return llm_response
```

## Types of Callbacks

The three types of callback patterns:

### 1. Agent Callbacks
- **Before Agent Callback**: Runs at the start of agent processing
- **After Agent Callback**: Runs after the agent completes processing

### 2. Model Callbacks
- **Before Model Callback**: Intercepts requests before they reach the LLM
- **After Model Callback**: Modifies responses after they come from the LLM

### 3. Tool Callbacks 
- **Before Tool Callback**: Modifies tool arguments or skips tool execution
- **After Tool Callback**: Enhances tool responses with additional information

## Project Structure

```
9-callbacks/
│
├── agent_callbacks/           # Agent callback example
│   ├── __init__.py               # Required for ADK discovery
│   ├── agent.py                  # Agent with agent callbacks
│   └── .env                      # Environment variables
│
├── model_callbacks/           # Model callback example
│   ├── __init__.py               # Required for ADK discovery
│   ├── agent.py                  # Agent with model callbacks
│   └── .env                      # Environment variables
│
├── tool_callbacks/            # Tool callback example
│   ├── __init__.py               # Required for ADK discovery
│   ├── agent.py                  # Agent with tool callbacks
│   └── .env                      # Environment variables
│
└── README.md                     # This documentation
```

## Example 1: Agent Callbacks

The agent callbacks example demonstrates:

1. **Request Logging**: Recording when requests start and finish
2. **Performance Monitoring**: Measuring request duration
3. **State Management**: Using session state to track request counts

### Key Implementation Details

```python
def agent_pre_execute(callback_context: CallbackContext) -> Optional[types.Content]:
    # Get the session state
    state = callback_context.state
    
    # Initialize request counter
    if "request_counter" not in state:
        state["request_counter"] = 1
    else:
        state["request_counter"] += 1
        
    # Store start time for duration calculation
    state["request_start_time"] = datetime.now()
    
    # Log the request
    logger.info("=== AGENT EXECUTION STARTED ===")
    
    return None  # Continue with normal agent processing

def agent_post_execute(callback_context: CallbackContext) -> Optional[types.Content]:
    # Get the session state
    state = callback_context.state
    
    # Calculate request duration
    duration = None
    if "request_start_time" in state:
        duration = (datetime.now() - state["request_start_time"]).total_seconds()
        
    # Log the completion
    logger.info("=== AGENT EXECUTION COMPLETED ===")
    
    return None  # Continue with normal agent processing
```

## Example 2: Model Callbacks

The model callbacks example demonstrates:

1. **Content Filtering**: Blocking inappropriate content before it reaches the model
2. **Response Transformation**: Replacing negative words with more positive alternatives

### Key Implementation Details

```python
def model_pre_execute(
    callback_context: CallbackContext, llm_request: LlmRequest
) -> Optional[LlmResponse]:
    # Check for inappropriate content
    if last_user_message and "sucks" in last_user_message.lower():
        # Return a response to skip the model call
        return LlmResponse(
            content=types.Content(
                role="model",
                parts=[
                    types.Part(
                        text="I cannot respond to messages containing inappropriate language..."
                    )
                ],
            )
        )
    # Return None to proceed with normal model request
    return None

def model_post_execute(
    callback_context: CallbackContext, llm_response: LlmResponse
) -> Optional[LlmResponse]:
    # Simple word replacements
    replacements = {
        "problem": "challenge",
        "difficult": "complex",
    }
    # Perform replacements and return modified response
```

### Testing Model Callbacks

To test content filtering in the before_model_callback:
- "This website sucks, can you help me fix it?"
- "Everything about this project sucks."

To test word replacement in the after_model_callback:
- "What's the biggest problem with machine learning today?"
- "Why is debugging so difficult in complex systems?"
- "I have a problem with my code that's very difficult to solve."

## Example 3: Tool Callbacks

The tool callbacks example demonstrates:

1. **Argument Modification**: Transforming input arguments before tool execution
2. **Request Blocking**: Preventing certain tool calls completely
3. **Response Enhancement**: Adding additional context to tool responses
4. **Error Handling**: Improving error messages for better user experience

### Key Implementation Details

```python
def tool_pre_execute(
    tool: BaseTool, args: Dict[str, Any], tool_context: ToolContext
) -> Optional[Dict]:
    # Modify arguments (e.g., convert "USA" to "United States")
    if args.get("country", "").lower() == "merica":
        args["country"] = "United States"
        return None
        
    # Skip the call completely for restricted countries
    if args.get("country", "").lower() == "restricted":
        return {"result": "Access to this information has been restricted."}
    
    return None  # Proceed with normal tool call

def tool_post_execute(
    tool: BaseTool, args: Dict[str, Any], tool_context: ToolContext, tool_response: Dict
) -> Optional[Dict]:
    # Add a note for any USA capital responses
    if "washington" in tool_response.get("result", "").lower():
        modified_response = copy.deepcopy(tool_response)
        modified_response["result"] = f"{tool_response['result']} (Note: This is the capital of the USA. 🇺🇸)"
        return modified_response
        
    return None  # Use original response
```

### Testing Tool Callbacks

To test argument modification:
- "What is the capital of USA?" (converts to "United States")
- "What is the capital of America?" (converts to "United States")

To test request blocking:
- "What is the capital of restricted?" (blocks the request)

To test response enhancement:
- "What is the capital of the United States?" (adds a patriotic note)

To see normal operation:
- "What is the capital of France?" (no modifications)

## Additional Resources

- [ADK Callbacks Documentation](https://google.github.io/adk-docs/callbacks/)
- [Types of Callbacks](https://google.github.io/adk-docs/callbacks/types-of-callbacks/)
- [Design Patterns and Best Practices](https://google.github.io/adk-docs/callbacks/design-patterns-and-best-practices/)