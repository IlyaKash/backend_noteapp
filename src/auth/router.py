from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from database import get_async_session
from .models import User
from .hash_pass import hash_password, verify_password
from .config_token import create_access_token, verify_access_token
from .schemas import UserCreate, UserCreateTelegram, UserResponse, Token, UserTelegramId
from typing import Union, Optional

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")



@router.post("/register", response_model=UserResponse)
async def register_user(
    user: Union[UserCreate, UserCreateTelegram],
    db: AsyncSession = Depends(get_async_session)
    ):
    result = await db.execute(select(User).filter(User.username == user.username))
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")
    hashed_password = hash_password(user.password)
    new_user = User(
        username=user.username, 
        email=user.email, 
        hashed_password=hashed_password,
        telegram_id=user.telegram_id if isinstance(user, UserCreateTelegram) else None #Если регестрация из телеграмма
        #Заполняем еще и поле telegram_id, иначе None
    )
    db.add(new_user)
    await db.commit()  # Асинхронная коммитация
    await db.refresh(new_user)  # Асинхронное обновление объекта пользователя

    return new_user


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_async_session)):
    result = await db.execute(select(User).filter(User.username == form_data.username))
    user = result.scalars().first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(data={"username": user.username, "user_id": user.id})  # передаем user_id
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me", response_model=UserResponse)
async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_async_session)):
    # Декодируем токен, чтобы получить имя пользователя
    user = verify_access_token(token)  # Проверка токена
    result = await db.execute(select(User).filter(User.username == user['username']))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/users/telegram_id", response_model=Token)
async def get_all_telegram_id(telegram_id : str, db: AsyncSession=Depends(get_async_session)):
    result = await db.execute(select(User).filter(User.telegram_id == telegram_id))
    user=result.scalars().first()
    if user:
        acces_token=create_access_token(data={'username': user.username, 'user_id': user.id})
        return {'access_token': acces_token, "token_type": 'bearer'}
    else:
        raise HTTPException(status_code=404, detail="User not found")
