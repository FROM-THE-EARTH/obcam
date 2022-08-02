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
        resolution: t.Tuple = (1920, 1080),
        framerate: int = 30,
        led_blink_freq: float = 2.,
    ) -> None:
        """
        Args:
            pin_flight: Pin number for a flight pin.
            pin_led: Pin number for a status LED.
            logger: Logger for the flight camera.
            resolution: Resolution of the video.
            framerate: Framerate of the video.
            led_blink_freq: Frequency of LED blinking.
        """
        self._logger = logger
        self._camera = picamera.PiCamera(
            resolution=resolution,
            framerate=framerate,
        )
        self._first_recording = True

        self._pin_flight = pin_flight
        self._pin_led = pin_led

        self._lock_in_recording = threading.RLock()
        self._in_recording = False

        self._lock_should_restart = threading.RLock()
        self._should_restart = False

        gpio.setmode(gpio.BCM)
        gpio.setup(self._pin_flight, gpio.IN, pull_up_down=gpio.PUD_DOWN)
        gpio.setup(self._pin_led, gpio.OUT)

        self._pwm_led = gpio.PWM(self._pin_led, led_blink_freq)
        self._pwm_led.start(0)

    def __del__(self) -> None:
        self._camera.stop_recording()
        self._pwm_led.stop()
        gpio.cleanup()
        self._logger.debug("Cleaned up the all GPIO pins.")

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
            self._lock_in_recording.acquire()
            if self._in_recording:
                break
            self._lock_in_recording.release()

            self._logger.debug(
                "Waiting the flight pin to be disconnected, "
                f"{round(time.time() - time_init, 3)} elapsing."
            )
            time.sleep(interval)

    def _command_restart(
        self,
        time_threshold: float = 3.,
        interval: float = 0.1,
    ) -> None:
        interval_mili = int(interval * 1e3)     # miliseconds
        time_init: t.Optional[float] = None
        while True:
            self._lock_in_recording.acquire()
            if not self._in_recording:
                return
            self._lock_in_recording.release()

            if time_init is None:
                channel = gpio.wait_for_edge(
                    self._pin_flight,
                    gpio.FALLING,
                    timeout=interval_mili,
                )
                if channel is not None:
                    time_init = time.time()
                continue

            time.sleep(interval)
            if self.in_flight:
                time_init = None
                continue

            if time.time() - time_init > time_threshold:
                break

        self._lock_should_restart.acquire()
        self._should_restart = True
        self._lock_should_restart.release()
        self._logger.info(
            "Activated the command `restart`. The application will be "
            "restarted."
        )

    def record(
        self,
        timeout: float,
        file_mov: t.Optional[str] = None,
        interval: float = 0.1,
        check_waiting_time: bool = False,
    ) -> bool:
        """Record a video while obseving state of the body.

        Args:
            timeout: Length of recording time.
            file_mov: Path to new video file.
            interval: Wating time for recording.
            check_waiting_time: If making log outputs during waiting time for
                disconnection of the flight pin or not.

        Returns:
            If the application should restart recording or not.

        Notes:
            `timeout` must be positive.
        """
        self._should_restart = False
        if file_mov is None:
            file_mov = get_timestamp("mov", "h264")
        elif not verify_video_format(file_mov):
            raise ValueError(f"'{file_mov}' has an invalid extension.")

        self._logger.info(
            f"Start the `record` method, path to new movie file: {file_mov}."
        )
        file = open(file_mov, "wb")
        format_ = os.path.splitext(file_mov)[1][1:]
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
        self._lock_in_recording.acquire()
        self._in_recording = True
        self._lock_in_recording.release()

        self._logger.debug(
            "Rising edge of the flight pin level was detected."
        )
        self._logger.info("Detected that the flight pin was disconnected.")
        self.turn_on_led()

        th_restart = threading.Thread(target=self._command_restart)
        th_restart.start()

        # Recording
        if self._first_recording:
            self._camera.start_recording(file, format=format_)
            self._first_recording = False
        else:
            self._camera.split_recording(file, format=format_)

        time_init = time.time()
        self._logger.info(
            f"Start recording, current time: {time_init}, timeout: {timeout}."
        )
        try:
            while True:
                elapsed_time = time.time() - time_init
                if 0 < timeout <= elapsed_time:
                    self._logger.debug("Timeout is over.")
                    break

                self._lock_should_restart.acquire()
                if self._should_restart:
                    self._lock_should_restart.release()
                    break
                self._lock_should_restart.release()

                self._camera.wait_recording(timeout=interval)
                file.flush()
                self._logger.debug(
                    "Recording in progress while writing into the file, "
                    f"remaining {round(timeout - elapsed_time, 3)} seconds..."
                )
        except Exception as e:
            self._logger.exception(
                "An exception occured during recording.",
                exc_info=e,
            )
            raise e
        finally:
            file.flush()
            self._logger.info("Stop recording.")
            self.turn_off_led()

            self._lock_in_recording.acquire()
            self._in_recording = False
            self._lock_in_recording.release()
            th_restart.join()

        return self._should_restart
