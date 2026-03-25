from datetime import datetime
from typing import Optional

from google.adk.agents import LlmAgent
from google.genai import types
from google.adk.agents.callback_context import CallbackContext

def agent_pre_execute(callback_context: CallbackContext) -> Optional[types.Content]:
    """
        Simple callback that logs when the agent starts processing a request.

        Args:
            callback_context: Contains state and context information

        Returns:
            None to continue with normal agent processing
    """
    # get session state
    session_state = callback_context.state

    start_time = datetime.now()

    if "agent_name" not in session_state:
        session_state["agent_name"] = "Greeting agent"
    if "request_count" not in session_state:
        session_state["request_count"] = 1
    else:
        session_state["request_count"] += 1
    
    session_state["request_start_time"] = start_time.timestamp()
    
    # Log the request
    print("---------- AGENT EXECUTION STARTED ----------")
    print(f"Request #: {session_state["request_count"]}")
    print(f"Start time: {start_time.strftime("%Y-%m-%d %H:%M:%S")}")

    # Print to console
    print(f"\n[BEFORE CALLBACK] Agent processing request #{session_state["request_count"]}")

    return None

def agent_post_execute(callback_context: CallbackContext) -> Optional[types.Content]:
    """
        Simple callback that logs when the agent finishes processing a request.

        Args:
            callback_context: Contains state and context information

        Returns:
            None to continue with normal agent processing
    """
    # get session state
    session_state = callback_context.state

    end_time = datetime.now()
    duration = None
    if "request_start_time" in session_state:
        duration = end_time.timestamp() - session_state["request_start_time"]
    
    # Log the completion
    print("---------- AGENT EXECUTION COMPLETED ----------")
    print(f"Request #: {session_state.get("request_count", "Unknown")}")
    if duration is not None:
        print(f"Duration: {duration:.2f} seconds")

    # Print to console
    print(
        f"[AFTER CALLBACK] Agent completed request #{session_state.get("request_count", "Unknown")}"
    )
    if duration is not None:
        print(f"[AFTER CALLBACK] Processing took {duration:.2f} seconds")

    return None

root_agent = LlmAgent(
    name = "agent_callback",
    model = "gemma-3-27b-it",
    description= "A basic agent that demonstrates before and after agent callbacks",
    instruction="""
        You are a friendly greeting agent. Your name is {agent_name}.
        
        Your job is to:
            - Greet users politely
            - Respond to basic questions
            - Keep your responses friendly and concise
    """,
    before_agent_callback= agent_pre_execute,
    after_agent_callback= agent_post_execute
)