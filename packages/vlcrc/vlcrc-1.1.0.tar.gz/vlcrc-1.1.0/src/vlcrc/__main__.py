"""
Command Line Interface for VLC Remote Control.

usage: vlcrc [-h] [--timeout TIMEOUT] host port {command} ...

positional arguments:
  host                  VLC host address
  port                  VLC Remote Control interface port
  {play,stop,next,prev,clear,status,pause,repeat,
  loop,random,playlist,quit,add,goto,volume,adev}
                        Commands
    play                play command
    stop                stop command
    next                next command
    prev                prev command
    clear               clear command
    status              status command
    pause               pause command
    repeat              repeat command
    loop                loop command
    random              random command
    playlist            playlist command
    quit                quit command
    add                 Add file to playlist
    goto                Go to specific track
    volume              Get/set volume
    adev                Audio device control

options:
  -h, --help            show this help message and exit
  --timeout TIMEOUT     Connection timeout in seconds (default: 1.0)
"""

import sys
import argparse
from pathlib import Path
from typing import Optional
from .vlc_remote_control import (
    VLCRemoteControl,
    UnknownCommandError,
    PausedPlayerError
)


class CommandLineArgs(argparse.Namespace):
    """Parsed command-line arguments for VLCRemoteControl.

    Attributes:
        host (str): VLC host address.
        port (int): VLC Remote Control interface port.
        command (Optional[str]): Command to execute.
        file (Optional[Path]): File path.
        index (Optional[int]): Playlist index.
        level (Optional[int]): Volume level.
        device_id (Optional[str]): Audio device ID.
        timeout (Optional[float]): Connection timeout in seconds.
    """
    # pylint: disable=too-few-public-methods
    host: str
    port: int
    command: Optional[str]
    file: Optional[Path]
    index: Optional[int]
    level: Optional[int]
    device_id: Optional[str]
    timeout: Optional[float]


def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser.

    Returns:
        argparse.ArgumentParser: Configured argument parser
    """
    parser = argparse.ArgumentParser(
        prog="vlcrc",
        description="Command Line Interface for VLC Remote Control",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        "host", help="VLC host address (e.g., 127.0.0.1, 192.168.1.100)")
    parser.add_argument(
        "port", type=int, help="VLC Remote Control interface port")
    parser.add_argument(
        "--timeout", type=float, default=1.0,
        help="Connection timeout in seconds (default: 1.0)")

    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Simple commands without arguments
    for cmd in ["play", "stop", "next", "prev", "clear", "status", "pause",
                "repeat", "loop", "random", "playlist", "quit"]:
        subparsers.add_parser(cmd, help=f"{cmd} command")

    # Add file to playlist
    add_parser = subparsers.add_parser("add", help="Add file to playlist")
    add_parser.add_argument("file", type=Path, help="File path")

    # Goto specific track
    goto_parser = subparsers.add_parser("goto", help="Go to specific track")
    goto_parser.add_argument("index", type=int,
                             help="Track index (starts at 1)")

    # Volume control
    volume_parser = subparsers.add_parser("volume", help="Get/set volume")
    volume_parser.add_argument("level", type=int, nargs="?",
                               help="Volume level (0-320)")

    # Audio device control
    adev_parser = subparsers.add_parser("adev", help="Audio device control")
    adev_parser.add_argument("device_id", nargs="?",
                             help="Device ID to set as active")

    return parser


def handle_command(vlc: VLCRemoteControl, args: CommandLineArgs) -> None:
    """Execute the VLC command based on parsed arguments.

    Args:
        vlc: VLCRemoteControl instance
        args: Parsed command line arguments

    Raises:
        SystemExit: On command execution error
    """
    match args.command:
        # Simple commands without arguments
        case "play" | "stop" | "next" | "prev" | "clear" | "pause" | "quit":
            getattr(vlc, args.command)()

        # Toggle commands that return boolean
        case "repeat" | "loop" | "random":
            result = getattr(vlc, args.command)()
            sys.stdout.write(f"{args.command}: {'on' if result else 'off'}")

        # Status command
        case "status":
            for line in vlc.status():
                sys.stdout.write(line+"\n")

        # Playlist command
        case "playlist":
            for i, item in enumerate(vlc.playlist(), 1):
                sys.stdout.write(f"{i}. {item}\n")

        # Add file command
        case "add":
            vlc.add(args.file)

        # Goto command
        case "goto":
            vlc.goto(args.index)

        # Volume command
        case "volume":
            if args.level is None:
                sys.stdout.write(f"Current volume: {vlc.get_volume()}")
            else:
                vlc.set_volume(args.level)

        # Audio device command
        case "adev":
            if args.device_id is None:
                devices = vlc.get_adev()
                for device in devices:
                    sys.stdout.write(f"{device.id} - {device.name}\n")
            else:
                vlc.set_adev(args.device_id)

        case _:
            sys.exit(f"Error: Unknown command '{args.command}'")


def main() -> None:
    """Entry point for the VLC remote control CLI."""
    parser = create_parser()
    args = parser.parse_args(namespace=CommandLineArgs())

    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        vlc = VLCRemoteControl(args.host, args.port, args.timeout)
        handle_command(vlc, args)
    except (FileNotFoundError, ValueError, UnknownCommandError,
            ConnectionError, PausedPlayerError) as e:
        sys.exit(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
