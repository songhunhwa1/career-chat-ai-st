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
    st.title("Chat with AI")

    # Sidebar for additional options or information
    with st.sidebar:
        st.markdown("Hello Joan. A good day.")

    # Ensure API key is loaded
    if not openai.api_key:
        st.error("API key not found. Please check your .env file.")
        return

    # Function to generate assistant response
    def get_ai_response(user_input):
        try:
            # Prepare messages
            messages = [{"role": "system", "content": "You are a helpful assistant. Kindly respond and the response should be clear, informative, and around 150-200 words long. Use a professional and neutral tone."},
                        {"role": "user", "content": user_input}]

            # Get OpenAI response
            response = openai.ChatCompletion.create(
                model="gpt-4.1-nano",
                messages=messages,
                max_tokens=500
            )
            return response.choices[0].message["content"]
        except Exception as e:
            return f"An error occurred: {e}"

    # Input box for user message
    user_input = st.text_input("Type your message here:", placeholder="Ask anything...", key="user_input")

    # Add a "Send" button
    send_button = st.button("SEND")
    
    # If user submits a message via Enter key or Send button
    if (send_button or user_input) and user_input.strip():
        with st.spinner("Generating response..."):
            # Generate AI response
            ai_response = get_ai_response(user_input.strip())

        # Display AI response
        st.markdown(f"**AI:** {ai_response}")

    # Add footer
    st.markdown("---")
    st.markdown("<div style='color: grey;'>© 2025 Chat with AI. All rights reserved.</div>", unsafe_allow_html=True)
    

if __name__ == "__main__":
    main()
