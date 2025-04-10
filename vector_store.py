from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
import os

# Path to store persistent Chroma DB
CHROMA_DB_DIR = "chroma_db"

def load_and_embed_documents(folder_path="static_docs"):
    """Loads .txt files from static_docs/, splits, embeds, and stores in ChromaDB."""
    documents = []

    for filename in os.listdir(folder_path):
        if filename.endswith(".txt") or filename.endswith(".md"):
            loader = TextLoader(os.path.join(folder_path, filename))
            documents.extend(loader.load())

    # Split long documents into chunks
    splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    split_docs = splitter.split_documents(documents)

    # Use HuggingFace embeddings
    embedding = HuggingFaceEmbeddings()

    # Create and persist the vector store
    vectordb = Chroma.from_documents(split_docs, embedding, persist_directory=CHROMA_DB_DIR)
    vectordb.persist()

    print(f"✅ Embedded {len(split_docs)} chunks into ChromaDB.")
    return vectordb

def get_vector_db():
    """Returns the existing Chroma vector DB for use in retrieval chains."""
    embedding = HuggingFaceEmbeddings()
    vectordb = Chroma(persist_directory=CHROMA_DB_DIR, embedding_function=embedding)
    return vectordb
