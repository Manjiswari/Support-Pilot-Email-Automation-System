import os
import tempfile
from pathlib import Path
from uuid import uuid4
from datetime import datetime, UTC
from sqlalchemy.orm import Session
from pinecone import Pinecone, EmbedQuery
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from database import engine, DocumentMetadata, Email

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")
PINECONE_NAMESPACE = "support-pilot"

if not PINECONE_API_KEY:
    raise ValueError("PINECONE_API_KEY missing")
if not PINECONE_INDEX_NAME:
    raise ValueError("PINECONE_INDEX_NAME missing")

pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(PINECONE_INDEX_NAME)


def extract_text(content: bytes, extension: str) -> str:
    """Write bytes to a temp file, load with the appropriate LangChain loader."""
    suffix = extension  # e.g. ".pdf"
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        tmp.write(content)
        tmp_path = tmp.name
    try:
        if extension == ".pdf":
            loader = PyPDFLoader(tmp_path)
        elif extension == ".docx":
            loader = Docx2txtLoader(tmp_path)
        else:  # .txt
            loader = TextLoader(tmp_path, encoding="utf-8")
        docs = loader.load()
        return "\n\n".join(doc.page_content for doc in docs)
    finally:
        os.unlink(tmp_path)


def chunk_text(text: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> list[str]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    return splitter.split_text(text)


def save_metadata(rows: list[dict]):
    with Session(engine) as session:
        session.add_all([
            DocumentMetadata(
                document_id=row["document_id"],
                filename=row["filename"],
                chunk_id=row["chunk_id"],
                pinecone_id=row["pinecone_id"],
                created_at=row["created_at"],
            )
            for row in rows
        ])
        session.commit()

def store_chunks(filename: str, chunks: list[str]) -> str:
    document_id = str(uuid4())
    upload_time = datetime.now(UTC)

    documents = []
    metadata_rows = []

    for i, chunk in enumerate(chunks):
        vector_id = f"{document_id}_chunk_{i}"

        documents.append({
            "_id": vector_id,
            "chunk_text": chunk,
            "title": filename,
            "document_id": document_id,
            "filename": filename,
            "chunk_id": i,
            "upload_time": upload_time.isoformat(),
        })

        metadata_rows.append({
            "document_id": document_id,
            "filename": filename,
            "chunk_id": i,
            "pinecone_id": vector_id,
            "created_at": upload_time,
        })

    index.documents.upsert(
        namespace=PINECONE_NAMESPACE,
        documents=documents,
    )

    save_metadata(metadata_rows)

    return document_id

def search_chunks(query: str, top_k: int = 5):
    return index.documents.search(
        namespace=PINECONE_NAMESPACE,
        top_k=top_k,
        score_by=[
            EmbedQuery(
                field="chunk_text",
                query=query,
            )
        ],
        include_fields=["chunk_text", "title"],
    )

def delete_document(document_id: str) -> int:
    with Session(engine) as session:
        rows = (
            session.query(DocumentMetadata)
            .filter(DocumentMetadata.document_id == document_id)
            .all()
        )

        if not rows:
            return 0

        ids = [row.pinecone_id for row in rows]

        index.documents.delete(
            namespace=PINECONE_NAMESPACE,
            ids=ids,
        )

        for row in rows:
            session.delete(row)

        session.commit()

        return len(ids)
    
def check_database_health() -> dict:
    """Check database health by running a simple query."""
    from sqlalchemy import text
    try:
        with Session(engine) as session:
            session.execute(text("SELECT 1"))
        return {"status": "healthy"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}


def check_pinecone_health() -> dict:
    """Check Pinecone health by calling describe_index_stats."""
    try:
        index.describe_index_stats()
        return {"status": "healthy"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

