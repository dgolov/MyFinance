import os
import logging.config

from dotenv import load_dotenv
from core.engine import EngineSessionFactory


load_dotenv()

log_config = {
    "version": 1,
    "formatters": {
        "formatter": {
            "format": '%(asctime)s - %(levelname)s - %(message)s',
            "datefmt": '%d-%b-%y %H:%M:%S',
        },
    },
    "handlers": {
        "console_handler": {
            "class": "logging.StreamHandler",
            "formatter": "formatter",
        },
        "file_handler": {
            "class": "logging.FileHandler",
            "formatter": "formatter",
            "filename": os.environ.get("LOGGING_PATH", None)
        },
    },
    "loggers": {
        "log": {
            "handlers": ["file_handler"],
            "level": os.environ.get("LOGGING_LEVEL", "DEBUG"),
        },
        "console": {
            "handlers": ["console_handler"],
            "level": os.environ.get("LOGGING_LEVEL", "DEBUG"),
        }
    },
}

logging.config.dictConfig(log_config)
logger_mode = 'console' if int(os.environ.get('DEBUG', True)) else 'log'
logger = logging.getLogger(logger_mode)

SQLALCHEMY_DATABASE_URL = os.environ.get('DB_URL')
db_engine = EngineSessionFactory(SQLALCHEMY_DATABASE_URL)
