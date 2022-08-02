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


FALLING_TIME_THRESHOLD = 0.5     # seconds


class IORecorder:

    def __init__(
        self,
        pin_flight: int,
        pin_led: int,
        logger: logging.Logger,
        file_mov: t.Optional[str] = None,
        resolution: t.Tuple = (1920, 1080),
        framerate: int = 30,
        led_blink_freq: float = 2.,
    ) -> None:
        """
        Args:
            pin_flight: Pin number for a flight pin.
            pin_led: Pin number for a status LED.
            logger: Logger for the flight camera.
            file_mov: Path to new video file.
            resolution: Resolution of the video.
            led_blink_freq: Frequency of LED blinking.
        """
        if file_mov is None:
            file_mov = get_timestamp("mov", "h264")
        elif not verify_video_format(file_mov):
            raise ValueError(f"'{file_mov}' has an invalid extension.")

        self._logger = logger
        self._camera = picamera.PiCamera(
            resolution=resolution,
            framerate=framerate,
        )

        self._pin_flight = pin_flight
        self._pin_led = pin_led
        self._fname = file_mov
        self._format = os.path.splitext(file_mov)[1][1:]
        self._thread: t.Optional[threading.Thread] = None

        self._lock_in_flight = threading.RLock()
        self._in_flight = False

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
        self._logger.debug("LED started to be blinking.")

    def turn_on_led(self) -> None:
        self._pwm_led.ChangeDutyCycle(100)
        self._logger.debug("Turned the LED on.")

    def turn_off_led(self) -> None:
        self._pwm_led.ChangeDutyCycle(0)
        self._logger.debug("Turned the LED off.")

    def _log_waiting_time(self, interval: float = 1.) -> None:
        time_init = time.time()
        while True:
            self._lock_in_flight.acquire()
            if self._in_flight:
                break
            self._lock_in_flight.release()

            self._logger.debug(
                "Waiting the flight pin to be disconnected, "
                f"{round(time.time() - time_init, 3)} elapsing."
            )
            time.sleep(interval)

    def record(
        self,
        timeout: float,
        interval: float = 0.1,
        check_waiting_time: bool = False,
    ) -> None:
        """Record a video while obseving state of the body.

        Args:
            timeout: Length of recording time.
            interval: Wating time for recording.
            check_waiting_time: If making log outputs during waiting time for
                disconnection of the flight pin or not.

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
        self._logger.info("Waiting a flight pin to be connected...")
        self.blink_led()

            # Noise measures
        is_flightpin_connected = False
        while True:
            gpio.wait_for_edge(self._pin_flight, gpio.FALLING)
            self._logger.debug(
                "Falling edge of the flight pin level was detected. "
                f"Waiting {FALLING_TIME_THRESHOLD} seconds to verify "
                "the flight pin was pulled out exactly."
            )

            time_init = time.time()
            while True:
                if self.in_flight:
                    self._logger.debug(
                        "Level of the flight pin is high. It means that "
                        "the flight pin is disconnected before time of "
                        "waiting threshold elapsed. Thus, detecting "
                        "the flight pin is to be continued."
                    )
                    break
                else:
                    if time.time() - time_init > FALLING_TIME_THRESHOLD:
                        is_flightpin_connected = True
                        self._logger.debug(
                            "Time of waiting threshold elapsed while level of "
                            "the flight pin is stable."
                        )
                        break

            if is_flightpin_connected:
                break

        self.turn_off_led()
        self._logger.info("Detected that the flight pin was connected.")

        # Wait until the level of the flight pin becomes low.
        self._logger.info("Wating the flight pin to be disconnected...")
        if check_waiting_time:
            th = threading.Thread(target=self._log_waiting_time)
            th.start()
            # This thread automatically exits after the flight pin
            # is disconnected.

        gpio.wait_for_edge(self._pin_flight, gpio.RISING)
        self._lock_in_flight.acquire()
        self._in_flight = True
        self._lock_in_flight.release()

        self._logger.debug(
            "Rising edge of the flight pin level was detected."
        )
        self._logger.info("Detected that the flight pin was disconnected.")
        self.turn_on_led()

        # Recording
        self._logger.info("Start recording.")
        self._camera.start_recording(file, format=self._format)
        time_init = time.time()
        try:
            while True:
                elapsed_time = time.time() - time_init
                if 0 < timeout <= elapsed_time:
                    break
                self._camera.wait_recording(timeout=interval)
                file.flush()
                self._logger.debug(
                    "Recording in progress while writing into the file, "
                    f"remaining {round(timeout - elapsed_time, 3)} seconds..."
                )
            self._logger.debug("Timeout is over.")
        finally:
            file.flush()
            self._camera.stop_recording()
            self._logger.info("Stop recording.")

            self.turn_off_led()

    def start_record(
        self,
        timeout: float,
        interval: float = 1.,
        check_waiting_time: bool = False,
    ) -> IORecorder:
        self._thread = threading.Thread(
            target=self.record,
            args=(timeout, interval, check_waiting_time),
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
