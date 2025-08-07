import logging
import speech_recognition as sr
from pydub import AudioSegment
from io import BytesIO

logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(levelname)s - %(message)s')


def record_audio(file_path,timeout=20,phrase_time_limit=None):
    
    recognizer=sr.Recognizer()
    
    try:
        with sr.Microphone() as source:
            logging.info("adjusting for amnient noise")
            recognizer.adjust_for_ambient_noise(source,duration=1)
            logging.info("start speking now")
            
            audio_data=recognizer.listen(source,timeout=timeout,phrase_time_limit=phrase_time_limit)
            logging.info("recording complted")
            
            
            wav_data=audio_data.get_wav_data()
            audio_segment=AudioSegment.from_wav(BytesIO(wav_data))
            audio_segment.export(file_path,format="mp3", bitrate="128k")
            
            logging.info(f"audio saved to {file_path}")
            
    except Exception as e:
        logging.error(f"Error recording audio: {e}")
        
#record_audio("output1.mp3")
audio_path="final.mp3"
import os
from groq import Groq

from dotenv import load_dotenv
load_dotenv()
#GROQ_API_KEY=os.environ.get("GROQ_API_KEY")
#stt_model="whisper-large-v3"

def transcribe_with_groq(GROQ_API_KEY,stt_model, audio_path):
    client=Groq(api_key=GROQ_API_KEY)
    
    audio_file=open(audio_path,"rb")
    transcription=client.audio.transcriptions.create(
        model=stt_model,
        file=audio_file,
        language="en"
    )

    return transcription.text