from langchain_community.llms import Ollama
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

# We specify the model we pulled in Step 1
llm = Ollama(model="llama3:8b")

# This tool will run a web search
search = DuckDuckGoSearchRun()

