import numpy as np
import torch
from gtts import gTTS
import playsound
import os
os.environ['PYTORCH_ENABLE_MPS_FALLBACK'] = '1'

from melo.api import TTS


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

def get_melo_tts(chunk):
    
    # Speed is adjustable
    speed = 1.0

    # CPU is sufficient for real-time inference.
    # You can set it manually to 'cpu' or 'cuda' or 'cuda:0' or 'mps'
    device = 'cpu' # Will automatically use GPU if available

    # English 
    text = chunk
    model = TTS(language='EN', device=device)
    speaker_ids = model.hps.data.spk2id

    output_path = 'audio_files/en-brit.wav'
    model.tts_to_file(text, speaker_ids['EN-BR'], output_path, speed=speed)
    playsound.playsound(output_path)

if __name__ == "__main__":
    from RealtimeTTS import TextToAudioStream, SystemEngine, AzureEngine, ElevenlabsEngine

    engine = SystemEngine() # replace with your TTS engine
    stream = TextToAudioStream(engine)
    stream.feed("Hello world! How are you today?")
    stream.play_async()