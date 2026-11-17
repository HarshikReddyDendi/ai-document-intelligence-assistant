
from app.services.pdf_loader import extract_text_from_pdf
from app.services.text_splitter import split_text
from app.services.embeddings import load_embedding_model
from app.services.vector_store import create_vector_store
from app.services.rag_pipeline import generate_answer

# Load PDF
pages = extract_text_from_pdf(
    "data/uploads/sample.pdf"
)

# Create chunks
chunks = split_text(pages)

# Load embedding model
embedding_model = load_embedding_model()

# Create vector database
vector_store = create_vector_store(
    chunks,
    embedding_model
)

# Ask question
question = "What is the company's maternity leave policy?"

# Generate answer
result = generate_answer(
    vector_store,
    question
)

print("\nAI ANSWER:")
print(result["answer"])

print("\nSOURCE REFERENCES:")

for source in result["sources"]:
    print("Page:", source["page_number"])
