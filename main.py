import os
from dotenv import load_dotenv
from groq import Groq
import streamlit as st
import time

# Load environment variables from .env file
load_dotenv()

# Initialize Groq client
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

# Page config
st.set_page_config(
    page_title="AI Chat Assistant",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        background-color: #f5f5f5;
    }
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 10px;
        border-radius: 5px;
        font-size: 16px;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .chat-message {
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 10px;
        max-width: 80%;
        color: white;
    }
    .user-message {
        background-color: #2b2b2b;
        margin-left: auto;
        color: white;
    }
    .bot-message {
        background-color: #1a1a1a;
        margin-right: auto;
        color: white;
    }
    .stTextArea>div>div>textarea {
        background-color: #f0f0f0;
        color: black !important;
    }
    .stTextArea>div>div>textarea::placeholder {
        color: #666666;
    }
    .stTextArea>div>div>textarea:focus {
        color: black !important;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("🤖 AI Chat Assistant")
    st.markdown("---")
    st.markdown("### Settings")
    model = st.selectbox(
        "Select Model",
        ["llama-3.3-70b-versatile","gemma2-9b-it","compound-beta"],
        index=0
    )
    st.markdown("---")
    st.markdown("### About")
    st.info("This is an AI chatbot powered by Groq's LLaMA model. Feel free to ask any questions!")

# Main content
st.title("💬 Chat with AI")
st.markdown("---")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.container():
        if message["role"] == "user":
            st.markdown(f'<div class="chat-message user-message">{message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-message bot-message">{message["content"]}</div>', unsafe_allow_html=True)

# Chat input
user_input = st.text_area("Type your message here...", height=100)

# Send button
if st.button("Send Message", key="send"):
    if user_input:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Show loading animation
        with st.spinner("AI is thinking..."):
            # Get AI response
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": user_input,
                    }
                ],
                model=model,
            )
            
            # Add AI response to chat history
            ai_response = chat_completion.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
        
        # Clear the input
        st.rerun()
















