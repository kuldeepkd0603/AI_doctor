import os 
from  gtts import gTTS

def text_to_speech_with_gtts_old(text,output_file_path):
    language='en'
    
    audioobject=gTTS(text=text,lang=language,slow=False)
    
    audioobject.save(output_file_path)
    
input_text="Hello, this is a kuldeep from dewas."
#text_to_speech_with_gtts_old(input_text,"output.mp3")


import elevenlabs
from dotenv import load_dotenv
load_dotenv()
from elevenlabs.client import ElevenLabs

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")



def text_speech_with_elevenlabs_old(text,output_file_path):
    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
    audio = client.text_to_speech.convert(
        text=text,
        voice_id="WnFIhLMD7HtSxjuKKrfY",
        output_format="mp3_44100_128",
        model_id="eleven_turbo_v2"
    )
    
    with open(output_file_path, "wb") as f:
        for chunk in audio:
            f.write(chunk)
    #elevenlabs.save_audio(audio, output_file_path)
#text_speech_with_elevenlabs_old(input_text,"elevel_output.mp3")


import subprocess
import platform

def text_to_speech_with_gtts(text,output_file_path):
    language='en'
    
    audioobject=gTTS(text=text,lang=language,slow=False)
    
    audioobject.save(output_file_path)
    os_name = platform.system()
    try:
        if os_name == "Darwin":  # macOS
            subprocess.run(['afplay', output_file_path])
        elif os_name == "Windows":  # Windows
            subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer "{output_file_path}").PlaySync();'])
        elif os_name == "Linux":  # Linux
            subprocess.run(['aplay', output_file_path])  # Alternative: use 'mpg123' or 'ffplay'
        else:
            raise OSError("Unsupported operating system")
    except Exception as e:
        print(f"An error occurred while trying to play the audio: {e}")
    
    
input_text="Hello, this is a kuldeep from dewas."
text_to_speech_with_gtts(input_text,"output.mp3")



def text_speech_with_elevenlabs(input_text,output_file_path):
    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
    audio = client.text_to_speech.convert(
        text=input_text,
        voice_id="lfQ3pGxnwOiKjnQKdwts",
        output_format="mp3_44100_128",
        model_id="eleven_turbo_v2"
    )
    
    with open(output_file_path, "wb") as f:
        for chunk in audio:
            f.write(chunk)
    #elevenlabs.save_audio(audio, output_file_path)
    
    os_name = platform.system()
    try:
        if os_name == "Darwin":  # macOS
            subprocess.run(['afplay', output_file_path])
        elif os_name == "Windows":  # Windows
            subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer "{output_file_path}").PlaySync();'])
        elif os_name == "Linux":  # Linux
            subprocess.run(['aplay', output_file_path])  # Alternative: use 'mpg123' or 'ffplay'
        else:
            raise OSError("Unsupported operating system")
    except Exception as e:
        print(f"An error occurred while trying to play the audio: {e}")
#text_speech_with_elevenlabs(input_text,"elevel_output.mp3")