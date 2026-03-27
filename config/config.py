# config.py — Central configuration for the RAG assistant

import os

# Ollama model to use (must be pulled locally)
OLLAMA_MODEL = "llama3:8b"

# Reads OLLAMA_HOST env var — set automatically by Docker Compose,
# falls back to localhost for running the app directly.
OLLAMA_BASE_URL = os.getenv("OLLAMA_HOST", "http://localhost:11434")

# System prompt injected into every query
SYSTEM_PROMPT = """You are a helpful AI assistant. You must answer the user's question 
based *only* on the following search results. If the search results 
are empty or do not contain the answer, say 'I could not find 
any information on that.'

Search Results:
{context}

Question:
{question}
"""

# App metadata
APP_TITLE = "🔍 Real-Time RAG Assistant"
APP_SUBTITLE = "Powered by Ollama + DuckDuckGo"