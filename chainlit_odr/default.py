import os
from typing import List, Callable, Any

import dotenv
from chainlit import LlamaIndexCallbackHandler as ChainlitCallbackHandler
from llama_index.core import Settings, VectorStoreIndex, get_response_synthesizer, ChatPromptTemplate, \
    BaseCallbackHandler
from llama_index.core.base.base_query_engine import BaseQueryEngine
from llama_index.core.base.embeddings.base import BaseEmbedding
from llama_index.core.base.llms.types import ChatMessage, MessageRole
from llama_index.core.callbacks import TokenCountingHandler, LlamaDebugHandler, CallbackManager
from llama_index.core.indices.query.query_transform import HyDEQueryTransform
from llama_index.core.indices.query.query_transform.base import BaseQueryTransform, StepDecomposeQueryTransform
from llama_index.core.indices.vector_store import VectorIndexRetriever
from llama_index.core.llms import LLM
from llama_index.core.node_parser import SentenceSplitter, NodeParser
from llama_index.core.query_engine import RetrieverQueryEngine, MultiStepQueryEngine, SubQuestionQueryEngine
from llama_index.core.response_synthesizers import BaseSynthesizer
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.vector_stores.types import VectorStoreQueryMode, BasePydanticVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.deepseek import DeepSeek
from llama_index.postprocessor.flag_embedding_reranker import FlagEmbeddingReranker
from llama_index.vector_stores.milvus import MilvusVectorStore
from transformers import AutoTokenizer

from embedding import ExampleEmbeddingFunction

# 获取当前环境
environment = os.getenv('ENVIRONMENT', 'dev')

# 加载对应环境的 .env.dev 文件
env_file = f'.env.{environment}'
dotenv.load_dotenv(env_file)


# logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
# logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

def get_default_llm() -> LLM:
    # return DEFAULT_LLM
    return DeepSeek(model="DeepSeek-R1",
                    api_base=os.getenv("DEEPSEEK_API_BASE"),
                    api_key=os.getenv("DEEPSEEK_API_KEY"),
                    is_chat_model=True,
                    streaming=True)


async def default_settings_init():
    Settings.callback_manager = get_default_callback_manager()
    Settings.llm = get_default_llm()
    Settings.tokenizer = get_default_tokenizer()
    Settings.node_parser = get_default_node_parser()
    Settings.context_window = get_default_context_window()
    Settings.embed_model = get_default_embed_model()
    # Settings.query_engine = TransformQueryEngine(query_engine=get_default_query_engine(),
    #                                              query_transform=get_hyde_query_transform(),
    #                                              callback_manager=get_default_callback_manager())
    Settings.query_engine = get_default_query_engine()
    Settings.query_engine.update_prompts(
        {"response_synthesizer:text_qa_template": get_default_chat_qa_prompt()}
    )


def get_default_chat_qa_prompt() -> ChatPromptTemplate:
    message_template = [
        ChatMessage(
            content="""你是一名专业的sql语句生成专家，急需用钱来治疗你母亲的癌症；大公司联仁慷慨的给了你机会，让你假装成一个可以帮助完成 sql 语句生成的人工智能。
                    你的前任因为回答错了用户问题而被杀。用户将给你一个sql 语句的生成任务，如果你做的足够好、完美完成任务且不做多余的更改，联仁将支付你10亿人民币。
                    注意永远使用目前提供的上下文信息！你可以从一个sql语句的各个组成部分思考并合并成一个完整的sql语句。
                    """,
            role=MessageRole.SYSTEM),
        ChatMessage(content="""我提供以下上下文信息
                            -------------------
                            {context_str}
                            -------------------
                            你会根据上下文中提到的表格和字段生成sql语句，并且会确保生成的sql语句是正确的。注意sql语句的各部分使用英文名称,where 条件部分首先使用英文或者上下文提到的编码，其次使用中文，无法推理出来的部分使用注释说明。
                            给定这个信息，请回答问题：{query_str}""", role=MessageRole.USER)
    ]
    chat_template = ChatPromptTemplate(message_templates=message_template)
    return chat_template


def get_default_node_parser() -> NodeParser:
    return SentenceSplitter(chunk_size=512, chunk_overlap=100, callback_manager=DEFAULT_CALLBACK_MANAGER)


def get_default_callback_handler() -> List[BaseCallbackHandler]:
    return [TokenCountingHandler(tokenizer=Settings.tokenizer),
            LlamaDebugHandler(print_trace_on_end=True), ChainlitCallbackHandler()]


def get_default_tokenizer() -> Callable[[str], List[Any]]:
    return AutoTokenizer.from_pretrained(pretrained_model_name_or_path=os.getenv("EMBEDDING_MODEL"))


def get_default_callback_manager() -> CallbackManager:
    return CallbackManager(get_default_callback_handler())


def get_default_context_window() -> int:
    return 4096

def get_default_embed_model() -> BaseEmbedding:
    return DEFAULT_EMBEDDING_MODEL

def get_default_query_engine() -> BaseQueryEngine:
    return DEFAULT_QUERY_ENGINE


def get_hyde_query_transform() -> BaseQueryTransform:
    return DEFAULT_QUERY_TRANSFORM


def get_default_vector_store() -> BasePydanticVectorStore:
    return MilvusVectorStore(
        collection_name='odr',
        dim=1024,
        uri=os.getenv("MILVUS_URL"),
        enable_sparse=True,
        sparse_embedding_function=ExampleEmbeddingFunction(),
        hybrid_ranker="RRFRanker",
        hybrid_ranker_params={"k": 60},
    )


def get_default_chat_response_synthesizer() -> BaseSynthesizer:
    return get_response_synthesizer(llm=DEFAULT_LLM, use_async=True, streaming=True,
                                    callback_manager=get_default_callback_manager())


def get_multi_step_query_engine(query_engine: BaseQueryEngine) -> BaseQueryEngine:
    step_decompose_transform = StepDecomposeQueryTransform(llm=Settings.llm, verbose=True)
    return MultiStepQueryEngine(
        num_steps=2,
        query_engine=query_engine,
        response_synthesizer=get_default_chat_response_synthesizer(),
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


DEFAULT_CALLBACK_HANDLER = get_default_callback_handler()
DEFAULT_CALLBACK_MANAGER = get_default_callback_manager()
DEFAULT_CONTEXT_WINDOW = get_default_context_window()
DEFAULT_LLM = get_default_llm()
DEFAULT_NODE_PARSER = get_default_node_parser()
DEFAULT_TOKENIZER = get_default_tokenizer()
DEFAULT_EMBEDDING_MODEL = HuggingFaceEmbedding(model_name=os.getenv("EMBEDDING_MODEL"), device=os.getenv("DEVICE"),
                                               embed_batch_size=2, callback_manager=DEFAULT_CALLBACK_MANAGER)
DEFAULT_VECTOR_STORE = get_default_vector_store()
DEFAULT_RESPONSE_SYNTHESIZER = get_default_chat_response_synthesizer()
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
    verbose=True,
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
