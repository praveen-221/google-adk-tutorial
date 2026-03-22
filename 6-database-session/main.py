import asyncio
import os
from dotenv import load_dotenv
from google.adk.sessions.database_session_service import DatabaseSessionService
from google.adk.runners import Runner
from todo_agent.agent import todo_agent
from utils import call_agent_async

async def main():
    """
        Main function to execute the session and agent
    """
    load_dotenv()
    APP_NAME = "To Do Agent"
    USER_NAME = "Harry Potter"

    DB_URL = "sqlite+aiosqlite:///./session_data.db"
    db_session_service = DatabaseSessionService(db_url = DB_URL)

    initial_state = {
        "user_name": USER_NAME,
        "todo_list": []
    }

    # Check if there are any session stored for the user 
    existing_sessions = await db_session_service.list_sessions(
        app_name = APP_NAME,
        user_id = USER_NAME
    )
    
    if existing_sessions and len(existing_sessions.sessions) > 0:
        # use the top most session
        SESSION_ID = existing_sessions.sessions[0].id
        print(f"Found existing session with id: {SESSION_ID}")
    else:
        new_session = await db_session_service.create_session(
            app_name = APP_NAME,
            user_id = USER_NAME,
            state = initial_state
        )
        SESSION_ID = new_session.id
        print(f"Created session with id: {SESSION_ID}")
    
    runner = Runner(
        app_name = APP_NAME,
        agent = todo_agent,
        session_service = db_session_service
    )
    
    print(f"\nWelcome to To Do agent")
    print(f"Your to-dos will be persisited across conversations")
    print(f"Type 'exit' or 'quit' to end the conversation\n")
    
    while True:
        user_input = input(f"{USER_NAME}: ")

        if user_input.strip().lower() in ["exit", "quit"]:
            print(f"Ending the conversation with id: {SESSION_ID}, session data is stored in database")
            break

        await call_agent_async(runner, user_input, SESSION_ID, USER_NAME)        

    return

if __name__ == "__main__":
    asyncio.run(main())