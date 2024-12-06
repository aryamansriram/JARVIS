from ollama import chat


if __name__ == "__main__":
    messages = []
    while True:
        inp = input("You: ")
        if inp == "exit":
            break
        messages.append({"role": "user", "content": inp})

        stream = chat(model="llama3.2", messages=messages, stream=True)
        out = ""
        for chunk in stream:
            print(chunk["message"]["content"], end="", flush=True)
            out += chunk["message"]["content"]

        messages.append({"role": "assistant", "content": out})
        print("\n")
