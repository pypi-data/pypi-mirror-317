import os
import asyncio
import shutil

import aiofiles
from loguru import logger


async def create_file(filepath: str, content: str):
    """
    Creates a file with the provided content if it does not already exist.
    """
    # Ensure the directory exists
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    # Check if the file already exists
    if not os.path.exists(filepath):
        # Write the content to the file asynchronously
        async with aiofiles.open(filepath, "w") as file:
            await file.write(content)
        logger.info(f"File '{filepath}' has been created successfully.")
    else:
        logger.info(f"File '{filepath}' already exists. No changes were made.")


async def create_model(folder_name: str, class_name: str):
    model_data = f"""
from sqlmodel import SQLModel, Field


class {class_name}Base(SQLModel):
    # name: str
    pass


class {class_name}({class_name}Base, table=True):
    id: int = Field(default=None, primary_key=True)
    
    """

    filepath = f"app/models/{folder_name}/models.py"
    await create_file(filepath, model_data)


async def schema_create(folder_name: str, class_name: str):
    model_data = f"""
from app.models.{folder_name}.models import {class_name}Base


class {class_name}Create({class_name}Base):
    pass

    """
    filepath = f"app/schemas/{folder_name}/create/schema.py"
    await create_file(filepath, model_data)


async def schema_update(folder_name: str, class_name: str):
    model_data = f"""
from app.schemas.{folder_name}.create.schema import {class_name}Create


class {class_name}Update({class_name}Create):
    id: int

    """

    filepath = f"app/schemas/{folder_name}/update/schema.py"
    await create_file(filepath, model_data)


async def schema_list(folder_name: str, class_name: str):
    model_data = f"""
from sqlmodel import SQLModel
from typing import List

from app.models.{folder_name}.models import {class_name}Base


class {class_name}ResponseListBase({class_name}Base):
    id: int


class {class_name}ResponseList(SQLModel):
    result: List[{class_name}ResponseListBase]
    total: int | None = 0

    """

    filepath = f"app/schemas/{folder_name}/response/list.py"
    await create_file(filepath, model_data)


async def schema_one(folder_name: str, class_name: str):
    model_data = f"""
from sqlmodel import SQLModel

from app.models.{folder_name}.models import {class_name}Base


class {class_name}ResponseOneBase({class_name}Base):
    id: int


class {class_name}ResponseOne(SQLModel):
    result: {class_name}ResponseOneBase | None

    """

    filepath = f"app/schemas/{folder_name}/response/one.py"
    await create_file(filepath, model_data)


async def schema_remote(folder_name: str, class_name: str):
    model_data = f"""
from sqlmodel import SQLModel
from typing import List

from app.models.{folder_name}.models import {class_name}Base


class {class_name}ResponseRemoteBase({class_name}Base):
    id: int

    @property
    def text(self):
        return f"{{self.id}}"


class {class_name}ResponseRemote(SQLModel):
    result: List[{class_name}ResponseRemoteBase]
    total: int | None = 0

    """

    filepath = f"app/schemas/{folder_name}/response/remote.py"
    await create_file(filepath, model_data)


async def schema_delete(folder_name: str, class_name: str):
    model_data = f"""
from sqlmodel import SQLModel


class {class_name}ResponseDelete(SQLModel):
    result: bool | None

    """

    filepath = f"app/schemas/{folder_name}/response/delete.py"
    await create_file(filepath, model_data)


async def create_service(folder_name: str, class_name: str):
    model_data = f"""
from cnb.core.services.services import CoreService


class {class_name}Service(CoreService):
    pass

    """

    filepath = f"app/services/{folder_name}/services.py"
    await create_file(filepath, model_data)


async def create_repository(folder_name: str, class_name: str):
    model_data = f"""
from cnb.core.repositories.repos import CoreRepository


class {class_name}Repository(CoreRepository):
    pass

    """

    filepath = f"app/repositories/{folder_name}/repos.py"
    await create_file(filepath, model_data)


