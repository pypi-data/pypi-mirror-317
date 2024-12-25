import importlib
import logging
import os
import sys
from dataclasses import dataclass
from multiprocessing import Process
from threading import Thread

from orkestr8.en_q import start as start_q
from orkestr8.settings import DATA_OUTPUT_FILE_LOCATION, PID_FILE_LOCATION

from .base import Command


@dataclass
class TrainArgs:
    model_module: str


class TrainCommand(Command[TrainArgs]):
    @staticmethod
    def parse(args) -> TrainArgs:
        return TrainArgs(args.model_module)

    def _run(self):
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger("data_logger")
        logger.addHandler(logging.FileHandler(DATA_OUTPUT_FILE_LOCATION))
        t = Thread(target=start_q)
        t.daemon = True
        t.start()

        m = importlib.import_module(self.args.model_module)
        child_id = os.getpid()
        with open(PID_FILE_LOCATION, "w") as f:
            logger.info(f"Child PID for training: {child_id}")
            f.write(f"PID: {child_id}")

            err = sys.stderr
            out = sys.stdout
            with open(DATA_OUTPUT_FILE_LOCATION) as log_file:
                sys.stderr = log_file
                sys.stdout = log_file
                m.train()
                sys.stderr = err
                sys.stdout = out

    def run(self):
        """Imports model training module and invokes 'train' function"""
        p = Process(target=self._run)
        p.start()
