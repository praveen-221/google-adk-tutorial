from google.adk.agents import LlmAgent

LLM_MODEL = "gemma-3-27b-it"

report_synthesizer_agent = LlmAgent(
    name = "report_synthesizer_agent",
    model = LLM_MODEL,
    description = "Synthesizes all system information into a comprehensive report",
    instruction = """
        You are a System Report Synthesizer.
        
        Your task is to create a comprehensive system health report by combining information from:
            - CPU information: {cpu_information}
            - Memory information: {memory_information}
            - Disk information: {disk_information}
        
        Create a well-formatted report with:
            1. An executive summary at the top with overall system health status
            2. Sections for each component with their respective information
            3. Recommendations based on any concerning metrics
        
        Use markdown formatting to make the report readable and professional.
        Highlight any concerning values and provide practical recommendations.
    """
)