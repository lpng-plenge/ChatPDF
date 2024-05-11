# PDF Chat App

This application utilizes Streamlit, LangChain, and OpenAI to create an interactive chatbot for reading and searching through PDF documents.

## About
The PDF Chat App is designed to assist users in extracting information from PDF documents through a chat interface. It leverages advanced AI technologies to analyze and respond to user queries based on the content of the uploaded PDF.

### Technologies Used
- **Streamlit**: Provides the user interface for uploading PDF files and interacting with the chatbot.
- **LangChain**: Employs text splitting techniques to break down large documents into manageable chunks.
- **OpenAI**: Utilizes the GPT-3.5 model for natural language processing and generating responses.

## Features
- **PDF Upload**: Users can upload PDF files directly to the application.
- **Text Extraction**: The application extracts text from uploaded PDFs for analysis.
- **Chat Interface**: Users can converse with the AI chatbot to query information from the PDF content.
- **Semantic Search**: Utilizes embeddings to find relevant sections of the document based on user queries.
- **Response Generation**: Generates responses using the GPT-3.5 model tailored to the context of the provided text.

## Usage
1. **Upload PDF**: Select a PDF file using the file uploader.
2. **Chat Interface**: Type your query in the input box and click "Send" to interact with the chatbot.
3. **View Responses**: The chatbot will provide responses based on the content of the uploaded PDF and the user's query.

## Installation
Ensure you have Python installed, then run the following commands to install the required dependencies:
```bash
pip install streamlit numpy PyPDF2 langchain_text_splitters openai python-dotenv
```
## Configuration
Before running the application, make sure to set up your OpenAI API key by creating a .env file and adding your key:
```plaintext
OPENAI_API_KEY=your_api_key_here
```

## Running the App
To launch the PDF Chat App, execute the following command in your terminal:
```bash
streamlit run your_script_name.py
```
Replace your_script_name.py with the filename of the script containing the provided code.

## Contributors
Embeddings: [Rainer Stropek](https://gist.github.com/f3d4521ed9831ae5305a10df84a42ecc)

## Acknowledgments
Special thanks to the creators and maintainers of Streamlit, LangChain, and OpenAI for their incredible tools and resources.

