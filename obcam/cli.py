import logging
import os
from os.path import (
    isdir,
    join,
)

import click
import gileum

from .glm import OBCamGileum
from .recorder import (
    Command,
    IORecorder,
)
from .util import (
    get_timestamp,
    shutdown_now,
)


LOG_PLACEHOLDER = "[%(asctime)s] [%(levelname)s] %(message)s"


def run_flight_camera(glm: OBCamGileum) -> None:
    # Setup the logger.
    if glm.file_log is None:
        file_log = get_timestamp("mov", "log")
    if glm.parent_dir is not None:
        if not isdir(glm.parent_dir):
            os.makedirs(glm.parent_dir)
        file_log = join(glm.parent_dir, file_log)

    handler = logging.FileHandler(file_log)
    handler.setLevel(glm.log_level)
    handler.setFormatter(logging.Formatter(LOG_PLACEHOLDER))
    logger = logging.getLogger()
    logger.setLevel(glm.log_level)
    logger.addHandler(handler)

    logger.info(
        "Start the Flight camera mode. "
        f"Setting; {', '.join([f'{k}: {v}' for k, v in glm.dict().items()])}"
    )

    try:
        recorder = IORecorder(
            glm.pin_flight,
            glm.pin_led,
            logger,
            resolution=glm.resolution,
            framerate=glm.framerate,
            led_blink_freq=glm.led_blink_freq,
        )

        while True:
            # Setup file paths.
            if glm.file_mov is None:
                file_mov = get_timestamp("mov", "h264")
            if glm.parent_dir is not None:
                file_mov = join(glm.parent_dir, file_mov)

            # Start recording.
            command = recorder.record(
                glm.timeout,
                file_mov=file_mov,
                interval_recording=glm.interval_recording,
                check_waiting_time=glm.check_waiting_time,
                interval_waiting_time=glm.interval_waiting_time,
                interval_watching=glm.interval_watching,
                threshold_restart=glm.threshold_restart,
                threshold_exit=glm.threshold_exit,
            )
            if command is Command.EXIT:
                break
            if command is Command.RESTART:
                continue
            else:
                break
    except Exception as e:
        logger.exception("Finish with an exception.", exc_info=e)
        raise e
    else:
        if glm.shutdown_after_recording and command is Command.NULL:
            logger.info("Shut down the system.")
            shutdown_now()


@click.command()
@click.argument(
    "glm_file",
    type=click.Path(exists=True),
)
def main(glm_file: str) -> None:
    gileum.load_glms_at(glm_file)
    glm = gileum.get_glm(OBCamGileum)

    run_flight_camera(glm)
