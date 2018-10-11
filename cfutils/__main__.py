from argparse import ArgumentParser
from .new import NewCommand
from .run import RunCommand
from .clear import ClearCommand

known_commands = {
    'new': NewCommand,
    'run': RunCommand,
    'clear': ClearCommand
}


def main():
    main_parser = ArgumentParser(description='Codeforces command line utilities')
    subparsers = main_parser.add_subparsers()
    for name, command in known_commands.items():
        parser = subparsers.add_parser(name, help=command.description(), description=command.description())
        command.setup_parser(parser)
        parser.set_defaults(run=command.run)
    args = main_parser.parse_args()
    if not hasattr(args, 'run'):
        main_parser.print_help()
    else:
        args.run(args)
