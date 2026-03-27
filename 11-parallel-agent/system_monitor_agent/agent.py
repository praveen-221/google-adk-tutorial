from google.adk.agents import ParallelAgent, SequentialAgent

# subagents
from .sub_agents.cpu_info_agent.agent import cpu_info_agent
from .sub_agents.disk_info_agent.agent import disk_info_agent
from .sub_agents.memory_info_agent.agent import memory_info_agent
from .sub_agents.report_synthesizer_agent.agent import report_synthesizer_agent

system_information_agent = ParallelAgent(
    name = "system_information_agent",
    description = "You are a helpful assistant who gathers ionformation about the system",
    sub_agents = [cpu_info_agent, disk_info_agent, memory_info_agent]
)

root_agent = SequentialAgent(
    name = "system_monitor_agent",
    description = "You are a helpful assistant who generates report based on system health",
    sub_agents = [system_information_agent, report_synthesizer_agent]
)