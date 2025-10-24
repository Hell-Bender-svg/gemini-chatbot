import streamlit as st
from google import genai
from PIL import Image
import os

st.set_page_config(page_title="Gemini Chatbot", page_icon="🤖")

# Get API key from environment variable
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error("Gemini API key not found.")
    st.stop()

client = genai.Client(api_key=api_key)

#Creating a list to store chat messages
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("🤖 Gemini Chatbot")

#Showing all previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("image"):
            st.image(message["image"])

uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

prompt = st.chat_input("Type your message here...")

if prompt:
    user_message = {"role": "user", "content": prompt}
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        user_message["image"] = image
    
    st.session_state.messages.append(user_message)
    
    with st.chat_message("user"):
        st.markdown(prompt)
        if uploaded_file:
            st.image(image)
    
    with st.chat_message("assistant"):
        if uploaded_file:
            response = client.models.generate_content(
                model="gemini-2.0-flash-exp",
                contents=[prompt, image]
            )
        else:
            response = client.models.generate_content(
                model="gemini-2.0-flash-exp",
                contents=prompt
            )
        
        st.markdown(response.text)
        
        st.session_state.messages.append({
            "role": "assistant",
            "content": response.text
        })