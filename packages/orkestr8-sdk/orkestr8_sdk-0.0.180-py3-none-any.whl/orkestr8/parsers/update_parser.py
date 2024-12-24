from argparse import ArgumentParser

from orkestr8.parsers.base_parser import BaseParser


class UpdateParser(BaseParser):
    @classmethod
    def create_sub_parser(cls, subparser) -> ArgumentParser:
        parser: ArgumentParser = subparser.add_parser(
            "update",
            help="Runs the data update function.",
            parents=[cls.all_option_parser, cls.aws_options_parser],
        )
        parser.add_argument(
            "remote_file_path", help="Where to direct Orkestr8 to pull the file from"
        )
        parser.add_argument(
            "dest_file_path", help="Where to direct Orkestr8 to write file path"
        )
        return parser
