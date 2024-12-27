from typing import Union, Any

from fastapi import HTTPException
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncSession


class CoreDelete:

    async def delete_one_record(self, db: AsyncSession, record_id: Union[int, str], model_class: SQLModel | Any):
        db_model = await db.get(model_class, record_id)
        if not db_model:
            raise HTTPException(status_code=404, detail="Record not found")

        await db.delete(db_model)
        await db.flush()
        return True
