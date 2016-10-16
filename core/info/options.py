# -*- coding: utf-8 -*-
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from .Ui_options import Ui_Dialog
from core.io.settings import Pyslvs_Settings_ini

class options_show(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super(options_show, self).__init__(parent)
        self.setupUi(self)
        self.option_file = Pyslvs_Settings_ini()
        self.EnvVariable.setText(self.option_file.settings.value("Environment_variables", "../"))
