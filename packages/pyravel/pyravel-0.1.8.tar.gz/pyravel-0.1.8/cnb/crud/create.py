from typing import Any
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncSession


class CoreCreate:
    async def create_one_record(self, db: AsyncSession, model_class: SQLModel | Any, schema_create: SQLModel | Any):
        db_model = model_class.model_validate(schema_create.model_dump())
        db.add(db_model)
        await db.flush()
        return db_model
