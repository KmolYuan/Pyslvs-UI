# -*- coding: utf-8 -*-

"""Information.

+ Module versions.
+ Help descriptions.
+ Check for update function.
"""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2019"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from sys import version_info as _vi
from platform import system, release, machine, python_compiler
from argparse import ArgumentParser
from pyslvs import __version__
from pyslvs_ui.qt_patch import API, QT_VERSION

SYS_INFO = (
    f"Pyslvs {__version__}",
    f"OS Type: {system()} {release()} [{machine()}]",
    f"Python Version: {_vi.major}.{_vi.minor}.{_vi.micro}({_vi.releaselevel})",
    f"Python Compiler: {python_compiler()}",
    f"Qt wrapper: {API}",
    f"Qt Version: {QT_VERSION}",
)

parser = ArgumentParser(
    description=(
        f"Pyslvs version {__version__} - "
        f"Open Source Planar Linkage Mechanism Simulation "
        f"and Mechanical Synthesis System"
    ),
    epilog=f"{__copyright__} {__license__} {__author__} {__email__}",
    add_help=False
)
g = parser.add_argument_group("startup options")
g.add_argument(
    'filepath',
    default=None,
    nargs='?',
    type=str,
    help="read a specific project from the file path"
)
g.add_argument(
    '-c',
    metavar="start path",
    default=None,
    nargs='?',
    type=str,
    help="change to specified path when startup Pyslvs"
)
g.add_argument(
    '--kernel',
    metavar="kernel",
    default=None,
    nargs='?',
    type=str,
    choices=['pyslvs', 'python_solvespace', 'sketch_solve'],
    help="startup Pyslvs with specified solver, "
         "default is depending on local setting"
)
g = parser.add_argument_group("information options")
g.add_argument(
    '-h',
    '--help',
    action='help',
    help="show this help message and exit"
)
g.add_argument(
    '-v',
    '--version',
    action='version',
    version=SYS_INFO[0]
)
g.add_argument(
    '-d',
    '--debug-mode',
    action='store_true',
    help="do not connect to GUI console when opening, "
         "and change the logger from INFO into DEBUG level"
)
g = parser.add_argument_group("graphical user interface options")
g.add_argument(
    '--fusion',
    default=False,
    action='store_true',
    help="run Pyslvs in Fusion style"
)
g.add_argument(
    '--full-screen',
    default=False,
    action='store_true',
    help="start Pyslvs with full-screen mode"
)
g = parser.add_argument_group("other options")
g.add_argument(
    '--test',
    default=False,
    action='store_true',
    help="just test the module import states and exit"
)
g.add_argument(
    '--platform',
    metavar="plugins",
    default="",
    nargs='?',
    type=str,
    help="startup Pyslvs with specified Qt platform plugins, "
         "such as WebGL (webgl:[port])"
)
if system() == "Linux":
    # AppImage options
    g = parser.add_argument_group(
        "AppImage arguments",
        "these options only work in package state. Pyslvs is a type 2 package, "
        "for more information: https://docs.appimage.org/"
    )
    g.add_argument(
        '--appimage-extract',
        action='store_true',
        help="extract the files of package into a 'squashfs-root' folder"
    )
    g.add_argument(
        '--appimage-mount',
        action='store_true',
        help="temporarily mount entire package into a folder, "
             "it can stop by terminating this program"
    )
    g.add_argument(
        '--appimage-offset',
        action='store_true',
        help="obtain offset value of 'mount' command, then mount it with: "
             "\"sudo mount PACKAGE MOUNT -o offset=VALUE\""
    )
ARGUMENTS = parser.parse_args()
del g, parser
