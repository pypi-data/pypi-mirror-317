from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel
from ..schemas.params import QueryParams


class CoreService:

    def __init__(self, db: AsyncSession, template: SQLModel | Any):
        self.repository = template.repository(db, template)
        self.template = template
        self.db = db

    async def create_one_record(self, schema_create: SQLModel | Any):
        db_record = await self.repository.create_one_record(schema_create)
        return db_record

    async def update_one_record(self, record_id: int, schema_update: SQLModel | Any):
        db_record = await self.repository.update_one_record(record_id, schema_update)
        return db_record

    async def delete_one_record(self, record_id: int):
        db_record = await self.repository.delete_one_record(record_id)
        return db_record

    async def get_one(self, record_id: int):
        result = await self.repository.get_one(self.db, record_id)
        return result

    async def get_list(self, param: QueryParams):
        result = await self.repository.get_list(self.db, param)
        return result

    async def get_list_with_count(self, param: QueryParams):
        result = await self.repository.get_list_with_count(self.db, param)
        return result
