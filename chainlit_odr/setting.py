import os

import dotenv
from chainlit import LlamaIndexCallbackHandler
from langfuse.llama_index import LlamaIndexCallbackHandler as LangfuseCallbackHandler
from llama_index.core import Settings, VectorStoreIndex, get_response_synthesizer, ChatPromptTemplate
from llama_index.core.base.llms.types import ChatMessage, MessageRole
from llama_index.core.callbacks import TokenCountingHandler, LlamaDebugHandler, CallbackManager
from llama_index.core.indices.vector_store import VectorIndexRetriever
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.vector_stores.types import VectorStoreQueryMode
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.postprocessor.flag_embedding_reranker import FlagEmbeddingReranker
from llama_index.vector_stores.milvus import MilvusVectorStore
from transformers import AutoTokenizer

from common.embedding import ExampleEmbeddingFunction

# 获取当前环境
environment = os.getenv('ENVIRONMENT', 'dev')

# 加载对应环境的 .env.dev 文件
print("Setting.py")
env_file = f'.env.{environment}'

dotenv.load_dotenv(env_file)
print("env_file", env_file)
print("EMBEDDING_MODEL", os.getenv("EMBEDDING_MODEL"))
print("DEEPSEEK_API_BASE", os.getenv("DEEPSEEK_API_BASE"))


# logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
# logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

async def custom_settings_init():
    callback_manager = CallbackManager([TokenCountingHandler(tokenizer=Settings.tokenizer),
                                        LlamaDebugHandler(print_trace_on_end=True),
                                        LlamaIndexCallbackHandler()])
    # langfuse_callback_handler = LangfuseCallbackHandler()
    # callback_manager.add_handler(langfuse_callback_handler)
    Settings.callback_manager = callback_manager
    Settings.node_parser = SentenceSplitter(chunk_size=512, chunk_overlap=100, callback_manager=callback_manager)
    Settings.tokenizer = AutoTokenizer.from_pretrained(pretrained_model_name_or_path=os.getenv("EMBEDDING_MODEL"))
    Settings.embed_model = HuggingFaceEmbedding(model_name=os.getenv("EMBEDDING_MODEL"), device=os.getenv("DEVICE"),
                                                embed_batch_size=2, callback_manager=callback_manager)
    Settings.llm = OpenAI(
        model="gpt-4o-mini",
        api_base=os.getenv("OPENAI_API_BASE"),
        api_key=os.getenv("OPENAI_API_KEY"),
        is_chat_model=True,
        streaming=True
    )
    # Settings.llm = DeepSeek(model="DeepSeek-R1",
    #                         api_base=os.getenv("DEEPSEEK_API_BASE"),
    #                         api_key=os.getenv("DEEPSEEK_API_KEY"),
    #                         is_chat_model=True,
    #                         streaming=True)

    Settings.context_window = 4096
    vector_store = MilvusVectorStore(
        collection_name='odr',
        dim=1024,
        uri=os.getenv("MILVUS_URL"),
        # overwrite=True,
        enable_sparse=True,
        sparse_embedding_function=ExampleEmbeddingFunction(),
        hybrid_ranker="RRFRanker",
        hybrid_ranker_params={"k": 60},
    )
    index = VectorStoreIndex.from_vector_store(vector_store, use_async=True, show_progress=True,
                                               embed_model=Settings.embed_model)
    retriever = VectorIndexRetriever(
        verbose=True,
        callback_manager=Settings.callback_manager,
        index=index,
        similarity_top_k=10,
        vector_store_query_mode=VectorStoreQueryMode.HYBRID,
    )
    response_synthesizer = get_response_synthesizer(llm=Settings.llm, use_async=True, streaming=True,
                                                    callback_manager=Settings.callback_manager)
    reranker = FlagEmbeddingReranker(
        top_n=4,
        model=os.getenv("RERANK_MODEL"),
        use_fp16=False
    )
    query_engine = RetrieverQueryEngine.from_args(
        llm=Settings.llm,
        retriever=retriever,
        response_synthesizer=response_synthesizer,
        node_postprocessors=[reranker],
        callback_manager=Settings.callback_manager,
    )
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
    query_engine.update_prompts(
        {"response_synthesizer:text_qa_template": chat_template}
    )
    Settings.query_engine = query_engine
    # QueryTransform
    # hyde = HyDEQueryTransform(include_original=True)
    # Settings.query_engine = TransformQueryEngine(query_engine=query_engine, query_transform=hyde,
    #                                              callback_manager=Settings.callback_manager)
    # step_decompose_transform = StepDecomposeQueryTransform(llm=Settings.llm, verbose=True)
    # Settings.query_engine = MultiStepQueryEngine(
    #     query_engine=query_engine,
    #     response_synthesizer=response_synthesizer,
    #     query_transform=step_decompose_transform,
    # )


async def reset_callback_handlers():
    handles = Settings.callback_manager.handlers
    for handle in handles:
        if isinstance(handle, LangfuseCallbackHandler):
            handle.flush()
        if isinstance(handle, TokenCountingHandler):
            handle.reset_counts()
        if isinstance(handle, LlamaDebugHandler):
            handle.flush_event_logs()
