from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
import uuid

from brain_doc import encode_image, analyze_image_with_query
from voice_of_patient import transcribe_with_groq
from demo import text_speech_with_elevenlabs

load_dotenv()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

system_prompt = """You have to act as a professional doctor, I know you are not but this is for learning purposes. 
What's in this image? Do you find anything wrong with it medically? 
If you make a differential, suggest some remedies for them. Do not add any numbers or special characters in 
your response. Your response should be in one long paragraph. Also, always answer as if you are answering to a real person.
Do not say 'In the image I see' but say 'With what I see, I think you have ....'
Don't respond as an AI model in markdown, your answer should mimic that of an actual doctor, not an AI bot. 
Keep your answer concise (max 2 sentences). No preamble, start your answer right away please."""

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/process", methods=["POST"])
def process():
    audio_file = request.files['audio']
    image_file = request.files['image']


    audio_filename = secure_filename(str(uuid.uuid4()) + "_" + audio_file.filename)
    image_filename = secure_filename(str(uuid.uuid4()) + "_" + image_file.filename)

    audio_path = os.path.join(app.config['UPLOAD_FOLDER'], audio_filename)
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)

    audio_file.save(audio_path)
    image_file.save(image_path)

    
    speech_to_text_output = transcribe_with_groq(
        GROQ_API_KEY=os.environ.get("GROQ_API_KEY"),
        audio_path=audio_path,
        stt_model="whisper-large-v3"
    )


    if image_path:
        doctor_response = analyze_image_with_query(
            query=system_prompt + speech_to_text_output,
            encoded_image=encode_image(image_path),
            model="meta-llama/llama-4-scout-17b-16e-instruct"
        )
    else:
        doctor_response = "No image provided for me to analyze."

    mp3_path = os.path.join("static", "outputs", "doctor_output.mp3")
    wav_path = os.path.join("static", "outputs", "doctor_output.wav")
    os.makedirs(os.path.dirname(mp3_path), exist_ok=True)

    text_speech_with_elevenlabs(
        input_text=doctor_response,
        output_mp3_path=mp3_path,
        output_wav_path=wav_path
    )

    return jsonify({
        "transcription": speech_to_text_output,
        "response": doctor_response,
        "audio": "/" + wav_path,
        "image": "/" + image_path
    })

if __name__ == '__main__':
    app.run(debug=True)
