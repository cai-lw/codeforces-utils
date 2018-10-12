import os
from shlex import quote
import subprocess
from .command import Command
from .common import tmp_base
from .config import config
from .runner import InterpretRunner, CompileRunner, JvmRunner
from .sample import CodeforcesSampleFetcher

known_runners = {
    'interpret': InterpretRunner,
    'compile': CompileRunner,
    'jvm': JvmRunner
}

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
        ext = os.path.splitext(args.file)[1]
        if args.command is not None:
            runner_config = config.command[args.command]
        else:
            runner_config = config.command[config.extension[ext].command]
        if runner_config.get('type', None) not in known_runners.keys():
            raise ValueError('Command type unknown or unspecified')
        with known_runners[runner_config.type](runner_config, args.file) as runner:
            if args.test:
                fetcher = CodeforcesSampleFetcher(args.test)
                for i, (sample_in, sample_out) in enumerate(fetcher.get()):
                    result = runner.run(sample_in)
                    verdict = 'AC'
                    if result.returncode != 0:
                        verdict = 'RE'
                    else:
                        result_tokens = result.stdout.strip().split()
                        sample_tokens = sample_out.strip().split()
                        if result_tokens != sample_tokens:
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
                runner.run()
