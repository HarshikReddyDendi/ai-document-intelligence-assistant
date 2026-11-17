import pymupdf


def extract_text_from_pdf(file_path: str) -> list:
    """
    Extract text from every page of a PDF.
    Returns page-wise extracted text.
    """

    extracted_pages = []

    try:
        document = pymupdf.open(file_path)

        for page_number, page in enumerate(document, start=1):
            text = page.get_text("text")

            if text.strip():
                extracted_pages.append({
                    "page_number": page_number,
                    "text": text
                })

        document.close()

        return extracted_pages

    except Exception as error:
        raise RuntimeError(
            f"Failed to extract PDF text: {error}"
        ) from error
