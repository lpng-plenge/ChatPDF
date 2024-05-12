import streamlit as st
import numpy as np
import time
from streamlit_extras.add_vertical_space import add_vertical_space
from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from openai import OpenAI
from string import Template

client = OpenAI(api_key = st.secrets["OpenAI_key"],
)

# Function to stream the data
def stream_data(response):
    for word in response.split(" "):
        yield word + " "
        time.sleep(0.02)

# Function to generate response from model
def generate_response(query, sorted_result):
    # Generate a response
    t = Template("""
    You are a helpful and expert assistant in text reading. Customers describe what they want to search for in their work, files, activities, and everyday life information. Make suggestions based on the descriptions of the texts provided below. ONLY use the descriptions of the provided text, you can use other sources of information.

    If you cannot generate a meaningful response based on the description of the given text, say "Sorry, I cannot help". If the user's input is not related to finding a definition, concept, and/or summary, say "Sorry, I can only help with information provided in the loaded text".

    ===========
    $options
    ===========
    """)
    system_prompt = t.substitute(options = "\n\n".join([item[0] for item in sorted_result[:3]]))
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": query,
                }
            ]
        )
    return completion.choices[0].message.content

# Function to calculate embeddings
def get_embedding_vec(input):
    """Returns the embeddings vector for a given input"""
    return client.embeddings.create(
        input=input,
        model="text-embedding-3-large",
    ).data[0].embedding

# Function to split the text in an array
def split_text_into_chunks(text):
    """
    Split the input text into smaller chunks using RecursiveCharacterTextSplitter.

    Args:
        text (str): The input text to be split into chunks.

    Returns:
        List[str]: A list of text chunks.
    """
    # Initialize RecursiveCharacterTextSplitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )

    # Split the text into chunks
    chunks = text_splitter.split_text(text=text)
    return chunks

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    pdf_reader = PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    
    return text

# Function to display chat history
def display_chat_history():
    #Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    #Display messages from history on app run
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

# Function to display a sidebar
def display_sidebar():
    with st.sidebar:
        st.title('PDF Chat App')
        st.markdown('''
        ## About
        This app is an LLM-powered chatbot built using :
        - [Streamlit](https://streamlit.io/)
        - [LangChain](https://python.langchain.com/)
        - [OpenAi](https://openai.com/api) LLM Model           
        ''')
        add_vertical_space(5)
        st.write('Made with ❤️ by [LPNG](https://bold.pro/my/luispablo-nietogil-240430122933)')

def main():
    st.header("Chat with PDF 💬")
    # Display sidebar
    display_sidebar() 
    #upload pdf file
    pdf = st.file_uploader("Upload your PDF", type='pdf')

    if pdf is not None:
        display_chat_history()
        pdf_text = extract_text_from_pdf(pdf)
        chunks = split_text_into_chunks(pdf_text)
        
        if query:= st.chat_input("Say something:"):

            with st.chat_message("human"):
                st.write(stream_data(query))
                st.session_state.messages.append({"role": "user", "content": query})
            
            with st.chat_message("ai"):
                st.write(stream_data("Hello 👋"))
                st.write(stream_data("typing..."))

                # Let's calculate the embedding vectors of all chunk docs.
                # Here we simply store them in an array in memory.
                embeddings = []
                for chunk_text in chunks:
                    embeddings.append((chunk_text, get_embedding_vec(chunk_text)))
                
                query_embedding = get_embedding_vec(query)
                
                sorted_result = []
                # Iterate over all chunk text and calculate the similarity (dot product) of
                # the paragraphs description and the query text.
                for chunk_text, embedding in embeddings:
                    similarity = np.dot(embedding, query_embedding)
                    sorted_result.append((chunk_text, embedding, similarity ))
                
                # We sort the result descending based on the similarity so that the top
                # elements are probably more relevant than the last ones.
                sorted_result = sorted(sorted_result, key=lambda x: x[2], reverse=True)
                
                # Generate response
                response = generate_response(query, sorted_result)
                st.write_stream(stream_data(response))
                st.session_state.messages.append({"role": "ai", "content": response})
           
if __name__ == '__main__':
    main()