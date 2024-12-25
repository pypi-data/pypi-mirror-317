import importlib
import logging
import os
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
            logging.basicConfig(level=logging.INFO, stream=data)
            logger = logging.getLogger("data_logger")
            t = Thread(target=start_q)
            t.daemon = True
            t.start()

            m = importlib.import_module(self.args.model_module)
            child_id = os.getpid()
            with open(PID_FILE_LOCATION, "w") as f:
                logger.info(f"Child PID for training: {child_id}")
                f.write(f"PID: {child_id}")

            m.train()
        data.close()

    def run(self):
        """Imports model training module and invokes 'train' function"""
        p = Process(target=self._run)
        p.start()
