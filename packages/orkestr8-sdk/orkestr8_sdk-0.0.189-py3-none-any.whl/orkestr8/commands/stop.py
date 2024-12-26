import logging
import os
import signal
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Union

from orkestr8.settings import PID_FILE_LOCATION, QUEUE_PID_FILE_LOCATION

from .base import Command

PROCESSES: Dict[str, Path] = {
    "TRAINING_PROCESS": PID_FILE_LOCATION,
    "QUEUE_PROCESS": QUEUE_PID_FILE_LOCATION,
}

LOGGER = logging.getLogger("app")


def _shut_down_processes() -> None:
    """Fetches PIDs from their saved file
    location and kills processes"""
    for process_name, file_name in PROCESSES.items():
        with open(file_name) as f:
            pid = f.read().split(":")[-1].strip()
        if pid:
            # clear file
            with open(file_name, "w"):
                pass
            LOGGER.info(f"Cleared active Orkestr8 process file '{process_name}'")
            for _ in range(10):
                if os.path.exists(f"/proc/{pid}"):
                    os.kill(int(pid), signal.SIGTERM)
                    LOGGER.info(
                        f"Process ID {pid} has terminated. '{process_name}' has stopped\n"
                    )
                    break
                time.sleep(1)


@dataclass
class StopArgs:
    pid: Union[str, None]


class StopCommand(Command[StopArgs]):
    @staticmethod
    def parse(args) -> StopArgs:
        return StopArgs(args.pid)

    def run(self):
        LOGGER.info("Shutdown command invoked")
        _shut_down_processes()
        LOGGER.info("Process shutdown complete")
