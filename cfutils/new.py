import os
import shutil
from warnings import warn
from .command import Command
from .config import config
from .common import template_base


class NewCommand(Command):
    def __init__(self):
        super().__init__()

    @staticmethod
    def description():
        return 'Create new source file'

    @staticmethod
    def setup_parser(parser):
        parser.add_argument('-t', '--template', help='Template file to use. '
                                                     'Use default template for the extension if not specified')
        parser.add_argument('-n', '--no-template', action='store_true',
                            help='Disable templates and just create an empty file')
        parser.add_argument('file', type=str, help='Name of the new file')

    @staticmethod
    def run(args):
        if args.template is None:
            ext = os.path.splitext(args.file)[1]
            template = config.extension[ext].template
        else:
            template = args.template
        if args.no_template or template == '':
            with open(args.file, 'w'):
                pass
        else:
            template_path = os.path.join(template_base, template)
            if not os.path.exists(template_path):
                warn('Template file {} does not exist. Creating empty file.'.format(template), RuntimeWarning)
                with open(args.file, 'w'):
                    pass
            else:
                shutil.copy(template_path, args.file)
