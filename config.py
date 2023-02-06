import os

from dotenv import load_dotenv
from core.engine import EngineSessionFactory


load_dotenv()

SQLALCHEMY_DATABASE_URL = os.environ.get('DB_URL')
db_engine = EngineSessionFactory(SQLALCHEMY_DATABASE_URL)
