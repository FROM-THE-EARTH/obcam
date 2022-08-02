import datetime
import subprocess
import typing as t


def get_timestamp(
    tag: t.Optional[str] = None,
    suffix: t.Optional[str] = None,
) -> str:
    timestamp = datetime.datetime.now().strftime("%y%m%d-%H%M%S")
    if tag is not None and len(tag):
        timestamp = "-".join((tag, timestamp))
    if suffix is not None and len(suffix):
        timestamp = ".".join((timestamp, suffix))
    return timestamp


def shutdown_now() -> None:
    subprocess.run(["shutdown", "-h", "now"])
