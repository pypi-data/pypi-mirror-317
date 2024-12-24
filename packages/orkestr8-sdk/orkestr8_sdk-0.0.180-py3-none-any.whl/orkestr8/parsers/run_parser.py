from argparse import ArgumentParser

from orkestr8.parsers.base_parser import BaseParser


class RunParser(BaseParser):
    @classmethod
    def create_sub_parser(cls, subparser) -> ArgumentParser:
        run_parser: ArgumentParser = subparser.add_parser(
            "run",
            help="Runs the data update and training logic",
            parents=[
                cls.all_option_parser,
                cls.file_option_parser,
                cls.aws_options_parser,
            ],
        )
        run_parser.add_argument(
            "--model-module",
            action="store",
            help="The module that contains the model to run. Module MUST have a `train` method defined",
        )
        run_parser.add_argument(
            "--remote_file_path", help="Where to direct Orkestr8 to pull the file from"
        )
        run_parser.add_argument(
            "--dest_file_path", help="Where to direct Orkestr8 to write file path"
        )
        return run_parser
