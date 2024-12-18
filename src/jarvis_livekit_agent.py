from __future__ import annotations

import logging
from dotenv import load_dotenv

from livekit import rtc
from livekit.agents import AutoSubscribe, JobContext, WorkerOptions, cli, llm

from livekit.agents.multimodal import MultimodalAgent
from livekit.agents.voice_assistant import VoiceAssistant
from livekit.plugins import openai, silero

load_dotenv(dotenv_path=".env")
logger = logging.getLogger("my-worker")
logger.setLevel(logging.INFO)


async def entrypoint(ctx: JobContext) -> None:
    logger.info("Starting worker...")

    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    run_voice_assistant(ctx)

    logger.info("Agent started....")


def run_voice_assistant(ctx: JobContext):
    initial_context = llm.ChatContext().append(
        role="system",
        text=(
            "Your name is Jarvis, You are a helpful and polite assistant like Tony Stark's Jarvis."
        ),
    )
    voice_assistant = VoiceAssistant(
        vad=silero.VAD.load(),
        stt=openai.STT(),
        llm=openai.LLM(),
        tts=openai.TTS(),
        chat_ctx=initial_context,
        allow_interruptions=True,
    )

    voice_assistant.start(ctx.room)

    voice_assistant.say(
        "Hi! I am Jarvis, your personal assistant. How can I help you today?"
    )


def run_multimodal_agent(ctx: JobContext, participant: rtc.Participant):
    model = openai.realtime.RealtimeModel(
        instructions="Your name is Jarvis, You are a helpful and polite assistant like Tony Stark's Jarvis.",
        modalities=["audio"],
    )

    agent = MultimodalAgent(model=model)
    agent.start(ctx.room, participant)
    agent.say("Hi! I am Jarvis, your personal assistant. How can I help you today?")

    session = model.sessions[0]
    session.conversation.item.create(
        llm.ChatMessage(
            role="assistant",
            content="""Your name is Jarvis, You are a helpful and polite assistant like Tony Stark's Jarvis.
            Please begin your interaction consistent with the instructions given to you""",
        )
    )

    session.response.create()


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
