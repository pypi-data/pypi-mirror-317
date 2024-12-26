"""
Installs ML package on the machine by unzipping file and installing
"""
import logging
import subprocess
import sys

logger = logging.getLogger()


def install():
    complete_log = None

    start_log = "Installing foodenie_ml.."
    logger.info(start_log)
    try:
        res = subprocess.run(
            ["tar -xvzf foodenie_ml.tar.gz"],
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        logger.info(res.stdout)
        res = subprocess.run(
            [
                "cd foodenie_ml && python3 -m pip install -r requirements/prod.txt && rm ../foodenie_ml.tar.gz"
            ],
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        logger.info(res.stdout)
    except Exception as e:
        error_log = (
            f"Encountered installation error. {type(e).__name__:str(e)}.\nExiting...\n"
        )
        logger.error(error_log)
    else:
        complete_log = (
            "Application install successfully. Existing installation script\n"
        )
        logger.info(complete_log)

    if complete_log is None:
        # We want the ENTIRE process to stop so exit the program completely
        sys.exit(1)
