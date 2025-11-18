from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain.community.embeddings import SentenceTransformerEmbeddings
from langchain.community.vectorstores import Chroma
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA

import os

def load_and_split_documents(file_path):
    #load .txt
    loader = TextLoader(file_path)
    documents = loader.load()

    #split the doc
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs = text_splitter._split_documents(documents)
    return docs

# use 
# file_path = "knowladge.txt"
# chunks = load_and_split_documents(file_path)


def create_vector_store(chunks):
    # Create embeddings
    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

    # Create vector store
    vector_store = Chroma.from_documents(documents=chunks, embeddings=embeddings)
    return vector_store

create_vector_store = create_vector_store(chunks)    


def setup_rag_chain(create_vector_store):
    llm = Ollama(model="llama2")
    retriever = vector_store.as_retriever()
    qa_chain = RetrievalQA.from_chain_type(
        llm,
        chain_type="stuff",
        retriever=retriever
    )
    return qa_chain
