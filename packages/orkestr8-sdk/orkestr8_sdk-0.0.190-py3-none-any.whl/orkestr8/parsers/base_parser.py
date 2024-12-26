import importlib
import os
import sys
from abc import ABC, abstractmethod
from argparse import ArgumentParser, _SubParsersAction
from pathlib import Path
from typing import List


def _build_global_aws_option_parser():
    """Parent parser for AWS options to be specific"""
    parser = ArgumentParser(add_help=False)
    parser.add_argument("--aws-access-key", nargs="?", action="store")
    parser.add_argument("--aws-secret-key", nargs="?", action="store")
    parser.add_argument("--aws-bucket-name", nargs="?", action="store")
    return parser


def _build_global_option_parser() -> ArgumentParser:
    "Parent parser to define optoins used for ALL commands"
    parser = ArgumentParser(add_help=False)
    parser.add_argument(
        "-y",
        dest="default_yes",
        action="store_true",
        help="Apply yes by default to all inputs",
    )
    parser.add_argument(
        "--generate-new-train-test",
        action="store_true",
        help="Generates new training and validation data. This is automatic"
        " if image data is add to the server",
    )

    return parser


def _build_file_location_parser() -> ArgumentParser:
    parser = ArgumentParser(add_help=False)
    parser.add_argument("--remote-file-path", nargs="?")
    parser.add_argument("--dest-file-path", nargs="?")
    return parser


class BaseParser(ABC):
    all_option_parser = _build_global_option_parser()
    file_option_parser = _build_file_location_parser()
    aws_options_parser = _build_global_aws_option_parser()
    sub_parsers: List["BaseParser"] = []

    def __init_subclass__(cls):
        cls.sub_parsers.append(cls)

    @classmethod
    def build_parser_args(cls):
        """Collects all subparsers. Parses Args"""
        # importlib.import_module('')
        for f in os.listdir(Path(__file__).parent):
            if f != "base_parser.py" and f.endswith("parser.py"):
                importlib.import_module(f"orkestr8.parsers.{f.rstrip('.py')}")
        parser = ArgumentParser(prog="Orchkestr8 ML train runner")

        subparser = parser.add_subparsers(dest="command", help="Invocation commands")
        for parser_cls in cls.sub_parsers:
            parser_cls.create_sub_parser(subparser)

        return parser.parse_args(args=None if sys.argv[1:] else ["--help"])

    @classmethod
    @abstractmethod
    def create_sub_parser(cls, subparser: _SubParsersAction) -> ArgumentParser:
        pass
