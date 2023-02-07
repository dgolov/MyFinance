from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response
from routes import routes
from config import db_engine, logger


app = FastAPI()


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = db_engine.get_session_local()
        response = await call_next(request)
    except Exception as e:
        logger.error(e)
    finally:
        request.state.db.close()
    return response


app.include_router(routes)
logger.debug("Start application")
