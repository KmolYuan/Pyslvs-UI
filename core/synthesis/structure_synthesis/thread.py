# -*- coding: utf-8 -*-

"""Thread object of atlas algorithm."""

from typing import List
from core.QtModules import (
    pyqtSignal,
    QWidget,
    QThread,
)
from core.libs import topo


class AtlasThread(QThread):

    """Thread class."""

    new_cj_type = pyqtSignal(list)
    update_count = pyqtSignal()
    finish = pyqtSignal(list, float)

    def __init__(self, link_assortment: List[int], no_degenerate: bool):
        super(AtlasThread, self).__init__()
        self.link_assortment = link_assortment
        self.no_degenerate = no_degenerate
        self.stopped = False

    def run(self):
        """Main process."""
        result, t = topo(
            self.link_assortment,
            self.no_degenerate,
            self.new_cj_type.emit,
            self.update_count.emit,
            lambda: self.stopped
        )
        self.finish.emit(result, t)

    def stop(self):
        """User canceled."""
        self.stopped = True
