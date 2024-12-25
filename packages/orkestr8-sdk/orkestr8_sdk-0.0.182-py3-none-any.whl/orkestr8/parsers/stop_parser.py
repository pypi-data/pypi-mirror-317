from argparse import ArgumentParser

from orkestr8.parsers.base_parser import BaseParser


class StopParser(BaseParser):
    @classmethod
    def create_sub_parser(cls, subparser) -> ArgumentParser:
        parser: ArgumentParser = subparser.add_parser(
            "stop", help="Invokes 'global' stop command to running process"
        )
        parser.add_argument(
            "--pid",
            help="PID of Python process to shutdown. If not specificed Orkstr8 will automatically retreive PID",
        )
        return parser
