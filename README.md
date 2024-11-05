# Leo Chat Application

## Overview

The Leo Chat Application allows users to interact with an AI assistant named Leo. Users can upload documents (PDF, DOCX, or images) and engage in conversation with Leo using both text and voice commands. Leo can extract information from the uploaded documents and respond to user queries.

## Features

- **Document Upload:** Users can upload PDF and DOCX documents.
- **Image Processing:** Users can upload images for text extraction using Optical Character Recognition (OCR).
- **Voice Interaction:** Users can interact with Leo using voice commands.
- **Text-to-Speech:** Leo can respond to queries using a text-to-speech engine.
- **Chat History:** Keeps track of previous interactions for a seamless experience.

## Technologies Used

- Streamlit for the web application
- Google Generative AI for response generation
- PyMuPDF for PDF reading
- SpeechRecognition for voice recognition
- Pyttsx3 for text-to-speech functionality
- Pytesseract for Optical Character Recognition (OCR)
- Python-docx for reading DOCX files
- NumPy and PyAudio for audio processing

## Prerequisites

Before running the application, ensure you have the following installed:

- Python 3.9 or higher
- Pip (Python package manager)

## Installation

1. Clone the repository to your local machine:
   ```bash
   git clone https://github.com/HarshKalburgi/leo-chat-application.git
   cd leo-chat-application
   ```

2. Create a Conda Environment

Create a new Conda environment for the project:

```bash
conda create --name leo_env python=3.10
conda activate leo_env
```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

   - **Note**: Make sure to include the required libraries in the `requirements.txt` file:

```bash
streamlit
pytesseract
python-docx
opencv-python
```
Install the dependencies required for the project:

```bash
pip install streamlit google-generativeai python-dotenv PyMuPDF wave numpy pyaudio SpeechRecognition pyttsx3 Pillow pytesseract python-docx
```

4. **Install the dependencies required for the project:**
   ```bash
   pip install streamlit google-generativeai python-dotenv PyMuPDF wave numpy pyaudio SpeechRecognition pyttsx3 Pillow pytesseract python-docx
   ```

5. Install Tesseract OCR:
   - Download Tesseract from [Tesseract at UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki).
   - Follow the installation instructions for your operating system.
   - Ensure Tesseract is added to your system's PATH.

6. Install Microsoft Word API for handling DOCX files if not already installed.

7. Create a `.env` file in the project root and add your Google Generative AI API key:
   ```plaintext
   API_KEY=your_api_key_here
   ```

## Running the Application

1. Start the Streamlit application:
   ```bash
   streamlit run app.py
   ```

2. Open your web browser and navigate to `http://localhost:8501` to use the application.

## Usage

1. Upload a PDF or DOCX document (optional).
2. Speak or type your query in the chat interface.
3. Leo will respond with relevant information extracted from the document or general knowledge.

## Troubleshooting

- If you encounter issues with voice recognition, ensure your microphone is properly configured.
- For Tesseract-related errors, verify that Tesseract is installed and correctly added to your PATH.
- If any required libraries are missing, ensure they are included in the `requirements.txt`.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to the developers of the libraries used in this project.

## Contact

For any inquiries or support, feel free to reach out to me:

- **Email**: harshkalburgi01@gmail.com
<<<<<<< HEAD
- **GitHub**: [HarshKalburgi](https://github.com/HarshKalburgi)
