import streamlit as st
import openai
import os
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def main():
    st.title("Chat with SQL-bot")
    st.markdown("""
        <style>
        .small-font {
            font-size:14px !important;
        }
        </style>
        <div class='small-font'>
            If you want to email me: <a href="mailto:songhunhwa@gmail.com">songhunhwa@gmail.com</a>
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

    # Function to handle submission
    def submit_query():
        user_input = st.session_state.query  # Access user input from session state
        if user_input:  # Check if there is input
            response = ask(user_input)
            st.session_state.response = response  # Store response in session state

    # Text input widget with on_change triggering submit_query function
    user_input = st.text_input("Ask something:", key="query", on_change=submit_query)

    # Submit button
    if st.button("SEND"):
        with st.spinner("Wait..."):
            submit_query()  # Call the submit function when the button is pressed

    # Function to determine if the response is likely SQL code
    def is_sql_code(text):
        # List of common SQL keywords, extend this list as needed
        sql_keywords = ['SELECT', 'INSERT', 'UPDATE', 'DELETE', 'FROM', 'WHERE', 'JOIN', 'CREATE', 'ALTER', 'DROP', 'TABLE']
        # Check if any SQL keyword exists in the text
        return any(keyword in text.upper() for keyword in sql_keywords)
    
    # Display the response if it exists in session state
    if 'response' in st.session_state:
        if is_sql_code(st.session_state['response']):
            # Response seems to be SQL, format as code
            response_formatted = f"```sql\n{st.session_state['response']}\n```"
            st.markdown(response_formatted, unsafe_allow_html=True)
        else:
            # Response seems to be commentary, format normally
            st.markdown(st.session_state['response'])

    
def ask(question):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a SQL code generator."},
            {"role": "user", "content": question},
        ]
    )
    return response.choices[0].message['content']


if __name__ == '__main__':
    main()
