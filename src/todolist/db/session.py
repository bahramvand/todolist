from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from todolist.core.settings import db_settings

engine = create_engine(
    db_settings.url,
    echo=False,
    future=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)
