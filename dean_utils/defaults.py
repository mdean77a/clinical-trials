"""
Contains default values, model setups, logging configuration, etc. that
can be imported by other modules or notebooks.
"""

from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_openai.chat_models import ChatOpenAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama
import getpass
import os
import logging
import sys

# Define what should be exported from this module
__all__ = [
    'logger',
    'set_api_key',
    'te3_embedding_model',
    'bge_embedding_model',
    'qdrant_local_url',
    'gpt4o_llm',
    'lmstudio_llama_8b_llm',
    'ollama_llama_8b_llm'
]

# Configure logging to output to terminal
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

# Remove any existing handlers to avoid duplicate output
logger.handlers = []

# Create a stream handler that writes to sys.stderr (terminal)
handler = logging.StreamHandler(sys.stderr)
handler.setLevel(logging.INFO)


# Create a formatter
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', 
                            datefmt='%Y-%m-%d %H:%M:%S')
handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(handler)

# Prevent propagation to root logger to avoid duplicate output
logger.propagate = False

def set_api_key(key_name: str) -> None:
    """
    Securely set an environment variable if it doesn't already exist.
    Prompts the user for input using a password-style hidden input.
    
    Args:
        key_name (str): Name of the environment variable to set (e.g., "OPENAI_API_KEY")
    """
    if not os.environ.get(key_name):
        os.environ[key_name] = getpass.getpass(f"{key_name}: ")

# Example usage:
# set_api_key("OPENAI_API_KEY")
# set_api_key("ANTHROPIC_API_KEY")


te3_embedding_model = OpenAIEmbeddings(model="text-embedding-3-small", api_key=set_api_key("OPENAI_API_KEY"))
bge_embedding_model = HuggingFaceEmbeddings(
    model_name="BAAI/bge-base-en", 
    encode_kwargs={"normalize_embeddings": True}
)
qdrant_local_url = "http://localhost:6333"
gpt4o_llm = ChatOpenAI(model="gpt-4o", api_key=set_api_key("OPENAI_API_KEY"), streaming=True, temperature=0)
lmstudio_llama_8b_llm = ChatOpenAI(
    model="meta-llama-3,1-8b-instruct",  # This can be any name, it's not used by LM Studio
    base_url="http://192.168.1.157:1234/v1",  # Default LM Studio URL
    api_key="not-needed",  # LM Studio doesn't require an API key
    streaming=True,
    temperature=0
)
ollama_llama_8b_llm = ChatOllama(
    model="llama3.1:8b-instruct-q8_0",  # This should match the model name you pulled in Ollama
    base_url="http://192.168.1.157:11434/v1",  # Default Ollama URL
    api_key="not-needed",  # Ollama doesn't require an API key
    streaming=True,
    temperature=0,
    top_k=40,
    top_p=0.95,
    num_keep=5,
    num_predict=100,
    min_p=0.05,
    typical_p=0.7,
    repeat_last_n=33,
    repeat_penalty=1.1,
    presence_penalty=0.0,
    frequency_penalty=0.0,
    mirostat=0,
    mirostat_tau=5.0,
    mirostat_eta=0.1,
    penalize_newline=True,
    stop=["\n", "user:"],
    numa=False,
    num_ctx=131072,
    num_batch=512,
    num_gpu=32,
    main_gpu=0,
    low_vram=False,
    vocab_only=False,
    use_mmap=True,
    use_mlock=False,
    num_thread=8   
    
)