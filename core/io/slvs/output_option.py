# -*- coding: utf-8 -*-

"""Output dialog for slvs format."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import Tuple, Callable
from os.path import isdir, isfile
from core.QtModules import (
    pyqtSlot,
    Qt,
    QDialog,
    QDir,
    QMessageBox,
    QFileDialog,
    QTextEdit,
)
from core.libs import VPoint
from .write import slvs_output
from .Ui_output_option import Ui_Dialog


class SlvsOutputDialog(QDialog, Ui_Dialog):
    
    """Setting the path and output name."""
    
    def __init__(self,
        env: str,
        file_name: str,
        vpoints: Tuple[VPoint],
        v_to_slvs: Callable[[], Tuple[int, int]],
        parent
    ):
        """Comes in environment variable, workbook name
            and parameters of 'v_to_slvs' function.
        """
        super(SlvsOutputDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.path_edit.setPlaceholderText(env)
        self.filename_edit.setPlaceholderText(file_name)
        self.vpoints = vpoints
        self.v_to_slvs = v_to_slvs
    
    @pyqtSlot()
    def on_choosedir_button_clicked(self):
        """Choose path and it will be set as environment variable if accepted."""
        path = self.path_edit.text()
        if not isdir(path):
            path = self.path_edit.placeholderText()
        path = QFileDialog.getExistingDirectory(self, "Choose a directory", path)
        if path:
            self.path_edit.setText(path)
    
    @pyqtSlot()
    def on_buttonBox_accepted(self):
        """Write file and close if saved successfully.
        
        TODO: Output types:
        + Assembly
        + Only wire frame
        """
        
        def getname(widget: QTextEdit) -> str:
            """Return the file name of widget."""
            text = widget.text()
            if text:
                return text
            else:
                return widget.placeholderText()
        
        file_name = QDir(getname(self.path_edit)).filePath(getname(self.filename_edit) + '.slvs')
        if self.warn_radio.isChecked() and isfile(file_name):
            QMessageBox.warning(self, "File exist", "The file is exist.")
            return
        slvs_output(
            self.vpoints,
            self.v_to_slvs,
            file_name
        )
        self.accept()
