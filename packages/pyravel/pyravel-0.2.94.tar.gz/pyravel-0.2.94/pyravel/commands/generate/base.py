from ..base import BaseCommand
from .controller import generate_controller_and_service
from .service import generate_service
from .docker import generate_docker
from .restapi import start_create
import questionary
from rich import print as rprint

class GenerateCommand(BaseCommand):
    def __init__(self, args):
        self.args = args
        self.options = {
            'controller': generate_controller_and_service,
            'restapi': start_create,
            'docker': generate_docker
        }

    def handle(self):
        rprint("[bold blue]🚀 Generate new component[/bold blue]")

        choice = questionary.select(
            "What would you like to generate?",
            choices=[
                {"name": "Controller and Service", "value": "Controller"},
                "RestAPI",
                "Docker"
            ],
        ).ask()

        if not choice:
            return 1

        choice = choice.lower()
        self.options[choice]()
        rprint(f"[bold green]✨ Successfully generated {choice == 'controller' and 'controller and service' or choice} ![/bold green]")

    @staticmethod
    def print_usage():
        print("  generate|gen|g    Generate new components (controller/service/restapi/docker)")