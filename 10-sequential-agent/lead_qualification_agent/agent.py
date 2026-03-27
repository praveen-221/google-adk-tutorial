"""
Sequential Agent with a Minimal Callback

A lead qualification pipeline with a minimal
"""

from google.adk.agents import SequentialAgent
from .subagents.recommender.agent import lead_action_recommender_agent
from .subagents.scorer.agent import lead_scorer_agent
from .subagents.validator.agent import lead_validator_agent

LLM_MODEL = "gemma-3-27b-it"

root_agent = SequentialAgent(
    name = "lead_qualification_agent_pipeline",
    description = "A pipeline that validates, scores, and recommends actions for sales leads",
    sub_agents = [lead_scorer_agent, lead_validator_agent, lead_action_recommender_agent]
)