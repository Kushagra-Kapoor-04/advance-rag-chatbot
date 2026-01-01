import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from utils import hash_files
from config import EMBEDDING_MODEL

VECTOR_CACHE_DIR = "data/vector_cache"
os.makedirs(VECTOR_CACHE_DIR, exist_ok=True)


def get_vectorstore(chunks, file_paths):
    file_hash = hash_files(file_paths)
    cache_path = os.path.join(VECTOR_CACHE_DIR, file_hash)

    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL
    )

    if os.path.exists(cache_path):
        return FAISS.load_local(cache_path, embeddings, allow_dangerous_deserialization=True)

    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local(cache_path)

    return vectorstore
