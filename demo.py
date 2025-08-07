import os
from gtts import gTTS
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from pydub import AudioSegment
import subprocess
import platform

load_dotenv()
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

def convert_to_wav(input_file, output_file):
    sound = AudioSegment.from_file(input_file)
    sound.export(output_file, format="wav")

def play_audio(file_path):
    os_name = platform.system()
    try:
        if os_name == "Darwin":
            subprocess.run(['afplay', file_path])
        elif os_name == "Windows":
            subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer "{file_path}").PlaySync();'])
        elif os_name == "Linux":
            subprocess.run(['aplay', file_path])
        else:
            raise OSError("Unsupported operating system")
    except Exception as e:
        print(f"An error occurred while trying to play the audio: {e}")

def text_to_speech_with_gtts(input_text, output_mp3_path, output_wav_path):
    tts = gTTS(text=input_text, lang='en', slow=False)
    tts.save(output_mp3_path)
    convert_to_wav(output_mp3_path, output_wav_path)
    play_audio(output_wav_path)

def text_speech_with_elevenlabs(input_text, output_mp3_path, output_wav_path):
    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
    audio = client.text_to_speech.convert(
        text=input_text,
        voice_id="lfQ3pGxnwOiKjnQKdwts",
        output_format="mp3_44100_128",
        model_id="eleven_turbo_v2"
    )
    with open(output_mp3_path, "wb") as f:
        for chunk in audio:
            f.write(chunk)
    convert_to_wav(output_mp3_path, output_wav_path)
    play_audio(output_wav_path)

#input_text = "Hello, this is Kuldeep from Dewas."

# Uncomment one of these based on what you want to run:
#text_to_speech_with_gtts(input_text, "output.mp3", "output.wav")
#text_speech_with_elevenlabs(input_text, "eleven_output.mp3", "eleven_output.wav")
