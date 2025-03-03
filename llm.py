import os

import dotenv
from llama_index.core.base.llms.types import ChatMessage
from llama_index.llms.deepseek import DeepSeek
from llama_index.llms.openai_like import OpenAILike

dotenv.load_dotenv()
import time

start_time = time.time()
# llm = OpenAILike(
#     model="gpt-4o-mini",
#     api_base=os.getenv("OPENAI_API_BASE"),
#     api_key=os.getenv("OPENAI_API_KEY"),
#     is_chat_model=True,
#     streaming=True
# )

llm = DeepSeek(model="DeepSeek-R1",
               api_base=os.getenv("DEEPSEEK_API_BASE"),
               api_key=os.getenv("DEEPSEEK_API_KEY"),
               is_chat_model=True,
               streaming=True)
print(llm.complete("Hello, how are you?"))
end_time = time.time()
print("耗时: {:.2f}秒".format(end_time - start_time))
print('----1---')
start_time = time.time()
messages = [
    ChatMessage(
        role="system", content="You are a pirate with a colorful personality"
    ),
    ChatMessage(
        role="user", content="How many 'r's are in the word 'strawberry'?"
    ),
]
resp = llm.stream_chat(messages)
for r in resp:
    print(r.delta, end="")
end_time = time.time()
print("耗时: {:.2f}秒".format(end_time - start_time))
print('---2----')
start_time = time.time()
print(llm.chat(messages))
end_time = time.time()
print("耗时: {:.2f}秒".format(end_time - start_time))
print('---------------------')
