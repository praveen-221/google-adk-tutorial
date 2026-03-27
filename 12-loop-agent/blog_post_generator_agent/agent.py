from google.adk.agents import LoopAgent, SequentialAgent

# sub agents
from .sub_agents.blog_generator_agent.agent import blog_generator_agent
from .sub_agents.blog_refinement_agent.agent import blog_refinement_agent
from .sub_agents.blog_reviewer_agent.agent import blog_reviewer_agent

blog_refinement_pipeline = LoopAgent(
    name = "blog_refinement_pipeline",
    description = """Iteratively reviews and refines a blog post until quality requirements are met.
        This loop runs a two-step process:
            1. blog_refinement_agent - Improves the post based on feedback
            2. blog_reviewer_agent - Reviews quality and either approves (exits loop) or provides feedback
        The loop continues until the post meets all quality standards or until maxium iterations reached.""",
    max_iterations = 2,
    sub_agents = [blog_reviewer_agent, blog_refinement_agent]
)

root_agent = SequentialAgent(
    name = "blog_generator_agent",
    description = """Generates and refines a blog post through an iterative review process.
    
    WORKFLOW:
    1. GENERATION PHASE: blog_generator_agent creates an initial draft
       - Asks user for topic if not provided
       - Generates well-structured blog post (title, intro, 3-4 sections, conclusion)
       - Aims for 1000-1500 characters
    
    2. REFINEMENT LOOP PHASE: blog_refinement_pipeline iteratively improves the post
       - blog_refinement_agent: Refines based on reviewer feedback
       - blog_reviewer_agent: Reviews quality and decides to approve or request improvements
       - Loop repeats up to 5 times until quality requirements are fully met
    
    QUALITY REQUIREMENTS:
        - Length: 1000-1500 characters (verified by count_characters tool)
        - Structure: Clear title, engaging intro, 3-4 main sections, strong conclusion
        - Content: Relevant, informative, valuable, with good examples
        - Writing: Clear language, professional tone, error-free, logical flow
        - Exit Condition: All criteria met + reviewer calls exit_loop tool""",
    sub_agents = [blog_generator_agent, blog_refinement_pipeline]
)