async def create_controller(folder_name: str, class_name: str):
    model_data = f"""
from fastapi import APIRouter, Depends, HTTPException
from loguru import logger
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.{folder_name}.models import {class_name}
from app.repositories.{folder_name}.repos import {class_name}Repository
from app.schemas.{folder_name}.create.schema import {class_name}Create
from app.schemas.{folder_name}.response.delete import {class_name}ResponseDelete
from app.schemas.{folder_name}.response.list import {class_name}ResponseList
from app.schemas.{folder_name}.response.one import {class_name}ResponseOne
from app.schemas.{folder_name}.response.remote import {class_name}ResponseRemote
from app.schemas.{folder_name}.update.schema import {class_name}Update
from app.services.{folder_name}.services import {class_name}Service
from cnb.core.controllers.controllers import CoreController
from cnb.core.schemas.params import QueryParams
from db.session import get_session


class {class_name}Template:
    model_class = {class_name}
    schema_create = {class_name}Create
    schema_update = {class_name}Update
    response_one = {class_name}ResponseOne
    response_delete = {class_name}ResponseDelete
    response_list = {class_name}ResponseList
    response_remote = {class_name}ResponseRemote
    service = {class_name}Service
    repository = {class_name}Repository


router = APIRouter(prefix="/{str(folder_name).lower()}")
template_cls = {class_name}Template
controller_cls = CoreController


@router.post("/create/", response_model=template_cls.response_one)
async def create_one_record(schema_create: template_cls.schema_create, db: AsyncSession = Depends(get_session)):
    try:
        # Initialize the controller
        controller = controller_cls(db, template_cls)
        return await controller.create_one_record(schema_create)
    except Exception as e:
        logger.error(f"Error creating record: {{e}}")
        raise e


@router.post(f"/one/{{{{record_id}}}}/", response_model=template_cls.response_one)
async def get_one_record(record_id: int, db: AsyncSession = Depends(get_session)):
    try:
        # Initialize the controller
        controller = controller_cls(db, template_cls)
        result = await controller.get_one_record(record_id)
        if not result:
            raise HTTPException(status_code=404, detail="Record not found")
        return result
    except Exception as e:
        logger.error(f"Error updating record: {{e}}")
        raise e


@router.patch(f"/update/{{{{record_id}}}}/", response_model=template_cls.response_one)
async def update_one_record(record_id: int, schema_update: template_cls.schema_update,
                            db: AsyncSession = Depends(get_session)):
    try:
        # Initialize the controller
        controller = controller_cls(db, template_cls)
        return await controller.update_one_record(record_id, schema_update)
    except Exception as e:
        logger.error(f"Error updating record: {{e}}")
        raise e


@router.delete(f"/delete/{{{{record_id}}}}/", response_model=template_cls.response_delete)
async def delete_one_record(record_id: int, db: AsyncSession = Depends(get_session)):
    try:
        # Initialize the controller
        controller = controller_cls(db, template_cls)
        return await controller.delete_one_record(record_id)
    except Exception as e:
        logger.error(f"Error updating record: {{e}}")
        raise e


@router.post("/list/", response_model=template_cls.response_list)
async def get_list_record(param: QueryParams, db: AsyncSession = Depends(get_session)):
    try:
        # Initialize the controller
        controller = controller_cls(db, template_cls)
        return await controller.get_list_record(param)
    except Exception as e:
        logger.error(f"Error getting record: {{e}}")
        raise e


@router.post("/remote/", response_model=template_cls.response_remote)
async def get_remote_record(param: QueryParams, db: AsyncSession = Depends(get_session)):
    try:
        # Initialize the controller
        controller = controller_cls(db, template_cls)
        return await controller.get_list_record(param)
    except Exception as e:
        logger.error(f"Error getting record: {{e}}")
        raise e

    """

    filepath = f"app/controllers/v1/{folder_name}/api.py"
    await create_file(filepath, model_data)


async def modify_file(file_path: str, import_stm: str, router_stm: str):
    # Read the file content asynchronously
    async with aiofiles.open(file_path, 'r') as file:
        lines = await file.readlines()

    if not lines:  # Check if the file is empty
        # If empty, write both lines to the file
        async with aiofiles.open(file_path, 'w') as file:
            await file.write(import_stm)
            await file.write(router_stm)
    else:
        # Find the first empty line and insert the import statement
        for i, line in enumerate(lines):
            if line.strip() == "":
                lines.insert(i, import_stm)
                break
        else:
            # If no empty line is found, append the import statement at the end
            lines.append(import_stm)

        # Add the router inclusion at the end
        lines.append(router_stm)

        # Write the modified content back to the file asynchronously
        async with aiofiles.open(file_path, 'w') as file:
            await file.writelines(lines)


async def register_api(folder_name: str, class_name: str):
    filepath = f"app/controllers/register_api.py"
    await create_file(filepath, "")
    import_stm = f"from .v1.{folder_name}.api import router as {folder_name}_router"
    router_stm = f"router.include_router({folder_name}_router, tags=[\"{class_name}\"])\n"
    await modify_file(filepath, import_stm, router_stm)


async def register_model(folder_name: str, class_name: str):
    await create_file("app/models/register_models.py", "")
    import_stm = f"from .{folder_name}.models import {class_name}\n"
    router_stm = f""
    filepath = f"app/models/register_models.py"
    await modify_file(filepath, import_stm, router_stm)


async def start_create():
    folder_name = input("Create folder name: ").lower().replace(" ", "_")
    class_name = input("Create class name: ").title()

    await create_model(folder_name, class_name)
    await schema_create(folder_name, class_name)
    await schema_list(folder_name, class_name)
    await schema_remote(folder_name, class_name)
    await schema_one(folder_name, class_name)
    await schema_update(folder_name, class_name)
    await schema_delete(folder_name, class_name)
    await create_service(folder_name, class_name)
    await create_repository(folder_name, class_name)
    await create_controller(folder_name, class_name)
    await register_api(folder_name, class_name)
    await register_model(folder_name, class_name)


# Run the async function
if __name__ == "__main__":
    asyncio.run(start_create())
