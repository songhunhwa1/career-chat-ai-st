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
    st.title("Chat with AI")
    st.markdown("Ask me anything!")

    # Sidebar with email address
    with st.sidebar:
        st.title("Contact Info")
        st.markdown("📧 Email: songhunhwa@gmail.com")
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
                messages=messages,
                stream=True  # Enables OpenAI streaming
            )
            for chunk in response:
                if "content" in chunk.choices[0].delta:
                    yield chunk.choices[0].delta["content"]
                time.sleep(0.02)  # Simulate delay for chunk updates
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
            with st.write_stream() as stream:
                for chunk in stream_response(user_input):
                    stream.write(chunk)
                    assistant_response.append(chunk)

        # Save assistant response to chat history
        full_response = "".join(assistant_response)
        st.session_state.chat_history.append({"role": "assistant", "content": full_response})

if __name__ == "__main__":
    main()
