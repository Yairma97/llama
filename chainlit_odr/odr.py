import asyncio
import logging
import sys

import chainlit
import dotenv
import nest_asyncio
from chainlit.cli import run_chainlit
from llama_index.core import Settings

from default import default_settings_init
from setting import reset_callback_handlers

nest_asyncio.apply()
dotenv.load_dotenv()

@chainlit.set_starters
async def set_starters():
    return [
        chainlit.Starter(
            label="Morning routine ideation",
            message="Can you help me create a personalized morning routine that would help increase my productivity throughout the day? Start by asking me about my current habits and what activities energize me in the morning.",
            icon="/public/idea.svg",
        ),

        chainlit.Starter(
            label="Explain superconductors",
            message="Explain superconductors like I'm five years old.",
            icon="/public/learn.svg",
        ),
        chainlit.Starter(
            label="Python script for daily email reports",
            message="Write a script to automate sending daily email reports in Python, and walk me through how I would set it up.",
            icon="/public/terminal.svg",
        ),
        chainlit.Starter(
            label="Text inviting friend to wedding",
            message="Write a text asking a friend to be my plus-one at a wedding next month. I want to keep it super short and casual, and offer an out.",
            icon="/public/write.svg",
        )
    ]


@chainlit.on_chat_start
async def on_chat_start():
    chainlit.user_session.set("query_engine", Settings.query_engine)
    print("The user connected!")


@chainlit.on_stop
async def on_stop():
    print("The user on_stop!")


@chainlit.on_chat_resume
async def on_chat_resume():
    chainlit.user_session.set("query_engine", Settings.query_engine)
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
    await default_settings_init()
    print("global Settings initialized!")


if __name__ == "__main__":
    print("Starting main")
    asyncio.run(main())
    run_chainlit(__file__)
