import streamlit as st
import openai
import os
from dotenv import load_dotenv
import time

# Load API key from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def main():
    # Page setup
    st.set_page_config(page_title="Chat with AI")
    st.title("Simple Chat with AI")

    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Ensure API key is loaded
    if not openai.api_key:
        st.error("API key not found. Please check your .env file.")
        return

    # Function to generate assistant response
    def stream_response(user_input):
        try:
            # Prepare messages with chat history
            messages = [{"role": "system", "content": "You are a helpful assistant."}]
            for message in st.session_state.chat_history:
                messages.append({"role": message["role"], "content": message["content"]})
            messages.append({"role": "user", "content": user_input})

            # Get OpenAI response
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
            return response.choices[0].message["content"]
        except Exception as e:
            return f"An error occurred: {e}"

    # Display chat history in plain format
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.markdown(f"**You:** {message['content']}")
        elif message["role"] == "assistant":
            st.markdown(f"**AI:** {message['content']}")

    # Input box for user message
    user_input = st.text_input("Type your message here:", key="user_input", placeholder="Ask anything...")

    # If user submits a message
    if st.button("Send") and user_input:
        # Add user message to chat history
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        # Generate AI response
        ai_response = stream_response(user_input)
        st.session_state.chat_history.append({"role": "assistant", "content": ai_response})

        # Clear input box
        st.session_state.user_input = ""

if __name__ == "__main__":
    main()
