from rich import print as rprint
from .generate_restapi import start_create
from ..base import BaseCommand
import questionary
import re
import asyncio

class GenerateCommand(BaseCommand):
    def __init__(self, args):
        self.args = args
        self.options = {
            'controller': self.generate_controller,
            'service': self.generate_service,
            'restapi': self.generate_api
        }

    async def handle(self):
        rprint("[bold blue]🚀 Generate new component[/bold blue]")

        # Create event loop since we're in an async context
        loop = asyncio.get_event_loop()

        # Run questionary synchronously using loop.run_in_executor
        choice = await loop.run_in_executor(None, lambda: questionary.select(
            "What would you like to generate?",
            choices=[
                "Controller",
                "Service",
                "RestAPI",
            ],
        ).ask())

        if not choice:
            return 1

        choice = choice.lower()

        name = await loop.run_in_executor(None, lambda: questionary.text(
            f"Enter {choice} name:",
            validate=lambda text: len(text) > 0 and bool(re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', text))
        ).ask())

        if name and choice in self.options:
            await self.options[choice](name)
            rprint(f"[bold green]✨ Successfully generated {choice}: {name}[/bold green]")
            return 0
        return 1

    def generate_controller(self, name):
        print(f"Generating controller: {name}")

    def generate_service(self, name):
        print(f"Generating service: {name}")

    async def generate_api(self, name):
        await start_create()
        print(f"Generating RestAPI: {name}")

    @staticmethod
    def print_usage():
        print("  generate|gen|g    Generate new components (controller/service/restapi)")