import asyncio
import logging
import os
import sys

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

nest_asyncio.apply()
# 获取当前环境
environment = os.getenv('ENVIRONMENT', 'dev')

# 加载对应环境的 .env.dev 文件
print("common.train.py")
env_file = f'.env.{environment}'

dotenv.load_dotenv(env_file)
print("env_file", env_file)
print("EMBEDDING_MODEL", os.getenv("EMBEDDING_MODEL"))
print("DEEPSEEK_API_BASE", os.getenv("DEEPSEEK_API_BASE"))

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))



class ExampleEmbeddingFunction(BaseSparseEmbeddingFunction):
    def __init__(self):
        self.model = BGEM3FlagModel(os.getenv("EMBEDDING_MODEL"), use_fp16=False, devices=os.getenv("DEVICE"))

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


def generate_doc(path: str) -> List[Document]:
    # 原始数据
    parser = PandasExcelReader()
    file_extractor = {".xlsx": parser}
    documents = SimpleDirectoryReader(input_files=[path], file_extractor=file_extractor).load_data()
    print(len(documents))
    print(documents[:1])
    return documents


if __name__ == '__main__':
    # 管道
    pipeline = IngestionPipeline(
        transformations=[
            SentenceSplitter(chunk_size=256, chunk_overlap=50),
            HuggingFaceEmbedding(model_name=os.getenv("EMBEDDING_MODEL"), device=os.getenv('DEVICE'),
                                 embed_batch_size=2),
        ],
        # 向量数据库
        vector_store=MilvusVectorStore(
            collection_name='dify',
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
    asyncio.run(pipeline.arun(documents=generate_doc('data/ODR模型说明.xlsx'), show_progress=True))
    print('============')
