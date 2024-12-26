from llama_index.core import ServiceContext
import os
import logging
from logging_config import LOGGING_CONFIG
logging.config.dictConfig(LOGGING_CONFIG)

from app.engine.constants import CHUNK_SIZE, CHUNK_OVERLAP
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.node_parser import SentenceSplitter
from llama_index.llms.openai import OpenAI
from llama_index.core import Settings
from llama_index.core.constants import DEFAULT_TEMPERATURE

def create_service_context():
    logger = logging.getLogger("uvicorn")
    print("Initializing the OpenAI configurations.......")
    logger.info("Initializing the OpenAI configurations.......")
    max_tokens = os.getenv("LLM_MAX_TOKENS")
    config = {
        "model": os.getenv("MODEL"),
        "temperature": float(os.getenv("LLM_TEMPERATURE", DEFAULT_TEMPERATURE)),
        "max_tokens": int(max_tokens) if max_tokens is not None else None,
    }
    Settings.llm = OpenAI(**config)
    dimensions = os.getenv("EMBEDDING_DIM")
    config = {
        "model": os.getenv("EMBEDDING_MODEL"),
        "dimensions": int(dimensions) if dimensions is not None else None,
    }
    Settings.embed_model = OpenAIEmbedding(**config)
    return Settings