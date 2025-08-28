from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base
from farm_cli.config import DATABASE_URL

engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def init_db():
    # create tables
    Base.metadata.create_all(bind=engine)

from contextlib import contextmanager

@contextmanager
def get_session():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
