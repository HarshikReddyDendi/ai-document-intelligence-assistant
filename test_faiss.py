
from app.services.pdf_loader import extract_text_from_pdf
from app.services.text_splitter import split_text
from app.services.embeddings import load_embedding_model
from app.services.vector_store import (
    create_vector_store,
    search_documents
)

# Step 1: Extract PDF text
pages = extract_text_from_pdf(
    "data/uploads/sample.pdf"
)

# Step 2: Split into chunks
chunks = split_text(pages)

# Step 3: Load embedding model
embedding_model = load_embedding_model()

# Step 4: Create FAISS vector database
vector_store = create_vector_store(
    chunks,
    embedding_model
)

print("FAISS database created successfully!")

# Step 5: Ask a question
query = "What AI projects are mentioned?"
query = "Which programming languages are listed?"
query = "What educational qualifications are mentioned?"

results = search_documents(
    vector_store,
    query,
    k=3
)

# Step 6: Display results
print("\nQuestion:", query)

for index, (document, score) in enumerate(
    results, start=1
):
    print(f"\nResult {index}")
    print("Page:", document.metadata["page_number"])
    print("Distance:", score)
    print("Content:", document.page_content)
