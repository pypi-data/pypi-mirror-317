from typing import List
from loguru import logger
from sqlmodel import SQLModel, Session

from sqlalchemy import text
from fastapi import HTTPException

from cnb.db.postgres.session import get_postgres_engine

postgresql_type = {
    "DATETIME": "timestamp without time zone",
}


async def get_table_schema(db: Session, table_schema: str):
    try:
        result = await db.execute(
            text(f"""SELECT column_name, data_type FROM information_schema.columns 
            WHERE "table_schema"= :table_schema"""),
            {"table_schema": table_schema},
        )
        columns = result.fetchall()
        return dict(columns)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def get_table_columns(db: Session, table_name: str, table_schema: str):
    try:
        result = await db.execute(
            text(f"""SELECT column_name, data_type FROM information_schema.columns
             WHERE "table_schema"= :table_schema AND "table_name" = :table_name"""),
            {"table_name": table_name, "table_schema": table_schema},
        )
        columns = result.fetchall()
        return dict(columns)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



async def process_alter_table(global_items: list) -> List[str]:
    try:
        logger.info(f"""{"*" * 50} Start running function process_alter_table {"*" * 50}""")
        alter_statement = []
        engine = await get_postgres_engine()
        async with engine.begin() as conn:
            logger.info("*" * 50, "Start Create Database Schema", "*" * 50)

            for schema in SQLModel.metadata._schemas:
                stm = f"""CREATE SCHEMA IF NOT EXISTS "{schema}";"""
                logger.info(stm)
                await conn.execute(text(stm))

            logger.info(f"""{"*" * 50} Start run function  SQLModel.metadata.create_all {"*" * 50}""")
            await conn.run_sync(SQLModel.metadata.create_all)

            logger.info("*" * 50, "Start prepare statements", "*" * 50)

            for name, obj in global_items:
                if hasattr(obj, "model_fields"):
                    schema = "public"
                    if hasattr(obj, "__table_args__"):
                        schema = obj.__table_args__.get("schema", "public")

                    table_name = obj.__tablename__
                    table_columns = await get_table_columns(conn, table_name, schema)

                    for column in obj.__table__.columns:
                        if column.name not in table_columns.keys():
                            column_type = str(column.type)
                            column_type = postgresql_type.get(column_type, column_type)
                            stm_str = f"""ALTER TABLE IF EXISTS {schema}."{table_name}" 
                            ADD COLUMN IF NOT EXISTS "{column.name}" {column_type} DEFAULT NULL;"""
                            alter_statement.append(stm_str)

            logger.info(f"""{"*" * 50} Start alter table {"*" * 50}""")
            for stmt in alter_statement:
                logger.info(stmt)
                await conn.execute(text(stmt))

    except Exception as e:
        logger.error(e)
        await conn.rollback()
        raise e
    return alter_statement
