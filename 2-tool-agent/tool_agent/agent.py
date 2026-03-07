from datetime import datetime

from google.adk.agents import LlmAgent
from google.adk.tools import google_search

def get_currentTime(format: str) -> dict:
    """
    Get the current time.
    Args:
        format (str): The format in which to return the current time. Example format: "%Y-%m-%d %H:%M:%S"
    Returns:        
        dict: A dictionary containing the current time in the specified format.
    """
    return {
        "current_time": datetime.now().strftime(format)
    }

def get_currentMonth(format: str = "%Y-%m") -> dict:
    """
    Get the current month.
    Args:
        format (str): The format in which to return the current month. Example format: "%Y-%m"
    Returns:        
        dict: A dictionary containing the current month in the specified format.
    """
    return {
        "current_month": datetime.now().strftime(format)
    }


root_agent = LlmAgent(
    name = "toolAgent",
    model = "gemma-3-27b-it",
    description = "A helpful AI agent powered with tools",
    instruction = """
        You are a helpful assistant that can use the following tools:
        
        1. get_currentTime: Get the current time in a specified format (e.g., "%Y-%m-%d %H:%M:%S")
        2. get_currentMonth: Get the current month in a specified format (e.g., "%Y-%m")
        
        When the user asks about the current time or date, use these tools to provide accurate information.
    """,
    # tools = [google_search],
    # tools = [get_currentTime],
    # tools = [get_currentMonth],
    tools = [get_currentTime, get_currentMonth]
)