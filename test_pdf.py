
from app.services.pdf_loader import extract_text_from_pdf

pdf_path = "data/uploads/sample.pdf"

pages = extract_text_from_pdf(pdf_path)

for page in pages:
    print(f"\nPage: {page['page_number']}")
    print(page["text"][:500])
