from __future__ import annotations
import enum
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


class Command(enum.Enum):
    """Command list of the application."""

    RESTART = enum.auto()
    """Command to restart recording."""

    EXIT = enum.auto()
    """Command to stop recording and exit immediately before shutting down."""

    NULL = enum.auto()
    """Represents no commands activated."""


GRACE_PERIOD_FOR_CHATTERING = 0.3     # seconds


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

        self._lock_command = threading.RLock()
        self._command = Command.NULL

        self._lock_flightpin_onoff = threading.RLock()
        self._flightpin_onoff: t.List[t.List[bool, float]] = []

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
            with self._lock_in_recording:
                if self._in_recording:
                    break

            self._logger.debug(
                "Waiting the flight pin to be disconnected, "
                f"{round(time.time() - time_init, 3)} elapsing."
            )
            time.sleep(interval)

    def _watch_flightpin(self, interval: float = 0.1) -> None:
        time_init = None
        last_level = None
        while True:
            with self._lock_in_recording:
                if not self._in_recording:
                    return

            level = self.in_flight
            with self._lock_flightpin_onoff:
                if last_level is None or level != last_level:
                    time_init = time.time()
                    self._flightpin_onoff.append([level, 0.])
                else:
                    self._flightpin_onoff[-1][1] = time.time() - time_init

            last_level = level
            time.sleep(interval)

    def _watch_commands(
        self,
        interval: float = 0.1,
        threshold_restart: float = 5.,
        threshold_exit: float = 2.,
    ) -> None:
        while True:
            with self._lock_in_recording:
                if not self._in_recording:
                    return

            with self._lock_flightpin_onoff:
                for i, (level, time_) in enumerate(self._flightpin_onoff):
                    if level:
                        continue

                    if time_ >= threshold_restart:
                        with self._lock_command:
                            self._command = Command.RESTART
                            return
                    elif GRACE_PERIOD_FOR_CHATTERING < time_ <= threshold_exit:
                        try:
                            if self._flightpin_onoff[i + 1][1] < threshold_exit:
                                continue

                            with self._lock_command:
                                self._command = Command.EXIT
                                return
                        except IndexError:
                            pass

            time.sleep(interval)

    def _wait_until_flightpin_connected(self) -> None:
        if not self.in_flight:
            return

        while True:
            gpio.wait_for_edge(self._pin_flight, gpio.FALLING)

            self._logger.debug(
                "Disconnection of the flight pin was detected. "
                f"Waiting {GRACE_PERIOD_FOR_CHATTERING} seconds to verify "
                "the flight pin was pulled out exactly."
            )
            time_init = time.time()
            is_flightpin_connected = False
            while True:
                if self.in_flight:
                    self._logger.debug(
                        "Level of the flight pin is high. It means that "
                        "the flight pin is disconnected before time of "
                        "waiting threshold elapsed. Thus, detecting "
                        "the flight pin is to be continued."
                    )
                    break

                if time.time() - time_init > GRACE_PERIOD_FOR_CHATTERING:
                    is_flightpin_connected = True
                    self._logger.debug(
                        "Time of waiting threshold elapsed while level of "
                        "the flight pin is stable."
                    )
                    break

            if is_flightpin_connected:
                break

    def record(
        self,
        timeout: float,
        file_mov: t.Optional[str] = None,
        interval_recording: float = 0.1,
        check_waiting_time: bool = False,
        interval_waiting_time: float = 0.1,
        interval_watching: float = 0.1,
        threshold_restart: float = 5.,
        threshold_exit: float = 2.,
    ) -> Command:
        """Record a video while obseving state of the body.

        Args:
            timeout: Length of recording time.
            file_mov: Path to new video file.
            interval_recording: Interval of recording.
            check_waiting_time: If making log outputs during waiting time for
                disconnection of the flight pin or not.
            interval_waiting_time: Interval of waiting time until the flight
                pin is disconnected. This parameter doesn't valid when the
                parameter `check_waiting_time` is `False`.
            interval_watching: Interval of watching processes in other
                threads.
            threshold_restart: Time threshold of waiting time to activate
                the command `restart`. The command `restart` is activated
                if the flight pin is connected again for more than
                `threshold_restart` seconds during recording.
            threshold_exit: Time threshold of waiting time to activate
                the command `exit`. The command `exit` is activated
                if the flight pin is connected for less than `threshold_exit`
                seconds and disconnected again for more than `threshold_exit`
                seconds during recording.

        Returns:
            Command that should be executed in the application after
            recording.

        Notes:
            `timeout` must be positive.
        """
        self._command = Command.NULL
        self._flightpin_onoff = []

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

        self._wait_until_flightpin_connected()
        self.turn_off_led()
        self._logger.info("Detected that the flight pin was connected.")

        # Wait until the level of the flight pin becomes low.
        self._logger.info("Wating the flight pin to be disconnected...")
        if check_waiting_time:
            th_check_waiting_time = threading.Thread(
                target=self._log_waiting_time,
                kwargs={"interval": interval_waiting_time},
            )
            th_check_waiting_time.start()
            self._logger.debug(
                "Thread for checking waiting time for disconnection "
                "of the flight pin started. This thread is to be "
                "terminated right after the flight pin is disconnected."
            )

        gpio.wait_for_edge(self._pin_flight, gpio.RISING)
        self._lock_in_recording.acquire()
        self._in_recording = True
        self._lock_in_recording.release()

        self._logger.debug(
            "Rising edge of the flight pin level was detected."
        )
        self._logger.info("Detected that the flight pin was disconnected.")
        self.turn_on_led()

        th_watch_flightpin = threading.Thread(
            target=self._watch_flightpin,
            kwargs={"interval": interval_watching},
        )
        th_watch_flightpin.start()
        self._logger.debug("Thread for watching the flight pin started.")

        th_watch_commands = threading.Thread(
            target=self._watch_commands,
            kwargs={
                "interval": interval_watching,
                "threshold_restart": threshold_restart,
                "threshold_exit": threshold_exit,
            },
        )
        th_watch_commands.start()
        self._logger.debug("Thread for watching commands started.")

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

                with self._lock_command:
                    if self._command is not Command.NULL:
                        self._logger.info(
                            f"Detected a command, {self._command}. "
                            "Exit the recording loop."
                        )
                        break

                self._camera.wait_recording(timeout=interval_recording)
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
            th_watch_commands.join()
            self._logger.debug("The thread for watching commands terminated.")
            th_watch_flightpin.join()
            self._logger.debug(
                "The thread for watching the flight pin terminated."
            )
            if check_waiting_time:
                th_check_waiting_time.join()
                self._logger.debug(
                    "Confirmed the thread for checking waiting time "
                    "was terminated successfully."
                )

        return self._command
