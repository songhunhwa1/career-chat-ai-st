import streamlit as st
import openai
import os
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def main():
    # Page setup
    st.set_page_config(page_title="Chat with AI")
    st.title("Simple Chat with AI")

    # Ensure API key is loaded
    if not openai.api_key:
        st.error("API key not found. Please check your .env file.")
        return

    # Function to generate assistant response
    def get_ai_response(user_input):
        try:
            # Prepare messages
            messages = [{"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": user_input}]

            # Get OpenAI response
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
            return response.choices[0].message["content"]
        except Exception as e:
            return f"An error occurred: {e}"

    # Input box for user message
    user_input = st.text_input("Type your message here:", placeholder="Ask anything...", key="user_input")

    # If user submits a message (Enter key or Send button)
    if user_input:
        # Generate AI response
        ai_response = get_ai_response(user_input)

        # Display AI response
        st.markdown(f"**AI:** {ai_response}")

        # Clear the input box
        st.session_state.user_input = ""

if __name__ == "__main__":
    main()
