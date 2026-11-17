
import sqlite3
from pathlib import Path

DATABASE_PATH = Path("data/documents.db")


def get_connection():
    DATABASE_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row

    return connection


def initialize_database():
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                document_id TEXT PRIMARY KEY,
                filename TEXT NOT NULL,
                file_path TEXT NOT NULL,
                vector_path TEXT NOT NULL,
                total_pages INTEGER,
                total_chunks INTEGER,
                uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)


def save_document(
    document_id,
    filename,
    file_path,
    vector_path,
    total_pages,
    total_chunks
):
    with get_connection() as connection:
        connection.execute("""
            INSERT INTO documents (
                document_id,
                filename,
                file_path,
                vector_path,
                total_pages,
                total_chunks
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            document_id,
            filename,
            file_path,
            vector_path,
            total_pages,
            total_chunks
        ))


def get_all_documents():
    with get_connection() as connection:
        rows = connection.execute("""
            SELECT * FROM documents
            ORDER BY uploaded_at DESC
        """).fetchall()

        return [dict(row) for row in rows]


def get_document(document_id):
    with get_connection() as connection:
        row = connection.execute("""
            SELECT * FROM documents
            WHERE document_id = ?
        """, (document_id,)).fetchone()

        return dict(row) if row else None
