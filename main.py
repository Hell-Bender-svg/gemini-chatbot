from fastapi import FastAPI
from google import genai
import os

app = FastAPI()


client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

@app.post("/chat")
def chat(message: str):
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=message
    )
    return {"response": response.text}