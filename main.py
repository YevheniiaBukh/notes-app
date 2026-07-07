from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse

import models
import schemas
from database import SessionLocal, engine, Base


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="📝 Notes Service API",
    description="""
    ### Вітаємо у Notes API! 🎉
    Цей сервіс дозволяє створювати, переглядати та редагувати ваші особисті нотатки.
    
    * База даних: PostgreSQL 🐘
    * Статус деплою: Live на Render 🚀
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url=None)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@app.get("/", include_in_schema=False)
def redirect_to_docs():
    return RedirectResponse(url="/docs")

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
