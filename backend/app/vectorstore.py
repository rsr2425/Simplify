"""
Super early version of a vector store. Just want to make something available for the rest of the app to use.
"""
import os
import requests
import nltk

from langchain_community.vectorstores import Qdrant
from langchain_openai.embeddings import OpenAIEmbeddings

nltk.download('punkt_tab')
nltk.download('averaged_perceptron_tagger_eng')

embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")

# Create static/data directory if it doesn't exist
os.makedirs("static/data", exist_ok=True)

# Download and save the webpage
url = "https://python.langchain.com/docs/tutorials/rag/"
response = requests.get(url)
with open("static/data/langchain_rag_tutorial.html", "w", encoding="utf-8") as f:
    f.write(response.text)

from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Load HTML files from static/data directory
loader = DirectoryLoader("static/data", glob="*.html")
documents = loader.load()

# Split documents into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
split_chunks = text_splitter.split_documents(documents)

vector_db = Qdrant.from_documents(
    split_chunks,
    embedding_model,
    location=":memory:",
    collection_name="extending_context_window_llama_3",
)