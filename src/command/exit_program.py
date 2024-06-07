# Command Interface
from src.command.command import Command
import sys


class ExitProgram(Command):
    def execute(self):
        sys.exit()

    def set_configuration(self):
        pass
