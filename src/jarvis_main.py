from ollama import chat
from rich import print
import speech_recognition as sr

from tts import get_melo_tts


def get_stt():
    # Initialize the recognizer
    r = sr.Recognizer()

    # Use the default microphone as the audio source
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)

    # Recognize speech using Google Speech Recognition
    try:
        text = r.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print(
            "Could not request results from Google Speech Recognition service; {0}".format(
                e
            )
        )


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

    get_melo_tts(welcome_message)

    while True:
        print("Say something....")
        inp = get_stt()
        print("You: ", inp)
        if inp == "exit":
            break
        messages.append({"role": "user", "content": inp})

        stream = chat(model="llama3.2", messages=messages, stream=True)
        out = ""
        k = 0
        for chunk in stream:
            out += chunk["message"]["content"]
            k += 1
            # if k!=0 and k%5==0:
            #     get_melo_tts(out)
            #     out = ""
        get_melo_tts(out)

        messages.append({"role": "assistant", "content": out})
        print("\n")
