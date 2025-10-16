"""Document repository for CRUD operations."""

from typing import Optional, List
from sqlalchemy.orm import Session
from models.document import Document
from utils.db_exceptions import NotFound


def create_document(session: Session, **data) -> Document:
    """Create a new document record."""
    document = Document(**data)
    session.add(document)
    session.flush()
    return document


def get_document_by_id(session: Session, document_id: int) -> Optional[Document]:
    """Get document by ID."""
    return session.query(Document).filter(Document.id == document_id).first()


def list_documents_by_client(session: Session, client_id: int) -> List[Document]:
    """List all documents for a specific client."""
    return (
        session.query(Document)
        .filter(Document.client_id == client_id)
        .order_by(Document.uploaded_at.desc())
        .all()
    )


def list_documents_by_user(session: Session, user_id: int, limit: int = 50, offset: int = 0) -> List[Document]:
    """List documents for a specific user with pagination."""
    return (
        session.query(Document)
        .filter(Document.user_id == user_id)
        .order_by(Document.uploaded_at.desc())
        .limit(limit)
        .offset(offset)
        .all()
    )


def list_documents_by_module(session: Session, user_id: int, module: str, limit: int = 50) -> List[Document]:
    """List documents for a specific user and module."""
    return (
        session.query(Document)
        .filter(Document.user_id == user_id, Document.module == module)
        .order_by(Document.uploaded_at.desc())
        .limit(limit)
        .all()
    )


def update_document(session: Session, document_id: int, **fields) -> Document:
    """Update document fields."""
    document = get_document_by_id(session, document_id)
    if not document:
        raise NotFound(f"Document {document_id} not found")
    
    for key, value in fields.items():
        if hasattr(document, key):
            setattr(document, key, value)
    
    session.flush()
    return document


def delete_document(session: Session, document_id: int) -> bool:
    """Delete document by ID. Returns True if deleted, False if not found."""
    document = get_document_by_id(session, document_id)
    if not document:
        return False
    
    session.delete(document)
    session.flush()
    return True

