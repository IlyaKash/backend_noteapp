from fastapi import FastAPI
from notes.router import router as router_notes
from auth.router import router as auth_router

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app:FastAPI):
    #Загрузка кеша из редис, возможно понадобится 
    #redis = aioredis.from_url("redis://localhost")
    #FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield


app=FastAPI(
    title="Notes App",
    lifespan=lifespan,
)

app.include_router(
    router=router_notes
)

app.include_router(
    router=auth_router
)


@app.get("/")
async def root():
    return {"message" : "Приложение для заметок"}