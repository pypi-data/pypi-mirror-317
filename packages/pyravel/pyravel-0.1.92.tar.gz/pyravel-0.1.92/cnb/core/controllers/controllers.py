from typing import Any
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from ..schemas.params import QueryParams


class CoreController:

    def __init__(self, db: AsyncSession, template_cls: SQLModel | Any):
        self.template = template_cls()
        self.db = db

    async def create_one_record(self, schema_create: SQLModel | Any):
        # Initialize the service
        service = self.template.service(self.db, self.template)

        async with self.db.begin():  # Begin the transaction
            result = await service.create_one_record(schema_create)  # Create the record

        # Accessing attributes after context safely
        await self.db.refresh(result)  # Ensure the record is refreshed after commit
        return {"result": result}

    async def update_one_record(self, record_id: int, schema_update: SQLModel | Any):
        # Initialize the service
        service = self.template.service(self.db, self.template)

        async with self.db.begin():  # Begin the transaction
            result = await service.update_one_record(record_id, schema_update)  # Update the record

        # Accessing attributes after context safely
        await self.db.refresh(result)  # Ensure the record is refreshed after commit
        return {"result": result}

    async def delete_one_record(self, record_id: int):
        # Initialize the service
        service = self.template.service(self.db, self.template)

        async with self.db.begin():  # Begin the transaction
            result = await service.delete_one_record(record_id)  # Delete the record

        return {"result": result}

    async def get_one_record(self, record_id: int):
        # Initialize the service
        service = self.template.service(self.db, self.template)
        result = await service.get_one(record_id)
        return {"result": result}

    async def get_list_record(self, param: QueryParams):
        # Initialize the service
        service = self.template.service(self.db, self.template)
        results = await service.get_list_with_count(param)
        return results

    async def get_remote_record(self, param: QueryParams):
        # Initialize the service
        service = self.template.service(self.db, self.template)
        results = await service.get_list_with_count(param)
        return results
