from __future__ import annotations

import logging
from dotenv import load_dotenv

from livekit import rtc
from livekit.agents import AutoSubscribe, JobContext, WorkerOptions, cli, llm

from livekit.agents.multimodal import MultimodalAgent
from livekit.agents.pipeline import VoicePipelineAgent
from livekit.agents.voice_assistant import VoiceAssistant
from livekit.plugins import openai, silero
#from functions import Functions
from AgentFunctions import agent_functions

load_dotenv(dotenv_path=".env")
logger = logging.getLogger("my-worker")
logger.setLevel(logging.INFO)


async def entrypoint(ctx: JobContext) -> None:
    logger.info("Starting worker...")

    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    participant = await ctx.wait_for_participant()

    # run_voice_assistant(ctx)
    await run_agent(ctx, participant, type="VOICE")

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
        fnc_ctx=Functions(),
        allow_interruptions=True,
        interrupt_speech_duration=0.5,
    )

    voice_assistant.start(ctx.room)

    voice_assistant.say(
        "Hi! I am Jarvis, your personal assistant. How can I help you today?"
    )


async def run_agent(ctx: JobContext, participant: rtc.Participant, type="MULTIMODAL"):
    initial_context = llm.ChatContext().append(
        role="system",
        text=("Your name is Jarvis, You are a helpful and polite personal assistant"),
    )

    if type == "MULTIMODAL":
        model = openai.realtime.RealtimeModel(
            instructions="You are a helpful and polite assistant. Answer the user's questions in a friendly and concise manner.",
            modalities=["audio", "text"],
        )
        agent = MultimodalAgent(
            model=model,
            chat_ctx=initial_context,
        )
        agent.start(ctx.room, participant)

        session = model.sessions[0]
        session.conversation.item.create(
            llm.ChatMessage(
                role="assistant",
                content="""
                Hello! I'm Jarvis, your personal assistant. How can I help you today?
                """,
            )
        )

        session.response.create()

    elif type == "VOICE":
        llm_openai = openai.LLM(model="gpt-4o-mini")

        agent = VoicePipelineAgent(
            vad=silero.VAD.load(),
            stt=openai.STT(),
            llm=llm_openai,
            tts=openai.TTS(),
            chat_ctx=initial_context,
            fnc_ctx=agent_functions.Functions(),
            allow_interruptions=True,
            interrupt_speech_duration=0.5,
        )

        agent.start(ctx.room, participant)

        await agent.say(
            "Hi! I am Jarvis, your own personal assistant. How can I help you today?"
        )


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
