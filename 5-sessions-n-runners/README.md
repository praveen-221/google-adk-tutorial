# Sessions and State Management in ADK

## What Are Sessions in ADK?

Sessions in ADK provide a way to:

1. **Maintain State**: Store and access user data, preferences, and other information between interactions
2. **Track Conversation History**: Automatically record and retrieve message history
3. **Personalize Responses**: Use stored information to create more contextual and personalized agent experiences

Unlike simple conversational agents that forget previous interactions, stateful agents can build relationships with users over time by remembering important details and preferences.

## Project Structure

```
5-sessions-n-runners/
│
├── stateful_session.py      # Main example script
├── .env                     # Environment variables
│
└── question_answering_agent/      # Agent implementation
    ├── __init__.py
    └── agent.py                   # Agent definition with template variables
```

## Key Components

### Session Service

The example uses the `InMemorySessionService` which stores sessions in memory:

```python
session_service = InMemorySessionService()
```

### Initial State

A state is a dictionary with key value pairs
Sessions are created with an initial state containing user information:

```python
initial_state = {
    "key 1": "value 1",
    "key 2": """
        value 2
    """,
}
```

### Creating a Session

The example creates a session with a unique identifier:

```python
stateful_session = session_service.create_session(
    app_name=APP_NAME,
    user_id=USER_ID,
    session_id=SESSION_ID,
    state=initial_state,
)
```

### Accessing State in Agent Instructions

The agent accesses session state using template variables in its instructions:

```python
instruction="""
You are a helpful assistant that answers questions about the user's preferences.

Here is some information about the user:
Name: 
{user_name}
Preferences: 
{user_preferences}
"""
```

### Running with Sessions

Sessions are integrated with the `Runner` to maintain state between interactions:

```python
runner = Runner(
    agent=agent-folder-name,
    app_name=APP_NAME,
    session_service=session_service,
)
```

## Additional Resources

- [Google ADK Sessions Documentation](https://google.github.io/adk-docs/sessions/session/)
- [State Management in ADK](https://google.github.io/adk-docs/sessions/state/)