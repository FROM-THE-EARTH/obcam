from __future__ import annotations
import logging
import os
import time
import threading
import typing as t

import picamera
import RPi.GPIO as gpio

from .util import get_timestamp


_VIDEO_FORMATS = {
    "h264",
    "mjpeg",
    "yuv",
    "rgb",
    "rgba",
    "bgr",
    "bgra",
}


def verify_video_format(path: str) -> bool:
    ext = os.path.splitext(path)[1]
    if not len(ext):
        return False
    return ext[1:] in _VIDEO_FORMATS


RISING_TIME_THRESHOLD = 0.5     # seconds


class IORecorder:

    def __init__(
        self,
        pin_flight: int,
        pin_led: int,
        file_log: t.Optional[str] = None,
        file_mov: t.Optional[str] = None,
        resolution: t.Tuple = (640, 480),
        led_blink_freq: float = 2.,
    ) -> None:
        """
        Args:
            pin_flight: Pin number for a flight pin.
            pin_led: Pin number for a status LED.
            file_mov: Path to new video file.
            resolution: Resolution of the video.
            led_blink_freq: Frequency of LED blinking.
        """
        if file_mov is None:
            file_mov = get_timestamp("mov", "h264")
        elif verify_video_format(file_mov):
            raise ValueError(f"'{file_mov}' has an invalid extension.")

        if file_log is None:
            file_log = get_timestamp("mov", "log")

        self._camera = picamera.PiCamera()
        self._camera.resolution = resolution

        self._logger = logging.getLogger()
        self._logger.setLevel(logging.DEBUG)
        handler = logging.FileHandler(file_log)
        handler.setLevel(logging.DEBUG)
        self._logger.addHandler(handler)

        self._pin_flight = pin_flight
        self._pin_led = pin_led
        self._fname = file_mov
        self._format = os.path.splitext(file_mov)[1][1:]
        self._thread: t.Optional[threading.Thread] = None

        gpio.setmode(gpio.BCM)
        gpio.setup(self._pin_flight, gpio.IN, pull_up_down=gpio.PUD_DOWN)
        gpio.setup(self._pin_led, gpio.OUT)

        self._pwm_led = gpio.PWM(self._pin_led, led_blink_freq)
        self._pwm_led.start(0)

    @property
    def in_flight(self) -> bool:
        """If the body is in flight or not."""
        return (gpio.input(self._pin_flight) == 1)

    def blink_led(self) -> None:
        self._pwm_led.ChangeDutyCycle(50)

    def turn_on_led(self) -> None:
        self._pwm_led.ChangeDutyCycle(100)

    def turn_off_led(self) -> None:
        self._pwm_led.ChangeDutyCycle(0)

    def record(
        self,
        timeout: float,
        interval: float = 1.,
    ) -> None:
        """Record a video while obseving state of the body.

        Args:
            timeout: Length of recording time.
            interval: Wating time for recording.

        Notes:
            `timeout` must be positive.
        """
        file = open(self._fname, "wb")
        if timeout <= 0:
            self._logger.error(
                "Argument `timeout` must be positive, while {} were given.",
                timeout,
            )
            raise ValueError("timeout must be positive.")

        # Wait until the flight pin is to be connected.
        self._logger.debug("Waiting a flight pin to be connected...")
        self.blink_led()

            # Noise measures
        is_flightpin_connected = False
        while True:
            gpio.wait_for_edge(self._pin_flight, gpio.FALLING)
            time_init = time.time()

            while True:
                if self.in_flight:
                    break
                else:
                    if time.time() - time_init > RISING_TIME_THRESHOLD:
                        is_flightpin_connected = True
                        break

            if is_flightpin_connected:
                break

        self.turn_off_led()
        self._logger.debug("A flight pin was connected.")

        # Wait until the level of the flight pin becomes low.
        self._logger.debug("Wating the flight pin to be disconnected...")
        gpio.wait_for_edge(self._pin_flight, gpio.RISING)
        self.turn_on_led()
        self._logger.debug("The flight pin was disconnected.")

        # Start recording
        self._logger.debug("Start recording.")
        self._camera.start_recording(file, format=self._format)
        time_init = time.time()
        try:
            while True:
                if 0 < timeout <= (time.time() - time_init):
                    break
                self._camera.wait_recording(timeout=interval)
                file.flush()
        finally:
            file.flush()
            self._camera.stop_recording()
            self._logger.debug("Stop recording.")

            self.turn_off_led()

    def start_record(
        self,
        timeout: float,
        interval: float = 1.,
    ) -> IORecorder:
        self._thread = threading.Thread(
            target=self.record,
            args=(timeout, interval),
        )
        self._thread.start()
        return self

    def stop_record(self, timeout: t.Optional[float] = None) -> None:
        if self._thread is None:
            return

        self._thread.join(timeout=timeout)
        self._thread = None

    def cleanup(self) -> None:
        self._pwm_led.stop()
        gpio.cleanup()

    def __enter__(self) -> IORecorder:
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.stop_record()
        self.cleanup()
