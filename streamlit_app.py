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
    st.title("🤖 Chat with AI")
    st.markdown("Ask me anything!")

    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

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

        # Generate response from OpenAI
        with st.spinner("AI is typing..."):
            response = ask_openai(user_input)

        # Display assistant response
        with st.chat_message("assistant"):
            st.markdown(response)

        # Save assistant response to chat history
        st.session_state.chat_history.append({"role": "assistant", "content": response})

def ask_openai(prompt):
    try:
        # Prepare the conversation history for context
        messages = [{"role": "system", "content": "You are a helpful assistant."}]
        for message in st.session_state.chat_history:
            messages.append({"role": message["role"], "content": message["content"]})
        messages.append({"role": "user", "content": prompt})

        # Get the response from OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        return response.choices[0].message["content"]
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == "__main__":
    main()
