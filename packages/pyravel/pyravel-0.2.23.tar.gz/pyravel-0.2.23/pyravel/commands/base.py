class BaseCommand:
    def handle(self):
        raise NotImplementedError("Command must implement handle method")

    @staticmethod
    def print_usage():
        raise NotImplementedError("Command must implement print_usage method")