# Persistent Storage in ADK

Persistent storage allows ADK agents to remember information and maintain conversation history across multiple sessions, application restarts, and even server deployments.

## What is Persistent Storage in ADK?

In `InMemorySessionService` which stores session data only in memory - this data is lost when the application stops. For real-world applications, you'll often need your agents to remember user information and conversation history long-term. This is where persistent storage comes in.

ADK provides the `DatabaseSessionService` that allows you to store session data in a SQL database, ensuring:

1. **Long-term Memory**: Information persists across application restarts
2. **Consistent User Experiences**: Users can continue conversations where they left off
3. **Multi-user Support**: Different users' data remains separate and secure
4. **Scalability**: Works with production databases for high-scale deployments


## Project Structure

```
5-database-session/
│
├── todo_agent/               # Agent package
│   ├── __init__.py             # Required for ADK to discover the agent
│   └── agent.py                # Agent definition with reminder tools
│
├── main.py                     # Application entry point with database session setup
├── utils.py                    # Utility functions for terminal UI and agent interaction
├── .env                        # Environment variables
├── session_data.db            # SQLite database file (created when first run)
└── README.md                   # This documentation
```

## Key Components

### 1. DatabaseSessionService

The core component that provides persistence is the `DatabaseSessionService`, which is initialized with a database URL:

```python
from google.adk.sessions import DatabaseSessionService

db_url = "sqlite:///./session_data.db"
session_service = DatabaseSessionService(db_url=db_url)
```

This service allows ADK to:
- Store session data in a SQLite database file
- Retrieve previous sessions for a user
- Automatically manage database schemas

### 2. Session Management

The example demonstrates proper session management:

```python
# Check for existing sessions for this user
existing_sessions = session_service.list_sessions(
    app_name=APP_NAME,
    user_id=USER_ID,
)

# If there's an existing session, use it, otherwise create a new one
if existing_sessions and len(existing_sessions.sessions) > 0:
    # Use the most recent session
    SESSION_ID = existing_sessions.sessions[0].id
    print(f"Continuing existing session: {SESSION_ID}")
else:
    # Create a new session with initial state
    session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
        state=initialize_state(),
    )
```

### 3. State Management with Tools

The agent includes tools that update the persistent state:

```python
def add_reminder(reminder: str, tool_context: ToolContext) -> dict:
    # Get current reminders from state
    reminders = tool_context.state.get("reminders", [])
    
    # Add the new reminder
    reminders.append(reminder)
    
    # Update state with the new list of reminders
    tool_context.state["reminders"] = reminders
    
    return {
        "action": "add_reminder",
        "reminder": reminder,
        "message": f"Added reminder: {reminder}",
    }
```

Each change to `tool_context.state` is automatically saved to the database.

### Running the code

To run the code:

```bash
python main.py
```

This will:
1. Connect to the SQLite database (or create it if it doesn't exist)
2. Check for previous sessions for the user
3. Start a conversation with the memory agent
4. Save all interactions to the database

## Using Database Storage in Production

`DatabaseSessionService` supports various database backends through SQLAlchemy:

- PostgreSQL: `postgresql://user:password@localhost/dbname`
- MySQL: `mysql://user:password@localhost/dbname`
- MS SQL Server: `mssql://user:password@localhost/dbname`

## Additional Resources

- [ADK Sessions Documentation](https://google.github.io/adk-docs/sessions/session/)
- [Session Service Implementations](https://google.github.io/adk-docs/sessions/session/#sessionservice-implementations)
- [State Management in ADK](https://google.github.io/adk-docs/sessions/state/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/) for advanced database configuration 