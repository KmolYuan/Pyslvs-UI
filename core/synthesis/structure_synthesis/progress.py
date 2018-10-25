# -*- coding: utf-8 -*-

"""Progress dialog of structural synthesis."""

from typing import List
from core.QtModules import (
    pyqtSlot,
    QDialog,
    QWidget,
    QTableWidgetItem,
    QSpinBox,
)
from core.libs import Graph
from .thread import AtlasThread
from .Ui_progress import Ui_Dialog


class AtlasProgressDialog(QDialog, Ui_Dialog):

    """Structural synthesis progress dialog."""

    def __init__(
        self,
        link_assortment: List[int],
        no_degenerate: bool,
        parent: QWidget
    ):
        super(AtlasProgressDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle(str(link_assortment))
        self.result_list: List[Graph] = []
        self.time = 0.
        self.thread = AtlasThread(link_assortment, no_degenerate)
        self.thread.new_cj_type.connect(self.__set_contracted_link)
        self.thread.update_count.connect(self.__update_count)
        self.thread.finish.connect(self.__set_result_list)

    def show(self):
        """Start thread after shown."""
        super(AtlasProgressDialog, self).show()
        self.thread.start()

    @pyqtSlot(list)
    def __set_contracted_link(self, cj_list: List[int]):
        """Create new contracted link assortment on table."""
        self.cla_list.addItem(str(cj_list))
        self.progress_bar.setMaximum(len(cj_list) + 1)

    @pyqtSlot()
    def __update_count(self):
        """Update count of a type of contracted link assortment."""
        self.progress_bar.setValue(self.progress_bar.value() + 1)

    @pyqtSlot(list, float)
    def __set_result_list(self, result_list: List[Graph], time: float):
        """Update result list."""
        self.result_list.extend(result_list)
        self.time = time
        self.accept()

    @pyqtSlot(name='on_cancel_button_clicked')
    def __canceled(self):
        """User canceled."""
        self.progress_thread.stop()
        self.progress_thread.terminate()
        self.progress_thread.wait()
        self.reject()
