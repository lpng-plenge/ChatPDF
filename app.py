import streamlit as st
import pickle
import os
from streamlit_extras.add_vertical_space import add_vertical_space
from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv

with st.sidebar:
    st.title('LLM Chat App')
    st.markdown('''
    ## About
    This app is an LLM-powered chatbot built using :
    - [Streamlit](https://streamlit.io/)
    - [LangChain](https://python.langchain.com/)
    - [OpenAi](https://openai.com/api) LLM Model           
    ''')
    add_vertical_space(5)
    st.write('Made with ❤️ by [LPNG](https://bold.pro/my/luispablo-nietogil-240430122933)')

load_dotenv()
def main():
    st.header("Chat with PDF 💬")
    

    #upload pdf files
    pdf = st.file_uploader("Upload your PDF", type='pdf')
    
    if pdf is not None:
        st.write(pdf.name)
        pdf_reader = PdfReader(pdf)

        text = ""
        for page in pdf_reader.pages:
            text +=page.extract_text()
        
        #Split the text into a smaller pieces
        text_splitter = RecursiveCharacterTextSplitter(
            #chunk_size: Determines the maximum number of characters in each chunk when splitting a text. It specifies the size or length of each chunk.
            chunk_size=1000,
            #Determines the number of characters that overlap between consecutive chunks when splitting text. It specifies how much of the previous chunk should be included in the next chunk.
            chunk_overlap = 200,
            length_function = len
        )
        #Provide the text chunks
        chunks = text_splitter.split_text(text=text)

        #Embedings 
        store_name = pdf.name[:-4] #Store the file extension
        if os.path.exists(f"{store_name}.pkl"):
            with open(f"{store_name}.pkl", "rb") as f:
                VectorStore = pickle.load(f)
            st.write("Embedings Loaded from the Disk")
        else:
            embeddings = OpenAIEmbeddings()
            VectorStore = FAISS.from_texts(chunks, embedding=embeddings)
        
            with open(f"{store_name}.pkl", "wb") as f:
                pickle.dump(VectorStore, f)
        
if __name__ == '__main__':
    main()