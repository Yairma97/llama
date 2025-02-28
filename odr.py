import asyncio
import os
import textwrap

import chainlit
import dotenv
import nest_asyncio
from chainlit.cli import run_chainlit
from langfuse.llama_index import LlamaIndexCallbackHandler
from llama_index.core import VectorStoreIndex, Settings
from llama_index.core.base.response.schema import AsyncStreamingResponse
from llama_index.core.callbacks import TokenCountingHandler, LlamaDebugHandler
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.openai_like import OpenAILike
from llama_index.vector_stores.milvus import MilvusVectorStore
from transformers import AutoTokenizer

from embeddingfunction import ExampleEmbeddingFunction

nest_asyncio.apply()
dotenv.load_dotenv()


# logging.basicConfig(stream=sys.stdout, level=logging.INFO)
# logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

async def global_settings_init():
    Settings.text_splitter = SentenceSplitter(chunk_size=512, chunk_overlap=100)
    Settings.tokenizer = AutoTokenizer.from_pretrained(pretrained_model_name_or_path=os.getenv("EMBEDDING_MODEL"))
    Settings.embed_model = HuggingFaceEmbedding(model_name=os.getenv("EMBEDDING_MODEL"), device='cpu',
                                                embed_batch_size=2)
    Settings.llm = OpenAILike(
        model="gpt-4o-mini",
        api_base=os.getenv("OPENAI_API_BASE"),
        api_key=os.getenv("OPENAI_API_KEY"),
        is_chat_model=True,
        streaming=True
    )
    # langfuse_callback_handler = LlamaIndexCallbackHandler()
    # token_counter = TokenCountingHandler(tokenizer=Settings.tokenizer)
    # llama_debug = LlamaDebugHandler(print_trace_on_end=True)
    chainlit_handler = chainlit.LlamaIndexCallbackHandler()
    # Settings.callback_manager.add_handler(langfuse_callback_handler)
    # Settings.callback_manager.add_handler(token_counter)
    # Settings.callback_manager.add_handler(llama_debug)
    Settings.callback_manager.add_handler(chainlit_handler)
    Settings.context_window = 4096
    Settings.query_engine = (VectorStoreIndex.from_vector_store(vector_store=MilvusVectorStore(
        dim=1024,
        uri="http://localhost:19530",
        # overwrite=True,
        enable_sparse=True,
        sparse_embedding_function=ExampleEmbeddingFunction(),
        hybrid_ranker="RRFRanker",
        hybrid_ranker_params={"k": 60},
    ), use_async=True).as_query_engine(vector_store_query_mode="hybrid", streaming=True))


async def reset_callback_handlers():
    handles = Settings.callback_manager.handlers
    for handle in handles:
        if isinstance(handle, LlamaIndexCallbackHandler):
            handle.flush()
        if isinstance(handle, TokenCountingHandler):
            handle.reset_counts()
        if isinstance(handle, LlamaDebugHandler):
            handle.flush_event_logs()
        if isinstance(handle, chainlit.LlamaIndexCallbackHandler):
            handle.reset_counts()


@chainlit.on_chat_start
async def on_chat_start():
    chainlit.user_session.set("query_engine", Settings.query_engine)
    await chainlit.Message(
        author="Assistant", content="Hello! Im an AI assistant. How may I help you?"
    ).send()


@chainlit.on_stop
async def on_stop():
    print("The user on_stop!")


@chainlit.on_chat_resume
async def on_chat_resume():
    print("The user on_chat_resume!")



@chainlit.on_chat_end
async def on_chat_end():
    print("The user disconnected!")
    await reset_callback_handlers()


@chainlit.on_message
async def on_message(msg: chainlit.Message):
    print("The user sent: ", msg.content)
    query_engine = chainlit.user_session.get("query_engine")
    llm_response = await query_engine.aquery(msg.content)
    resp = chainlit.Message(content="", author="Assistant")
    async for token in llm_response.async_response_gen():
        await resp.stream_token(token)
    print("The assistant sent: ", resp.content)


async def main():
    print("Initializing global")
    await global_settings_init()
    print("global Settings initialized!")


if __name__ == "__main__":
    asyncio.run(main())
    run_chainlit(__file__)
