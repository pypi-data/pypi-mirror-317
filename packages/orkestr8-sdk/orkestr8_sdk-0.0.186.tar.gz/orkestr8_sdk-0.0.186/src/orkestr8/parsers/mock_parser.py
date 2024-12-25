from argparse import ArgumentParser

from orkestr8.parsers.base_parser import BaseParser


class MockParser(BaseParser):
    @classmethod
    def create_sub_parser(cls, subparser) -> ArgumentParser:
        parser: ArgumentParser = subparser.add_parser(
            "mock_run", help="Invokes a mocked training scenario"
        )

        parser.add_argument("--model-module", default="orkestr8_mock")
        return parser
