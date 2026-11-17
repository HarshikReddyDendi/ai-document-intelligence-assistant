
from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_text(pages: list) -> list:
    """
    Split extracted PDF pages into smaller chunks.
    Preserve page numbers as metadata.
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        separators=["\n\n", "\n", " ", ""]
    )

    chunks = []

    for page in pages:
        page_chunks = splitter.split_text(page["text"])

        for chunk in page_chunks:
            chunks.append({
                "text": chunk,
                "page_number": page["page_number"]
            })

    return chunks
