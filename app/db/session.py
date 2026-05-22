from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    # SQLite blocks concurrent access by default. FastAPI runs handlers in a
    # thread pool, so this flag is required to avoid "check same thread" errors.
    connect_args={"check_same_thread": False},
    echo=False,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    except Exception:
        # Roll back any uncommitted changes if the request handler raises,
        # keeping the session in a clean state before it is closed.
        db.rollback()
        raise
    finally:
        db.close()
