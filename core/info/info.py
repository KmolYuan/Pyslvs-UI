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

from typing import Tuple
from sys import version_info as _vi
from platform import (
    system,
    release,
    machine,
    python_compiler,
)
from argparse import ArgumentParser
import requests
from pyslvs import __version__
from core.QtModules import (
    QCoreApplication,
    QProgressDialog,
    QT_VERSION_STR,
    PYQT_VERSION_STR,
)


SYS_INFO: Tuple[str, ...] = (
    f"Pyslvs {__version__}",
    f"OS Type: {system()} {release()} [{machine()}]",
    f"Python Version: {_vi.major}.{_vi.minor}.{_vi.micro}({_vi.releaselevel})",
    f"Python Compiler: {python_compiler()}",
    f"Qt Version: {QT_VERSION_STR}",
    f"PyQt Version: {PYQT_VERSION_STR}",
)

_POWERED_BY = ", ".join((
    "PyQt5",
    "ezdxf",
    "Cython",
    "openpyxl",
    "psutil",
    "peewee",
    "Lark-parser",
    "NetworkX",
    "Pygments",
    "PyYAML",
))

_parser = ArgumentParser(
    description=(
        "Pyslvs - Open Source Planar Linkage Mechanism Simulation "
        "and Mechanical Synthesis System."
    ),
    epilog=f"Powered by {_POWERED_BY}."
)
_parser.add_argument(
    '-v',
    '--version',
    action='version',
    version=SYS_INFO[0]
)
_parser.add_argument(
    'file',
    metavar="file path",
    default=None,
    nargs='?',
    type=str,
    help="read workbook from the file path"
)
_parser.add_argument(
    '-c',
    metavar="start path",
    default=None,
    nargs='?',
    type=str,
    help="change to specified path when startup Pyslvs"
)
_parser.add_argument(
    '--fusion',
    action='store_true',
    help="run Pyslvs in Fusion style"
)
_parser.add_argument(
    '--full-screen',
    action='store_true',
    help="start Pyslvs with full-screen mode"
)
_parser.add_argument(
    '-d',
    '--debug-mode',
    action='store_true',
    help=(
        "do not connect to GUI console when opening, "
        "and change the logger from INFO into DEBUG level"
    )
)
_parser.add_argument(
    '--test',
    action='store_true',
    help="just test module states and exit"
)
_parser.add_argument(
    '--kernel',
    metavar="kernel",
    default=None,
    nargs='?',
    type=str,
    choices=['pyslvs', 'python_solvespace', 'sketch_solve'],
    help=(
        "startup Pyslvs with specified solver, "
        "default is depending on local setting"
    )
)
_parser.add_argument(
    '--platform',
    metavar="plugins",
    default="",
    nargs='?',
    type=str,
    help="startup Pyslvs with specified Qt platform plugins, "
         "such as WebGL (webgl:[port])"
)

ARGUMENTS = _parser.parse_args()


def check_update(dlg: QProgressDialog) -> str:
    """Check for update."""
    ver_list = [int(v) for v in __version__.split('.') if v.isdigit()]
    m = len(ver_list)
    for i in range(m):
        if i == 0:
            text = "major"
        elif i == 1:
            text = "minor"
        else:
            text = "build"
        dlg.setLabelText(f"Checking for {text}...")
        QCoreApplication.processEvents()
        if dlg.wasCanceled():
            return ""
        next_ver = ver_list[:m]
        next_ver[i] += 1
        url = (
            "https://github.com/KmolYuan/Pyslvs-UI/releases/tag/"
            f"v{next_ver[0]}.{next_ver[1]:02}.{next_ver[2]}"
        )
        request = requests.get(url)
        dlg.setValue(i + 1)
        if request.status_code == 200:
            dlg.setValue(m)
            return url
    return ""
