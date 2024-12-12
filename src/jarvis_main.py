from ollama import chat
from rich import print
from transformers import AutoProcessor, BarkModel
import scipy
from gtts import gTTS
import playsound


def get_bark_tts(chunk):
    processor = AutoProcessor.from_pretrained("suno/bark-small")
    model = BarkModel.from_pretrained("suno/bark-small")

    voice_preset = "v2/en_speaker_6"

    inputs = processor(chunk, voice_preset=voice_preset)

    audio_array = model.generate(**inputs)
    audio_array = audio_array.cpu().numpy().squeeze()

    sample_rate = model.generation_config.sample_rate
    scipy.io.wavfile.write("bark_out.wav", rate=sample_rate, data=audio_array)


def get_gtts(chunk):
    tts = gTTS(chunk, lang="en")
    tts.save("audio_files/temp.mp3")
    playsound.playsound("audio_files/temp.mp3")


if __name__ == "__main__":
    messages = [
        {
            "role": "system",
            "content": "Your name is Jarvis, You are a helpful and polite assistant like Tony Stark's Jarvis.",
        }
    ]
    welcome_message = (
        "Hello! I'm Jarvis, your personal assistant. How can I help you today?"
    )
    messages.append({"role": "assistant", "content": welcome_message})

    get_gtts(welcome_message)

    while True:
        inp = input("You: ")
        if inp == "exit":
            break
        messages.append({"role": "user", "content": inp})

        stream = chat(model="llama3.2", messages=messages, stream=True)
        out = ""
        for chunk in stream:
            out += chunk["message"]["content"]

        get_gtts(out)

        messages.append({"role": "assistant", "content": out})
        print("\n")
