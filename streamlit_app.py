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

    # Sidebar for additional options or information
    with st.sidebar:
        st.markdown("Email: songhunhwa@gmail.com")

    # Ensure API key is loaded
    if not openai.api_key:
        st.error("API key not found. Please check your .env file.")
        return

    # Function to generate assistant response with streaming
    def stream_ai_response(user_input):
        try:
            # Prepare messages
            messages = [{"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": user_input}]
            
            # Simulate a streaming OpenAI response
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=messages
            )
            full_response = response.choices[0].message["content"]
            
            # Stream response word by word
            for word in full_response.split():
                yield word + " "
                time.sleep(0.05)  # Simulate streaming delay
        except Exception as e:
            yield f"An error occurred: {e}"

    # Input box for user message
    user_input = st.text_input("Type your message here:", placeholder="Ask anything...", key="user_input")

    # Add a "Send" button
    send_button = st.button("Send")

    # If user submits a message via Enter key or Send button
    if (send_button or user_input) and user_input.strip():
        # Create a placeholder for streaming output
        output_placeholder = st.empty()
        
        # Stream AI response
        response_stream = stream_ai_response(user_input.strip())
        final_response = ""
        for chunk in response_stream:
            final_response += chunk
            output_placeholder.markdown(f"**AI:** {final_response}")

    # Add footer
    st.markdown("---")
    st.markdown("<div style='color: grey;'>© 2025 Chat with AI. All rights reserved.</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
