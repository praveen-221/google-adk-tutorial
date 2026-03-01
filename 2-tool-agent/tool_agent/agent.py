from datetime import datetime

from google.adk.agents import LlmAgent
from google.adk.tools import google_search

def get_currentTime(format: str) -> dict:
    """
    Get the current time in the specified format.
    Args:
        format (str): The format in which to return the current time. Default is "%Y-%m-%d %H:%M:%S"."
    Returns:        
        dict: A dictionary containing the current time in the specified format.
    """
    format  = "%Y-%m-%d %H:%M:%S" if format is None else format
    return {
        "current_time": datetime.now().strftime(format)
    }

def get_currentMonth(format: str = "%Y-%m") -> dict:
    """
    Get the current month in the specified format.
    Args:
        format (str): The format in which to return the current month. Default is "%Y-%m"."
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
            - google_search,
            - get_currentTime,
            - get_currentMonth
    """,
    # tools = [google_search],
    # tools = [get_currentTime],
    # tools = [get_currentMonth],
    tools = [get_currentTime, get_currentMonth]
)