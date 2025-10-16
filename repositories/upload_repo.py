"""Upload repository for CRUD operations."""

from typing import Optional, List
from sqlalchemy.orm import Session
from models.upload import Upload, UploadTab
from utils.db_exceptions import NotFound


def create_upload(session: Session, **data) -> Upload:
    """Create a new upload record."""
    upload = Upload(**data)
    session.add(upload)
    session.flush()
    return upload


def get_upload_by_id(session: Session, upload_id: int) -> Optional[Upload]:
    """Get upload by ID."""
    return session.query(Upload).filter(Upload.id == upload_id).first()


def list_uploads_by_user(session: Session, user_id: int, limit: int = 50, offset: int = 0) -> List[Upload]:
    """List uploads for a specific user with pagination."""
    return (
        session.query(Upload)
        .filter(Upload.user_id == user_id)
        .order_by(Upload.uploaded_at.desc())
        .limit(limit)
        .offset(offset)
        .all()
    )


def list_uploads_by_client(session: Session, client_id: int) -> List[Upload]:
    """List all uploads for a specific client."""
    return (
        session.query(Upload)
        .filter(Upload.client_id == client_id)
        .order_by(Upload.uploaded_at.desc())
        .all()
    )


def list_uploads_by_tab(session: Session, user_id: int, tab: UploadTab, limit: int = 50) -> List[Upload]:
    """List uploads for a specific user and tab category."""
    return (
        session.query(Upload)
        .filter(Upload.user_id == user_id, Upload.tab == tab)
        .order_by(Upload.uploaded_at.desc())
        .limit(limit)
        .all()
    )


def update_upload(session: Session, upload_id: int, **fields) -> Upload:
    """Update upload fields."""
    upload = get_upload_by_id(session, upload_id)
    if not upload:
        raise NotFound(f"Upload {upload_id} not found")
    
    for key, value in fields.items():
        if hasattr(upload, key):
            setattr(upload, key, value)
    
    session.flush()
    return upload


def delete_upload(session: Session, upload_id: int) -> bool:
    """Delete upload by ID. Returns True if deleted, False if not found."""
    upload = get_upload_by_id(session, upload_id)
    if not upload:
        return False
    
    session.delete(upload)
    session.flush()
    return True

