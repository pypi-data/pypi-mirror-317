import os
from loguru import logger


def ensure_lines_at_top(filepath, lines_to_add):
    try:
        # Read the current file content
        with open(filepath, 'r') as file:
            existing_lines = file.readlines()
    except FileNotFoundError:
        # If the file does not exist, start with an empty list
        existing_lines = []

    # Determine which lines need to be added
    lines_to_prepend = [line for line in lines_to_add if
                        line + '\n' not in existing_lines and line not in existing_lines]

    # Prepend the missing lines and write back to the file
    with open(filepath, 'w') as file:
        file.writelines([line + '\n' for line in lines_to_prepend] + existing_lines)


# Lines to add to the top of the file
lines_at_top = [
    "from starlette.exceptions import HTTPException as StarletteHTTPException",
    "from fastapi.exceptions import RequestValidationError",
    "from cnb.exception.asgi import ASGIErrorLoggingMiddleware",
    "from cnb.exception.handler import ExceptionHandlers",
    "from cnb.middleware.log_request import AuditMiddleware",
    "from app.controllers.register_api import router as register_router",
    "from db.base import create_db_table",
    "from fastapi import FastAPI",
    "from loguru import logger"
]


def ensure_lines_in_file(filepath, lines_to_add):
    try:
        # Read the existing lines in the file
        with open(filepath, 'r') as file:
            existing_lines = file.readlines()
    except FileNotFoundError:
        # If the file does not exist, start with an empty list
        existing_lines = []

    # Open the file in append mode
    with open(filepath, 'a') as file:
        for line in lines_to_add:
            # Check if the line already exists in the file
            if line + '\n' not in existing_lines and line not in existing_lines:
                # Write the line if it doesn't exist
                file.write(line + '\n')


# Lines to add to the file
lines = [
    "app = FastAPI()\n",
    "@app.on_event(\"startup\")",
    "async def on_startup():",
    "    logger.info(\"ASGI application startup\")",
    "    await create_db_table()",
    "@app.on_event(\"shutdown\")",
    "async def shutdown_event():",
    "    logger.info(\"ASGI application shutdown\")",
    "app.add_middleware(AuditMiddleware)",
    "app.add_middleware(ASGIErrorLoggingMiddleware)",
    "app.include_router(register_router)",
    "# Register the handlers",
    "handlers = ExceptionHandlers()",
    "app.add_exception_handler(StarletteHTTPException, handlers.http_exception_handler)",
    "app.add_exception_handler(RequestValidationError, handlers.validation_exception_handler)",
]


def create_file_if_not_exists(filepath: str, content_text: str = ""):
    # Ensure the directories in the path exist
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    # Check if the file exists
    if not os.path.exists(filepath):
        # Create the file
        with open(filepath, 'w') as file:
            # Create an empty file
            file.write(content_text)
        logger.info(f"File '{filepath}' created.")
    else:
        logger.info(f"File '{filepath}' already exists.")


requirements = [
    "fastapi~=0.115.6",
    "uvicorn",
    "sqlmodel~=0.0.22",
    "sqlalchemy~=2.0.36",
    "asyncpg",
    "psycopg2-binary",
    "pydantic-settings~=2.7.0",
    "loguru~=0.7.3",
    "setuptools~=75.6.0",
    "wheel",
    "pytest",
    "aiofiles~=24.1.0",
    "pydantic~=2.10.3",
    "starlette~=0.41.3"
]
db_base_file = """
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
db_session_file = """
from cnb.db.postgres.session import get_pg_session

get_session = get_pg_session

"""
register_api_file = """
from fastapi import APIRouter

prefix = "/api/v1"
router = APIRouter(prefix=prefix)
"""

env_postgres_file = [
    "POSTGRES_HOST=localhost",
    "POSTGRES_PORT=5432",
    "POSTGRES_DB=postgres_db",
    "POSTGRES_USER=postgres_user",
    "POSTGRES_PASSWORD=postgres_pass",
    "POSTGRES_DRIVER=postgresql+asyncpg",
    "ENABLE_LOG_REQUEST_HEADER=True",
    "ENABLE_LOG_REQUEST_BODY=True"
]


def process():
    ensure_lines_at_top("main.py", lines_at_top)
    ensure_lines_in_file("main.py", lines)

    file_path = "app/controllers/v1/__init__.py"
    create_file_if_not_exists(file_path)

    file_path = "app/controllers/register_api.py"
    create_file_if_not_exists(file_path, register_api_file)

    file_path = "app/models/register_models.py"
    create_file_if_not_exists(file_path)

    file_path = "app/schemas/__init__.py"
    create_file_if_not_exists(file_path)

    file_path = "app/services/__init__.py"
    create_file_if_not_exists(file_path)

    file_path = "app/repositories/__init__.py"
    create_file_if_not_exists(file_path)

    file_path = "db/base.py"
    create_file_if_not_exists(file_path, db_base_file)

    file_path = "db/__init__.py"
    create_file_if_not_exists(file_path)

    file_path = "db/session.py"
    create_file_if_not_exists(file_path, db_session_file)

    file_path = "requirements.txt"
    ensure_lines_at_top(file_path, requirements)

    file_path = ".env"
    ensure_lines_at_top(file_path, env_postgres_file)


process()
