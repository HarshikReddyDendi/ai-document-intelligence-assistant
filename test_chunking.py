
from app.services.pdf_loader import extract_text_from_pdf
from app.services.text_splitter import split_text

pdf_path = "data/uploads/sample.pdf"

pages = extract_text_from_pdf(pdf_path)

chunks = split_text(pages)

print("Total pages:", len(pages))
print("Total chunks:", len(chunks))

for index, chunk in enumerate(chunks, start=1):
    print(f"\n--- Chunk {index} ---")
    print("Page:", chunk["page_number"])
    print("Text:", chunk["text"])
