# -*- coding: utf-8 -*-

"""Thread of synthesis process."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2019"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from abc import abstractmethod
from core.QtModules import (
    Slot,
    QABCMeta,
    QThread,
    QWidget,
)


class BaseThread(QThread, metaclass=QABCMeta):

    """Base thread of Cython functions."""

    @abstractmethod
    def __init__(self, parent: QWidget):
        super(BaseThread, self).__init__(parent)
        self.finished.connect(self.deleteLater)
        self.is_stop = False

    @Slot()
    def stop(self):
        """Stop the algorithm."""
        self.is_stop = True