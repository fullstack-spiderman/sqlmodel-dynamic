from fastapi import Depends, FastAPI
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_session, init_db
from models import Song, SongCreate, SongRead
# , app_settings
from settings import AppSettings, DBSettings, get_app_settings, get_db_settings, read_attrs
from config import cnf

app = FastAPI()


@app.on_event("startup")
async def on_startup():
    await init_db()


@app.get("/ping")
async def pong():
    # return {"ping": "pong"}
    return {
        "ping": "pong",
        'updated': True,
        "pg_dsn": cnf.dict().get('uri'),
    }


# @app.get("/ping")
# async def pong(app_settings: AppSettings = Depends(get_app_settings), settings: DBSettings = Depends(get_db_settings)):
#     # return {"ping": "pong"}
#     attrs = read_attrs(app_settings.environment)
#     print({'att': attrs})
#     return {
#         "ping": "pong",
#         "env": app_settings.environment,
#         "pg_dsn": settings._pg_dsn,
#         "db_env": settings.env,
#         'updated': True,
#         'attrss': attrs,
#         "pg_dsn": cnf.uri
#     }


@app.get("/songs", response_model=list[SongRead])
async def get_songs(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Song))
    songs = result.scalars().all()

    print({"data": songs})
    return songs
    # return [
    #     Song(name=song.name, artist=song.artist, year=song.year, id=song.id)
    #     for song in songs
    # ]


@app.post("/songs")
async def add_song(song: SongCreate, session: AsyncSession = Depends(get_session)):
    # new_song = Song(**song.dict())
    new_song = Song(name=song.name, artist=song.artist)
    session.add(new_song)
    await session.commit()
    await session.refresh(new_song)
    return new_song
