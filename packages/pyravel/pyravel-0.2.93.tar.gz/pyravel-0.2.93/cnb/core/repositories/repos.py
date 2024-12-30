from typing import Any
from sqlalchemy.future import select
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from ..schemas.params import QueryParams
from cnb.crud.crud import CoreCRUD


class CoreRepository:

    def __init__(self, db: AsyncSession, template: SQLModel | Any):
        self.db = db
        self.template = template
        self.crud = CoreCRUD()

    async def create_one_record(self, schema_create: SQLModel):
        db_record = await self.crud.create_one_record(self.db, self.template.model_class, schema_create)
        return db_record

    async def update_one_record(self, record_id: int, schema_update: SQLModel):
        db_record = await self.crud.update_one_record(self.db, record_id, self.template.model_class, schema_update)
        return db_record

    async def delete_one_record(self, record_id: int):
        db_record = await self.crud.delete_one_record(self.db, record_id, self.template.model_class)
        return db_record

    async def get_one(self, db: AsyncSession, record_id: int):
        result = await db.execute(select(self.template.model_class).where(self.template.model_class.id == record_id))
        return result.scalar()

    async def get_list(self, db: AsyncSession, param: QueryParams):
        result = await self.crud.get_list(db, param, self.template.model_class)
        return result

    async def get_list_with_count(self, db: AsyncSession, param: QueryParams):
        result = await self.crud.get_list_with_count(db, param, self.template.model_class)
        return result
