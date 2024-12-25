import streamlit as st
import openai
import os
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def main():
    st.title("👩‍🚀 Chat with AI")
    st.subheader("Hi Joan. Have a good day.")

    # Initialize chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    def submit_query():
        user_input = st.session_state.query
        if user_input:
            response = ask(user_input)
            st.session_state.chat_history.append((user_input, response))
            st.session_state.query = ""  # Clear input box

    # Chat input box
    user_input = st.text_input("Ask something:", key="query", on_change=submit_query)

    # Chat display
    for q, a in st.session_state.chat_history:
        with st.chat_message("user"):
            st.markdown(q)
        with st.chat_message("assistant"):
            st.markdown(a)

    # Sidebar for conversation history
    with st.sidebar:
        st.title("Conversation History")
        for i, (q, a) in enumerate(st.session_state.chat_history, 1):
            st.markdown(f"**Q{i}:** {q}")
            st.markdown(f"**A{i}:** {a}")
            st.markdown("---")
        if st.button("Clear Chat"):
            st.session_state.chat_history = []
            st.experimental_rerun()

def ask(question):
    try:
        # Include chat history for context
        messages = [{"role": "system", "content": "You are a helpful assistant."}]
        for q, a in st.session_state.chat_history:
            messages.append({"role": "user", "content": q})
            messages.append({"role": "assistant", "content": a})
        messages.append({"role": "user", "content": question})

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        return response.choices[0].message['content']
    except Exception as e:
        return f"An error occurred: {str(e)}"

if __name__ == '__main__':
    main()
