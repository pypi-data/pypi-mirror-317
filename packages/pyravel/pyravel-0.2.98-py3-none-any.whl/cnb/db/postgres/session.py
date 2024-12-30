import asyncio
import logging
from fastapi import Depends
from sqlalchemy.exc import InterfaceError
from sqlalchemy import URL, make_url
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlmodel import create_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker

from cnb.db.postgres.pg_settings import pg_settings

engine = None


async def get_postgres_engine():
    try:
        pg_host = pg_settings.POSTGRES_HOST
        pg_port = pg_settings.POSTGRES_PORT
        pg_user = pg_settings.POSTGRES_USER
        pg_password = pg_settings.POSTGRES_PASSWORD
        pg_db = pg_settings.POSTGRES_DB
        pg_driver = pg_settings.POSTGRES_DRIVER

        pg_db_url = f"{pg_driver}://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_db}"
        pg_make_db_url = make_url(pg_db_url)
        logging.info(pg_db_url)

        pg_engine_db_url = URL(
            drivername=pg_driver,
            username=pg_user,
            password=pg_password,
            host=pg_host,
            port=pg_port,
            database=pg_db,
            query=pg_make_db_url.query
        )

        engine_instance = AsyncEngine(create_engine(pg_engine_db_url, echo=None, future=True, pool_pre_ping=True))

        return engine_instance
    except Exception as e:
        raise e


async def get_session_bak(engine_db=Depends(get_postgres_engine)) -> AsyncSession:
    async_session = sessionmaker(engine_db, class_=AsyncSession)
    try:
        async with async_session() as session:
            yield session
    except InterfaceError:
        logging.info("Check variable check_init_engine: ", "*" * 100)


async def get_pg_session() -> AsyncSession:
    global engine

    if not engine:
        logging.info("Start connect to database!", "*" * 100)
        for i in range(1000):
            try:
                engine = await get_postgres_engine()
                async with engine.begin() as conn:
                    logging.info("Already connect to database!")
                    break
            except Exception as e:
                engine = None
                logging.warning(f"{i} Attempting to reconnect to database... {str(e)}", "*" * 100)
                await asyncio.sleep(10)  # Use asyncio.sleep instead of time.sleep

    if not engine:
        engine = await get_postgres_engine()

    async_session = sessionmaker(engine, class_=AsyncSession)
    check_init_engine = False

    try:
        async with async_session() as session:
            yield session
    except InterfaceError:
        engine = None
        logging.info("Check variable check_init_engine: ", check_init_engine, "*" * 100)
