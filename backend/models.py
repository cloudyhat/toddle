from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime, func
from sqlalchemy.orm import declarative_base
from datetime import datetime, UTC

Base = declarative_base()

class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)

    created_at = Column(
    DateTime(timezone=True),
    server_default=func.now(),
    nullable=False,
    )

    updated_at = Column(
    DateTime(timezone=True),
    server_default=func.now(),
    onupdate=func.now(), 
    nullable=False,
    )
    
    deleted_at = Column(DateTime(timezone=True), nullable=True)