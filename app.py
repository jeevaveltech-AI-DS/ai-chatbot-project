import os
import requests
import streamlit as st
from dotenv import load_dotenv


# Load API key
load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    st.error("API key is missing. Check your .env file.")
    st.stop()


# Chatbot title
st.title("🤖 My AI Chatbot")
st.write("Ask me anything!")


# Store conversation
if "messages" not in st.session_state:
    st.session_state.messages = []


# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


# Get user message
user_message = st.chat_input("Type your message...")


if user_message:

    # Display user message
    with st.chat_message("user"):
        st.write(user_message)

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_message
    })

    # Send message to OpenRouter
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json={
            "model": "openrouter/free",
            "messages": st.session_state.messages
        }
    )

    # Get AI response
    if response.status_code == 200:

        data = response.json()

        ai_response = data["choices"][0]["message"]["content"]

    else:

        ai_response = "Sorry, something went wrong."

    # Display AI response
    with st.chat_message("assistant"):
        st.write(ai_response)

    # Save AI response
    st.session_state.messages.append({
        "role": "assistant",
        "content": ai_response
    })