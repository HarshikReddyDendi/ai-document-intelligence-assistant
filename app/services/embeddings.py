
from functools import lru_cache
from langchain_huggingface import HuggingFaceEmbeddings


@lru_cache(maxsize=1)
def load_embedding_model():
    """
    Load the embedding model once and reuse it.
    """

    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True}
    )


def generate_embeddings(text_chunks: list):
    """
    Convert text chunks into numerical vectors.
    """

    model = load_embedding_model()

    texts = [chunk["text"] for chunk in text_chunks]

    return model.embed_documents(texts)
