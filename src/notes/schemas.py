from pydantic import BaseModel

class NoteBase(BaseModel):
    pass

class NoteCreate(NoteBase):
    title: str
    text: str

class NoteResponse(NoteBase):
    id: int
    title: str
    text: str

