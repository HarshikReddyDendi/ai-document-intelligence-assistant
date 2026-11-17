
from app.services.pdf_loader import extract_text_from_pdf
from app.services.text_splitter import split_text
from app.services.embeddings import generate_embeddings

pdf_path = "data/uploads/sample.pdf"

# Step 1: Extract PDF text
pages = extract_text_from_pdf(pdf_path)

# Step 2: Create chunks
chunks = split_text(pages)

# Step 3: Generate embeddings
vectors = generate_embeddings(chunks)

print("Total chunks:", len(chunks))
print("Total embeddings:", len(vectors))

# Display first embedding
print("\nFirst embedding:")
print(vectors[0][:10])

# Check vector dimensions
print("\nEmbedding dimensions:", len(vectors[0]))
