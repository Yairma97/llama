import asyncio
import cProfile
import logging
import os
import pstats
import sys
import textwrap

import dotenv
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, StorageContext, Settings, Document
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

from embedding import ExampleEmbeddingFunction

nest_asyncio.apply()
dotenv.load_dotenv()

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

Settings.text_splitter = SentenceSplitter(chunk_size=512, chunk_overlap=50)
Settings.embed_model = HuggingFaceEmbedding(model_name=os.getenv("EMBEDDING_MODEL"), device=os.getenv('DEVICE'), embed_batch_size=4)


def generate_doc(path: str) -> List[Document]:
    # 原始数据
    parser = PandasExcelReader()
    file_extractor = {".xlsx": parser}
    documents = SimpleDirectoryReader(input_dir=path,file_extractor=file_extractor).load_data()
    print(len(documents))
    print(documents[:1])
    return documents


if __name__ == '__main__':
    # 管道
    pipeline = IngestionPipeline(
        transformations=[
            Settings.text_splitter,
            Settings.embed_model,
        ],
        # 向量数据库
        vector_store=MilvusVectorStore(
            collection_name='odr',
            dim=1024,
            uri="http://localhost:19530",
            # overwrite=True,
            enable_sparse=True,
            sparse_embedding_function=ExampleEmbeddingFunction(),
            hybrid_ranker="RRFRanker",
            hybrid_ranker_params={"k": 60},
        ),
        # 文档缓存
        cache=IngestionCache(
            cache=RedisKVStore.from_host_and_port(host="localhost", port=6379),
            collection="cache",
        ),
        # 文档存储
        docstore=RedisDocumentStore.from_host_and_port(
            "localhost", 6379, namespace="doc_store"
        )
    )
    print('-----------')
    asyncio.run(pipeline.arun(documents=generate_doc('data'), show_progress=True))
    print('============')
