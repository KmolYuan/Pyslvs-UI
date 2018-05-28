# -*- coding: utf-8 -*-

"""Informations.

+ Module versions.
+ Help descriptions.
+ Check for update function.
"""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from sys import version_info
import platform
import argparse
from typing import Tuple
import requests
from core.QtModules import (
    QProgressDialog,
    qVersion,
    PYQT_VERSION_STR,
)
from core.libs import __version__


_Qt_Version = qVersion().strip()
_PyQt_Version = PYQT_VERSION_STR.strip()

INFO = (
    "Pyslvs {}.{}.{}({})".format(*__version__),
    "OS Type: {} {} [{}]".format(platform.system(), platform.release(), platform.machine()),
    "Python Version: {v.major}.{v.minor}.{v.micro}({v.releaselevel})".format(v=version_info),
    "Python Compiler: {}".format(platform.python_compiler()),
    "Qt Version: {}".format(_Qt_Version),
    "PyQt Version: {}".format(_PyQt_Version)
)

_POWERBY = (
    "Python IDE Eric 6",
    "PyQt 5",
    "dxfwrite",
    "Cython",
    "openpyxl",
    "psutil",
    "peewee",
    "Lark-_parser",
    "NetworkX",
    "Pydot",
    "Pygments",
)

#--help arguments
_parser = argparse.ArgumentParser(
    description = ("Pyslvs - Open Source Planar Linkage Mechanism Simulation" +
        "and Mechanical Synthesis System."),
    epilog = "Power by {}.".format(", ".join(_POWERBY))
)
_parser.add_argument(
    '-v',
    '--version',
    action = 'version',
    help = "show version infomations and exit",
    version = INFO[0]
)
_parser.add_argument(
    'r',
    metavar = "file path",
    default = False,
    nargs = '?',
    type = str,
    help = "read workbook from the file path"
)
_parser.add_argument(
    '-i',
    metavar = "start path",
    default = False,
    nargs = '?',
    type = str,
    help = "start Pyslvs in the specified path"
)
_parser.add_argument(
    '-w',
    action = 'store_true',
    help = "show rebuild warning of canvas"
)
_parser.add_argument(
    '-f',
    '--fusion',
    action = 'store_true',
    help = "run Pyslvs in Fusion style"
)
_parser.add_argument(
    '--full-screen',
    action = 'store_true',
    help = "start Pyslvs with full-screen mode"
)
_parser.add_argument(
    '-d',
    '--debug-mode',
    action = 'store_true',
    help = "do not connect to GUI console when opening"
)
_parser.add_argument(
    '-t',
    '--test',
    action = 'store_true',
    help = "just test module states and exit"
)
ARGUMENTS = _parser.parse_args()


def check_update(progdlg: QProgressDialog) -> Tuple[str, bool]:
    """Check for update."""
    m = progdlg.maximum()
    from core.QtModules import QCoreApplication
    for i in range(m):
        QCoreApplication.processEvents()
        if progdlg.wasCanceled():
            return
        next_ver = list(__version__[:m])
        next_ver[i] += 1
        url = ("https://github.com/KmolYuan/Pyslvs-PyQt5/releases/tag/" +
            "v{}.{:02}.{}".format(*next_ver))
        request = requests.get(url)
        progdlg.setValue(i + 1)
        if request.status_code == 200:
            progdlg.setValue(m)
            return url
    return False
