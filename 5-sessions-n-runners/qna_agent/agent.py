from google.adk.agents import Agent

qna_agent = Agent(
    name = "QnA_agent",
    model = "gemma-3-27b-it",
    description = "You are a helpful agent who answers the questions",
    instruction = """
        You are a helpful assistant who answers about the user.

        Here are the information about the user:
        {user_name},
        and user details: {user_details}
    """
)