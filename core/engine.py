from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


class EngineSessionFactory:
    """ Класс для обработки сессии SQLAlchemy. """
    def __init__(self, uri):
        engine = create_engine(uri)
        self.session_factory = sessionmaker(bind=engine, autocommit=False, autoflush=False)
        self.session = scoped_session(self.session_factory)

    def get_session_local(self):
        return self.session_factory()
