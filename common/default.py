import os
from typing import Callable, List, Any

import dotenv
from langchain_core.output_parsers import BaseOutputParser, JsonOutputParser
from llama_index.core import Settings, get_response_synthesizer, BaseCallbackHandler, ChatPromptTemplate, \
    VectorStoreIndex
from llama_index.core.base.base_query_engine import BaseQueryEngine
from llama_index.core.base.base_retriever import BaseRetriever
from llama_index.core.base.embeddings.base import BaseEmbedding
from llama_index.core.base.llms.types import MessageRole, ChatMessage
from llama_index.core.callbacks import CallbackManager, TokenCountingHandler, LlamaDebugHandler
from llama_index.core.indices.query.query_transform import StepDecomposeQueryTransform
from llama_index.core.indices.query.query_transform.base import BaseQueryTransform
from llama_index.core.indices.vector_store import VectorIndexRetriever
from llama_index.core.llms import LLM
from llama_index.core.node_parser import NodeParser, SentenceSplitter
from llama_index.core.postprocessor.types import BaseNodePostprocessor
from llama_index.core.query_engine import SubQuestionQueryEngine, MultiStepQueryEngine, RetrieverQueryEngine
from llama_index.core.response_synthesizers import BaseSynthesizer
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.vector_stores.types import BasePydanticVectorStore, VectorStoreQueryMode
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.output_parsers.langchain import LangchainOutputParser
from llama_index.postprocessor.flag_embedding_reranker import FlagEmbeddingReranker
from llama_index.vector_stores.milvus import MilvusVectorStore
from pydantic import BaseModel, Field
from transformers import AutoTokenizer
from langchain.output_parsers import StructuredOutputParser, ResponseSchema

from common.embedding import ExampleEmbeddingFunction

# 获取当前环境
environment = os.getenv('ENVIRONMENT', 'dev')

# 加载对应环境的 .env.dev 文件
print("common.default.py")
env_file = f'.env.{environment}'

dotenv.load_dotenv(env_file)
print("env_file", env_file)
print("EMBEDDING_MODEL", os.getenv("EMBEDDING_MODEL"))
print("DEEPSEEK_API_BASE", os.getenv("DEEPSEEK_API_BASE"))


class SQL(BaseModel):
    sql: str = Field(description="根据用户提问生成的sql 语句")

def get_default_llm() -> LLM:
    return OpenAI(
        model="gpt-4o-mini",
        api_base=os.getenv("OPENAI_API_BASE"),
        api_key=os.getenv("OPENAI_API_KEY"),
        is_chat_model=True,
        streaming=True
    )
    # return DeepSeek(model="DeepSeek-R1",
    #                 api_base=os.getenv("DEEPSEEK_API_BASE"),
    #                 api_key=os.getenv("DEEPSEEK_API_KEY"),
    #                 is_chat_model=True,
    #                 streaming=True)


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
    return SentenceSplitter(chunk_size=512, chunk_overlap=100, callback_manager=get_default_callback_manager())


def get_default_callback_handler() -> List[BaseCallbackHandler]:
    return [TokenCountingHandler(tokenizer=get_default_tokenizer()),
            LlamaDebugHandler(print_trace_on_end=True)]


def get_default_tokenizer() -> Callable[[str], List[Any]]:
    return AutoTokenizer.from_pretrained(pretrained_model_name_or_path=os.getenv("EMBEDDING_MODEL"))


def get_default_callback_manager() -> CallbackManager:
    return CallbackManager(get_default_callback_handler())


def get_default_context_window() -> int:
    return 4096


def get_default_embed_model() -> BaseEmbedding:
    return HuggingFaceEmbedding(model_name=os.getenv("EMBEDDING_MODEL"), device=os.getenv("DEVICE"),
                                embed_batch_size=2, callback_manager=get_default_callback_manager())


def get_default_vector_store() -> BasePydanticVectorStore:
    return MilvusVectorStore(
        collection_name=os.getenv("COLLECTION_NAME"),
        dim=1024,
        uri=os.getenv("MILVUS_URL"),
        enable_sparse=True,
        sparse_embedding_function=ExampleEmbeddingFunction(),
        hybrid_ranker="RRFRanker",
        hybrid_ranker_params={"k": 60},
    )


def get_default_chat_response_synthesizer() -> BaseSynthesizer:
    return get_response_synthesizer(llm=get_default_llm(), use_async=True, streaming=True,
                                    callback_manager=get_default_callback_manager())


def get_multi_step_query_engine(query_engine: BaseQueryEngine) -> BaseQueryEngine:
    step_decompose_transform = StepDecomposeQueryTransform(llm=get_default_llm(), verbose=True)
    return MultiStepQueryEngine(
        num_steps=2,
        query_engine=query_engine,
        response_synthesizer=get_default_chat_response_synthesizer(),
        query_transform=step_decompose_transform,
    )


def get_default_index() -> VectorStoreIndex:
    return VectorStoreIndex.from_vector_store(get_default_vector_store(), embed_model=get_default_embed_model(),
                                              callback_manager=get_default_callback_manager(), use_async=True,
                                              show_progress=True)


def get_default_retriever() -> BaseRetriever:
    return VectorIndexRetriever(
        verbose=True,
        index=get_default_index(),
        callback_manager=get_default_callback_manager(),
        similarity_top_k=10,
        vector_store_query_mode=VectorStoreQueryMode.HYBRID,
    )


def get_default_rerank() -> BaseNodePostprocessor:
    return FlagEmbeddingReranker(
        top_n=4,
        model=os.getenv("RERANK_MODEL"),
        use_fp16=False
    )

def get_sql_output_parser() -> LangchainOutputParser:
    lc_output_parser = JsonOutputParser(pydantic_object=SQL)
    return LangchainOutputParser(lc_output_parser)

def get_default_query_engine() -> BaseQueryEngine:
    return RetrieverQueryEngine.from_args(
        retriever=get_default_retriever(),
        response_synthesizer=get_default_chat_response_synthesizer(),
        node_postprocessors=[get_default_rerank()],
        callback_manager=get_default_callback_manager(),
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
