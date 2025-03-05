import os
from typing import List, Callable, Any

import dotenv
from chainlit import LlamaIndexCallbackHandler as ChainlitCallbackHandler
from langfuse.llama_index import LlamaIndexCallbackHandler as LangfuseCallbackHandler
from llama_index.core import Settings, VectorStoreIndex, get_response_synthesizer, BaseCallbackHandler
from llama_index.core.base.base_query_engine import BaseQueryEngine
from llama_index.core.base.embeddings.base import BaseEmbedding
from llama_index.core.callbacks import TokenCountingHandler, LlamaDebugHandler, CallbackManager
from llama_index.core.indices.query.query_transform import HyDEQueryTransform
from llama_index.core.indices.query.query_transform.base import BaseQueryTransform, StepDecomposeQueryTransform
from llama_index.core.indices.vector_store import VectorIndexRetriever
from llama_index.core.llms import LLM
from llama_index.core.node_parser import SentenceSplitter, NodeParser
from llama_index.core.query_engine import RetrieverQueryEngine, MultiStepQueryEngine, TransformQueryEngine, \
    SubQuestionQueryEngine
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.vector_stores.types import VectorStoreQueryMode
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.deepseek import DeepSeek
from llama_index.llms.openai import OpenAI
from llama_index.postprocessor.flag_embedding_reranker import FlagEmbeddingReranker
from llama_index.vector_stores.milvus import MilvusVectorStore
from transformers import AutoTokenizer

from embedding import ExampleEmbeddingFunction

dotenv.load_dotenv()
DEFAULT_CALLBACK_HANDLER = [LangfuseCallbackHandler(), TokenCountingHandler(tokenizer=Settings.tokenizer),
                            LlamaDebugHandler(print_trace_on_end=True)]
DEFAULT_CALLBACK_MANAGER = CallbackManager(DEFAULT_CALLBACK_HANDLER)
DEFAULT_CONTEXT_WINDOW = 4096
DEFAULT_LLM = OpenAI(
    callback_manager=DEFAULT_CALLBACK_MANAGER,
    model="gpt-4o-mini",
    api_base=os.getenv("OPENAI_API_BASE"),
    api_key=os.getenv("OPENAI_API_KEY"),
    is_chat_model=True,
    streaming=True
)
DEFAULT_NODE_PARSER = SentenceSplitter(chunk_size=512, chunk_overlap=100, callback_manager=DEFAULT_CALLBACK_MANAGER)
DEFAULT_TOKENIZER = AutoTokenizer.from_pretrained(pretrained_model_name_or_path=os.getenv("EMBEDDING_MODEL"))
DEFAULT_EMBEDDING_MODEL = HuggingFaceEmbedding(model_name=os.getenv("EMBEDDING_MODEL"), device='cpu',
                                               embed_batch_size=2, callback_manager=DEFAULT_CALLBACK_MANAGER)

DEFAULT_VECTOR_STORE = MilvusVectorStore(
    collection_name='odr',
    dim=1024,
    uri="http://localhost:19530",
    enable_sparse=True,
    sparse_embedding_function=ExampleEmbeddingFunction(),
    hybrid_ranker="RRFRanker",
    hybrid_ranker_params={"k": 60},
)
DEFAULT_RESPONSE_SYNTHESIZER = get_response_synthesizer(llm=DEFAULT_LLM, use_async=True, streaming=True,
                                                        callback_manager=DEFAULT_CALLBACK_MANAGER)
DEFAULT_INDEX = VectorStoreIndex.from_vector_store(DEFAULT_VECTOR_STORE, embed_model=DEFAULT_EMBEDDING_MODEL,
                                                   callback_manager=DEFAULT_CALLBACK_MANAGER, use_async=True,
                                                   show_progress=True)
DEFAULT_RERANK = FlagEmbeddingReranker(
    top_n=4,
    model=os.getenv("RERANK_MODEL"),
    use_fp16=False
)
DEFAULT_SIMILARITY_TOP_K = 10
DEFAULT_RETRIEVER = VectorIndexRetriever(
    index=DEFAULT_INDEX,
    callback_manager=DEFAULT_CALLBACK_MANAGER,
    similarity_top_k=DEFAULT_SIMILARITY_TOP_K,
    vector_store_query_mode=VectorStoreQueryMode.HYBRID,
)
DEFAULT_QUERY_TRANSFORM = HyDEQueryTransform(include_original=True, llm=DEFAULT_LLM)
DEFAULT_QUERY_ENGINE = RetrieverQueryEngine.from_args(
    llm=DEFAULT_LLM,
    retriever=DEFAULT_RETRIEVER,
    response_synthesizer=DEFAULT_RESPONSE_SYNTHESIZER,
    node_postprocessors=[DEFAULT_RERANK],
    callback_manager=DEFAULT_CALLBACK_MANAGER,
)


# logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
# logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

async def default_settings_init():
    Settings.callback_manager = get_default_callback_manager()
    Settings.llm = get_default_llm()
    Settings.tokenizer = get_default_tokenizer()
    Settings.node_parser = get_default_node_parser()
    Settings.context_window = get_default_context_window()
    Settings.embed_model = get_default_embed_model()
    Settings.query_engine = TransformQueryEngine(query_engine=get_default_query_engine(),
                                                 query_transform=get_hyde_query_transform(),
                                                 callback_manager=get_default_callback_manager())


def get_default_node_parser() -> NodeParser:
    return DEFAULT_NODE_PARSER


def get_default_tokenizer() -> Callable[[str], List[Any]]:
    return DEFAULT_TOKENIZER


def get_default_embed_model() -> BaseEmbedding:
    return DEFAULT_EMBEDDING_MODEL


def get_default_llm() -> LLM:
    return DEFAULT_LLM


def get_hospital_llm() -> LLM:
    return DeepSeek(model="DeepSeek-R1",
                    api_base=os.getenv("DEEPSEEK_API_BASE"),
                    api_key=os.getenv("DEEPSEEK_API_KEY"),
                    is_chat_model=True,
                    streaming=True)


def get_default_callback_manager() -> CallbackManager:
    return DEFAULT_CALLBACK_MANAGER


def get_default_context_window() -> int:
    return DEFAULT_CONTEXT_WINDOW


def get_default_query_engine() -> BaseQueryEngine:
    return DEFAULT_QUERY_ENGINE


def get_hyde_query_transform() -> BaseQueryTransform:
    return DEFAULT_QUERY_TRANSFORM


def get_multi_step_query_engine(query_engine: BaseQueryEngine) -> BaseQueryEngine:
    step_decompose_transform = StepDecomposeQueryTransform(llm=Settings.llm, verbose=True)
    return MultiStepQueryEngine(
        num_steps=2,
        query_engine=query_engine,
        response_synthesizer=DEFAULT_RESPONSE_SYNTHESIZER,
        query_transform=step_decompose_transform,
    )


def get_subquestion_query_engine(query_engine: BaseQueryEngine) -> BaseQueryEngine:
    query_engine_tools = [
        QueryEngineTool(
            query_engine=query_engine,
            metadata=ToolMetadata(
                name="sql generator",
                description="根据提出的问题，结合检索上下文完成sql语句的生成",
            ),
        ),
    ]
    return SubQuestionQueryEngine.from_defaults(
        query_engine_tools=query_engine_tools,
        use_async=True,
    )
