import os
from .command import Command
from .common import tmp_base


class ClearCommand(Command):
    def __init__(self):
        super().__init__()

    @staticmethod
    def description():
        return 'Clear cache'

    @staticmethod
    def setup_parser(parser):
        pass

    @staticmethod
    def run(args):
        for file in os.listdir(tmp_base):
            os.remove(os.path.join(tmp_base, file))