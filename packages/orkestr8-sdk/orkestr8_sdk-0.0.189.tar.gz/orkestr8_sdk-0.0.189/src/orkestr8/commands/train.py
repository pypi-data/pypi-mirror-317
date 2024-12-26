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
        with open(DATA_OUTPUT_FILE_LOCATION, "a") as data:
            old_err, old_out = sys.stderr, sys.stdout
            sys.stdout = StreamToFile(data)
            sys.stderr = sys.stdout

            logging.basicConfig(level=logging.INFO)
            logger = logging.getLogger("data_logger")
            app_logger = logging.getLogger("app")
            t = Thread(target=start_q)
            t.daemon = True
            t.start()

            m = importlib.import_module(self.args.model_module)
            child_id = os.getpid()
            with open(PID_FILE_LOCATION, "w") as f:
                _log = f"Child PID for training: {child_id}"
                logger.info(_log)
                app_logger.info(_log)

                f.write(f"PID: {child_id}")

            m.train()
            sys.stderr = old_err
            sys.stdout = old_out

    def run(self):
        """Imports model training module and invokes 'train' function"""
        p = Process(target=self._run)
        p.start()


class StreamToFile:
    def __init__(self, file):
        self.file = file

    def write(self, data):
        self.file.write(data)
        self.file.flush()  # Ensure immediate write to file

    def flush(self):
        self.file.flush()
