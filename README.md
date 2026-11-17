
# 📄 AI Document Intelligence Assistant

An AI-powered PDF document intelligence application that allows users to upload multiple PDF documents, search their contents, and ask natural-language questions using Retrieval-Augmented Generation (RAG).

Built with **Python, FastAPI, Streamlit, FAISS, Hugging Face Embeddings, SQLite, and Groq LLM**.

## 🚀 Features

- **Multiple PDF Uploads:** Upload multiple PDF documents through the Streamlit interface.
- **PDF Text Extraction:** Extract text from PDF files using PyMuPDF.
- **Intelligent Text Chunking:** Split extracted content into smaller chunks using LangChain.
- **Semantic Embeddings:** Generate vector embeddings using Sentence Transformers.
- **Vector Search:** Store and retrieve relevant document chunks using FAISS.
- **AI-Powered Question Answering:** Generate contextual answers using Groq LLM.
- **Retrieval-Augmented Generation:** Ground answers in retrieved document content.
- **Persistent Document Library:** Store document metadata using SQLite.
- **Document Selection:** Select previously uploaded PDFs and chat with them.
- **Source References:** Display relevant document passages and page numbers.
- **REST API:** Expose document upload and question-answering functionality through FastAPI.

## 🏗️ System Architecture

```text
                 User
                  |
                  v
          Streamlit Frontend
                  |
                  v
             FastAPI
                  |
          +-------+-------+
          |               |
          v               v
      PDF Upload      Chat API
          |               |
          v               v
      PyMuPDF         User Query
          |               |
          v               v
     Text Chunking    FAISS Search
          |               |
          v               v
    Hugging Face      Relevant Chunks
     Embeddings           |
          |               v
          v           RAG Pipeline
         FAISS             |
          |               v
          v             Groq LLM
      Vector Store         |
                          v
                    AI Response
                          |
                          v
                    Streamlit UI

       SQLite: Document Metadata
```

## 🛠️ Technology Stack

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Frontend | Streamlit |
| Backend | FastAPI |
| LLM | Groq |
| Embeddings | Hugging Face Sentence Transformers |
| Vector Database | FAISS |
| Database | SQLite |
| PDF Processing | PyMuPDF |
| AI Framework | LangChain |
| API Testing | Swagger UI, Postman |
| Version Control | Git, GitHub |

## 📁 Project Structure

```text
ai-document-intelligence-assistant/
│
├── app/
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   │
│   ├── models/
│   │   └── schemas.py
│   │
│   ├── routes/
│   │   ├── upload.py
│   │   └── chat.py
│   │
│   └── services/
│       ├── pdf_loader.py
│       ├── text_splitter.py
│       ├── embeddings.py
│       ├── vector_store.py
│       └── rag_pipeline.py
│
├── frontend/
│   └── streamlit_app.py
│
├── data/
│   └── uploads/
│
├── vectorstore/
│
├── tests/
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/HarshikReddyDendi/ai-document-intelligence-assistant.git

cd ai-document-intelligence-assistant
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
```

Get your API key from [Groq Console](https://console.groq.com/).

Never commit your `.env` file or expose your API key.

### 5. Start the FastAPI backend

```bash
uvicorn app.main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

### 6. Start the Streamlit frontend

Open another terminal:

```bash
streamlit run frontend/streamlit_app.py
```

Frontend:

```text
http://localhost:8501
```

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | API welcome endpoint |
| GET | `/health` | Health check |
| GET | `/documents` | Retrieve registered documents |
| POST | `/upload` | Upload and process a PDF |
| POST | `/ask` | Ask questions about a document |

### Example: Ask a Question

**POST** `/ask`

Request:

```json
{
  "document_id": "your-document-uuid",
  "question": "What are the main topics in this document?"
}
```

The response contains the AI-generated answer and source references.

## 🧠 How RAG Works

1. **Document ingestion:** Upload a PDF and extract its text.
2. **Chunking:** Divide extracted text into manageable sections.
3. **Embedding generation:** Convert text chunks into numerical vectors.
4. **Vector storage:** Store vectors in FAISS.
5. **Query processing:** Convert the user's question into an embedding.
6. **Similarity search:** Retrieve relevant document chunks.
7. **Context construction:** Pass retrieved content to the LLM.
8. **Answer generation:** Generate a contextual response with source references.

## 🧪 Testing

The project includes test scripts for individual components:

```bash
python test_pdf.py
python test_chunking.py
python test_embeddings.py
python test_faiss.py
python test_rag.py
```

## 🔐 Security Considerations

- Keep API keys in environment variables.
- Exclude uploaded documents and local databases from Git.
- Validate uploaded PDF files before processing.
- Only load trusted local FAISS indexes.
- Do not commit personal or confidential documents.

## 🔮 Future Improvements

- Persistent chat history using SQLite.
- Document deletion and management.
- Multi-document question answering.
- Automatic PDF summarization.
- Improved retrieval accuracy and relevance filtering.
- Docker containerization.
- Cloud deployment and authentication.

## 👨‍💻 Author

**Harshik Reddy Dendi**

GitHub: [HarshikReddyDendi](https://github.com/HarshikReddyDendi)

---

⭐ If you find this project interesting, consider giving it a star!

**Built as a practical AI Engineering project exploring RAG, vector databases, LLM integration, and backend development.**
