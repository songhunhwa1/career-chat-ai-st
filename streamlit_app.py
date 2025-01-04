import streamlit as st
import openai
import os
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def main():
    # Page setup
    st.set_page_config(page_title="Chat with AI", layout="wide")
    st.title("Chat with AI")

    # Initialize session state for chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Ensure API key is loaded
    if not openai.api_key:
        st.error("API key not found. Please check your .env file.")
        return

    # Function to generate assistant response
    def get_ai_response(user_input):
        try:
            # Prepare messages
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

    # Display chat history in a chat-like format
    st.markdown("### Conversation")
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.markdown(f"<div style='text-align: right; color: blue;'><strong>You:</strong> {message['content']}</div>", unsafe_allow_html=True)
        elif message["role"] == "assistant":
            st.markdown(f"<div style='text-align: left; color: green;'><strong>AI:</strong> {message['content']}</div>", unsafe_allow_html=True)

    # Input box and send button at the bottom
    with st.container():
        user_input = st.text_input("Type your message here:", placeholder="Ask anything...", key="user_input")
        send_button = st.button("Send", key="send_button")

    # If user submits a message via Enter key or Send button
    if (send_button or user_input) and user_input.strip():
        # Add user message to chat history
        st.session_state.chat_history.append({"role": "user", "content": user_input.strip()})

        # Generate AI response
        ai_response = get_ai_response(user_input.strip())
        st.session_state.chat_history.append({"role": "assistant", "content": ai_response})

        # Clear the input box
        st.session_state.user_input = ""
        st.experimental_rerun()  # Refresh to display the new messages

if __name__ == "__main__":
    main()
