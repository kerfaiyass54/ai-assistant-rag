# chain.py — Builds and exposes the RAG chain

from langchain_community.llms import Ollama
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

from config import OLLAMA_MODEL, OLLAMA_BASE_URL, SYSTEM_PROMPT


def build_chain():
    """
    Constructs and returns the RAG chain.

    The chain:
      1. Runs a DuckDuckGo web search using the user's question.
      2. Injects the search results as `context` into the prompt.
      3. Sends the filled prompt to the local Ollama LLM.
    """
    llm = Ollama(model=OLLAMA_MODEL, base_url=OLLAMA_BASE_URL)
    search = DuckDuckGoSearchRun()
    prompt = ChatPromptTemplate.from_template(SYSTEM_PROMPT)

    chain = (
        RunnablePassthrough.assign(
            context=lambda x: search.run(x["question"])
        )
        | prompt
        | llm
    )

    return chain


def query(chain, question: str) -> str:
    """
    Runs a single question through the RAG chain and returns the answer.

    Args:
        chain: The LangChain chain returned by build_chain().
        question: The user's question string.

    Returns:
        The model's response as a plain string.
    """
    return chain.invoke({"question": question})