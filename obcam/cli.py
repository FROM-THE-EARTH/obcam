import click
import gileum

from .glm import OBCamGileum
from .recorder import IORecorder


@click.command()
@click.argument(
    "glm_file",
    type=click.Path(exists=True),
)
def main(glm_file: str) -> None:
    gileum.load_glms_at(glm_file)
    glm = gileum.get_glm(OBCamGileum)

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
