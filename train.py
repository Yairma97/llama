import asyncio
import cProfile
import logging
import os
import pstats
import sys
import textwrap

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

OPENAI_API_KEY = 'sk-wNDMy7OZEz18JiPiu2GXwhnSn5FDBnhW5V8itYzDJvq5FVeY'
OPENAI_API_BASE = 'https://api.kksj.org/v1'
os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY
os.environ['OPENAI_API_BASE'] = OPENAI_API_BASE
os.environ["GRPC_ENABLE_FORK_SUPPORT"] = "FALSE"
os.environ["TOKENIZERS_PARALLELISM"] = "FALSE"
os.environ["EMBEDDING_MODEL"] = "/Volumes/TiPlus7100/Models/bge-m3"

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


Settings.text_splitter = SentenceSplitter(chunk_size=512, chunk_overlap=100)
Settings.embed_model = HuggingFaceEmbedding(model_name=os.getenv("EMBEDDING_MODEL"), device='cpu', embed_batch_size=2)


def generate_doc(filename: str) -> List[Document]:
    # 原始数据
    parser = PandasExcelReader()
    file_extractor = {".xlsx": parser}
    documents = SimpleDirectoryReader(input_files=[filename],
                                      file_extractor=file_extractor).load_data()
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
    asyncio.run(pipeline.arun(documents=generate_doc('./data/18 HDR-病案模型目录.xlsx'), show_progress=True))
    print('============')
