from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session


Base = declarative_base()


class EngineSessionFactory:
    """ Класс для обработки сессии SQLAlchemy. """
    def __init__(self, uri):
        engine = create_engine(uri)
        self.session_factory = sessionmaker(bind=engine, autocommit=False, autoflush=False)
        self.session = scoped_session(self.session_factory)
