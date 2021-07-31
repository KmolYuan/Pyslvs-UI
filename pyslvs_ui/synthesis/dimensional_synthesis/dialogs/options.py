# -*- coding: utf-8 -*-

"""The option dialog use to adjust the setting of algorithm."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2021"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import cast, Mapping, Union
from qtpy.QtCore import Slot, Qt
from qtpy.QtWidgets import (
    QDialog,
    QTableWidgetItem,
    QDoubleSpinBox,
    QSpinBox,
    QWidget,
)
from pyslvs.metaheuristics import default, AlgorithmType
from .options_ui import Ui_Dialog

_Value = Union[int, float]


class AlgorithmOptionDialog(QDialog, Ui_Dialog):
    """Option dialog.

    Only edit the settings after closed.
    """

    def __init__(
        self,
        opt: AlgorithmType,
        settings: Mapping[str, _Value],
        parent: QWidget
    ):
        """Load the settings to user interface."""
        super(AlgorithmOptionDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags()
                            & ~Qt.WindowContextHelpButtonHint)
        self.setWindowTitle(f"{opt.value} Options")
        self.opt = opt
        self.dft = {tag: value for tag, value in default(self.opt).items()
                    if tag not in {'pop_num', 'report', 'max_gen', 'min_fit',
                                   'max_time', 'slow_down'}}
        self.__init_alg_table()
        self.alg_table.setColumnWidth(0, 200)
        self.alg_table.setColumnWidth(1, 90)
        self.__set_args(settings)

    def __init_alg_table(self) -> None:
        """Initialize the algorithm table widgets."""
        self.alg_table.setRowCount(len(self.dft))
        for i, (tag, value) in enumerate(self.dft.items()):
            self.alg_table.setItem(i, 0, QTableWidgetItem(tag))
            if isinstance(value, int):
                w = QSpinBox()
                w.setMaximum(1e5)
            else:
                w = QDoubleSpinBox()
            w.setValue(value)
            self.alg_table.setCellWidget(i, 1, w)

    def __set_args(self, settings: Mapping[str, _Value]) -> None:
        """Set arguments by settings dict."""
        if 'max_gen' in settings:
            self.max_gen.setValue(settings['max_gen'])
        elif 'min_fit' in settings:
            self.min_fit_option.setChecked(True)
            self.min_fit.setValue(settings['min_fit'])
        elif 'max_time' in settings:
            self.max_time_option.setChecked(True)
            # In second (int)
            max_time = cast(int, settings['max_time'])
            self.max_time_h.setValue(max_time // 3600)
            self.max_time_m.setValue((max_time % 3600) // 60)
            self.max_time_s.setValue(max_time % 3600 % 60)
        self.pop_size.setValue(settings['pop_num'])
        self.report.setValue(settings['report'])
        for i, tag in enumerate(self.dft):
            self.alg_table.cellWidget(i, 1).setValue(settings.get(tag, self.dft[tag]))

    @Slot(name='on_reset_btn_clicked')
    def __reset(self) -> None:
        """Reset the settings to default."""
        self.__set_args(default(self.opt))
