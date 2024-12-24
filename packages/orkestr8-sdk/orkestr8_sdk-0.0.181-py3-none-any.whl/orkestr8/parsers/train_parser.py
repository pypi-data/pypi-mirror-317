from argparse import ArgumentParser

from orkestr8.parsers.base_parser import BaseParser


class TrainParser(BaseParser):
    @classmethod
    def create_sub_parser(cls, subparser) -> ArgumentParser:
        train_parser: ArgumentParser = subparser.add_parser(
            "train",
            help="Runs the training logic only",
            parents=[cls.all_option_parser],
        )
        train_parser.add_argument(
            "model_module",
            action="store",
            help="The module that contains the model to run. Module MUST have a `train` method defined",
        )
        return train_parser
