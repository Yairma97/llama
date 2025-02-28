import os

import chainlit
from langfuse.llama_index import LlamaIndexCallbackHandler
from llama_index.core import Settings, VectorStoreIndex, get_response_synthesizer
from llama_index.core.callbacks import TokenCountingHandler, LlamaDebugHandler
from llama_index.core.indices.vector_store import VectorIndexRetriever
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.postprocessor import SimilarityPostprocessor
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.vector_stores.types import VectorStoreQueryMode
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.llms.openai_like import OpenAILike
from llama_index.vector_stores.milvus import MilvusVectorStore
from transformers import AutoTokenizer

from embedding import ExampleEmbeddingFunction


async def global_settings_init():
    Settings.text_splitter = SentenceSplitter(chunk_size=512, chunk_overlap=100)
    Settings.tokenizer = AutoTokenizer.from_pretrained(pretrained_model_name_or_path=os.getenv("EMBEDDING_MODEL"))
    Settings.embed_model = HuggingFaceEmbedding(model_name=os.getenv("EMBEDDING_MODEL"), device='cpu',
                                                embed_batch_size=2)
    Settings.llm = OpenAILike(
        model="gpt-4o-mini",
        api_base=os.getenv("OPENAI_API_BASE"),
        api_key=os.getenv("OPENAI_API_KEY"),
        is_chat_model=True,
        streaming=True
    )
    langfuse_callback_handler = LlamaIndexCallbackHandler()
    token_counter = TokenCountingHandler(tokenizer=Settings.tokenizer)
    llama_debug = LlamaDebugHandler(print_trace_on_end=True)
    chainlit_handler = chainlit.LlamaIndexCallbackHandler()
    Settings.callback_manager.add_handler(langfuse_callback_handler)
    Settings.callback_manager.add_handler(token_counter)
    Settings.callback_manager.add_handler(llama_debug)
    Settings.callback_manager.add_handler(chainlit_handler)
    Settings.context_window = 4096
    vector_store = MilvusVectorStore(
        dim=1024,
        uri="http://localhost:19530",
        # overwrite=True,
        enable_sparse=True,
        sparse_embedding_function=ExampleEmbeddingFunction(),
        hybrid_ranker="RRFRanker",
        hybrid_ranker_params={"k": 60},
    )
    index = VectorStoreIndex.from_vector_store(vector_store, use_async=True)
    retriever = VectorIndexRetriever(
        index=index,
        similarity_top_k=1,
        vector_store_query_mode=VectorStoreQueryMode.HYBRID
    )
    response_synthesizer = get_response_synthesizer(use_async=True,streaming=True)
    Settings.query_engine = RetrieverQueryEngine(
        retriever=retriever,
        response_synthesizer=response_synthesizer,
        node_postprocessors=[],
    )

async def reset_callback_handlers():
    handles = Settings.callback_manager.handlers
    for handle in handles:
        if isinstance(handle, LlamaIndexCallbackHandler):
            handle.flush()
        if isinstance(handle, TokenCountingHandler):
            handle.reset_counts()
        if isinstance(handle, LlamaDebugHandler):
            handle.flush_event_logs()
        if isinstance(handle, chainlit.LlamaIndexCallbackHandler):
            handle.reset_counts()
