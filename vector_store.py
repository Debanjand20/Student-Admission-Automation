from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
import os

def load_and_embed_documents(folder_path="static_docs"):
    """Loads .txt files, splits, embeds, and stores them in memory (ChromaDB)."""
    documents = []

    for filename in os.listdir(folder_path):
        if filename.endswith(".txt") or filename.endswith(".md"):
            loader = TextLoader(os.path.join(folder_path, filename))
            documents.extend(loader.load())

    # Split long documents
    splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    split_docs = splitter.split_documents(documents)

    # Embedding
    embedding = HuggingFaceEmbeddings()

    # Use in-memory Chroma (no persist_directory)
    vectordb = Chroma.from_documents(split_docs, embedding)
    print(f"✅ Embedded {len(split_docs)} chunks into in-memory ChromaDB.")
    return vectordb

def get_vector_db():
    """Creates a fresh in-memory vector DB from embedded docs every time."""
    embedding = HuggingFaceEmbeddings()
    return Chroma(embedding_function=embedding)  # no persistent mode
