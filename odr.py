import asyncio
import cProfile
import logging
import os
import pstats
import sys
import textwrap

import dotenv
from langfuse.llama_index import LlamaIndexCallbackHandler
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, StorageContext, Settings, set_global_handler, \
    global_handler
from llama_index.core.callbacks import CallbackManager, TokenCountingHandler, LlamaDebugHandler, CBEventType
from llama_index.core.ingestion import IngestionPipeline, IngestionCache, DocstoreStrategy
from llama_index.core.node_parser import SentenceSplitter, SimpleFileNodeParser
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.openai_like import OpenAILike
from llama_index.readers.file import PandasExcelReader
from llama_index.storage.docstore.redis import RedisDocumentStore
from llama_index.storage.kvstore.redis import RedisKVStore
from llama_index.vector_stores.milvus import MilvusVectorStore

from FlagEmbedding import BGEM3FlagModel
from typing import List
from llama_index.vector_stores.milvus.utils import BaseSparseEmbeddingFunction
import nest_asyncio
from transformers import AutoTokenizer

from embeddingfunction import ExampleEmbeddingFunction

nest_asyncio.apply()
dotenv.load_dotenv()

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))


def global_settings_init():
    Settings.text_splitter = SentenceSplitter(chunk_size=512, chunk_overlap=100)
    Settings.tokenizer = AutoTokenizer.from_pretrained(pretrained_model_name_or_path=os.getenv("EMBEDDING_MODEL"))
    Settings.embed_model = HuggingFaceEmbedding(model_name=os.getenv("EMBEDDING_MODEL"), device='cpu',
                                                embed_batch_size=2)
    Settings.llm = OpenAILike(
        model="gpt-4o-mini",
        api_base=os.getenv("OPENAI_API_BASE"),
        api_key=os.getenv("OPENAI_API_KEY"),
        is_chat_model=True,
    )
    langfuse_callback_handler = LlamaIndexCallbackHandler()
    Settings.callback_manager = CallbackManager([langfuse_callback_handler])


def callback_handler_reset():
    handles = Settings.callback_manager.handlers
    for handle in handles:
        if isinstance(handle, LlamaIndexCallbackHandler):
            handle.flush()
        if isinstance(handle, TokenCountingHandler):
            handle.reset_counts()
        if isinstance(handle, LlamaDebugHandler):
            handle.flush_event_logs()


if __name__ == '__main__':
    global_settings_init()
    token_counter = TokenCountingHandler(
        tokenizer=Settings.tokenizer
    )
    llama_debug = LlamaDebugHandler(print_trace_on_end=True)
    Settings.callback_manager.add_handler(token_counter)
    Settings.callback_manager.add_handler(llama_debug)

    # 向量数据库
    vector_store = MilvusVectorStore(
        dim=1024,
        uri="http://localhost:19530",
        # overwrite=True,
        enable_sparse=True,
        sparse_embedding_function=ExampleEmbeddingFunction(),
        hybrid_ranker="RRFRanker",
        hybrid_ranker_params={"k": 60},
    )
    index = VectorStoreIndex.from_vector_store(
        vector_store, embed_model=Settings.embed_model
    )
    # index.storage_context.persist(persist_dir="./milvus")
    query_engine = index.as_query_engine(vector_store_query_mode="hybrid")
    response = query_engine.query("INPATIENT_ILLNESS_CODE的中文字段意思是什么?他在哪张表里？")
    print(llama_debug.get_event_pairs(CBEventType.RETRIEVE))
    print(textwrap.fill(str(response), 100))
    callback_handler_reset()