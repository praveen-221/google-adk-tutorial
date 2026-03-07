import os
import random
from dotenv import load_dotenv
from google.adk.models.lite_llm import LiteLlm
from google.adk.agents import LlmAgent

load_dotenv()
model = LiteLlm(
    model = "gemini/gemma-3-27b-it",    # provider/model_name
    api_key = os.getenv("GOOGLE_API_KEY")
)

def random_city() -> str:
    """
    Returns a random city name
    """
    cities = [
        "New York",
        "Los Angeles",
        "Chicago",
        "Houston",
        "Phoenix",
        "Philadelphia",
        "San Antonio",
        "San Diego",
        "Dallas",
        "San Jose"
    ]

    return random.choice(cities)

root_agent = LlmAgent(
    name = "liteLLM_agent",
    model = model,
    description = "A helpful AI agent(using liteLLm) powered with tools",
    instruction = """
        You are a helpful assistant that returns a random city name 
        when user asks only using tools provided
    """,
    # tools = [random_city]     # gemma can not access tools when used inside LiteLLM 
)