import os
import uuid
import asyncio
from dotenv import load_dotenv
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types
from qna_agent import qna_agent

load_dotenv()
inMemory_session_service = InMemorySessionService()
APP_NAME = "Harry Potter QnA bot"

# creating a runner [agents + session]
runner = Runner(
    app_name = APP_NAME,
    agent = qna_agent,
    session_service = inMemory_session_service
)

# Helper method to send query to the runner
async def call_agent(query, session_id, user_id):
    # create the message to the agent
    content = types.Content(role='user', parts=[types.Part(text=query)])

    async for event in runner.run_async(
        user_id=user_id, 
        session_id=session_id,
        new_message=content
    ):
        if event.is_final_response():
            if event.content and event.content.parts:
                final_response = event.content.parts[0].text
                print("Agent Response: ", final_response)

    return


# main function to create the session adn call the agent
async def main(): 
    initial_state = {
        "user_name": "Harry Potter",
        "user_details": """
            1. Student at Hogwarts magical school
            2. Interested in magic and potions
            3. Hang out with Ron and Hermione 
            4. Part of Gryffindor house 
            5. Won the Goblet of fire competition
        """
    }

    # Creating a new session
    USER_ID = "Harry Potter"
    SESSION_ID = str(uuid.uuid4())

    stateful_session = await inMemory_session_service.create_session(
        app_name = APP_NAME,
        user_id = USER_ID,
        session_id = SESSION_ID,
        state = initial_state
    )

    print(f"In Memory session [session id: {SESSION_ID}] created with the following state: ")
    session = await inMemory_session_service.get_session(
        app_name = APP_NAME, user_id = USER_ID, session_id = SESSION_ID
    )

    # for key, value in session.state.items():
    #     print(f"{key}: {value}")

    await call_agent(
        query = "Which competition did he win ?",
        session_id = SESSION_ID,
        user_id = USER_ID
    )

if __name__ == "__main__":
   asyncio.run(main())