from google.adk.agents import LlmAgent

root_agent = LlmAgent(
    name = "greetingAgent",
    model = "gemma-3-27b-it",
    description = "A sample greeting agent",
    instruction = "You're a useful AI assitant which asks the user name and greets the user with a welcome message and positive quotes"
)