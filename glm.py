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

    # Resolution of the video to be recorded.
    resolution=(1920, 1080),

    # Framerate of the video to be recorded.
    framerate=30,

    # Wating time for recording.
    interval=0.1,

    # Frequency of LED blinking.
    led_blink_freq=2.,
)
