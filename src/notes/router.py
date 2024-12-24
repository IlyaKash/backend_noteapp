from fastapi import APIRouter, Depends, HTTPException
from database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .models import Note
from .schemas import NoteCreate, NoteResponse
from .get_user_id import get_current_user
from auth.config_token import verify_access_token
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter(
    prefix="/notes",
    tags=["Notes"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@router.get("/get_all_notes")
async def get_all_notes(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_async_session)):
    # Декодируем токен, чтобы получить user_id
    user_id=verify_access_token(token)['user_id']
    
    # Получаем заметки, принадлежащие текущему пользователю
    result = await db.execute(select(Note).filter(Note.user_id == user_id))  # Фильтруем по user_id
    notes = result.scalars().all()  # Извлекаем все заметки
    
    if not notes:
        raise HTTPException(status_code=404, detail="No notes found for this user")

    return notes

@router.post("/add_note", response_model=NoteResponse)
async def post_new_note(
    note: NoteCreate,
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_async_session),
):
    user=verify_access_token(token)
    user_id=user['user_id']
    new_note = Note(title=note.title, text=note.text, user_id=user_id)
    session.add(new_note)
    await session.commit()
    await session.refresh(new_note)
    return new_note


@router.delete("/{note_id}", response_model=dict)
async def delete_note(note_id: int, token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_async_session)):
    user = verify_access_token(token)
    user_id = user['user_id']

    # Исправлено условие фильтрации с использованием & для логического И
    result = await session.execute(select(Note).where(Note.id == note_id, Note.user_id == user_id))
    note = result.scalars().first()

    if not note:
        raise HTTPException(status_code=404, detail="Заметка не найдена")

    await session.delete(note)
    await session.commit()

    return {"message": "Заметка удалена"}

@router.patch("/{note_id}", response_model=NoteResponse)
async def patch_note(
    note_id: int, 
    new_note:NoteCreate, 
    token:str=Depends(oauth2_scheme), 
    session:AsyncSession=Depends(get_async_session)
    ):
    user=verify_access_token(token)
    user_id=user['user_id']
    result=await session.execute(select(Note).where(Note.id==note_id, Note.user_id==user_id))
    note=result.scalars().first()

    if not note:
        raise HTTPException(status_code=404, detail="Заметка не найдена")
    
    # Обновляем поля заметки
    if (new_note.title!=""): note.title = new_note.title
    if (new_note.text!=""): note.text = new_note.text

    # Сохраняем изменения в базе данных
    session.add(note)
    await session.commit()
    await session.refresh(note)

    # Возвращаем обновленный объект заметки
    return note


