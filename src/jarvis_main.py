from ollama import chat
import time
from transformers import pipeline,AutoModelForCausalLM

def sample_dataset():
    ls = [
        {'role': 'user', 'content': 'How many countries are there in this world? Just tell me in one line'},
        {'role': 'assistant', 'content': 'Tell me in 3 lines who Theodore Roosevelt was'},
        {'role': 'user', 'content': 'Write me a essay about the film: Inglorious Bastards'},
       
    ]
    return ls


if __name__ == '__main__':
    dset = sample_dataset()
    times = []
    MODE='coreml'
    for example in dset:
        #inp = input('You: ')
        start = time.time()
        if MODE == 'ollama':
            stream = chat(
                model='llama3.2',
                messages=[example],
                stream=True
            )
            print('Jarvis: ', end='', flush=True)
            for chunk in stream:
                print(chunk['message']['content'], end='', flush=True)
            end = time.time()
            times.append(end - start)
            print('\n')
    
        elif MODE == 'mlx-hf':
            
            
            pipe = pipeline("text-generation", model="mlx-community/Llama-3.2-3B-Instruct")
            start  = time.time()
            out = pipe([example])
            end = time.time()
            times.append(end - start)
            print("OP: ",out)
        
        elif MODE == 'coreml':
            model = AutoModelForCausalLM.from_pretrained("andmev/Llama-3.2-3B-Instruct-CoreML")
            # pipe = pipeline("text-generation", model="andmev/Llama-3.2-3B-Instruct-CoreML")
            # start  = time.time()
            # out = pipe([example])
            # end = time.time()
            # times.append(end - start)
            # print("OP: ",out)

    print(times)
    print('Average time: ', sum(times) / len(times))
