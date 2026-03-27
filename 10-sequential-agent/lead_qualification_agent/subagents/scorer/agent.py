"""
Lead Scorer Agent
This agent is responsible for scoring a lead's qualification level based on given criteria.
"""

from google.adk.agents import LlmAgent

LLM_MODEL = "gemma-3-27b-it"

lead_scorer_agent = LlmAgent(
    name = "lead_scorer_agent",
    model = LLM_MODEL,
    description = "Scores qualified leads on a scale of 1-10.",
    instruction = """
        You are a Lead Scoring AI.
        
        Analyze the lead information and assign a qualification score from 1-10 based on:
            - Expressed need (urgency/clarity of problem)
            - Decision-making authority
            - Budget indicators
            - Timeline indicators
        
        Output ONLY a numeric score and ONE sentence justification.
        
        Example output: '8: Decision maker with clear budget and immediate need'
        Example output: '3: Vague interest with no timeline or budget mentioned'
    """,
    output_key = "lead_score"
)