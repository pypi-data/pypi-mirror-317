"""
VLC Remote Control.

This library provides the core functionality for controlling
VLC media player via its Remote Control interface.

Basic usage:
    >>> from vlcrc import VLCRemoteControl
    >>> from pathlib import Path
    >>> vlc = VLCRemoteControl("127.0.0.1", 50000)
    >>> vlc.add(Path("/path/to/media/file.mp4"))
    >>> vlc.status()
"""

from .vlc_remote_control import (
    VLCRemoteControl,
    UnknownCommandError,
    PausedPlayerError,
    AudioDevice
)

__all__ = [
    "VLCRemoteControl",
    "UnknownCommandError",
    "PausedPlayerError",
    "AudioDevice"
]
