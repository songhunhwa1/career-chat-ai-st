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
    st.title("💬 Chat with AI")

    # Sidebar with email address
    with st.sidebar:
        st.markdown("📧 Email: songhunhwa@gmail.com")

    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Ensure API key is loaded
    if not openai.api_key:
        st.error("API key not found. Please check your .env file.")
        return

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
                time.sleep(0.02)  # Adjust delay for streaming
        except Exception as e:
            st.error("An error occurred while generating the response.")
            print(f"Error: {e}")
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
    if user_input := st.chat_input("Ask me anything!"):
        # Display user message immediately
        with st.chat_message("user"):
            st.markdown(user_input)

        # Save user message to chat history
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        # Stream assistant response
        assistant_response = []
        with st.chat_message("assistant"):
            for chunk in stream_response(user_input):
                st.markdown(chunk, unsafe_allow_html=True)
                assistant_response.append(chunk)

        # Combine the chunks into a full response
        full_response = "".join(assistant_response)
        st.session_state.chat_history.append({"role": "assistant", "content": full_response})

if __name__ == "__main__":
    main()
