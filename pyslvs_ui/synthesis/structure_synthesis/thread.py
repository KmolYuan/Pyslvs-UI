# -*- coding: utf-8 -*-

"""Thread of structural synthesis."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2021"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import Sequence, Dict, List
from qtpy.QtCore import Signal
from qtpy.QtWidgets import QWidget, QTreeWidgetItem
from pyslvs.graph import (
    link_synthesis,
    contracted_link_synthesis,
    contracted_graph,
    conventional_graph,
    Graph,
)
from pyslvs_ui.synthesis.thread import BaseThread

Assortment = Sequence[int]


def assortment_eval(links_expr: str) -> Assortment:
    """Return link assortment from expr."""
    return tuple(int(n.split('=')[-1]) for n in links_expr.split(", "))


class LinkThread(BaseThread):
    """Link assortment synthesis thread."""

    progress_update = Signal(int)
    result = Signal(dict)
    size_update = Signal(int)

    def __init__(self, nl: int, nj: int, parent: QWidget):
        super(LinkThread, self).__init__(parent)
        self.nl = nl
        self.nj = nj

    def run(self) -> None:
        """Run and return contracted link assortment."""
        try:
            la_list = link_synthesis(self.nl, self.nj, lambda: self.is_stop)
        except ValueError:
            self.progress_update.emit(1)
            self.result.emit({})
            self.finished.emit()
            return

        self.size_update.emit(len(la_list))
        assortment = {}
        for i, la in enumerate(la_list):
            if self.is_stop:
                break
            assortment[la] = contracted_link_synthesis(la, lambda: self.is_stop)
            self.progress_update.emit(1 + i)
        self.result.emit(assortment)
        self.finished.emit()


class GraphThread(BaseThread):
    """Graphs enumeration thread."""
    progress_update = Signal(int)
    count_update = Signal(QTreeWidgetItem, int)
    result = Signal(list)

    def __init__(self, jobs: Sequence[QTreeWidgetItem], degenerate: int, parent: QWidget):
        super(GraphThread, self).__init__(parent)
        self.jobs = jobs
        self.degenerate = degenerate

    def run(self) -> None:
        """Run and return conventional graph."""
        cg_list: Dict[Sequence[int], List[Graph]] = {}
        answers = []
        for i, item in enumerate(self.jobs):
            if self.is_stop:
                break

            root = item.parent()
            la = assortment_eval(root.text(0))
            cla = assortment_eval(item.text(0))
            if la not in cg_list:
                cg_list[la] = contracted_graph(la, lambda: self.is_stop)

            answer = conventional_graph(
                cg_list[la],
                cla,
                self.degenerate,
                lambda: self.is_stop
            )
            self.count_update.emit(item, len(answer))
            answers.extend(answer)
            self.progress_update.emit(1 + i)

        self.result.emit(answers)
        self.finished.emit()
