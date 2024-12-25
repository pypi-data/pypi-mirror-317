from argparse import ArgumentParser

from orkestr8.parsers.base_parser import BaseParser


class CheckParser(BaseParser):
    @classmethod
    def create_sub_parser(cls, subparser) -> ArgumentParser:
        parser: ArgumentParser = subparser.add_parser(
            "check", help="Checks running state of training session"
        )

        parser.add_argument(
            "--file",
            help=(
                "File which contains process information. If file can be accessed AND has PID value"
                + ", will return ACTIVE, else INACTIVE for all other scenarios"
            ),
        )

        return parser
