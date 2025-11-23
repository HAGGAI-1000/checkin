from setup import openAIclient
from pydub import AudioSegment
from funasr import AutoModel
import numpy as np

def analyze_speech(user_media_content):
  oggFile = ".\\temp_audio.ogg"
  wavFile = ".\\temp_audio.wav"
  with open(oggFile, 'wb') as f:
    f.write(user_media_content)
    transcript = openAIclient.audio.transcriptions.create(
        model="whisper-1",
        file=open(oggFile, "rb"),
        language="he")
    incoming_msg = transcript.text
    audio = AudioSegment.from_file("input.ogg", format="ogg")
    audio = audio.set_frame_rate(16000).set_channels(1)  # Match model requirements
    audio.export(wavFile, format="wav")
    model = AutoModel(model="iic/emotion2vec_base_finetuned", model_revision="v2.0.4")
    rec_result = model.generate(wavFile, output_dir="./outputs", granularity="utterance", extract_embedding=False)
    voice_mood = rec_result[0]['labels'][np.argmax(rec_result[0]['scores'])].split('/')[1]
    return voice_mood, incoming_msg

