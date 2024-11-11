import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import fitz  # PyMuPDF for PDF reading
import docx  # For reading DOCX files
import pandas as pd  # For reading Excel and CSV files
from bs4 import BeautifulSoup  # For reading HTML files
import wave
import numpy as np
import pyaudio
import io
import speech_recognition as sr
import threading
import queue  # For managing audio processing
import pyttsx3  # Text-to-speech for Leo's voice responses
import markdown  # For reading markdown files
import xml.etree.ElementTree as ET  # For reading XML files
from PIL import Image  # For image handling
import pytesseract  # OCR tool for extracting text from images
import pyth  # For reading RTF files (replacing rtfparse)

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

# Initialize chat history and TTS engine
if "messages" not in st.session_state:
    st.session_state.messages = []
if "document_text" not in st.session_state:
    st.session_state.document_text = ""
if "tts_thread" not in st.session_state:
    st.session_state.tts_thread = None
if "stop_speech" not in st.session_state:
    st.session_state.stop_speech = False

# Initialize TTS engine
engine = pyttsx3.init()

# Function to toggle stop/start speech
def toggle_stop_speech():
    # Toggle the speech flag
    st.session_state.stop_speech = not st.session_state.stop_speech
    if st.session_state.stop_speech:
        # Stop the TTS engine if currently speaking
        if st.session_state.tts_thread and st.session_state.tts_thread.is_alive():
            engine.stop()
    else:
        st.info("Leo's speech is re-enabled.")

# Button to toggle Leo's speech
if st.button("🛑 Toggle Leo's Voice"):
    toggle_stop_speech()

# Function for Leo to talk back
def leo_talk(text):
    def speak():
        engine.say(text)
        engine.runAndWait()
    if st.session_state.stop_speech:
        return
    st.session_state.tts_thread = threading.Thread(target=speak, daemon=True)
    st.session_state.tts_thread.start()

# Function to extract text from PDF
def extract_text_from_pdf(file):
    pdf_reader = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in pdf_reader:
        text += page.get_text()
    return text

# Function to extract text from DOCX
def extract_text_from_docx(file):
    doc = docx.Document(file)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

# Function to extract text from TXT
def extract_text_from_txt(file):
    text = file.read().decode("utf-8")
    return text

# Function to extract text from Excel (XLSX)
def extract_text_from_excel(file):
    df = pd.read_excel(file, sheet_name=None)
    text = ""
    for sheet_name, sheet_data in df.items():
        text += f"Sheet: {sheet_name}\n"
        text += sheet_data.to_string(index=False) + "\n\n"
    return text

# Function to extract text from CSV
def extract_text_from_csv(file):
    df = pd.read_csv(file)
    return df.to_string(index=False)

# Function to extract text from HTML
def extract_text_from_html(file):
    soup = BeautifulSoup(file, "html.parser")
    return soup.get_text()

# Function to extract text from Markdown
def extract_text_from_markdown(file):
    text = file.read().decode("utf-8")
    return markdown.markdown(text)

# Function to extract text from JavaScript
def extract_text_from_js(file):
    text = file.read().decode("utf-8")
    return text

# Function to extract text from Python
def extract_text_from_python(file):
    text = file.read().decode("utf-8")
    return text

# Function to extract text from CSS
def extract_text_from_css(file):
    text = file.read().decode("utf-8")
    return text

# Function to extract text from XML
def extract_text_from_xml(file):
    tree = ET.parse(file)
    root = tree.getroot()
    text = ET.tostring(root, encoding='unicode')
    return text

# Function to extract text from RTF
def extract_text_from_rtf(file):
    rtf = file.read()
    text = rtfparse.parse(rtf)
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
uploaded_file = st.file_uploader("Upload a document (PDF, DOCX, TXT, XLSX, CSV, HTML, JS, Python, CSS, Markdown, XML, RTF)", type=["pdf", "docx", "txt", "xlsx", "csv", "html", "js", "py", "css", "md", "xml", "rtf"])

if uploaded_file is not None:
    file_extension = uploaded_file.name.split('.')[-1].lower()

    if file_extension == "pdf":
        document_text = extract_text_from_pdf(uploaded_file)
    elif file_extension == "docx":
        document_text = extract_text_from_docx(uploaded_file)
    elif file_extension == "txt":
        document_text = extract_text_from_txt(uploaded_file)
    elif file_extension == "xlsx":
        document_text = extract_text_from_excel(uploaded_file)
    elif file_extension == "csv":
        document_text = extract_text_from_csv(uploaded_file)
    elif file_extension == "html":
        document_text = extract_text_from_html(uploaded_file)
    elif file_extension == "js":
        document_text = extract_text_from_js(uploaded_file)
    elif file_extension == "py":
        document_text = extract_text_from_python(uploaded_file)
    elif file_extension == "css":
        document_text = extract_text_from_css(uploaded_file)
    elif file_extension == "md":
        document_text = extract_text_from_markdown(uploaded_file)
    elif file_extension == "xml":
        document_text = extract_text_from_xml(uploaded_file)
    elif file_extension == "rtf":
        document_text = extract_text_from_rtf(uploaded_file)
    else:
        document_text = "Sorry, this file type is not supported for text extraction."

    st.session_state.document_text = document_text

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

        # Make Leo talk
        leo_talk(leo_reply)

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
            st.error("Could not request results from Leo Speech Recognition service.")
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

            # Make Leo talk
            leo_talk(leo_reply)

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

        # Make Leo talk
        leo_talk(leo_reply)
