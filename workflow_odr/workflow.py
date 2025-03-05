import asyncio

from llama_index.core.workflow import Workflow, StartEvent, StopEvent, step, Event

from default import get_default_callback_manager, get_default_llm, get_default_tokenizer, \
    get_default_node_parser, get_default_context_window, get_default_embed_model, get_default_query_engine


class QuestionTransformEvent(Event):
    hyde_question: str
    original_question: str


class Text2SQLWorkflow(Workflow):
    callback_manager = get_default_callback_manager()
    llm = get_default_llm()
    tokenizer = get_default_tokenizer()
    node_parser = get_default_node_parser()
    context_window = get_default_context_window()
    embed_model = get_default_embed_model()
    query_engine = get_default_query_engine()

    @step()
    async def on_start(self, ev: StartEvent) -> QuestionTransformEvent:
        """
        Hyde the question and return the transformed question.
        """
        question = ev.question
        print(f"Received question: {question}")
        prompt = f"以下是关于某个指标口径的描述，用户将要通过以下口径生成 sql 语句；要求：1.理解口径信息；2.给出对生成 sql 语句 各组成部分的预测但不具体生成 sql；3.要求回答简洁只需要给出预测的内容。 口径：{question}"
        hyde = await self.llm.acomplete(prompt)
        print(f"Hyde Response: {hyde}")
        return QuestionTransformEvent(hyde_question=str(hyde), original_question=question)

    @step
    async def on_stop(self, ev: QuestionTransformEvent) -> StopEvent:
        return StopEvent()


text2sqlWorkflow = Text2SQLWorkflow(timeout=30, verbose=True)


async def main():
    print(await text2sqlWorkflow.run(
        question="三级评审第七章定义的糖尿病伴短期与长期并发症出院患者15日内再住院例数（来源：病案系统），糖尿病伴短期与长期并发症定义：主要诊断编码为ICD-10: E10-E14的所有非产妇/非新生儿出院患者。合并症包括：酮症酸中毒、高渗透压、昏迷、肾脏、眼睛、神经、坏疽、循环或其他未特指并发症。排除编码：E10.9 1型糖尿病,E11.9 2型糖尿病,E12.9营养不良相关性糖尿病不伴并发症, E13.9 特指糖尿病, E14.9 糖尿病；根据以上指标口径生成 sql 语句"))


if __name__ == "__main__":
    asyncio.run(main())
