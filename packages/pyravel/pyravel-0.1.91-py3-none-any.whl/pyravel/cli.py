import sys
from .commands.init.base import InitCommand
from .commands.generate.base import GenerateCommand

COMMANDS = {
    'init': InitCommand,

    # generate command
    'generate': GenerateCommand,
    'gen': GenerateCommand,
    'g': GenerateCommand
}

def main():
    if len(sys.argv) < 2:
        print("Usage: pyravel <command> [options]")
        print("\nAvailable commands:")
        for cmd in COMMANDS.keys():
            COMMANDS[cmd].print_usage()
        return 1

    command = sys.argv[1]
    command_args = sys.argv[2:]

    if command not in COMMANDS:
        print("Unknown command. Available commands:")
        for cmd in COMMANDS.keys():
            COMMANDS[cmd].print_usage()
        return 1

    command_class = COMMANDS[command]
    command_instance = command_class(command_args)
    return command_instance.handle()

if __name__ == "__main__":
    sys.exit(main())