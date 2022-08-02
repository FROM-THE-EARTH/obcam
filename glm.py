import logging

from obcam import OBCamGileum


glm = OBCamGileum(
    # Length of recording time.
    timeout=210,

    # Pin number for a flight pin.
    pin_flight=22,

    # Pin number for a status LED.
    pin_led=12,

    # Path to new video file.
    file_mov=None,

    # Path to new log file.
    file_log=None,

    # Path to the parent directory of output files.
    parent_dir=None,

    # Resolution of the video to be recorded.
    resolution=(1920, 1080),

    # Framerate of the video to be recorded.
    framerate=30,

    # Wating time for recording.
    interval_recording=0.1,

    # Frequency of LED blinking.
    led_blink_freq=2.,

    # Log level used in the application.
    log_level=logging.INFO,

    # If making log outputs during waiting time for disconnection
    # of the flight pin or not
    check_waiting_time=False,

    # Interval of waiting time until the flight pin is disconnected. This
    # parameter doesn't valid when the parameter `check_waiting_time` is
    # `False`.
    interval_waiting_time=0.1,

    # If shutting down the system after recording or not.
    shutdown_after_recording=True,

    # Interval of watching processes in other threads.
    interval_watching=0.1,

    # Time threshold of waiting time to activate the command `restart`. The
    # command `restart` is activated if the flight pin is connected again for
    # more than `threshold_restart` seconds during recording.
    threshold_restart=5.,

    # Time threshold of waiting time to activate the command `exit`. The
    # command `exit` is activated if the flight pin is connected for less than
    # `threshold_exit` seconds and disconnected again for more than
    # `threshold_exit` seconds during recording.
    threshold_exit=2.,
)
