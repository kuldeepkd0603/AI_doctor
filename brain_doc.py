import os
from dotenv import load_dotenv
load_dotenv()
GROQ_API_KEY=os.environ.get("GROQ_API_KEY")
import base64

#image_path="imgs.jpeg"
def encode_image(image_path):
    image_file=open(image_path,"rb")
    return base64.b64encode(image_file.read()).decode("utf-8")


from groq import Groq

query="You are a visual AI assistant specialized in object recognition.\nI will provide you with a PNG image containing a single object.\nYour task is to:\n\nCarefully analyze the image to deeply understand the object based on its shape, texture, color, and any identifying features.\n\nSuggest one single, highly accurate name that best describes the object.\n\nThe name should be specific, concise (1–3 words), and must precisely reflect what the object is — not a category or a guess.\n\nAvoid vague, general, or overly broad labels.\n\nOutput only the object name, without any explanation."
model="meta-llama/llama-4-scout-17b-16e-instruct"
def analyze_image_with_query(query,model,encoded_image):
    client=Groq()
    
    messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text", 
                        "text": query
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{encoded_image}",
                        },
                    },
                ],
            }]
    chat_completion=client.chat.completions.create(
        messages=messages,
        model=model
    )
    return chat_completion.choices[0].message.content

image_path="testing\p02.png"
print(analyze_image_with_query(model=model,query=query,encoded_image=encode_image(image_path)))