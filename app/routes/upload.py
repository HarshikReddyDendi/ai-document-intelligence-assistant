
import os
import uuid

from fastapi import APIRouter, UploadFile, File, HTTPException

from app.database import save_document

from app.services.pdf_loader import extract_text_from_pdf
from app.services.text_splitter import split_text
from app.services.embeddings import load_embedding_model
from app.services.vector_store import create_vector_store


router = APIRouter()

UPLOAD_DIR = "data/uploads"
VECTOR_DIR = "vectorstore"

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(VECTOR_DIR, exist_ok=True)


@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )

    document_id = str(uuid.uuid4())

    file_path = os.path.join(
        UPLOAD_DIR,
        f"{document_id}.pdf"
    )

    vector_path = os.path.join(
        VECTOR_DIR,
        document_id
    )

    try:
        content = await file.read()

        if not content:
            raise HTTPException(
                status_code=400,
                detail="Uploaded PDF is empty."
            )

        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413,
                detail="PDF size cannot exceed 10 MB."
            )

        if not content.startswith(b"%PDF-"):
            raise HTTPException(
                status_code=400,
                detail="Invalid PDF file."
            )

        # Save PDF
        with open(file_path, "wb") as pdf_file:
            pdf_file.write(content)

        # Extract text
        pages = extract_text_from_pdf(file_path)

        if not pages:
            raise HTTPException(
                status_code=400,
                detail="No extractable text found in PDF."
            )

        # Split text into chunks
        chunks = split_text(pages)

        if not chunks:
            raise HTTPException(
                status_code=400,
                detail="No text chunks generated."
            )

        # Generate embeddings
        embedding_model = load_embedding_model()

        # Create document-specific FAISS index
        create_vector_store(
            chunks,
            embedding_model,
            vector_path
        )

        # Register document in SQLite
        save_document(
            document_id=document_id,
            filename=file.filename,
            file_path=file_path,
            vector_path=vector_path,
            total_pages=len(pages),
            total_chunks=len(chunks)
        )

        return {
            "message": "PDF uploaded and registered successfully",
            "document_id": document_id,
            "filename": file.filename,
            "total_pages": len(pages),
            "total_chunks": len(chunks)
        }

    except HTTPException:
        raise

    except Exception as error:

        # Clean up incomplete processing artifacts
        if os.path.exists(file_path):
            os.remove(file_path)

        if os.path.exists(vector_path):
            import shutil
            shutil.rmtree(vector_path, ignore_errors=True)

        raise HTTPException(
            status_code=500,
            detail=f"PDF processing failed: {error}"
        ) from error

    finally:
        await file.close()
