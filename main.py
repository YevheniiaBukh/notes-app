from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import models
import schemas
from database import SessionLocal, engine, Base


Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@app.get("/")
def home():
    return {"message": "Notes API works!"}
        
@app.post("/notes/")
def create_note(note: schemas.NoteCreate, db: Session = Depends(get_db)):
    new_note = models.Note(title=note.title, content=note.content)
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note

@app.get("/notes/")
def get_notes(db: Session = Depends(get_db)):
    notes = db.query(models.Note).all()
    return notes
@app.get("/notes/{note_id}")
def get_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if note:
        return note
    else:
        raise HTTPException(status_code=404, detail="Note not found")
    
    
@app.put("/notes/{note_id}")
def update_note(note_id: int, note: schemas.NoteCreate, db: Session = Depends(get_db)):
    existing_note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if existing_note:
        existing_note.title = note.title
        existing_note.content = note.content
        db.commit()
        db.refresh(existing_note)
        return existing_note
    else:
        raise HTTPException(status_code=404, detail="Note not found")

@app.delete("/notes/{note_id}") 
def delete_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if note:
        db.delete(note)
        db.commit()
        return {"message": "Note deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Note not found")
