from typing import Union, Any

from fastapi import HTTPException
from pydantic import BaseModel
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncSession


class CoreUpdate:
    async def get_pk_name(self, model_class: SQLModel):
        return model_class.__table__.primary_key.columns.values()[0].name if model_class else None

    async def update_one_record(self, db: AsyncSession, record_id: Union[int, str], model_class: SQLModel | Any,
                                schema_create: BaseModel | Any):
        pk_name = await self.get_pk_name(model_class)
        update_pk_value = schema_create.model_dump().get(pk_name)

        if update_pk_value != record_id:
            raise HTTPException(status_code=400,
                                detail=f"Cannot change record id form {record_id} to {update_pk_value}")

        db_model = await db.get(model_class, record_id)
        if not db_model:
            raise HTTPException(status_code=404, detail="Record not found")

        data = schema_create.model_dump(exclude_unset=True)
        db_model.sqlmodel_update(data)
        db.add(db_model)
        await db.flush()
        return db_model
