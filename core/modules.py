# -*- coding: utf-8 -*-
#PyQt5
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
#CSV & SQLite
import sys, csv, math, webbrowser
from peewee import *
#Dialog Ports
from .info.version import version_show
from .info.info import Info_show
from .info.help import Help_info_show
from .info.path_point_data import path_point_data_show
from .info.options import options_show
from .io.script import Script_Dialog
#Warning Dialog Ports
from .warning.reset_workbook import reset_show
from .warning.zero_value import zero_show
from .warning.repeated_value import same_show
from .warning.restriction_conflict import restriction_conflict_show
#Drawing Dialog Ports
from .draw.point import New_point
from .draw.link import New_link
from .draw.stay_chain import chain_show
from .draw.edit_point import edit_point_show
from .draw.edit_link import edit_link_show
from .draw.edit_stay_chain import edit_stay_chain_show
#Simulate Dialog Ports
from .simulate.set_drive_shaft import shaft_show
from .simulate.set_slider import slider_show
from .simulate.set_rod import rod_show
from .simulate.edit_drive_shaft import edit_shaft_show
from .simulate.edit_slider import edit_slider_show
from .simulate.edit_rod import edit_rod_show
#Panel
from .panel.run_Path_Track import Path_Track_show
from .panel.run_Drive import Drive_show
from .panel.run_Measurement import Measurement_show
from .panel.run_AuxLine import AuxLine_show
from .panel.delete import deleteDlg
#Solve
from .calculation.calculation import Solvespace
#Canvas
if '--view' in sys.argv:
    from .calculation.canvasView import DynamicCanvas
else:
    from .calculation.canvas_0 import DynamicCanvas
#File & Example
from .io.fileForm import File
from .io.example import *
from .io.dxfType import dxfCode
from .info.editFileInfo import editFileInfo_show
from .info.fileInfo import fileInfo_show
#Option
from .io.settings import Pyslvs_Settings_ini
