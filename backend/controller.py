from datetime import datetime, UTC
from sqlalchemy.orm import Session
from backend.models import Note
from backend.schemas import NoteCreate

def create_note(db: Session, note: NoteCreate):
    db_note = Note(title=note.title, content=note.content)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

def get_notes(db: Session):
    return db.query(Note).filter(Note.deleted_at.is_(None)).all()

def get_note(db: Session, note_id: int):
    return db.query(Note).filter(Note.id == note_id, Note.deleted_at.is_(None)).first()

def update_note(db: Session, note_id: int, note_data: dict):
    note = db.query(Note).filter(Note.id == note_id, Note.deleted_at.is_(None)).first()
    if note:
        for key, value in note_data.items():
            setattr(note, key, value)
        db.commit()
        db.refresh(note)
    return note

def delete_note(db: Session, note_id: int):
    note = db.query(Note).filter(Note.id == note_id).first()
    if note:
        note.deleted_at = datetime.now(UTC)
        db.commit()
    return note