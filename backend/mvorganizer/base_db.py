from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.engine.base import Engine
from sqlalchemy import event


def _fk_pragma_on_connect(e: Engine, _):
    e.execute("pragma foreign_keys=ON")


SQLALCHEMY_DATABASE_URI: str = "sqlite:///./movies.db"

engine: Engine = create_engine(
    SQLALCHEMY_DATABASE_URI, connect_args={"check_same_thread": False}
)

event.listen(engine, "connect", _fk_pragma_on_connect)


SessionLocal: Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
