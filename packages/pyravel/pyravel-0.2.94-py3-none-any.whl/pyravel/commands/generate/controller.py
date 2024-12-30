import re
import questionary
from ...utils.helper import create_file

def generate_controller_and_service():
    folder_name = questionary.text(
        f"Enter folder name:",
        validate=lambda text: len(text) > 0 and bool(re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', text))
    ).ask()
    controller = questionary.text(
        f"Enter controller and service name:",
        validate=lambda text: len(text) > 0 and bool(re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', text))
    ).ask()

    folder_name = str(folder_name).lower()
    controller_name = str(controller).title()


    controller = f"""
from fastapi import APIRouter

from cnb.core.exceptions.endpoint_exception import handle_exceptions
from app.schemas.{folder_name}.create.schema import {controller_name}Schemas
from app.schemas.{folder_name}.response.one import {controller_name}Response
from app.services.test.services import {controller_name}Service


class {controller_name}Template:
    schemas = {controller_name}Schemas
    response_create = {controller_name}Response
    service = {controller_name}Service


router = APIRouter(prefix="/{str(folder_name).lower()}")
template_cls = {controller_name}Template
    """
    filepath = f"app/controllers/v1/{folder_name}/controller.py"
    create_file(filepath, controller)

    schema = f"""
from pydantic import BaseModel


class {controller_name}Create(BaseModel):
    pass
    """
    filepath = f"app/schemas/{folder_name}/create/schema.py"
    create_file(filepath, schema)

    response = f"""
from pydantic import BaseModel


class {controller_name}Response(BaseModel):
    pass
"""
    filepath = f"app/schemas/{folder_name}/response/one.py"
    create_file(filepath, response)

    service = f"""
class {controller_name}Service:
    pass
"""