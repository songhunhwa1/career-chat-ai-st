import streamlit as st
import openai
import os
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def main():
    st.title("Chat with AI")
    st.markdown("""
        <style>
        .small-font {
            font-size:14px !important;
        }
        </style>
        <div class='small-font'>
            Email me: <a href="mailto:songhunhwa@gmail.com">songhunhwa@gmail.com</a>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
        <style>
        div.stButton > button {
            color: white;
            background-color: orange;
            border-color: orange;
        }
        </style>""", unsafe_allow_html=True)

    # Initialize the chat history if it doesn't exist
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    def submit_query():
        user_input = st.session_state.query
        # Prevent redundant API calls
        if user_input and (user_input != st.session_state.get('last_query', '')):
            response = ask(user_input)
            # Store the interaction in chat history
            st.session_state.chat_history.append((user_input, response))
            st.session_state.last_query = user_input
            # Update the displayed response
            st.session_state.displayed_response = response

    # Text input widget with on_change triggering submit_query function
    user_input = st.text_input("Ask something:", key="query", on_change=submit_query)

    # Submit button
    if st.button("SEND"):
        with st.spinner("Wait..."):
            submit_query()  # Call the submit function when the button is pressed

    # Display the last response in the main area
    if 'displayed_response' in st.session_state:
        st.markdown(st.session_state.displayed_response)

    # Display the chat history in the sidebar
    if 'chat_history' in st.session_state and st.session_state.chat_history:
        st.sidebar.title("Conversation History")
        for i, (q, a) in enumerate(st.session_state.chat_history, 1):
            st.sidebar.markdown(f"**Q{i}:** {q}")
            st.sidebar.markdown(f"**A{i}:** {a}")
            st.sidebar.markdown("---")

def ask(question):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question},
            ]
        )
        return response.choices[0].message['content']
    except Exception as e:
        return f"An error occurred: {str(e)}"

if __name__ == '__main__':
    main()
