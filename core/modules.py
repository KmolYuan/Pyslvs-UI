# -*- coding: utf-8 -*-
#PyQt5
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
#CSV & SQLite
import sys, csv, math, webbrowser, platform
from peewee import *
#Dialog Ports
from .info.version import Help_info_show, Info_show, version_show
from .info.path_point_data import path_point_data_show
from .info.options import options_show
from .io.script import Script_Dialog
from .io.slvsType import slvsTypeSettings
#Drawing Dialog Ports
from .draw.edit_point import edit_point_show
from .draw.edit_link import edit_link_show
from .draw.edit_stay_chain import edit_stay_chain_show
#Simulate Dialog Ports
from .simulate.edit_drive_shaft import edit_shaft_show
from .simulate.edit_slider import edit_slider_show
from .simulate.edit_rod import edit_rod_show
#Dialog
from .dialog.delete import deleteDlg
from .dialog.replacePoint import replacePoint_show
from .dialog.batchMoving import batchMoving_show
from .dialog.association import Association_show
#Panel
from .panel.run_Path_Track import Path_Track_show
from .panel.run_Drive import Drive_show
from .panel.run_Measurement import Measurement_show
from .panel.run_AuxLine import AuxLine_show
from .panel.run_Path_Solving import Path_Solving_show
#Solve
from .calculation.calculation import slvsProcess
#Canvas
from .calculation.canvas_0 import DynamicCanvas
#File & Example
from .io.fileForm import File
from .io.example import *
from .io.dxfType import dxfCode
from .info.editFileInfo import editFileInfo_show
from .info.fileInfo import fileInfo_show
#Option
from .io.settings import Pyslvs_Settings_ini
