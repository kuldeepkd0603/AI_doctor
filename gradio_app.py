import os
import gradio as gr
from dotenv import load_dotenv

from brain_doc import encode_image, analyze_image_with_query
from voice_of_patient import transcribe_with_groq
from demo import text_speech_with_elevenlabs
from chat_memory import add_to_chat_memory, get_chat_context

load_dotenv()

system_prompt = """You have to act as a professional doctor, I know you are not but this is for learning purposes. 
What's in this image? Do you find anything wrong with it medically? 
If you make a differential, suggest some remedies for them. Do not add any numbers or special characters in 
your response. Your response should be in one long paragraph. Also, always answer as if you are answering to a real person.
Do not say 'In the image I see' but say 'With what I see, I think you have ....'
Don't respond as an AI model in markdown, your answer should mimic that of an actual doctor, not an AI bot. 
Keep your answer concise (max 2 sentences). No preamble, start your answer right away please."""


def format_chat_history(chat_history, max_turns=5):
    formatted = ""
    turns = chat_history[-max_turns * 2:]  
    for msg in turns:
        role = "User" if msg["role"] == "user" else "Doctor"
        formatted += f"{role}: {msg['content']}\n"
    return formatted


def process_inputs(audio_filepath, image_filepath, typed_input, chat_history, stored_image):
    if audio_filepath:
        user_input = transcribe_with_groq(
            GROQ_API_KEY=os.environ.get("GROQ_API_KEY"),
            audio_path=audio_filepath,
            stt_model="whisper-large-v3"
        )
    elif typed_input:
        user_input = typed_input
    else:
        return "No input provided.", "Please speak or type.", None, chat_history, stored_image

  
    history_text = format_chat_history(chat_history)
    full_prompt = system_prompt + "\n" + history_text + f"User: {user_input}"

    
    image_to_use = image_filepath or stored_image

    if image_to_use:
        encoded = encode_image(image_to_use)
        doctor_response = analyze_image_with_query(
            query=full_prompt,
            encoded_image=encoded,
            model="meta-llama/llama-4-scout-17b-16e-instruct"
        )
    else:
        doctor_response = "No image provided for me to analyze."

    mp3_path = "doctor_output.mp3"
    wav_path = "doctor_output.wav"
    text_speech_with_elevenlabs(
        input_text=doctor_response,
        output_mp3_path=mp3_path,
        output_wav_path=wav_path
    )

    add_to_chat_memory(f"User: {user_input}")
    add_to_chat_memory(f"Doctor: {doctor_response}")

    chat_history.append({"role": "user", "content": user_input})
    chat_history.append({"role": "assistant", "content": doctor_response})


    new_stored_image = image_filepath or stored_image
    return user_input, doctor_response, wav_path, chat_history, new_stored_image


def reset_chat():
    return "", "", None, [], None


with gr.Blocks(title="AI Doctor with Vision and Voice") as app:
    gr.Markdown("## AI Doctor with Vision and Voice")
    gr.Markdown("Upload a medical image and describe your symptoms via voice or text. The doctor will respond accordingly.")

    with gr.Row():
        audio_input = gr.Audio(sources=["microphone"], type="filepath", label="Speak your symptoms")
        image_input = gr.Image(type="filepath", label="Upload medical image")
    
    typed_input = gr.Textbox(label="(Optional) Type your symptoms")

    with gr.Row():
        submit_btn = gr.Button("Submit")
        reset_btn = gr.Button("Reset")

    output_text = gr.Textbox(label="Speech to Text / Typed Input")
    doctor_reply = gr.Textbox(label="Doctor's Response")
    audio_output = gr.Audio(label="Doctor's Voice Response")
    chatbox = gr.Chatbot(label="Chat History", type="messages")

    stored_image = gr.State(value=None)

    submit_btn.click(
        fn=process_inputs,
        inputs=[audio_input, image_input, typed_input, chatbox, stored_image],
        outputs=[output_text, doctor_reply, audio_output, chatbox, stored_image]
    )

    reset_btn.click(
        fn=reset_chat,
        inputs=[],
        outputs=[output_text, doctor_reply, audio_output, chatbox, stored_image]
    )

if __name__ == "__main__":
    app.launch(debug=True)
