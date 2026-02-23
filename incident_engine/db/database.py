from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from contextlib import contextmanager
from incident_engine.config import DATABASE_URL


DATABASE = str(DATABASE_URL)

engine = create_engine(DATABASE)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

engine = create_engine(DATABASE, echo=False)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()


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