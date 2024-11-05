
# Leo - Chat Application with Optical Character Recognition (OCR) and Document Processing

## Overview

**Leo** is an innovative chat application designed to provide seamless interaction using voice and video input while leveraging Optical Character Recognition (OCR) capabilities. Built using Python and Streamlit, Leo integrates the Gemini API for generative models, enabling real-time conversations and document processing. 

This project aims to demonstrate advanced features such as real-time video and voice interaction, text extraction from images, and document reading capabilities, making it an ideal tool for various applications.

## Features

- **Voice and Video Interaction**: Users can engage in conversations with Leo using voice commands and real-time video input.
- **OCR Integration**: Extract text from images and documents using `pytesseract`.
- **Document Processing**: Read DOCX files and extract content for seamless communication.
- **User-Friendly Interface**: Built with Streamlit for an interactive and responsive user experience.

## Technologies Used

- Python
- Streamlit
- Gemini API (for generative models)
- Pytesseract (for OCR)
- Python-docx (for DOCX file handling)
- OpenCV (for video processing)

## Installation

To set up and run the Leo application on your local machine, follow these steps:

### Prerequisites

Ensure you have the following installed:

- Python 3.x
- Anaconda (for managing environments)

### Step 1: Clone the Repository

```bash
git clone https://github.com/HarshKalburgi/leo.git
cd leo
```

### Step 2: Create a Conda Environment

Create a new Conda environment for the project:

```bash
conda create --name leo_env python=3.8
conda activate leo_env
```

### Step 3: Install Required Packages

Install the necessary Python packages:

```bash
pip install -r requirements.txt
```

- **Note**: Make sure to include the required libraries in the `requirements.txt` file:

```
streamlit
pytesseract
python-docx
opencv-python
```

### Step 4: Install Tesseract

1. Download and install Tesseract from [this link](https://github.com/tesseract-ocr/tesseract).
2. Add Tesseract to your system's PATH variable. For Windows, the installation path usually looks like this: `C:\Program Files\Tesseract-OCR`.

### Step 5: Run the Application

To start the Leo application, use the following command:

```bash
streamlit run app.py
```

## Usage

1. Open your browser and go to `http://localhost:8501`.
2. Interact with Leo using voice commands or by uploading images and DOCX files for text extraction and processing.

## Contributing

Contributions are welcome! If you have suggestions for improvements or new features, please fork the repository and create a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to the developers of the libraries used in this project.
- Special thanks to the OpenAI community for providing resources and support.

## Contact

For any inquiries or support, feel free to reach out to me:

- **Email**: harshkalburgi01@gmail.com
- **GitHub**: [HarshKalburgi](https://github.com/HarshKalburgi)
