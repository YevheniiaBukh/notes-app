from database import Base
from pydantic import BaseModel as BaseSModel
from sqlalchemy import Column, Integer, String

class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)

class NoteResponse(BaseSModel):
    id: int
    title: str
    content: str

    class Config:
        from_attributes = True
        