from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.models import Base

DB_URL = "sqlite:///./ag_lab.db"
engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def init_db() -> None:
    Base.metadata.create_all(engine)


def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
