from typing import Union, Any
from sqlmodel import SQLModel
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ..core.schemas.params import QueryParams


class CoreRead:
    def get_paging(self, paging: SQLModel):
        if paging.limit <= 0:
            paging.limit = 20
        return paging

    async def get_one(self, db: AsyncSession, record_id: Union[int, str], model_class: SQLModel | Any):
        result = await db.execute(select(model_class).where(model_class.id == record_id))
        return result.scalar()

    async def get_list(self, db: AsyncSession, param: QueryParams, model_class: SQLModel | Any):
        paging = self.get_paging(param.paging)
        query = select(model_class).offset(paging.offset).limit(paging.limit)
        statement = await db.execute(query)
        result = statement.scalars().all()
        return result

    async def get_list_with_count(self, db: AsyncSession, param: QueryParams, model_class: SQLModel | Any):
        paging = self.get_paging(param.paging)
        query = select(model_class).offset(paging.offset).limit(paging.limit)
        total_count = await db.scalar(select(func.count(model_class.id)))
        statement = await db.execute(query)
        result = statement.scalars().all()
        return {"total": total_count, "result": result}
