import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import fitz  # PyMuPDF for PDF reading
import wave
import numpy as np
import pyaudio
import io
import speech_recognition as sr
import threading
import queue  # For managing audio processing

# Load environment variables
load_dotenv()
API_KEY = os.getenv("API_KEY")

# Configure the Leo API SDK
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash") 

# Streamlit app setup
st.set_page_config(page_title="Leo Chat Application", layout="wide")
st.title("Leo")
st.write("Chat with Leo")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
if "document_text" not in st.session_state:
    st.session_state.document_text = ""

# Function to read and extract text from PDF documents
def extract_text_from_pdf(file):
    pdf_reader = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in pdf_reader:
        text += page.get_text()
    return text

# Function to interact with Leo API
def get_leo_response(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Error: {e}")
        return None

# Function to recognize audio
def recognize_audio(audio_queue):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        while True:
            try:
                audio_data = r.listen(source)
                text = r.recognize_google(audio_data)
                audio_queue.put(text)
            except sr.UnknownValueError:
                continue
            except sr.RequestError:
                st.error("Could not request results from Leo Speech Recognition service.")
                break

# Create an audio queue for threading
audio_queue = queue.Queue()

# Start the audio recognition thread
audio_thread = threading.Thread(target=recognize_audio, args=(audio_queue,), daemon=True)
audio_thread.start()

# Upload document
uploaded_file = st.file_uploader("Upload a PDF document (optional)", type="pdf")

if uploaded_file is not None:
    # Extract text from the uploaded PDF
    document_text = extract_text_from_pdf(uploaded_file)
    st.session_state.document_text = document_text
    st.session_state.messages.clear()  # Clear previous messages
    st.session_state.messages.append({"role": "assistant", "content": "Document loaded. You can now ask questions about it."})

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Check for audio input
while not audio_queue.empty():
    audio_input = audio_queue.get()
    # Add audio input to chat history
    st.session_state.messages.append({"role": "user", "content": audio_input})

    # Display audio message in chat message container
    with st.chat_message("user"):
        st.markdown(audio_input)

    # Build the context for the prompt
    if st.session_state.document_text:
        full_prompt = st.session_state.document_text + "\n\n" + audio_input
    else:
        full_prompt = audio_input  # Use only the audio input if no document is uploaded

    # Get Leo's response
    leo_reply = get_leo_response(full_prompt)

    if leo_reply:
        # Add Leo's response to chat history
        st.session_state.messages.append({"role": "assistant", "content": leo_reply})

        # Display Leo's message in chat message container
        with st.chat_message("assistant"):
            st.markdown(leo_reply)

# Function to handle audio input from microphone button
def record_audio():
    with sr.Microphone() as source:
        st.info("Listening...")
        audio_data = sr.Recognizer().listen(source)
        st.info("Processing...")
        try:
            text = sr.Recognizer().recognize_google(audio_data)
            return text
        except sr.UnknownValueError:
            st.error("Could not understand audio.")
            return ""
        except sr.RequestError:
            st.error("Could not request results from Google Speech Recognition service.")
            return ""

# Microphone button
if st.button("🎤"):
    audio_text = record_audio()
    if audio_text:
        st.session_state.messages.append({"role": "user", "content": audio_text})

        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(audio_text)

        # Build the context for the prompt
        if st.session_state.document_text:
            full_prompt = st.session_state.document_text + "\n\n" + audio_text
        else:
            full_prompt = audio_text  # Use only the audio input if no document is uploaded

        # Get Leo's response
        leo_reply = get_leo_response(full_prompt)

        if leo_reply:
            # Add Leo's response to chat history
            st.session_state.messages.append({"role": "assistant", "content": leo_reply})

            # Display Leo's message in chat message container
            with st.chat_message("assistant"):
                st.markdown(leo_reply)

# Accept user text input
if prompt := st.chat_input("What would you like to ask?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Build the context for the prompt
    if st.session_state.document_text:
        full_prompt = st.session_state.document_text + "\n\n" + prompt
    else:
        full_prompt = prompt  # Use only the user's prompt if no document is uploaded

    # Get Leo's response
    leo_reply = get_leo_response(full_prompt)

    if leo_reply:
        # Add Leo's response to chat history
        st.session_state.messages.append({"role": "assistant", "content": leo_reply})

        # Display Leo's message in chat message container
        with st.chat_message("assistant"):
            st.markdown(leo_reply)

# Add custom CSS for styling (if needed)
st.markdown("""
    <style>
    .chat-message {
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 10px;
        width: auto;
    }
    .user {
        background-color: #e0f7fa;
        align-self: flex-start;
    }
    .assistant {
        background-color: #ffe0b2;
        align-self: flex-end;
    }
    </style>
""", unsafe_allow_html=True)
