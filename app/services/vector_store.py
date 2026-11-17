
import os
from functools import lru_cache

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

from app.services.embeddings import load_embedding_model


def create_vector_store(
    chunks: list,
    embedding_model,
    save_path: str = "vectorstore/faiss_index"
):
    """
    Create a FAISS vector store and save it locally.
    """

    documents = [
        Document(
            page_content=chunk["text"],
            metadata={
                "page_number": chunk["page_number"]
            }
        )
        for chunk in chunks
    ]

    vector_store = FAISS.from_documents(
        documents,
        embedding_model
    )

    os.makedirs(save_path, exist_ok=True)
    vector_store.save_local(save_path)

    # Remove any stale cached version of this index
    _load_vector_store_cached.cache_clear()

    return vector_store


@lru_cache(maxsize=32)
def _load_vector_store_cached(save_path: str):
    """
    Load and cache a FAISS index.
    """

    if not os.path.isdir(save_path):
        raise FileNotFoundError(
            f"Vector store not found: {save_path}"
        )

    embedding_model = load_embedding_model()

    return FAISS.load_local(
        save_path,
        embedding_model,
        allow_dangerous_deserialization=True
    )


def load_vector_store(save_path: str, embedding_model=None):
    """
    Return a cached FAISS vector store.
    """

    return _load_vector_store_cached(
        os.path.normpath(save_path)
    )


def clear_vector_store_cache():
    """
    Clear cached FAISS indexes.
    """

    _load_vector_store_cached.cache_clear()


def search_documents(vector_store, query: str, k: int = 3):
    """
    Retrieve the most relevant document chunks.
    Lower distance generally indicates greater similarity.
    """

    results = vector_store.similarity_search_with_score(
        query,
        k=k
    )

    return results
