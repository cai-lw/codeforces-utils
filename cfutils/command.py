class Command:
    def __init__(self):
        pass

    @staticmethod
    def description():
        raise NotImplementedError

    @staticmethod
    def setup_parser(parser):
        raise NotImplementedError

    @staticmethod
    def run(args):
        raise NotImplementedError
