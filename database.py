from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()
engine = create_async_engine("sqlite+aiosqlite:///./music.db", echo=True)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, index=True)

class Track(Base):
    __tablename__ = "tracks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    artist = Column(String)
    file_id = Column(String, unique=True, index=True)
    title_lower = Column(String, index=True)  # Нормализованное название в нижнем регистре
    artist_lower = Column(String, index=True)  # Нормализованный исполнитель в нижнем регистре

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
