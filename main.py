from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response
from routes import routes

import logging


app = FastAPI()


app.include_router(routes)
# logger.debug("Start application")
