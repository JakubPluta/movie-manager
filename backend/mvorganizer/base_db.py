from sqlite3 import connect
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.engine.base import Engine


SQLALCHEMY_DATABASE_URI: str = "sqlite:///./movies.db"

engine: Engine = create_engine(SQLALCHEMY_DATABASE_URI, connect_args={
    'check_same_thread': False
})

SessionLocal: Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()