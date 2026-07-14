from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from backend.models import Base
from backend.database import engine, get_db
from backend.schemas import NoteCreate, NoteRead
from backend import controller

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

@app.post("/notes", response_model=NoteRead)
def create_note(
    note: NoteCreate,
    db: Session = Depends(get_db),
):
    return controller.create_note(db, note)

@app.get("/notes", response_model=list[NoteRead])
def get_notes(db: Session = Depends(get_db)):
    return controller.get_notes(db)

@app.get("/notes/{note_id}", response_model=NoteRead)
def get_note(note_id: int, db: Session = Depends(get_db)):
    note = controller.get_note(db, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@app.put("/notes/{note_id}", response_model=NoteRead)
def update_note(note_id: int, note_data: NoteCreate, db: Session = Depends(get_db)):
    note = controller.update_note(db, note_id, note_data.model_dump())
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@app.delete("/notes/{note_id}", response_model=NoteRead)
def delete_note(note_id: int, db: Session = Depends(get_db)):
    note = controller.delete_note(db, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note