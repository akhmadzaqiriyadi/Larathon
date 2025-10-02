from Illuminate.Console.Commands.Migrate import MigrateCommand
from Illuminate.Console.Commands.MakeMigration import MakeMigrationCommand

class Kernel:
    def __init__(self):
        self.commands = {
            "migrate": MigrateCommand(),
            "make:migration": MakeMigrationCommand(),
        }

    def handle(self, argv):
        if len(argv) < 2:
            print("❌ No command given")
            return

        cmd = argv[1]
        args = argv[2:]

        if cmd in self.commands:
            self.commands[cmd].handle(args)
        else:
            print(f"❌ Command {cmd} not found")
