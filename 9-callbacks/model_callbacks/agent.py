import copy
from datetime import datetime
from typing import Optional

from google.adk.agents import LlmAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_request import LlmRequest
from google.adk.models.llm_response import LlmResponse
from google.genai import types

def model_pre_execute(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    """
        Before Model Callback that filters inappropriate content and logs request info.

        Args:
            callback_context: Contains state and context information
            llm_request: The LLM request being sent

        Returns:
            Optional LlmResponse to override model response
    """
    # get session state
    session_state = callback_context.state
    agent_name = callback_context.agent_name

    # fetch the latest user query
    user_query = None
    if llm_request.contents and len(llm_request.contents) > 0:
        for content in reversed(llm_request.contents):
            if content.role == "user" and content.parts and len(content.parts) > 0:
                if hasattr(content.parts[0], "text") and len(content.parts[0].text) > 0:
                    user_query = content.parts[0].text
                    break
    
    print("---------- MODEL REQUEST STARTED ----------")
    print(f"Agent: {agent_name}")
    if user_query:
        print(f"User message: {user_query[:100]}...")
        session_state["latest_user_message"] = user_query
    else: 
        print(f"User message: <empty>")
    
    if user_query and "sucks" in user_query.lower():
        print("[BEFORE MODEL] Request blocked due to inappropriate content")
        return LlmResponse(
            content = types.Content(
                role = "model",
                parts = [
                    types.Part(
                        text = "Inappropriate language detected in the request. " 
                        "Please rephrase the message without the word 'sucks'"
                    )
                ]
            ) 
        )
    
    session_state["model_start_time"] = datetime.now().timestamp()

    return None

def model_post_execute(callback_context: CallbackContext, llm_response: LlmResponse) -> Optional[LlmResponse]:
    """
        After Model callback that replaces negative words with more positive alternatives.

        Args:
            callback_context: Contains state and context information
            llm_response: The LLM response received

        Returns:
            Optional LlmResponse to override model response
    """
    # Log completion
    print("[AFTER MODEL] Processing response")
    if not llm_response or not llm_response.content or not llm_response.content.parts:
        return None
    
    model_response = ""
    for part in llm_response.content.parts:
        if hasattr(part, "text") and part.text:
            model_response += part.text
    
    if not model_response:
        return None
    
    substitutes = {
        "problem": "Challenge",
        "difficult": "Complex"
    }
    updated_response = model_response
    is_response_modified = False

    for original, replacement in substitutes.items():
        if original in updated_response.lower():
            updated_response = updated_response.replace(original, replacement)
            updated_response = updated_response.replace(original.capitalize(), replacement.capitalize())
            is_response_modified = True
    
    if is_response_modified:
        print(f"Model response modified")
        final_model_response = [copy.deepcopy(part) for part in llm_response.content.parts]
        for i, part in enumerate(final_model_response):
            if hasattr(part, "text") and part.text:
                # print(f"part: {part.text}\nand\ni: {final_model_response[i].text}")
                part.text = updated_response
                # final_model_response[i].text = updated_response
                # print(f"part: {part.text}\nand\ni: {final_model_response[i].text}")
        return LlmResponse(
            content = types.Content(role = "model", parts = final_model_response)
        )
    return None

root_agent = LlmAgent(
    name = "model_callback_agent",
    model = "gemma-3-27b-it",
    description="An agent that demonstrates model callbacks for content filtering and logging",
    instruction="You are a helpful assistant. Your job is to answer user questions concisely",
    before_model_callback = model_pre_execute,
    after_model_callback = model_post_execute
)