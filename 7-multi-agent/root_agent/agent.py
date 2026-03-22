from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool

from .sub_agents.stock_analyst.agent import stock_agent
from .sub_agents.funny_nerd.agent import nerd_agent
from .sub_agents.news_analyst.agent import news_agent
from .tools.get_current_time import get_current_time
from .tools.get_current_month import get_current_month

root_agent = Agent(
    name = "Manager",
    model = "gemma-3-27b-it",
    description = "Delegation Agent",
    instruction = """
        You are a manager agent that is responsible for overseeing the work of the other agents.

        Always delegate the task to the appropriate agent. Use your best judgement 
        to determine which agent to delegate to.

        You are responsible for delegating tasks to the following agent:
        - stock_agent
        - nerd_agent

        You also have access to the following tools:
        - news_agent
        - get_current_time,
        - get_current_month
    """,
    sub_agents = [
        stock_agent,
        nerd_agent
    ],
    tools = [
        get_current_month,
        get_current_time,
        AgentTool(news_agent)
    ]
)