from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum
from sqlalchemy.sql import func
import enum
from models.base import Base


class UploadTab(enum.Enum):
    """Upload tab categories."""
    property = "property"
    case = "case"
    research = "research"
    junior = "junior"


class Upload(Base):
    __tablename__ = "uploads"
    
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    tab = Column(Enum(UploadTab), nullable=False)
    filename = Column(String(500), nullable=False)
    filepath = Column(String(1000), nullable=False)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())

