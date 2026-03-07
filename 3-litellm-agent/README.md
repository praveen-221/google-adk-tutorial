# LiteLLM Agent Example

## What is LiteLLM?

LiteLLM is a Python library that provides a unified interface for interacting with multiple Large Language Model (LLM) providers through a single, consistent API. It serves as an adapter that allows you to:

- Use the same code to access 100+ different LLMs from providers like OpenAI, Anthropic, Google, AWS Bedrock, and more
- Standardize inputs and outputs across different LLM providers
- Track costs, manage API keys, and handle errors consistently
- Implement fallbacks and load balancing across different models

In essence, LiteLLM acts as a unified wrapper that makes it easy to switch between different LLM providers without changing your application code.

## Why Use LiteLLM with ADK?

The Agent Development Kit (ADK) is designed to be model-agnostic, meaning it can work with various LLM providers. LiteLLM enhances this capability by:

1. **Provider Flexibility**: Easily switch between LLM providers (OpenAI, Anthropic, etc.) without changing your agent code
2. **Cost Optimization**: Choose the most cost-effective model for your specific use case
3. **Model Exploration**: Experiment with different models to find the best performance for your task
4. **Future-Proofing**: As new models are released, you can quickly adopt them without major code changes

This example demonstrates how to use LiteLLM with ADK to create an agent powered by models through OpenRouter rather than Google's Gemini models.

## Limitations When Using Non-Google Models

When using LiteLLM to integrate non-Google models with ADK, there are some important limitations to be aware of:

1. **No Access to Google Built-in Tools**: Non-Google models (like OpenAI, Anthropic, etc.) cannot use ADK's built-in Google tools such as:
   - Google Search
   - Code Execution
   - Vertex AI Search

2. **Custom Function Tools Only**: When using non-Google models, you can only use custom function tools (like the `get_dad_joke()` function in this example).


These limitations exist because built-in tools are specifically designed to work with Google's models and infrastructure. However, you can still create powerful agents using custom function tools and the wide variety of models available through LiteLLM.

## Additional Resources

- [Google ADK LiteLLM Integration Documentation](https://google.github.io/adk-docs/tutorials/agent-team/#step-2-going-multi-model-with-litellm-optional)
- [LiteLLM Documentation](https://docs.litellm.ai/docs/)
- [LiteLLM Supported Providers](https://docs.litellm.ai/docs/providers)
- [Anthropic Claude Models Overview](https://docs.anthropic.com/en/docs/about-claude/models/all-models)