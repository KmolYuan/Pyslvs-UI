# -*- coding: utf-8 -*-
#System infomation
import sys, platform
py_nm = sys.version[0:sys.version.find(" ")][0:3]
#IO
from ..io.slvs_type import *
#Qt5
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
#SLVS Version
if platform.system().lower()=="windows":
    if py_nm=="3.5": from ..kernel.py35w.slvs import *
elif platform.system().lower()=="linux":
    if py_nm=="3.4": from ..kernel.py34.slvs import *
    elif py_nm=="3.5": from ..kernel.py35.slvs import *
else: print("Python Version Not Support.")

from copy import copy
