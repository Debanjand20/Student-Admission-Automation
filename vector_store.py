from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
import os

faiss_index_path = "faiss_index"

def load_and_embed_documents(folder_path="static_docs"):
    """Load and embed documents into FAISS index."""
    documents = []

    for filename in os.listdir(folder_path):
        if filename.endswith(".txt") or filename.endswith(".md"):
            loader = TextLoader(os.path.join(folder_path, filename))
            documents.extend(loader.load())

    # Split large documents
    splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    split_docs = splitter.split_documents(documents)

    # HuggingFace embeddings
    embedding = HuggingFaceEmbeddings()

    # Create FAISS index
    vectordb = FAISS.from_documents(split_docs, embedding)

    # Save index locally
    vectordb.save_local(faiss_index_path)

    print(f"✅ Embedded {len(split_docs)} chunks into FAISS index.")
    return vectordb

def get_vector_db():
    """Load FAISS index from local storage."""
    embedding = HuggingFaceEmbeddings()
    return FAISS.load_local(faiss_index_path, embeddings=embedding)
