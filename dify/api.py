from typing import AsyncGenerator

import nest_asyncio
from fastapi import FastAPI
from llama_index.core import QueryBundle, ChatPromptTemplate
from llama_index.core.base.llms.types import ChatMessage, MessageRole
from llama_index.core.schema import MetadataMode

from sse_starlette import EventSourceResponse
from starlette.responses import StreamingResponse

from common.default import get_default_query_engine, get_default_llm
import uvicorn

nest_asyncio.apply()
query_engine = get_default_query_engine()
app = FastAPI()


# 创建流式接口
@app.get("/stream")
async def stream(query: str) -> StreamingResponse:
    return StreamingResponse(generate(query))


@app.get("/sse")
async def sse(query: str) -> EventSourceResponse:
    return EventSourceResponse(generate(query))


@app.get("/sql")
async def sql(query: str) -> EventSourceResponse:
    local_query_engine = query_engine
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
    res = await local_query_engine.aquery(query)

    return EventSourceResponse(generate(query))


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
