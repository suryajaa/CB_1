import streamlit as st
import os
import google.generativeai as genai
from langchain_utils import invoke_chain

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


st.title("Langchain NL2SQL Chatbot")

# Set Gemini API key from Streamlit secrets
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Set a default model
if "gemini_model" not in st.session_state:
    st.session_state["gemini_model"] = "text-bison-001"  # Replace with actual Gemini model name

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.spinner("Generating response..."):
        with st.chat_message("assistant"):
            response = invoke_chain(prompt, st.session_state.messages)
            st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
