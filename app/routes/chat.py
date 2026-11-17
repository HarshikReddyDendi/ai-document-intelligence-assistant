
from fastapi import APIRouter, HTTPException

from app.models.schemas import QuestionRequest
from app.database import get_document
from app.services.vector_store import load_vector_store
from app.services.rag_pipeline import generate_answer

router = APIRouter()


@router.post("/ask")
def ask_question(request: QuestionRequest):
    """
    Ask questions about an uploaded PDF using RAG.
    """

    document_id = str(request.document_id)
    question = request.question.strip()

    # 1. Validate question
    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    # 2. Retrieve document from SQLite
    document = get_document(document_id)

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found. Please upload it first."
        )

    # 3. Load cached FAISS vector store
    try:
        vector_store = load_vector_store(
            document["vector_path"]
        )

    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="FAISS index not found for this document."
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Error loading vector store: {str(error)}"
        )

    # 4. Generate answer
    try:
        result = generate_answer(
            vector_store,
            question
        )

        return {
            "document_id": document_id,
            "filename": document["filename"],
            "question": question,
            "answer": result["answer"],
            "sources": result["sources"]
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Question processing failed: {str(error)}"
        )
