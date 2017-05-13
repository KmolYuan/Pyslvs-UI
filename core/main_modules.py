# -*- coding: utf-8 -*-
#Splash
from .info.info import Pyslvs_Splash
#CSV
import sys, os, webbrowser, platform
from math import acos
#Dialog Ports
from .info.info import version_show
from .info.path_point_data import path_point_data_show
from .io.script import Script_Dialog
#Drawing Dialog Ports
from .entities.edit_point import edit_point_show
from .entities.edit_link import edit_link_show
from .entities.edit_chain import edit_chain_show
#Simulate Dialog Ports
from .simulate.edit_shaft import edit_shaft_show
from .simulate.edit_slider import edit_slider_show
from .simulate.edit_rod import edit_rod_show
#Dialog
from .dialog.delete import deleteDlg
from .dialog.replacePoint import replacePoint_show
from .dialog.batchMoving import batchMoving_show
from .dialog.association import Association_show
from .dialog.run_Path_Track import Path_Track_show
#Panel
from .panel.run_Path_Solving import Path_Solving_show
from .panel.run_Triangle_Solver import Triangle_Solver_show
from .panel.run_Drive_shaft import Drive_shaft_show
from .panel.run_Drive_rod import Drive_rod_show
from .panel.run_Measurement import Measurement_show
from .panel.run_AuxLine import AuxLine_show
#Solve
from .calculation.planeSolving import slvsProcess
#Canvas
from .graphics.canvas_0 import DynamicCanvas
#File & Example
from .io.fileForm import File
from .io import example
from .io.dxfType import dxfTypeSettings
from .io.dxfForm.sketch import dxfSketch
from .io.slvsType import slvsTypeSettings
from .io.slvsForm.sketch import slvs2D
from .info.fileInfo import fileInfo_show, editFileInfo_show
#Logging
from .io.loggingHandler import XStream
