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


@click.command()
@click.argument(
    "glm_file",
    type=click.Path(exists=True),
)
def main(glm_file: str) -> None:
    gileum.load_glms_at(glm_file)
    glm = gileum.get_glm(OBCamGileum)

    if glm.file_mov is None:
        glm.file_mov = get_timestamp("mov", "h264")
    if glm.file_log is None:
        glm.file_log = get_timestamp("mov", "log")

    if glm.parent_dir is not None:
        if not isdir(glm.parent_dir):
            os.makedirs(glm.parent_dir)

        glm.file_mov = join(glm.parent_dir, glm.file_mov)
        glm.file_log = join(glm.parent_dir, glm.file_log)

    with IORecorder(
        glm.pin_flight,
        glm.pin_led,
        file_mov=glm.file_mov,
        file_log=glm.file_log,
        resolution=glm.resolution,
        framerate=glm.framerate,
        led_blink_freq=glm.led_blink_freq,
    ) as rec:
        rec.start_record(
            glm.timeout,
            interval=glm.interval,
        )
