# -*- coding: utf-8 -*-

"""Information.

+ Module versions.
+ Help descriptions.
+ Check for update function.
"""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2020"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import Optional
from sys import version_info as _vi
from platform import system, release, machine, python_compiler
from argparse import ArgumentParser, Namespace
from dataclasses import dataclass
from pyslvs import __version__
from pyslvs_ui.qt_patch import API, QT_VERSION


def parse_args() -> Namespace:
    parser = ArgumentParser(
        prog='pyslvs',
        description=(
            f"Pyslvs {__version__} - "
            f"Open Source Planar Linkage Mechanism Simulation "
            f"and Mechanical Synthesis System"
        ),
        epilog=f"{__copyright__} {__license__} {__author__} {__email__}",
        add_help=False
    )
    main_info = parser.add_argument_group("information options")
    main_info.add_argument(
        '-v',
        '--version',
        action='version',
        version=SYS_INFO[0]
    )
    main_info.add_argument(
        '-d',
        '--debug-mode',
        action='store_true',
        help="show debug message to stdout, and "
             "change the logger from INFO into DEBUG level"
    )
    s = parser.add_subparsers(title="CLI command", dest='cmd')
    s.add_parser(
        'test',
        help="just test the module import states and exit",
        add_help=False
    )
    gui_cmd = s.add_parser('gui', help="arguments for gui only", add_help=False)
    gui_startup = gui_cmd.add_argument_group("startup options")
    gui_startup.add_argument(
        'filepath',
        default="",
        nargs='?',
        type=str,
        help="read a specific project from the file path"
    )
    gui_startup.add_argument(
        '-c',
        metavar="start path",
        default="",
        nargs='?',
        type=str,
        help="change to specified path when startup Pyslvs"
    )
    gui_startup.add_argument(
        '--kernel',
        metavar="kernel",
        default='',
        nargs='?',
        type=str,
        choices=['pyslvs', 'python_solvespace', 'sketch_solve'],
        help="startup Pyslvs with specified solver, "
             "default is depending on local setting"
    )
    qt = gui_cmd.add_argument_group("Qt options")
    qt.add_argument(
        '--fusion',
        default=False,
        action='store_true',
        help="run Pyslvs in Fusion style"
    )
    qt.add_argument(
        '--full-screen',
        default=False,
        action='store_true',
        help="start Pyslvs with full-screen mode"
    )
    qt.add_argument(
        '--platform',
        metavar="plugins",
        default="",
        nargs='?',
        type=str,
        help="startup Pyslvs with specified Qt platform plugins, "
             "such as WebGL (webgl:[port])"
    )
    gui_info = gui_cmd.add_argument_group("information options")
    extract_cmd = s.add_parser(
        'extract',
        help="extract data from a supported file",
        add_help=False
    )
    extract_cmd.add_argument(
        'filepath',
        default="",
        type=str,
        help="input file path"
    )
    extract_info = extract_cmd.add_argument_group("information options")
    for group in (main_info, gui_info, extract_info):
        group.add_argument(
            '-h',
            '--help',
            action='help',
            help="show this help message and exit"
        )
    if system() == "Linux":
        # AppImage options
        appimage = parser.add_argument_group(
            "AppImage arguments",
            "these options only work in package state. "
            "Pyslvs is a type 2 package, "
            "for more information: https://docs.appimage.org/"
        )
        appimage.add_argument(
            '--appimage-extract',
            action='store_true',
            help="extract the files of package into a 'squashfs-root' folder"
        )
        appimage.add_argument(
            '--appimage-mount',
            action='store_true',
            help="temporarily mount entire package into a folder, "
                 "it can stop by terminating this program"
        )
        appimage.add_argument(
            '--appimage-offset',
            action='store_true',
            help="obtain offset value of 'mount' command, then mount it with: "
                 "\"sudo mount PACKAGE MOUNT -o offset=VALUE\""
        )
    return parser.parse_args()


@dataclass(repr=False, eq=False)
class Arguments:
    """Argument container."""
    cmd: Optional[str]
    c: str = ""
    filepath: str = ""
    kernel: str = ""
    debug_mode: bool = False
    fusion: bool = False
    appimage_extract: bool = False
    appimage_mount: bool = False
    appimage_offset: bool = False


SYS_INFO = (
    f"Pyslvs {__version__}",
    f"OS Type: {system()} {release()} [{machine()}]",
    f"Python Version: {_vi.major}.{_vi.minor}.{_vi.micro}({_vi.releaselevel})",
    f"Python Compiler: {python_compiler()}",
    f"Qt wrapper: {API}",
    f"Qt Version: {QT_VERSION}",
)
ARGUMENTS = Arguments(**vars(parse_args()))
del parse_args
