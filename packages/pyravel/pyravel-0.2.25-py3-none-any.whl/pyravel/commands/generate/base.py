from ..base import BaseCommand
from .generate_restapi import start_create
import questionary
from rich import print as rprint

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

    def generate_controller(self, name):
        # Add controller generation logic here
        rprint("[bold green]✅ Controller generated successfully![/bold green]")

    def generate_service(self):
        # Add service generation logic here
        rprint("[bold green]✅ Service generated successfully![/bold green]")

    def generate_api(self):
        start_create()
        rprint("[bold green]✅ RestAPI generated successfully![/bold green]")

    @staticmethod
    def print_usage():
        print("  generate|gen|g    Generate new components (controller/service/restapi)")