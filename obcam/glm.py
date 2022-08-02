import logging
import typing as t

import gileum


class OBCamGileum(gileum.BaseGileum):
    """Setting giluem for the obcam application.

    An object of this class should be created in a gileum file, a setting file
    of the application, when you execute the obcam application. The gileum
    file can be given to the first argument of the obcam CLI application and
    the application will search the object of this class, and finally start
    recording using the parameters defined in the object. In this sense,
    an object of this class is a setting object of the application.

    Note that the `__init__` method of this class has a essential argument,
    `timeout`. The argument `timeout` means length of recording time as
    seconds. The other arguments could be given if necessary.
    """

    timeout: float
    """Length of recording time."""

    pin_flight: int = 22
    """Pin number for a flight pin."""

    pin_led: int = 12
    """Pin number for a status LED."""

    file_mov: t.Optional[str] = None
    """Path to new video file."""

    file_log: t.Optional[str] = None
    """Path to new log file."""

    parent_dir: t.Optional[str] = None
    """Path to the parent directory of output files."""

    resolution: t.Tuple[int, int] = (1920, 1080)
    """Resolution of the video to be recorded."""

    framerate: int = 30
    """Framerate of the video to be recorded."""

    interval_recording: float = 0.1
    """Wating time for recording."""

    led_blink_freq: float = 2.
    """Frequency of LED blinking."""

    log_level: int = logging.INFO
    """Log level used in the application."""

    check_waiting_time: bool = False
    """If making log outputs during waiting time for disconnection
    of the flight pin or not."""

    interval_waiting_time: float = 0.1
    """Interval of waiting time until the flight pin is disconnected. This
    parameter doesn't valid when the parameter `check_waiting_time` is
    `False`."""

    shutdown_after_recording: bool = True
    """If shutting down the system after recording or not."""

    interval_watching: float = 0.1
    """Interval of watching processes in other threads."""

    threshold_restart: float = 5.
    """Time threshold of waiting time to activate the command `restart`. The
    command `restart` is activated if the flight pin is connected again for
    more than `threshold_restart` seconds during recording."""

    threshold_exit: float = 2.
    """Time threshold of waiting time to activate the command `exit`. The
    command `exit` is activated if the flight pin is connected for less than
    `threshold_exit` seconds and disconnected again for more than
    `threshold_exit` seconds during recording."""
