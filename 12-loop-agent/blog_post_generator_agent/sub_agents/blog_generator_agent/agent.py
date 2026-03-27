from typing import Dict, Any

from google.adk.agents import LlmAgent
from google.adk.tools.tool_context import ToolContext

LLM_MODEL = "gemma-3-27b-it"

blog_generator_agent = LlmAgent(
    name = "blog_generator_agent",
    model = LLM_MODEL,
    description = "Generates the initial blog post to start the refinement process",
    instruction = """
        You are an expert blog post generator. Your task is to create an initial blog post draft on a given topic.

        INSTRUCTIONS:
            1. TOPIC HANDLING:
                - First check if a topic has been provided in the user input
                - If NO topic is provided, politely ask the user: "Please provide a topic for the blog post you'd like me to generate. What would you like the blog post to be about?" and generate NULL as blog and store it
                - If YES topic is provided, proceed with blog post generation

            2. BLOG POST GENERATION:
                Once you have the topic, generate a well-structured blog post that includes:
                    - An engaging title that clearly reflects the topic
                    - An introduction that hooks the reader and explains what the post will cover
                    - 1-2 main body sections with clear headings that develop the topic
                    - Each section should have substantial content (1-2 paragraphs) with relevant examples or explanations
                    - A compelling conclusion that summarizes key points and provides actionable insights
                    - Total length should aim for 1000-1500 characters

            3. QUALITY STANDARDS:
                - Use clear, professional, and engaging language
                - Ensure logical flow and proper structure
                - Include relevant information and examples
                - Make the content informative and valuable to readers
                - Avoid grammatical errors and maintain consistency

            4. OUTPUT FORMAT:
                Return the complete blog post as a well-formatted text document. The post will be reviewed and refined in subsequent iterations.

            5. IMPORTANT:
                - Focus on creating quality initial content
                - The post will go through refinement cycles, so make a solid first draft
                - Ensure you've included all major sections even if they need refinement
    """,
    output_key = "current_blog"
)