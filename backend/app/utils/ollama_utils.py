import os
from typing import Dict, Any
from langchain_community.llms import Ollama
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnableSequence

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")

# Initialize the Ollama LLM
ollama = Ollama(
    base_url=OLLAMA_HOST,
    model="llama3.2",
    callback_manager=CallbackManager([StreamingStdOutCallbackHandler()])
)

async def generate_ollama_response(prompt: str, model: str = "llama2") -> Dict[str, Any]:
    """
    Generate a response from Ollama using the specified model.

    Args:
        prompt (str): The input prompt for the model.
        model (str): The name of the Ollama model to use. Defaults to "llama2".

    Returns:
        Dict[str, Any]: The response from Ollama.
    """
    # Update the model if it's different from the default
    if model != ollama.model:
        ollama.model = model

    response = await ollama.agenerate([prompt])
    return {"response": response.generations[0][0].text}

def create_prompt_template(template: str) -> PromptTemplate:
    """
    Create a PromptTemplate from a given template string.

    Args:
        template (str): The template string with placeholders for variables.

    Returns:
        PromptTemplate: A LangChain PromptTemplate object.
    """
    return PromptTemplate.from_template(template)

async def run_llm_chain(prompt_template: PromptTemplate, **kwargs: Any) -> str:
    """
    Run an LLM chain with the given prompt template and input variables.

    Args:
        prompt_template (PromptTemplate): The PromptTemplate to use.
        **kwargs: The input variables for the prompt template.

    Returns:
        str: The generated response from the LLM chain.
    """
    chain = RunnableSequence(prompt_template | ollama)
    response = await chain.ainvoke(kwargs)
    return response  # RunnableSequence already returns the generated text
