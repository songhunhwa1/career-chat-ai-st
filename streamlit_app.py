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
    st.set_page_config(page_title="Chat with AI", layout="wide")
    st.title("🤖 Chat with AI")
    st.markdown("Ask me anything!")

    # Sidebar with email address
    with st.sidebar:
        st.title("Contact Info")
        st.markdown("📧 **Email:** your_email@example.com")
        st.markdown("---")  # Separator for aesthetic purposes

    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Function to generate assistant response in chunks
    def stream_response(user_input):
        try:
            # Prepare messages with chat history
            messages = [{"role": "system", "content": "You are a helpful assistant."}]
            for message in st.session_state.chat_history:
                messages.append({"role": message["role"], "content": message["content"]})
            messages.append({"role": "user", "content": user_input})

            # Simulate streaming with OpenAI response
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
            full_response = response.choices[0].message["content"]

            # Yield the response in chunks
            for word in full_response.split():
                yield word + " "
                time.sleep(0.05)  # Simulate delay for streaming
        except Exception as e:
            yield f"An error occurred: {e}"

    # Display chat history
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            with st.chat_message("user"):
                st.markdown(message["content"])
        elif message["role"] == "assistant":
            with st.chat_message("assistant"):
                st.markdown(message["content"])

    # Chat input box at the bottom
    if user_input := st.chat_input("Type your message here..."):
        # Display user message immediately
        with st.chat_message("user"):
            st.markdown(user_input)

        # Save user message to chat history
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        # Stream assistant response
        assistant_response = []
        with st.chat_message("assistant"):
            st.write_stream(stream_response(user_input))

        # Save assistant response to chat history
        full_response = "".join(stream_response(user_input))
        st.session_state.chat_history.append({"role": "assistant", "content": full_response})

if __name__ == "__main__":
    main()
