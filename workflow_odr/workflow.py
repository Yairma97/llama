import asyncio
import os
import sys

import nest_asyncio
nest_asyncio.apply()
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(project_root))
from llama_index.core.workflow import Workflow, StartEvent, StopEvent, step, Event, Context, draw_all_possible_flows
from common.default import get_default_callback_manager, get_default_llm, get_default_tokenizer, \
    get_default_node_parser, get_default_context_window, get_default_embed_model, get_default_query_engine


class QuestionTransformEvent(Event):
    hyde_question: str
    original_question: str


class ProgressEvent(Event):
    msg: str


class Text2SQLWorkflow(Workflow):
    llm = get_default_llm()
    query_engine = get_default_query_engine()

    @step()
    async def on_start(self, ev: StartEvent) -> QuestionTransformEvent:
        """
        Hyde the question and return the transformed question.
        """
        question = ev.question
        print(f"Received question: {question}")
        # prompt = f"以下是关于某个指标口径的描述，用户将要通过以下口径生成 sql 语句；要求：1.理解口径信息；2.给出对生成 sql 语句 各组成部分的预测但不具体生成 sql；3.要求回答简洁只需要给出预测的内容。 口径：{question}"
        # hyde = await self.llm.acomplete(prompt)
        # print(f"Hyde Response: {hyde}")
        hyde = ""
        return QuestionTransformEvent(hyde_question=str(hyde), original_question=question)

    @step
    async def on_stop(self, ctx: Context, ev: QuestionTransformEvent) -> StopEvent:
        llm_response = await self.query_engine.aquery(ev.original_question)
        async for token in llm_response.async_response_gen():
            ctx.write_event_to_stream(ProgressEvent(msg=token))
        return StopEvent(result="Workflow complete.")


async def main():
    w = Text2SQLWorkflow(timeout=60, verbose=True)
    handler = w.run(question="急性心肌梗死结算出院患者的总例数（来源：病案系统），急性心肌梗死定义：主要诊断ICD-10编码为的所有非产妇出院患者。排除编码：I21.302 冠状动脉旁路术后心肌梗塞，I21.303冠状动脉介入治疗术后心肌梗塞；按上述口径描述生成 sql")

    async for ev in handler.stream_events():
        if isinstance(ev, ProgressEvent):
            print(ev.msg)


if __name__ == "__main__":
    asyncio.run(main())
