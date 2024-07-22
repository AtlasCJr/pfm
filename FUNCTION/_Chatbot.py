import google.generativeai as genai
import os
from colored import fg


genai.configure(api_key="AIzaSyB5iU1LJKRpeJWYsGpFiYW7jXiXZiiirV4")

generation_config = {
    "temperature": 0.0,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048
}

model = genai.GenerativeModel(
    model_name="gemini-1.0-pro",
    generation_config=generation_config
)

prompt = """
Answer the following questions briefly. Only 1 paragraph is allowed and don't use bold/italic/underlined messages. Write your answers in paragraphs, not points.
"""

conversation = model.start_chat(history=[
    {
        "role": "user",
        "parts": [{
            "text": prompt
        }]
    }, 
    {
        "role": "model",
        "parts": [{
            "text": "Understood, User."
        }]
    }
])

conversation.send_message("Give me a way to cut my expenses")

print(conversation.last.text.replace("*", ""))