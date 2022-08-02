import logging
import os
from os.path import (
    isdir,
    join,
)

import click
import gileum

from .glm import OBCamGileum
from .recorder import IORecorder
from .util import get_timestamp


LOG_PLACEHOLDER = "[%(asctime)s] [%(levelname)s] %(message)s"


def run_flight_camera(glm: OBCamGileum) -> None:
    # Setup file paths.
    if glm.file_mov is None:
        glm.file_mov = get_timestamp("mov", "h264")
    if glm.file_log is None:
        glm.file_log = get_timestamp("mov", "log")

    if glm.parent_dir is not None:
        if not isdir(glm.parent_dir):
            os.makedirs(glm.parent_dir)

        glm.file_mov = join(glm.parent_dir, glm.file_mov)
        glm.file_log = join(glm.parent_dir, glm.file_log)

    # Setup the logger.
    handler = logging.FileHandler(glm.file_log)
    handler.setLevel(glm.log_level)
    handler.setFormatter(logging.Formatter(LOG_PLACEHOLDER))
    logger = logging.getLogger()
    logger.setLevel(glm.log_level)
    logger.addHandler(handler)

    logger.info(
        "Start the Flight camera mode. "
        f"Setting; {', '.join([f'{k}: {v}' for k, v in glm.dict().items()])}"
    )

    recorder = IORecorder(
        glm.pin_flight,
        glm.pin_led,
        logger,
        file_mov=glm.file_mov,
        resolution=glm.resolution,
        framerate=glm.framerate,
        led_blink_freq=glm.led_blink_freq,
    )
    try:
        recorder.record(
            glm.timeout,
            interval=glm.interval,
            check_waiting_time=glm.check_waiting_time,
        )
    except Exception as e:
        logger.exception("Finish with an exception.", exc_info=e)
        raise e
    finally:
        recorder.cleanup()


@click.command()
@click.argument(
    "glm_file",
    type=click.Path(exists=True),
)
def main(glm_file: str) -> None:
    gileum.load_glms_at(glm_file)
    glm = gileum.get_glm(OBCamGileum)

    run_flight_camera(glm)
