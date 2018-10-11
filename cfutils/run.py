import os
from shlex import quote
from hashlib import sha1
import subprocess
from .command import Command
from .common import tmp_base
from .config import Config
from .sample import CodeforcesSampleFetcher


def tokens_equal(a, b):
    a_tokens = a.strip().split()
    b_tokens = b.strip().split()
    return a_tokens == b_tokens


class RunCommand(Command):
    def __init__(self):
        super().__init__()

    @staticmethod
    def description():
        return 'Run source file'

    @staticmethod
    def setup_parser(parser):
        parser.add_argument('-c', '--command', help='Command used to run this file. '
                                                    'Use default command for the extension if not specified')
        parser.add_argument('-t', '--test', help='Run sample tests scraped from problem page', metavar='PROBLEM_ID')
        parser.add_argument('file', type=str, help='Name of the source file')

    @staticmethod
    def run(args):
        root, ext = os.path.splitext(args.file)
        if args.command is None:
            compile_cmd, run_cmd = Config.get_default_command(ext)
        else:
            compile_cmd, run_cmd = Config.get_command(args.command)
        if not compile_cmd:
            target = args.file
        else:
            with open(args.file, 'rb') as f:
                target = os.path.join(tmp_base, sha1(f.read()).hexdigest())
            if not os.path.exists(target):
                subprocess.run(compile_cmd.format(quote(args.file), quote(target)), shell=True, check=True)
        if args.test:
            fetcher = CodeforcesSampleFetcher(args.test)
            for i, (sample_in, sample_out) in enumerate(fetcher.get()):
                result = subprocess.run(run_cmd.format(quote(target)), stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                        shell=True, input=sample_in, encoding='utf8')
                verdict = 'AC'
                if result.returncode != 0:
                    verdict = 'RE'
                elif not tokens_equal(result.stdout, sample_out):
                    verdict = 'WA'
                print('Test', i + 1, verdict)
                print('Sample input:')
                print(sample_in)
                print('Sample output:')
                print(sample_out)
                print('Your output:')
                print(result.stdout)
                if result.stderr:
                    print(result.stderr)
        else:
            subprocess.run(run_cmd.format(quote(target)), shell=True)
