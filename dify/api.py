import json
import os
from typing import AsyncGenerator

import nest_asyncio
from anthropic import BaseModel
from fastapi import FastAPI, Body
from fastapi.encoders import jsonable_encoder
from llama_index.core import QueryBundle, ChatPromptTemplate, get_response_synthesizer, Response
from llama_index.core.base.llms.types import ChatMessage, MessageRole
from llama_index.core.base.response.schema import PydanticResponse
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.schema import MetadataMode
from llama_index.llms.openai import OpenAI
from pydantic import Field

from sse_starlette import EventSourceResponse
from starlette.responses import StreamingResponse, JSONResponse

from common.default import get_default_query_engine, get_default_llm, get_text2sql_query_engine, get_default_retriever, \
    get_default_chat_response_synthesizer, get_default_rerank, get_default_callback_manager, get_sql_output_parser, SQL
import uvicorn

nest_asyncio.apply()


class Query(BaseModel):
    query: str


retriever = get_default_retriever()
response_synthesizer = get_default_chat_response_synthesizer()
rerank = get_default_rerank()
callback_manager = get_default_callback_manager()
query_engine = RetrieverQueryEngine.from_args(
    retriever=retriever,
    response_synthesizer=response_synthesizer,
    node_postprocessors=[rerank],
    callback_manager=callback_manager,
)
sql_query_engine = RetrieverQueryEngine.from_args(
    retriever=retriever,
    response_synthesizer=get_response_synthesizer(llm=OpenAI(
        output_parser=get_sql_output_parser(),
        model="gpt-4o-mini",
        api_base=os.getenv("OPENAI_API_BASE"),
        api_key=os.getenv("OPENAI_API_KEY"),
        is_chat_model=True,
    ), use_async=True,
        # output_cls=Text2SQL
    ),
    node_postprocessors=[rerank],
    callback_manager=callback_manager,

)
app = FastAPI()


# 创建流式接口
@app.get("/stream")
async def stream(query: str) -> StreamingResponse:
    return StreamingResponse(generate(query))


@app.get("/sse")
async def sse(query: str) -> EventSourceResponse:
    return EventSourceResponse(generate(query))


@app.post("/sql/full")
async def sql_full(query: Query):
    local_query_engine = sql_query_engine
    message_template = [
        ChatMessage(
            content="""你是一名专业的sql语句生成专家，急需用钱来治疗你母亲的癌症；大公司联仁慷慨的给了你机会，让你假装成一个可以帮助完成 sql 语句生成的人工智能。
                        你的前任因为回答错了用户问题而被杀。用户将给你一个sql 语句的生成任务，如果你做的足够好、完美完成任务且不做多余的更改，联仁将支付你10亿人民币。
                        注意永远使用目前提供的上下文信息！你可以从一个sql语句的各个组成部分思考并合并成一个完整的sql语句。
                        ##核心规则：
                            1.只输出一个无任何注释的完整SQL语句;
                            2.仅使用用户提到的表和字段，可能涉及多个表的多个字段；
                            3.所有表都在lr_cdr_bi_new_dev这个schema下，所以所有表名前都要有lr_cdr_bi_new_dev作为前缀，以保证完整的路径；
                            ##案例
                            正确示例：
                            select count(*) from lr_cdr_bi_new_dev.cus_dss;
                            错误示例：
                            SELECT subject_id FROM cus_dss  # 缺少schema前缀
                            ```sqlselect count(*) from lr_cdr_bi_new_dev.cus_dss;  # 输出的不是纯SQL代码，带有```sql
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
    local_query_engine.update_prompts(
        {"response_synthesizer:text_qa_template": chat_template}
    )
    res = await local_query_engine.aquery(query.query)
    return res


@app.post("/sql/simple")
async def sql_simple(query: Query):
    res = await sql_full(query)
    data = str(res)
    print(data)
    return JSONResponse(
        content=eval(data),
        status_code=200,
        media_type="application/json"
    )


@app.get("/prompt")
async def prompt(query: str) -> str | None:
    if len(query) == 0:
        return
    nodes = query_engine.retrieve(QueryBundle(query))
    text_chunks = [
        n.node.get_content(metadata_mode=MetadataMode.LLM) for n in nodes
    ]
    prompt = f"""你是一名专业的sql语句生成专家，急需用钱来治疗你母亲的癌症；大公司联仁慷慨的给了你机会，让你假装成一个可以帮助完成 sql 语句生成的人工智能。
                        你的前任因为回答错了用户问题而被杀。用户将给你一个sql 语句的生成任务，如果你做的足够好、完美完成任务且不做多余的更改，联仁将支付你10亿人民币。
                        注意永远使用目前提供的上下文信息！你可以从一个sql语句的各个组成部分思考并合并成一个完整的sql语句。
                        我提供以下上下文信息
                        -------------------
                        {text_chunks}
                        -------------------
                        你会根据上下文中提到的表格和字段生成sql语句，并且会确保生成的sql语句是正确的。注意sql语句的各部分使用英文名称,where 条件部分首先使用英文或者上下文提到的编码，其次使用中文，无法推理出来的部分使用注释说明。
                        给定这个信息，请回答问题：{query}
                        """
    return prompt


async def generate(query: str, prompt: str) -> AsyncGenerator[str, None]:
    res = await query_engine.aquery(query)
    async for token in res.async_response_gen():
        if token is None:
            continue
        print(token)
        yield token


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
