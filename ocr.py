import logging
import os
import sys
import textwrap

from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, StorageContext, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.llms.openai_like import OpenAILike
from llama_index.readers.file import PandasExcelReader
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
            return_dense=False,
            return_sparse=True,
            return_colbert_vecs=False,
        )["lexical_weights"]
        return [self._to_standard_dict(output) for output in outputs]

    def encode_documents(self, documents: List[str]):
        outputs = self.model.encode(
            documents,
            return_dense=False,
            return_sparse=True,
            return_colbert_vecs=False,
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
    api_version="v1",
)
resp = Settings.llm.complete("Paul Graham is ")
print(resp)
# load some documents
# parser = PandasExcelReader()
# file_extractor = {".xlsx": parser}
# documents = SimpleDirectoryReader(input_files=['./data/18 HDR-病案模型目录.xlsx'],
#                                 file_extractor=file_extractor).load_data()
# print(len(documents))
# print(documents[:5])

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
# index = VectorStoreIndex.from_documents(
#     documents, storage_context=storage_context,show_progress=True
# )
index = VectorStoreIndex.from_vector_store(
    vector_store, storage_context=storage_context,show_progress=True
)
index.storage_context.persist(persist_dir="./milvus")
query_engine = index.as_query_engine(vector_store_query_mode="hybrid")
response = query_engine.query("EMR_CR_INPAT_OPER_INFO?")
print(textwrap.fill(str(response), 100))
