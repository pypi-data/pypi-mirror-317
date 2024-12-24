from argparse import ArgumentParser

from orkestr8.commands.download_model import Destination
from orkestr8.parsers.base_parser import BaseParser


class DownloadModelParser(BaseParser):
    @classmethod
    def create_sub_parser(cls, subparser) -> ArgumentParser:
        parser: ArgumentParser = subparser.add_parser(
            "download_model",
            help="Download the trained weights of the model",
            parents=[cls.aws_options_parser],
        )
        parser.add_argument(
            "to", help="Location to save the model", choices=Destination._member_names_
        )
        parser.add_argument(
            "--model-location", help="Location of .pth file", required=True
        )
        parser.add_argument(
            "--remote-location",
            help="File path to place model of 'to' argument",
            required=True,
        )
        return parser
