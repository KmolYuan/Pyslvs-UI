from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class Pyslvs_Settings_ini():
    def __init__(self):
        self.settings = QSettings("./Pyslvs_Settings.ini", QSettings.IniFormat)
        self.settings.setValue("Environment_variables", QVariant("../"))
