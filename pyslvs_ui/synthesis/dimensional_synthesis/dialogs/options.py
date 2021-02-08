# -*- coding: utf-8 -*-

"""The option dialog use to adjust the setting of algorithm."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2021"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import cast, List, Tuple, Dict, Union, Optional
from qtpy.QtCore import Slot, Qt
from qtpy.QtWidgets import (
    QDialog,
    QTableWidgetItem,
    QDoubleSpinBox,
    QSpinBox,
    QWidget,
)
from pyslvs.metaheuristics import default, AlgorithmType
from pyslvs_ui.info import html
from .options_ui import Ui_Dialog

_Value = Union[int, float]


class AlgorithmOptionDialog(QDialog, Ui_Dialog):
    """Option dialog.

    Only edit the settings after closed.
    """

    def __init__(
        self,
        opt: AlgorithmType,
        settings: Dict[str, _Value],
        parent: QWidget
    ):
        """Load the settings to user interface."""
        super(AlgorithmOptionDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags()
                            & ~Qt.WindowContextHelpButtonHint)
        self.setWindowTitle(f"{opt.value} Options")
        self.opt = opt
        self.__init_alg_table()
        self.alg_table.setColumnWidth(0, 200)
        self.alg_table.setColumnWidth(1, 90)
        self.__set_args(settings)

    def __init_alg_table(self) -> None:
        """Initialize the algorithm table widgets."""
        def write_table(
            integers: Optional[List[Tuple[str, str, str]]] = None,
            floats: Optional[List[Tuple[str, str, str]]] = None
        ):
            """Use to write table data."""
            if integers is None:
                integers = []
            if floats is None:
                floats = []
            i = 0
            for options, box, max_value in (
                (integers, QSpinBox, 9),
                (floats, QDoubleSpinBox, 10.)
            ):
                for name, tooltip, tooltip in options:
                    self.alg_table.insertRow(i)
                    name_cell = QTableWidgetItem(name)
                    name_cell.setToolTip(tooltip)
                    self.alg_table.setItem(i, 0, name_cell)
                    spinbox = box()
                    spinbox.setMaximum(max_value)
                    spinbox.setToolTip(tooltip)
                    self.alg_table.setCellWidget(i, 1, spinbox)
                    i += 1

        if self.opt == AlgorithmType.RGA:
            write_table(
                floats=[
                    ("Crossover Rate", 'pCross',
                        html("The chance of crossover.")),
                    ("Mutation Rate", 'pMute',
                        html("The chance of mutation.")),
                    ("Winning Rate", 'pWin',
                        html("The chance of winning.")),
                    ("Delta value", 'bDelta',
                        html("The power value when matching chromosome."))
                ]
            )
        elif self.opt == AlgorithmType.Firefly:
            write_table(
                floats=[
                    ("Alpha value", 'alpha', html(
                        "Alpha value is the step size of the firefly.")),
                    ("Minimum Beta value", 'beta_min', html(
                        "The minimal attraction, must not less than this.")),
                    ("Gamma value", 'gamma', html(
                        "Beta will multiplied by exponential power value "
                        "with this weight factor.")),
                    ("Beta0 value", 'beta0', html(
                        "The attraction of two firefly in 0 distance."))
                ]
            )
        elif self.opt == AlgorithmType.DE:
            write_table(
                integers=[
                    ("Evolutionary strategy (0-9)", 'strategy',
                        html("There are 10 way to evolution."))
                ],
                floats=[
                    ("Weight factor", 'F', html(
                        "Weight factor is usually between 0.5 and 1"
                        "(in rare cases > 1).")),
                    ("Recombination factor", 'CR',
                        html("The chance of crossover possible."))
                ]
            )

    def __set_args(self, settings: Dict[str, _Value]) -> None:
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
        self.report.setValue(settings['report'])
        if self.opt == AlgorithmType.RGA:
            self.pop_size.setValue(settings['nPop'])
            for i, tag in enumerate(('pCross', 'pMute', 'pWin', 'bDelta')):
                self.alg_table.cellWidget(i, 1).setValue(settings[tag])
        elif self.opt == AlgorithmType.Firefly:
            self.pop_size.setValue(settings['n'])
            for i, tag in enumerate(('alpha', 'beta_min', 'gamma', 'beta0')):
                self.alg_table.cellWidget(i, 1).setValue(settings[tag])
        elif self.opt == AlgorithmType.DE:
            self.pop_size.setValue(settings['NP'])
            for i, tag in enumerate(('strategy', 'F', 'CR')):
                self.alg_table.cellWidget(i, 1).setValue(settings[tag])
        elif self.opt == AlgorithmType.TLBO:
            self.pop_size.setValue(settings['class_size'])

    @Slot(name='on_reset_button_clicked')
    def __reset(self) -> None:
        """Reset the settings to default."""
        self.__set_args(default(self.opt))
