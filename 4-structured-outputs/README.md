# Structured Outputs in ADK

## What are Structured Outputs?

ADK allows you to define structured data formats for agent inputs and outputs using Pydantic models:

1. **Controlled Output Format**: Using `output_schema` ensures the LLM produces responses in a consistent JSON structure
2. **Data Validation**: Pydantic validates that all required fields are present and correctly formatted
3. **Improved Downstream Processing**: Structured outputs are easier to handle in downstream applications or by other agents

Use structured outputs when you need guaranteed format consistency for integration with other systems or agents.

## Email Generator Example

In this example, the agent uses a Pydantic model called `EmailContent` to define this structure, ensuring every response follows the same format.

### Output Schema Definition

The Pydantic model defines exactly what fields are required and includes descriptions for each:

```python
class EmailContent(BaseModel):
    """Schema for email content with subject and body."""
    
    subject: str = Field(
        description="The subject line of the email. Should be concise and descriptive."
    )
    body: str = Field(
        description="The main content of the email. Should be well-formatted with proper greeting, paragraphs, and signature."
    )
```

### How It Works

1. The user provides a description of the email they need
2. The LLM agent processes this request and generates both a subject and body
3. The agent formats its response as a JSON object matching the `EmailContent` schema
4. ADK validates the response against the schema before returning it
5. The structured output is stored in the session state under the specified `output_key`

## Important Limitations

When using `output_schema`:

1. **No Tool Usage**: Agents with an output schema cannot use tools during their execution
2. **Direct JSON Response**: The LLM must produce a JSON response matching the schema as its final output
3. **Clear Instructions**: The agent's instructions must explicitly guide the LLM to produce properly formatted JSON

## Project Structure

```
4-structured-outputs/
│
├── email_agent/                   # Email Generator Agent package
│   └── agent.py                   # Agent definition with output schema
│
└── README.md                      # This documentation
```

## Key Concepts: Structured Data Exchange

Structured outputs are part of ADK's broader support for structured data exchange, which includes:

1. **input_schema**: Define expected input format
2. **output_schema**: Define required output format
3. **output_key**: Store the result in session state for use by other agents

This pattern enables reliable data passing between agents and integration with external systems that expect consistent data formats.

## Additional Resources

- [ADK Structured Data Documentation](https://google.github.io/adk-docs/agents/llm-agents/#structuring-data-input_schema-output_schema-output_key)
- [Pydantic Documentation](https://docs.pydantic.dev/latest/) 