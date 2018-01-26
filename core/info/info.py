# -*- coding: utf-8 -*-
##Pyslvs - Open Source Planar Linkage Mechanism Simulation and Dimensional Synthesis System.
##Copyright (C) 2016-2018 Yuan Chang
##E-mail: pyslvs@gmail.com
##
##This program is free software; you can redistribute it and/or modify
##it under the terms of the GNU Affero General Public License as published by
##the Free Software Foundation; either version 3 of the License, or
##(at your option) any later version.
##
##This program is distributed in the hope that it will be useful,
##but WITHOUT ANY WARRANTY; without even the implied warranty of
##MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##GNU Affero General Public License for more details.
##
##You should have received a copy of the GNU Affero General Public License
##along with this program; if not, write to the Free Software
##Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

from sys import version_info
import platform
import argparse
try:
    from PyQt5.QtCore import qVersion, PYQT_VERSION_STR
    Qt_Version = qVersion().strip()
    PyQt_Version = PYQT_VERSION_STR.strip()
except ImportError:
    Qt_Version = "No Qt"
    PyQt_Version = "No PyQt"

VERSION = (18, 1, 0, 'release')

INFO = (
    "Pyslvs {}.{}.{}({})".format(*VERSION),
    "OS Type: {} {} [{}]".format(platform.system(), platform.release(), platform.machine()),
    "Python Version: {v.major}.{v.minor}.{v.micro}({v.releaselevel})".format(v=version_info),
    "Python Compiler: {}".format(platform.python_compiler()),
    "Qt Version: {}".format(Qt_Version),
    "PyQt Version: {}".format(PyQt_Version)
)

POWERBY = (
    "Python IDE Eric 6",
    "PyQt 5",
    "dxfwrite",
    "Cython",
    "PyZMQ",
    "openpyxl",
    "psutil",
    "peewee",
    "Lark-parser",
    "NetworkX",
    "Pydot"
)

#--help
parser = argparse.ArgumentParser(
    description="Pyslvs - Open Source Planar Linkage Mechanism Simulation and Dimensional Synthesis System.",
    epilog="Power by {}.".format(", ".join(POWERBY))
)
parser.add_argument('-v', '--version', action='version', help="show version infomations and exit", version=INFO[0])
parser.add_argument('r', metavar='FILE PATH', default=False, nargs='?', type=str, help="read workbook from the file path")
parser.add_argument('-i', metavar='START PATH', default=False, nargs='?', type=str, help="start Pyslvs in the specified path")
parser.add_argument('-w', action='store_true', help="show rebuild warning of canvas")
parser.add_argument('-f', '--fusion', action='store_true', help="run Pyslvs in Fusion style")
parser.add_argument('--full-screen', action='store_true', help="start Pyslvs with full-screen mode")
parser.add_argument('--server', metavar='PORT', default=False, nargs='?', type=str, help="start ZMQ server")
parser.add_argument('-d', '--debug-mode', action='store_true', help="do not connect to GUI console when opening")
parser.add_argument('--test', action='store_true', help="startup the program to test imported modules")
args = parser.parse_args()
