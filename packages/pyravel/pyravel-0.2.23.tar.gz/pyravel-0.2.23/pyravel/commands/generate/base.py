from ..base import BaseCommand
from .generate_restapi import start_create
import questionary
from rich import print as rprint
import re

class GenerateCommand(BaseCommand):
    def __init__(self, args):
        self.args = args
        self.options = {
            'controller': self.generate_controller,
            'service': self.generate_service,
            'restapi': self.generate_api
        }

    def handle(self):
        rprint("[bold blue]🚀 Generate new component[/bold blue]")

        choice = questionary.select(
            "What would you like to generate?",
            choices=[
                "Controller",
                "Service",
                "RestAPI",
            ],
        ).ask()

        if not choice:
            return 1

        choice = choice.lower()

        name = questionary.text(
            f"Enter {choice} name:",
            validate=lambda text: len(text) > 0 and bool(re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', text))
        ).ask()

        if name and choice in self.options:
            self.options[choice](name)
            rprint(f"[bold green]✨ Successfully generated {choice}: {name}[/bold green]")
            return 0
        return 1

    def generate_controller(self, name):
        # Add controller generation logic here
        print(f"Generating controller: {name}")

    def generate_service(self, name):
        # Add service generation logic here
        print(f"Generating service: {name}")

    def generate_api(self, name):
        folder_name = questionary.text(
            f"Enter folder name:",
            validate=lambda text: len(text) > 0 and bool(re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', text))
        ).ask()
        class_name = questionary.text(
            f"Enter class name:",
            validate=lambda text: len(text) > 0 and bool(re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', text))
        ).ask()
        folder_name = str(folder_name).lower()
        class_name = str(class_name).title()
        start_create(folder_name, class_name)

    @staticmethod
    def print_usage():
        print("  generate|gen|g    Generate new components (controller/service/restapi)")