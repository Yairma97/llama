import asyncio
import cProfile
import logging
import os
import pstats
import sys
import textwrap

from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, StorageContext, Settings
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


OPENAI_API_KEY = 'sk-wNDMy7OZEz18JiPiu2GXwhnSn5FDBnhW5V8itYzDJvq5FVeY'
OPENAI_API_BASE = 'https://api.kksj.org/v1'
os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY
os.environ['OPENAI_API_BASE'] = OPENAI_API_BASE
os.environ["TOKENIZERS_PARALLELISM"] = "FALSE"
os.environ["EMBEDDING_MODEL"] = "/Users/mayifan/Documents/environment/bge-m3"

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))


class ExampleEmbeddingFunction(BaseSparseEmbeddingFunction):
    def __init__(self):
        self.model = BGEM3FlagModel(os.getenv("EMBEDDING_MODEL"), use_fp16=False)

    def encode_queries(self, queries: List[str]):
        outputs = self.model.encode(
            queries,
            return_dense=True,
            return_sparse=True,
        )["lexical_weights"]
        return [self._to_standard_dict(output) for output in outputs]

    def encode_documents(self, documents: List[str]):
        outputs = self.model.encode(
            documents,
            return_dense=True,
            return_sparse=True,
        )["lexical_weights"]
        return [self._to_standard_dict(output) for output in outputs]

    def _to_standard_dict(self, raw_output):
        result = {}
        for k in raw_output:
            result[int(k)] = raw_output[k]
        return result


Settings.embed_model = HuggingFaceEmbedding(model_name=os.getenv("EMBEDDING_MODEL"))
Settings.llm = OpenAILike(
    model="gpt-4o-mini",
    api_base=OPENAI_API_BASE,
    api_key=OPENAI_API_KEY,
    is_chat_model=True,
)
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
storage_context = StorageContext.from_defaults(vector_store=vector_store)

# 原始数据
parser = PandasExcelReader()
file_extractor = {".xlsx": parser}
documents = SimpleDirectoryReader(input_files=['./data/18 HDR-病案模型目录.xlsx'],
                                  file_extractor=file_extractor).load_data()
print(len(documents))
print(documents[:2])
# 文档缓存
cache = IngestionCache(
    cache=RedisKVStore.from_host_and_port(host="localhost", port=6379),
    collection="cache",
)
# 文档存储
doc_store = RedisDocumentStore.from_host_and_port(
    "localhost", 6379, namespace="doc_store"
)

# 管道
pipeline = IngestionPipeline(
    transformations=[
        # SimpleFileNodeParser(),
        # TitleExtractor(),
        Settings.embed_model,
    ],
    vector_store=vector_store,
    cache=cache,
    docstore=doc_store,
)
print("---------")
nodes = pipeline.run(documents=documents, show_progress=True)
print("==========")
# index = VectorStoreIndex.from_vector_store(
#     vector_store, embed_model=Settings.embed_model
# )
# index.storage_context.persist(persist_dir="./milvus")
# query_engine = index.as_query_engine(vector_store_query_mode="hybrid")
# response = query_engine.query("What documents do you see?")
# print(textwrap.fill(str(response), 100))
