from argparse import ArgumentParser

from orkestr8.parsers.base_parser import BaseParser


class PollParser(BaseParser):
    @classmethod
    def create_sub_parser(cls, subparser) -> ArgumentParser:
        return subparser.add_parser(
            "poll", help="Retrieve data from the active process"
        )
