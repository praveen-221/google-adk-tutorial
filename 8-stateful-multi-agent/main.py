import asyncio
import os

from dotenv import load_dotenv
from google.adk.sessions.in_memory_session_service import InMemorySessionService
from google.adk.runners import Runner
from utils import call_agent_async
from customer_service_agent.agent import customer_service_agent

async def main_async():
    """
        Main function to execute the session and agent
    """
    load_dotenv()
    APP_NAME = "Customer Service Agent"
    USER_NAME = "Harry Potter"

    inmemory_session_service = InMemorySessionService()

    initial_state = {
        "user_name": USER_NAME,
        "purchased_courses": [],
        "interaction_history": []
    }
    
    new_session = await inmemory_session_service.create_session(
        app_name = APP_NAME,
        user_id = USER_NAME,
        state = initial_state
    )
    SESSION_ID = new_session.id
    print(f"Created session with id: {SESSION_ID}")
    
    runner = Runner(
        app_name = APP_NAME,
        agent = customer_service_agent,
        session_service = inmemory_session_service
    )
    
    print(f"\nWelcome to Customer Service agent")
    print(f"Type 'exit' or 'quit' to end the conversation\n")
    
    while True:
        user_input = input(f"{USER_NAME}: ")

        if user_input.strip().lower() in ["exit", "quit"]:
            print(f"Ending the support session with id: {SESSION_ID}")
            break

        await call_agent_async(runner, user_input, SESSION_ID, USER_NAME)        

    return

def main():
    # call async function which is the entry point for application
    asyncio.run(main_async())

if __name__ == "__main__":
    main()