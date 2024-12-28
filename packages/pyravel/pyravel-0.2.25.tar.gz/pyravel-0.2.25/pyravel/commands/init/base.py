from ..base import BaseCommand
import os

requirement = """\
fastapi~=0.115.6
uvicorn
sqlmodel~=0.0.22
sqlalchemy~=2.0.36
asyncpg
psycopg2-binary
pydantic-settings~=2.7.0
loguru~=0.7.3
setuptools~=75.6.0
wheel
pytest
aiofiles~=24.1.0
pydantic~=2.10.3
starlette~=0.41.3
"""

main="""\
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError
from cnb.exception.asgi import ASGIErrorLoggingMiddleware
from cnb.exception.handler import ExceptionHandlers
from cnb.middleware.log_request import AuditMiddleware
from app.controllers.register_api import router as register_router
from db.base import create_db_table
from fastapi import FastAPI
from loguru import logger
app = FastAPI()

@app.on_event("startup")
async def on_startup():
    logger.info("ASGI application startup")
    await create_db_table()
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("ASGI application shutdown")
app.add_middleware(AuditMiddleware)
app.add_middleware(ASGIErrorLoggingMiddleware)
app.include_router(register_router)
# Register the handlers
handlers = ExceptionHandlers()
app.add_exception_handler(StarletteHTTPException, handlers.http_exception_handler)
app.add_exception_handler(RequestValidationError, handlers.validation_exception_handler)
"""

register_api="""\
from fastapi import APIRouter

prefix = "/api/v1"
router = APIRouter(prefix=prefix)
"""

db_base="""\
from cnb.db.postgres.session import get_postgres_engine
from loguru import logger
from app.models.register_models import *
from cnb.db.postgres.create_table import process_alter_table

global_items = globals().items()

async def create_db_table():
    logger.info(f"{'*' * 50} Start running function create_db_table {'*' * 50}")

    await process_alter_table(global_items)
    return {"message": "Created Table Successfully!"}
"""

session="""\
from cnb.db.postgres.session import get_pg_session

get_session = get_pg_session
"""

class InitCommand(BaseCommand):
    def __init__(self, args):
        self.args = args

    def handle(self):
        os.mkdir('app')
        os.mkdir('app/controllers')
        with open('app/controllers/register_api.py', 'w') as f:
            f.write(register_api)
        os.mkdir('app/models')
        os.mkdir('app/repositories')
        os.mkdir('app/schemas')
        os.mkdir('app/services')
        with open('main.py', 'w') as f:
            f.write(main)
        with open('requirements.txt', 'w') as f:
            f.write(requirement)
        os.system('pip install -r requirements.txt')
        os.mkdir('db')
        with open('db/base.py', 'w') as f:
            f.write(db_base)
        with open('db/session.py', 'w') as f:
            f.write(session)