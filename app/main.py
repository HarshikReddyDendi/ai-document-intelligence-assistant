
from fastapi import FastAPI

from app.database import initialize_database, get_all_documents

from app.routes.upload import router as upload_router
from app.routes.chat import router as chat_router


app = FastAPI(
    title="AI Document Intelligence Assistant",
    description="AI-powered PDF question answering using RAG",
    version="2.0.0"
)


@app.on_event("startup")
def startup_event():
    initialize_database()


@app.get("/")
def home():
    return {
        "message": "Welcome to AI Document Intelligence Assistant",
        "status": "running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.get("/documents")
def list_documents():
    return {
        "total_documents": len(get_all_documents()),
        "documents": get_all_documents()
    }


app.include_router(upload_router)
app.include_router(chat_router)
