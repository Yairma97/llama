import os

from chainlit import LlamaIndexCallbackHandler as ChainlitCallbackHandler
from langfuse.llama_index import LlamaIndexCallbackHandler as LangfuseCallbackHandler
from llama_index.core import Settings, VectorStoreIndex, get_response_synthesizer
from llama_index.core.callbacks import TokenCountingHandler, LlamaDebugHandler
from llama_index.core.indices.query.query_transform import HyDEQueryTransform
from llama_index.core.indices.vector_store import VectorIndexRetriever
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.query_engine import RetrieverQueryEngine, TransformQueryEngine
from llama_index.core.vector_stores.types import VectorStoreQueryMode
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.postprocessor.flag_embedding_reranker import FlagEmbeddingReranker
from llama_index.vector_stores.milvus import MilvusVectorStore
from transformers import AutoTokenizer

from embedding import ExampleEmbeddingFunction


# logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
# logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

async def global_settings_init():
    Settings.text_splitter = SentenceSplitter(chunk_size=512, chunk_overlap=100)
    Settings.tokenizer = AutoTokenizer.from_pretrained(pretrained_model_name_or_path=os.getenv("EMBEDDING_MODEL"))
    Settings.embed_model = HuggingFaceEmbedding(model_name=os.getenv("EMBEDDING_MODEL"), device='cpu',
                                                embed_batch_size=2)
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
    langfuse_callback_handler = LangfuseCallbackHandler()
    token_counter = TokenCountingHandler(tokenizer=Settings.tokenizer)
    llama_debug = LlamaDebugHandler(print_trace_on_end=True)
    chainlit_handler = ChainlitCallbackHandler()
    Settings.callback_manager.add_handler(langfuse_callback_handler)
    Settings.callback_manager.add_handler(token_counter)
    Settings.callback_manager.add_handler(llama_debug)
    Settings.callback_manager.add_handler(chainlit_handler)
    Settings.context_window = 4096

    vector_store = MilvusVectorStore(
        dim=1024,
        uri="http://localhost:19530",
        # overwrite=True,
        enable_sparse=True,
        sparse_embedding_function=ExampleEmbeddingFunction(),
        hybrid_ranker="RRFRanker",
        hybrid_ranker_params={"k": 60},
    )
    index = VectorStoreIndex.from_vector_store(vector_store, use_async=True, show_progress=True)
    retriever = VectorIndexRetriever(
        callback_manager=Settings.callback_manager,
        index=index,
        similarity_top_k=10,
        vector_store_query_mode=VectorStoreQueryMode.HYBRID,
    )
    response_synthesizer = get_response_synthesizer(use_async=True, streaming=True)
    reranker = FlagEmbeddingReranker(
        top_n=4,
        model=os.getenv("RERANK_MODEL"),
        use_fp16=False
    )
    query_engine = RetrieverQueryEngine.from_args(
        retriever=retriever,
        response_synthesizer=response_synthesizer,
        node_postprocessors=[reranker],
    )
    # QueryTransform
    hyde = HyDEQueryTransform(include_original=True)
    Settings.query_engine = TransformQueryEngine(query_engine=query_engine, query_transform=hyde,callback_manager=Settings.callback_manager)
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
